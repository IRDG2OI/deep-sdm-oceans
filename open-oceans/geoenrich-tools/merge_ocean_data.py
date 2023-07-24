import pandas as pd
import geopandas as gpd
from pathlib import Path
import sys

_, filename = sys.argv[:2]

data_path = Path('/data')
oceans = gpd.read_file(data_path / "oceans.gpkg")
oceans.set_index('id',inplace=True)

df = pd.read_csv(data_path / 'datasets' / filename, index_col = 'id')

for i in range(0,3):
    dfi = pd.read_csv(data_path / 'datasets' / f"{i}.csv", index_col = 'id')
    df[oceans.loc[i, 'name']] = dfi[oceans.loc[i, 'name']]

df.to_csv(data_path / 'datasets' / (filename[:-4] + '_oceans.csv'))
