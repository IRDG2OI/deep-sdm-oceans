# Deep-SDMs in the open oceans

This is the code used to train the model, and prepare the outputs for the preprint named **Predicting species distributions in the open oceans with convolutional neural networks**, available on .

This code uses the Malpolon framework, created and maintained by the Pl@ntNet team at INRIA.
See the [original repository](https://github.com/plantnet/malpolon) for installation instructions and documentation.
As we had to slightly edit some files, we include the modified version in this repository.

## Directory structure

The root of this directory is the same as the original malpolon repository, except non-essential elements were removed.
All code that is specific to our use case is in the *open-oceans* folder.

## Data links

### Input data

Numpy input data + csv database

### Model checkpoint

Model checkpoint & config file

### Outputs

Raw predictions files (CSV)

- Global 2021 distribution maps: PNG, GeoTIFF
- Western Indian Ocean 2021 distribution maps: GIF, GeoTIFF
- +2°C projection: PNG, GeoTIFF

