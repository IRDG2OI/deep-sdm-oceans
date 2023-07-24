import os
from pathlib import Path

import numpy as np
import pandas as pd
import csv

import torch
from torch.utils.data import Dataset
import hydra
from omegaconf import DictConfig
from malpolon.models.utils import check_loss, check_model, check_optimizer
import pytorch_lightning as pl
import torchmetrics.functional as Fmetrics
from pytorch_lightning.callbacks import ModelCheckpoint
from torchvision import transforms

from malpolon.data.data_module import BaseDataModule
from malpolon.models import GenericPredictionSystem
from malpolon.logging import Summary


from transforms import RGBDataTransform

class Multi38Dataset(Dataset):
    """Pytorch dataset handler for a subset of GeoLifeCLEF 2022 dataset.
    It consists in a restriction to France and to the 100 most present plant species.

    Parameters
    ----------
    root : string or pathlib.Path
        Root directory of dataset.
    subset : string, either "train", "val", "train+val" or "test"
        Use the given subset ("train+val" is the complete training data).
    transform : callable (optional)
        A function/transform that takes a list of arrays and returns a transformed version.
    target_transform : callable (optional)
        A function/transform that takes in the target and transforms it.
    """

    def __init__(
        self,
        root,
        dataset_name,
        subset,
        transform=None,
        target_transform=None,
        ignore_indices=[],
    ):
        root = Path(root)

        self.root = root
        self.subset = subset
        self.transform = transform
        self.target_transform = target_transform
        self.ignore_indices = ignore_indices
        self.dataset_name = dataset_name

        df = pd.read_csv(
            root / dataset_name,
            index_col="id",
        )

        file = (self.root / 'species.csv').open()
        species = list(csv.DictReader(file))
        
        self.species_index = {x['id']:int(x['index']) for x in species}
        
        if subset != "train+val":
            ind = df.index[df["subset"] == subset]
        else:
            ind = df.index[np.isin(df["subset"], ["train", "val"])]
        df = df.loc[ind]

        self.observation_ids = df.index
        self.targets = df["species"].values

    def __len__(self):
        """Returns the number of observations in the dataset."""
        return len(self.observation_ids)

    def __getitem__(self, index):
        observation_id = self.observation_ids[index]
        
        species = self.targets[index]
        patches = self.load_patch(observation_id, self.root / 'npy-norm' / (species + '-norm-npy'))

        if self.transform:
            patches = self.transform(patches)

        assert not(torch.isnan(patches).any())

        species_target = self.targets[index]
        zeros = [0]*38
        
        if species_target in self.species_index:
            zeros[self.species_index[species_target]] = 1
            
        target = torch.tensor(zeros).float()

        if self.target_transform:
            target = self.target_transform(target)

        return patches, target


    def load_patch(self, observation_id, patches_path):
        """Loads the patch data associated to an observation id.

        Parameters
        ----------
        observation_id : integer / string
            Identifier of the observation.
        patches_path : string / pathlib.Path
            Path to the folder containing all the patches.

        Returns
        -------
        patches : dict containing 2d array-like objects
            Returns a dict containing the requested patches.
        """
        filename = Path(patches_path) / str(observation_id)

        patches = {}

        patch25_filename = filename.with_name(filename.stem + ".npy")
        patch25 = np.load(patch25_filename)
        

        for i in self.ignore_indices:
            patch25[...,i] = 0   


        # # Test with summary values
        # av, std = np.average(patch25, (0,1)), np.std(patch25, (0,1))
        # mi, ma = np.min(patch25, (0,1)), np.max(patch25, (0,1))

        # patch25 = np.zeros_like(patch25)
        # patch25[0,0] = av
        # patch25[0,1] = std
        # patch25[0,2] = mi
        # patch25[0,3] = ma
        # # End of test code


        if(np.isnan(patch25).any()):
            print(patch25_filename, patch25.shape,np.isnan(patch25).sum())

        patches["25"] = patch25

        return patches


class Multi38DataModule(BaseDataModule):
    r"""
    Data module for MicroGeoLifeCLEF 2022.

    Parameters
    ----------
        dataset_path: Path to dataset
        train_batch_size: Size of batch for training
        inference_batch_size: Size of batch for inference (validation, testing, prediction)
        num_workers: Number of workers to use for data loading
    """
    def __init__(
        self,
        dataset_path: str,
        dataset_name: str = None,
        train_batch_size: int = 32,
        inference_batch_size: int = 256,
        num_workers: int = 8,
        ignore_indices: list = [],
        pin_memory: bool = True,
    ):
        super().__init__(pin_memory, train_batch_size, inference_batch_size, num_workers)
        self.dataset_path = dataset_path
        self.ignore_indices = ignore_indices
        self.dataset_name = dataset_name
        

    @property
    def train_transform(self):
        return transforms.Compose(
            [
                lambda data: RGBDataTransform()(data["25"])
            ]
        )

    @property
    def test_transform(self):
        return transforms.Compose(
            [
                lambda data: RGBDataTransform()(data["25"])
            ]
        )
    

    def get_dataset(self, split, transform, **kwargs):
        dataset = Multi38Dataset(
            self.dataset_path,
            dataset_name=self.dataset_name,
            subset=split,
            transform=transform,
            target_transform= None,
            ignore_indices=self.ignore_indices,
            **kwargs
        )
        return dataset


