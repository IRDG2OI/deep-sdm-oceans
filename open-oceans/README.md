# Instructions

## Training the model

First prepare environmental data following instructions from [geoenrich-tools/README.md](geoenrich-tools/README.md).

Then format the input data properly with the [Prepare_data](Prepare_data.ipynb) notebook.

Then edit your configuration file (yaml file in the conf subfolder) and start training by calling
```bash
python multi38.py
```
If you want to retrain from a checkpoint, set other.train_from_checkpoint to *true* and indicate the path to your checkpoint in ckpt_path and ckpt_name (these two paths will be concatenated to obtain the full path).

## Generating outputs

Either use your own checkpoint and config file, or the provided ones (cf. checkpoint link in the next section).

Then you can make predictions and generate output maps using the [Generate_outputs](Generate_outputs.ipynb) notebook.

## Data links

### Input data

[Numpy input data + csv database](https://doi.org/10.5281/zenodo.8188512)

### Model checkpoint

[Model checkpoint & config file](https://doi.org/10.5281/zenodo.8202914)

### Outputs

- [Global 2021 distribution maps](https://doi.org/10.5281/zenodo.8202261)
- [Western Indian Ocean 2021 distribution maps](https://doi.org/10.5281/zenodo.8202056)
- [+2°C projection](https://doi.org/10.5281/zenodo.8202709)
