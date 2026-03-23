#!/usr/bin/env python3

import requests
import os
import math
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io.img_tiles import OSM
from cartopy.io.img_tiles import GoogleTiles
from datetime import datetime

API_ROOT = "https://api.synopticdata.com/v2/"
API_TOKEN = "33e3c8ee12dc499c86de1f2076a9e9d4"

# --------------------------------------------------
# Bounding box
# --------------------------------------------------

#bbox = "-122.853652,40.331588,-122.023955,40.902376"
bbox = "-124.953652,39.831588,-121.023955,41.502376"

start_time = "201807270100"
end_time   = "201807270400"

#201807270200 = 07/26 1900 LT
target_time = datetime.strptime("201807270300","%Y%m%d%H%M")

# --------------------------------------------------
# Request station data
# --------------------------------------------------

api_request_url = os.path.join(API_ROOT,"stations/timeseries")

api_arguments = {
    "token":API_TOKEN,
    "bbox":bbox,
    "vars":"wind_speed,wind_direction",
    "start":start_time,
    "end":end_time
}

req = requests.get(api_request_url,params=api_arguments)

data = req.json()

stations = data["STATION"]

print("Stations returned:",len(stations))

# --------------------------------------------------
# Extract station winds nearest target time
# --------------------------------------------------

lats=[]
lons=[]
u=[]
v=[]
stids=[]

for st in stations:

    obs = st.get("OBSERVATIONS", {})

    # ---- Check that wind variables exist ----
    if "wind_speed_set_1" not in obs or "wind_direction_set_1" not in obs:
        continue

    times = obs.get("date_time", [])
    winds = obs.get("wind_speed_set_1", [])
    dirs  = obs.get("wind_direction_set_1", [])

    if len(times) == 0 or len(winds) == 0 or len(dirs) == 0:
        continue

    try:

        # convert timestamps
        times_dt = [datetime.strptime(t,"%Y-%m-%dT%H:%M:%SZ") for t in times]

        # find closest timestep
        idx = np.argmin([abs((t-target_time).total_seconds()) for t in times_dt])

        wspd = winds[idx]
        wdir = dirs[idx]

        # skip missing values
        if wspd is None or wdir is None:
            continue

        wspd = float(wspd)
        wdir = float(wdir)

        rad = math.radians(wdir)

        u_comp = -wspd * math.sin(rad)
        v_comp = -wspd * math.cos(rad)

        lat = float(st["LATITUDE"])
        lon = float(st["LONGITUDE"])

        lats.append(lat)
        lons.append(lon)
        u.append(u_comp)
        v.append(v_comp)
        stids.append(st["STID"])

    except Exception:
        continue

# --------------------------------------------------
# Basemap
# --------------------------------------------------

#tiler = OSM()
#
#plt.figure(figsize=(12,10))
#ax = plt.axes(projection=tiler.crs)
#ax.add_image(tiler, 8)
#
#
#extent = [-122.853652,-122.023955,40.331588,40.902376]
#ax.set_extent(extent, crs=ccrs.PlateCarree())
#
#gl = ax.gridlines(draw_labels=True)
#gl.top_labels = False
#gl.right_labels = False
#gl.xlabel_style = {'size': 14}
#gl.ylabel_style = {'size': 14}

# --------------------------------------------------
# Basemap (ESRI shaded relief)
# --------------------------------------------------

#tiler = GoogleTiles(
#            url="https://a.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png"
#            )
tiler = GoogleTiles(
            url="https://services.arcgisonline.com/ArcGIS/rest/services/World_Shaded_Relief/MapServer/tile/{z}/{y}/{x}"
            )

plt.figure(figsize=(12,10))
ax = plt.axes(projection=tiler.crs)

ax.add_image(tiler, 11)

#extent = [-122.853652,-122.023955,40.331588,40.902376]
extent = [-124.953652,-121.023955,39.831588,41.502376]
ax.set_extent(extent, crs=ccrs.PlateCarree())

# --------------------------------------------------
# Plot wind vectors
# --------------------------------------------------

lons = np.array(lons)
lats = np.array(lats)
u = np.array(u)
v = np.array(v)

print("u=", u)
print("v=", v)
print("stid=", stids)

ax.quiver(
    lons,
    lats,
    u,
    v,
    scale=100,
    width=0.004,
    color="black",
    transform=ccrs.PlateCarree()
)

# --------------------------------------------------
# Station markers
# --------------------------------------------------

ax.scatter(
    lons,
    lats,
    color="red",
    s=30,
    transform=ccrs.PlateCarree(),
    zorder=5
)

# --------------------------------------------------
# Labels
# --------------------------------------------------

for i,stid in enumerate(stids):

    ax.text(
        lons[i]+0.01,
        lats[i]+0.01,
        stid,
        fontsize=9,
        transform=ccrs.PlateCarree()
    )

plt.title("Observed Surface Winds Near 2018-07-26 20:00 LT")
plt.tight_layout()
plt.show()

