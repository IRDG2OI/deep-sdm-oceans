# Deep-SDMs in the open oceans

This is the code used to train the model, and prepare the outputs for the preprint named **Predicting species distributions in the open oceans with convolutional neural networks**, available on (Link will be added shortly).

This code uses the Malpolon framework, created and maintained by the Pl@ntNet team at INRIA.
See the [original repository](https://github.com/plantnet/malpolon) for installation instructions and documentation.
As we had to slightly edit some files, we include the modified version in this repository.

## Directory structure

The root of this directory is the same as the original malpolon repository, except non-essential elements were removed.
All code that is specific to our use case is in the *open-oceans* folder.

## Data links

### Input data

[Numpy input data + csv database](https://doi.org/10.5281/zenodo.8188512)

### Model checkpoint

[Model checkpoint & config file](https://doi.org/10.5281/zenodo.8202914)

### Outputs

- [Global 2021 distribution maps](https://doi.org/10.5281/zenodo.8202261)
- [Western Indian Ocean 2021 distribution maps](https://doi.org/10.5281/zenodo.8202056)
- [+2°C projection](https://doi.org/10.5281/zenodo.8202709)
