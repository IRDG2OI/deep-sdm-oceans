
import pandas as pd
import csv
from geoenrich.credentials import *
from pathlib import Path
from random import random

data_path = Path('/data')
file = (data_path / 'species.csv').open()
species = list(csv.DictReader(file))
ldf = []

for s in species:
    
    ds_ref = s['id']
    df = pd.read_csv(biodiv_path / (ds_ref + '.csv'), index_col = 'id')[['geometry', 'eventDate']]
    df['species'] = ds_ref
    ldf.append(df)

all_data = pd.concat(ldf)
all_data['rand'] = [random() for i in range(len(all_data))]
all_data['subset'] = 'train'
all_data.loc[all_data['rand'] < 0.2, 'subset'] = 'val'
all_data.loc[all_data['rand'] > 0.8, 'subset'] = 'test'
    
all_data.drop(columns=['rand'], inplace=True)
all_data.to_csv(data_path / 'datasets' / 'all_v2.csv')
