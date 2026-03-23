#!/usr/bin/env python3

import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import math

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
gl=ax.gridlines(draw_labels=True)
gl.top_labels=False
gl.right_labels=False
gl.bottom_labels=True
gl.left_labels=True
gl.xlabel_style = {'size': 16}
gl.ylabel_style = {'size': 16}

# Plot terrain (filled contour)
terrain = ax.pcolormesh(lon1, lat1, hgt1, cmap='terrain', shading='auto', transform=proj)
cbar = plt.colorbar(terrain, ax=ax, orientation='vertical', pad=0.02, aspect=40)
cbar.ax.tick_params(labelsize=15)   # adjust numbers
cbar.set_label('Terrain Height (m)', fontsize=18)

# Function to plot domain box
def plot_box(lat, lon, color, label):
    ax.plot(lon[0, :], lat[0, :], color=color, linewidth=2)
    ax.plot(lon[-1, :], lat[-1, :], color=color, linewidth=2)
    ax.plot(lon[:, 0], lat[:, 0], color=color, linewidth=2)
    ax.plot(lon[:, -1], lat[:, -1], color=color, linewidth=2)
    ax.text(lon[0, 0] + 0.1, lat[0, 0] + 0.1, label, color=color, fontsize=18, weight='bold')

# Plot domains
plot_box(lat1, lon1, 'black', 'd01')
plot_box(lat2, lon2, 'black', 'd02')


# Add major cities from Natural Earth shapefile
shapename = 'populated_places'  # Can also use 'populated_places'
cities_shp = shpreader.natural_earth(resolution='110m', category='cultural', name='populated_places')

reader = shpreader.Reader(cities_shp)
for city in reader.records():
    lon, lat = city.geometry.x, city.geometry.y
    if lon_min <= lon <= lon_max and lat_min <= lat <= lat_max:
        ax.plot(lon, lat, marker='o', color='black', markersize=3, transform=proj)
        ax.text(lon + 0.1, lat + 0.1, city.attributes['NAME'], fontsize=12, transform=proj)

# --- Add a custom lat/lon point (Redding, CA) ---
redding_lat, redding_lon = 40.5865, -122.3917  # Approx coordinates for Redding, CA
ax.plot(redding_lon, redding_lat, marker='*', color='black', markersize=12,
                transform=proj, label="Redding, CA")
ax.text(redding_lon + 0.1, redding_lat + 0.1, "Redding",
                color='black', fontsize=18, weight='bold', transform=proj)

# --- Add 320° transect line ---
center_lat = 40.608912
center_lon = -122.436602
bearing_deg = 320.0
transect_half_length_km = 110

R = 6371.0  # Earth radius (km)

lat1 = math.radians(center_lat)
lon1 = math.radians(center_lon)
bearing_rad = math.radians(bearing_deg)
d = transect_half_length_km / R

# Forward endpoint
lat2 = math.asin(math.sin(lat1)*math.cos(d) +
    math.cos(lat1)*math.sin(d)*math.cos(bearing_rad))

lon2 = lon1 + math.atan2(math.sin(bearing_rad)*math.sin(d)*math.cos(lat1),
    math.cos(d)-math.sin(lat1)*math.sin(lat2))

# Reverse endpoint (bearing + 180°)
bearing_rev = math.radians((bearing_deg + 180) % 360)

lat3 = math.asin(math.sin(lat1)*math.cos(d) +
    math.cos(lat1)*math.sin(d)*math.cos(bearing_rev))

lon3 = lon1 + math.atan2(math.sin(bearing_rev)*math.sin(d)*math.cos(lat1),
    math.cos(d)-math.sin(lat1)*math.sin(lat3))

# Convert back to degrees
lat2 = math.degrees(lat2)
lon2 = math.degrees(lon2)
lat3 = math.degrees(lat3)
lon3 = math.degrees(lon3)

# Plot transect line
ax.plot([lon2, lon3], [lat2, lat3],
    color='brown', linewidth=2, linestyle="--",
    transform=ccrs.PlateCarree())

# Title and show
#ax.set_title("WRF Domains with Terrain Elevation", fontsize=18)
plt.show()







