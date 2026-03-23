#!/usr/bin/env python3

import requests
import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

API_ROOT = "https://api.synopticdata.com/v2/"
API_TOKEN = "33e3c8ee12dc499c86de1f2076a9e9d4"

# --------------------------------------------------
# Station and time range
# --------------------------------------------------

station = "MSGRB"

start_time = "201807262000"
end_time   = "201807270900"

# --------------------------------------------------
# Request station data
# --------------------------------------------------

api_request_url = os.path.join(API_ROOT, "stations/timeseries")

api_arguments = {
    "token": API_TOKEN,
    "stid": station,
    "vars": "wind_speed,wind_direction",
    "start": start_time,
    "end": end_time
}

req = requests.get(api_request_url, params=api_arguments)

data = req.json()

stations = data["STATION"]

if len(stations) == 0:
    print("No station data returned.")
    exit()

st = stations[0]

obs = st.get("OBSERVATIONS", {})

times = obs.get("date_time", [])
winds = obs.get("wind_speed_set_1", [])
dirs  = obs.get("wind_direction_set_1", [])

# --------------------------------------------------
# Convert times
# --------------------------------------------------

times_dt = [datetime.strptime(t,"%Y-%m-%dT%H:%M:%SZ") for t in times]

winds = np.array(winds, dtype=float)
dirs  = np.array(dirs, dtype=float)

# --------------------------------------------------
# Plot
# --------------------------------------------------

fig, (ax1, ax2) = plt.subplots(
    2, 1,
    figsize=(10,6),
    sharex=True
)

# Wind speed
ax1.plot(times_dt, winds, marker="o")
ax1.set_ylabel("Wind Speed (m/s)")
ax1.set_title(f"{station} Wind Observations")

ax1.grid(True)

# Wind direction
ax2.plot(times_dt, dirs, marker="o", color="orange")
ax2.set_ylabel("Wind Direction (°)")
ax2.set_xlabel("Time (UTC)")

ax2.set_ylim(0,360)
ax2.set_yticks([0,90,180,270,360])

ax2.grid(True)

plt.tight_layout()
plt.show()

