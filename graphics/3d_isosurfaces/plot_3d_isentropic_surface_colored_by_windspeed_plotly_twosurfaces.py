#!/usr/bin/env python3

import numpy as np
import plotly.graph_objects as go
from netCDF4 import Dataset
from wrf import getvar, interplevel, latlon_coords, to_np
from scipy.ndimage import gaussian_filter

# ============================================================
# SETTINGS
# ============================================================

ncfile = Dataset("/home/natalie/carr/wrf/output/d02_more_vertical_layers/wrfout_d02_2018-07-26_070000.nc")
time_index = 19

theta_levels = [317.0, 318.0]  # two surfaces
#lat_min, lat_max = 40.521191, 40.709792
#lon_min, lon_max = -122.579788, -122.217254
lat_min, lat_max = 40.521191, 40.709792
lon_min, lon_max = -122.779788, -122.227161

fire_lat = 40.60998
fire_lon = -122.432530

# ============================================================
# FUNCTION TO GET SURFACE
# ============================================================

def get_surface(theta_level, time_index=time_index):
    theta = getvar(ncfile, "theta", timeidx=time_index)
    z     = getvar(ncfile, "z", timeidx=time_index)
    u     = getvar(ncfile, "ua", timeidx=time_index)
    v     = getvar(ncfile, "va", timeidx=time_index)

    wspd = np.sqrt(to_np(u)**2 + to_np(v)**2)

    z_theta    = interplevel(z, theta, theta_level)
    wspd_theta = interplevel(wspd, theta, theta_level)

    lats, lons = latlon_coords(z_theta)

    z_np    = to_np(z_theta)
    wspd_np = to_np(wspd_theta)
    lats    = to_np(lats)
    lons    = to_np(lons)

    # Crop domain
    mask = (
    (lats >= lat_min) & (lats <= lat_max) &
    (lons >= lon_min) & (lons <= lon_max)
    )
    rows, cols = np.where(mask)
    i_min, i_max = rows.min(), rows.max()
    j_min, j_max = cols.min(), cols.max()

    z_np    = z_np[i_min:i_max+1, j_min:j_max+1]
    wspd_np = wspd_np[i_min:i_max+1, j_min:j_max+1]
    lats    = lats[i_min:i_max+1, j_min:j_max+1]
    lons    = lons[i_min:i_max+1, j_min:j_max+1]

    # Smooth + subsample
    z_np = gaussian_filter(z_np, sigma=1)
    skip = 2
    z_np    = z_np[::skip, ::skip]
    wspd_np = wspd_np[::skip, ::skip]
    lats    = lats[::skip, ::skip]
    lons    = lons[::skip, ::skip]

    # Remove NaNs
    z_np = np.nan_to_num(z_np, nan=np.nanmin(z_np))
    wspd_np = np.nan_to_num(wspd_np, nan=0)

    return lons, lats, z_np, wspd_np

# ============================================================
# CREATE FIGURE
# ============================================================

fig = go.Figure()

colorscales = ['Viridis', 'Cividis']

for idx, theta_level in enumerate(theta_levels):
    lons, lats, z_np, wspd_np = get_surface(theta_level)

    fig.add_trace(go.Surface(
        x=lons,
        y=lats,
        z=z_np,
        surfacecolor=wspd_np,
        colorscale=colorscales[idx],
        opacity=0.8,
        colorbar=dict(title=f'Wind Speed (m/s) for θ={theta_level}K') if idx==0 else None,
        showscale=(idx==0)
    ))

# ============================================================
# FIRE MARKER
# ============================================================

# Use first surface for fire height
lons, lats, z_np, wspd_np = get_surface(theta_levels[0])
dist = (lats - fire_lat)**2 + (lons - fire_lon)**2
i_fire, j_fire = np.unravel_index(np.argmin(dist), dist.shape)
fire_z = z_np[i_fire, j_fire]

fig.add_trace(go.Scatter3d(
    x=[fire_lon],
    y=[fire_lat],
    z=[fire_z],
    mode='markers+text',
    marker=dict(size=8, color='red', line=dict(color='black', width=2)),
    text=["Fire"],
    textposition="top center"
))

# ============================================================
# LAYOUT
# ============================================================

fig.update_layout(
    title="Static Isentropic Surfaces θ = 316 K and 317 K",
    scene=dict(
        xaxis=dict(range=[lon_min, lon_max]),
        yaxis=dict(range=[lat_min, lat_max]),
        zaxis=dict(range=[500, 5000]),
        xaxis_title='Longitude',
        yaxis_title='Latitude',
        zaxis_title='Height (m)'
    ),
    margin=dict(l=0, r=0, b=0, t=40)
)

fig.show()