class Multi38ClassificationSystem(GenericPredictionSystem):
    r"""
    Basic finetuning classification system.

    Parameters
    ----------
        model: model to use
        lr: learning rate
        weight_decay: weight decay value
        momentum: value of momentum
        nesterov: if True, uses Nesterov's momentum
        metrics: dictionnary containing the metrics to compute
        binary: if True, uses binary classification loss instead of multi-class one
    """

    def __init__(
        self,
        model,
        lr: float = 1e-2,
        weight_decay: float = 0,
        momentum: float = 0.9,
        nesterov: bool = True,
        metrics = None,
        weight: torch.Tensor = None,
    ):
        self.lr = lr
        self.weight_decay = weight_decay
        self.momentum = momentum
        self.nesterov = nesterov    

        model = check_model(model)

        optimizer = torch.optim.SGD(
            model.parameters(),
            lr=self.lr,
            weight_decay=self.weight_decay,
            momentum=self.momentum,
            nesterov=self.nesterov,
        )

        loss = torch.nn.BCELoss(weight=weight)
        #loss = torch.nn.BCELoss()

        super().__init__(model, loss, optimizer, metrics)
    


class ClassificationSystem(Multi38ClassificationSystem):
    def __init__(
        self,
        model: dict,
        lr: float,
        weight_decay: float,
        momentum: float,
        nesterov: bool,
        loss_weights: list,
    ):
        metrics = {
            "acc": Fmetrics.classification.binary_accuracy,
            "f1": Fmetrics.classification.binary_f1_score,
            #"cm": Fmetrics.classification.binary_confusion_matrix,
            "jac": Fmetrics.classification.binary_jaccard_index,
        }

        super().__init__(
            model,
            lr,
            weight_decay,
            momentum,
            nesterov,
            metrics,
            weight = torch.Tensor(loss_weights),
        )


@hydra.main(version_base="1.1", config_path="conf", config_name="multi38_config")
def main(cfg: DictConfig) -> None:

    torch.set_num_threads(32)
    
    run_path = Path.cwd()
    logger = pl.loggers.TensorBoardLogger(save_dir=run_path.parent, name='', version = run_path.stem,
                                            sub_dir='logs', default_hp_metric = False)
    logger.log_hyperparams(cfg)

    datamodule = Multi38DataModule(**cfg.data)
    
    if cfg.other.train_from_checkpoint:
        ckpt_path = cfg.other.ckpt_path + cfg.other.ckpt_name
        model = ClassificationSystem.load_from_checkpoint(ckpt_path, model=cfg.model, **cfg.optimizer)
    else:
        model = ClassificationSystem(cfg.model, **cfg.optimizer)



    callbacks = [
        Summary(),
        ModelCheckpoint(
            dirpath=os.getcwd(),
            filename="checkpoint-{epoch:02d}--{val_f1:.4f}",
            monitor="val_f1",
            mode="max",
        ),
    ]
    trainer = pl.Trainer(logger=logger, callbacks=callbacks, **cfg.trainer)
    trainer.fit(model, datamodule=datamodule)

    trainer.validate(model, datamodule=datamodule)

    

    
    
    
    
    
    


def predict(cfg: DictConfig) -> list:

    datamodule = Multi38DataModule(**cfg.data)
    model = ClassificationSystem(cfg.model, **cfg.optimizer)
    trainer = pl.Trainer(**cfg.trainer)

    ckpt_path = cfg.other.ckpt_path + cfg.other.ckpt_name
    predictions = trainer.predict(model, datamodule=datamodule, ckpt_path=ckpt_path)
  
    return(torch.cat(predictions).numpy())



def test(cfg: DictConfig) -> list:

    datamodule = Multi38DataModule(**cfg.data)
    model = ClassificationSystem(cfg.model, **cfg.optimizer)
    trainer = pl.Trainer(**cfg.trainer)

    ckpt_path = cfg.other.ckpt_path + cfg.other.ckpt_name
    trainer.test(model, datamodule=datamodule, ckpt_path=ckpt_path)


def last_checkpoint() -> str:
    
    cur_path = os.getcwd()
    os.chdir('/home/gaetan/multi38/outputs/multi38')
    avail = [str(p) for p in Path('.').glob('*/*.ckpt')]
    avail.sort()
    os.chdir(cur_path)
    
    return(avail[-1])
    
    
if __name__ == "__main__":
    main()
