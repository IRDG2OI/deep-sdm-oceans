from shapely import wkt
from pathlib import Path
from mpi4py import MPI
import pandas as pd
import geopandas as gpd
import sys

_, filename = sys.argv[:2]

data_path = Path('/data')
oceans = gpd.read_file(data_path / "oceans.gpkg")
oceans.set_index('id',inplace=True)


rank = MPI.COMM_WORLD.Get_rank()
df = pd.read_csv(data_path / 'datasets' / filename, index_col = 'id')

if ('geometry' in df.columns):
	df['geometry'] = df['geometry'].apply(wkt.loads)
else:
	df['geometry'] = gpd.points_from_xy(df['lon'], df['lat'])

gdf = gpd.GeoDataFrame(df, crs='epsg:4326')

geom = oceans.loc[rank, 'geometry'].buffer(0.05)
gdf[oceans.loc[rank, 'name']] = gdf.within(geom).astype(int)

gdf[[oceans.loc[rank, 'name']]].to_csv(data_path / 'datasets' / f"{rank}.csv")
