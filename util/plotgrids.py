#!/usr/bin/env python3

import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader

# Load the domain file
ds1 = xr.open_dataset("/home/natalie/src/wrf/WPS/geo_em.d01.nc")
ds2 = xr.open_dataset("/home/natalie/src/wrf/WPS/geo_em.d02.nc")

# Get lat/lon and terrain
lat1, lon1, hgt1 = ds1['XLAT_M'][0], ds1['XLONG_M'][0], ds1['HGT_M'][0]
lat2, lon2 = ds2['XLAT_M'][0], ds2['XLONG_M'][0]

# Calculate bounds of d01 domain for extent
lat_min = lat1.min().item() - 2.0
lat_max = lat1.max().item() + 2.0
lon_min = lon1.min().item() - 2.0
lon_max = lon1.max().item() + 2.0

# Define projection
proj = ccrs.PlateCarree()

# Create plot
fig = plt.figure(figsize=(12, 9))
ax = plt.axes(projection=proj)
ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=proj)

# Add map features
ax.coastlines()
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.STATES, linewidth=0.5)
ax.gridlines(draw_labels=True)

# Plot terrain (filled contour)
terrain = ax.pcolormesh(lon1, lat1, hgt1, cmap='terrain', shading='auto', transform=proj)
cbar = plt.colorbar(terrain, ax=ax, orientation='vertical', pad=0.02, aspect=40)
cbar.set_label('Terrain Height (m)')

# Function to plot domain box
def plot_box(lat, lon, color, label):
    ax.plot(lon[0, :], lat[0, :], color=color, linewidth=2)
    ax.plot(lon[-1, :], lat[-1, :], color=color, linewidth=2)
    ax.plot(lon[:, 0], lat[:, 0], color=color, linewidth=2)
    ax.plot(lon[:, -1], lat[:, -1], color=color, linewidth=2)
    ax.text(lon[0, 0], lat[0, 0], label, color=color, fontsize=12, weight='bold')

# Plot domains
plot_box(lat1, lon1, 'blue', 'd01')
plot_box(lat2, lon2, 'red', 'd02')


# Add major cities from Natural Earth shapefile
shapename = 'populated_places'  # Can also use 'populated_places'
cities_shp = shpreader.natural_earth(resolution='110m', category='cultural', name='populated_places')

reader = shpreader.Reader(cities_shp)
for city in reader.records():
    lon, lat = city.geometry.x, city.geometry.y
    if lon_min <= lon <= lon_max and lat_min <= lat <= lat_max:
        ax.plot(lon, lat, marker='o', color='black', markersize=3, transform=proj)
        ax.text(lon + 0.1, lat + 0.1, city.attributes['NAME'], fontsize=8, transform=proj)


# Title and show
ax.set_title("WRF Domains with Terrain Elevation")
plt.show()







