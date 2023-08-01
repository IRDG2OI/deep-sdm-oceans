# Geoenrich tools

These are snippets of code used after downloading environmental data with GeoEnrich.
Their aim is to prepare and export the data for the deep learning training / predictions.

List of files:
- calculate_oceans.py
- collate_npy_multi38.py
- merge-and-split.py
- merge_ocean_data.py
- oceans.gpkg

## Process

GeoEnrich stores environmental data into large NetCDF files. We need to export those into individual files (one per occurrence) containing all environmental layers.
We also split the training dataset and add additional information on the ocean basin.

### Enrich data with geoenrich ([separate documentation](https://geoenrich.readthedocs.io))

### Merge and split the dataset

Create one CSV file for the whole dataset with the *merge-and-split.py* script (merging each species' file). Then assign a train/validation/test subset to each occurrence.

### Calculate the ocean basin

The calculate_oceans.py file calculates the ocean basins based on latitude and longitude and the oceans.gpkg shape.
It is supposed to be run in parallel with mpiexec, and creates one temporary file per ocean basin. They are named 0.csv, 1.csv and 2.csv.

These three files are then merged using the *merge_oceans.py* script. 

### Collate data using the *geoenrich.exports.collate_npy* function

The *collate_npy_multi38.py* script handles parallelized collation with mpiexec.

### Transfer data

Now data is ready to be transfered to your Deep Learning computer/server.
You have to transfer all the individual numpy files as well as the csv dataset.

Then you can use the *Prepare data* python notebook.