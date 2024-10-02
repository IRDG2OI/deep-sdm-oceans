# ACKNOWLEDGEMENT

This project is being developed as part of the G2OI project, cofinanced by the European Union, the Reunion region, and the French Republic.
<div align="center">


<img src="https://github.com/IRDG2OI/geoflow-g2oi/blob/main/img/logos_partenaires.png?raw=True" height="80px">

</div>

# Deep-SDMs in the open oceans

This is the code used to train the model, and prepare the outputs for the preprint named **Predicting species distributions in the open oceans with convolutional neural networks**, available on [bioRxiv](https://doi.org/10.1101/2023.08.11.551418
). Please refer to the Methods section of this article for information on using this repository.

This code uses the Malpolon framework, created and maintained by the Pl@ntNet team at INRIA.
See the [original repository](https://github.com/plantnet/malpolon) for installation instructions and documentation.
As we had to slightly edit some files, we include the modified version in this repository.

## Directory structure

The root of this directory is the same as the original malpolon repository, except non-essential elements were removed.
All code that is specific to our use case is in the [open-oceans](open-oceans) folder.

## Citing

If you use this work please cite the related article:

> Morand, Gaétan; Joly, Alexis; Rouyer, Tristan; Lorieul, Titouan; Barde, Julien. Predicting species distributions in the open ocean with convolutional neural networks. Peer Community Journal, Volume 4 (2024), article no. e93. doi : 10.24072/pcjournal.471. https://peercommunityjournal.org/articles/10.24072/pcjournal.471/
