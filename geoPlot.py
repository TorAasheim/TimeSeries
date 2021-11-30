import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import contextily as ctx

#Read datafile and Shapefile
df = pd.read_csv('processedData.csv')
#gdf = gpd.read_file('shapefile/roads.shp')
crs ='EPSG:4308'

#Cleaning of out of bounds coordinates
#outOfBounds = df[df['geo_lat'] < 50]
df = df.set_index('trip_id')
df = df.drop(1741.0, axis=0)


#Convert lat long columns to shapely geometry points
geometry = [Point(xy) for xy in zip(df['geo_long'], df['geo_lat'])]

#creata a geopandas dataframe from the csv dataframe
gdf = gpd.GeoDataFrame(df, geometry=geometry)
#bounding box, to remove instances outside of oslo
xmin, ymin, xmax, ymax = 10.138,59.6453,11.201,60.1435
gdf = gdf.cx[xmin:xmax, ymin:ymax]
gdf.set_crs(epsg=4308)


#plot geopandas dataframe coordinates ontop of basemap
ax = gdf.plot(color='red', markersize=1)
ctx.add_basemap(ax, crs=crs, source=ctx.providers.OpenStreetMap.Mapnik, zoom=15)
plt.show()


