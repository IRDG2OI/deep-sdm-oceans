from geoenrich.exports import collate_npy
import csv
from pathlib import Path
from mpi4py import MPI


### For training data
#### Usage one process per species (reduce n if your CPU has less than 38 threads.
# mpiexec -n 38 collate_npy_multi38.py


data_path = Path('/data')

file = (data_path / 'species.csv').open()
species = list(csv.DictReader(file))

rank = MPI.COMM_WORLD.Get_rank()
size = MPI.COMM_WORLD.Get_size()

for i in range(len(species)):
   if (i == rank):
   	ds_ref = species[i]['id']
   	collate_npy(ds_ref, data_path / 'collated/')
   	print(f"Rank {i} over ({ds_ref})")



### For wio-tiled and world-tiled, divide in chunks:

#ds_ref = 'wio-tiled'
#chunksize = 2700   ## Must be larger than dataset length / number of threads

#collate_npy(ds_ref, data_path / 'collated', slice = [chunksize*rank, chunksize*(rank+1)])
