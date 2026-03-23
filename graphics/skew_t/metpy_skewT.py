#!/usr/bin/env python3

# Full Skew-T (MetPy) from WRF sounding
import xarray as xr
from netCDF4 import Dataset
from wrf import ll_to_xy, getvar
import numpy as np
import matplotlib.pyplot as plt

# MetPy imports
import metpy.calc as mpcalc
from metpy.plots import SkewT, add_metpy_logo
from metpy.units import units

# -------------------------
# User inputs
# -------------------------
wrf_file = "/home/natalie/carr/wrf/output/d02_more_vertical_layers/wrfout_d02_2018-07-26_070000.nc"
#downstream
target_lat = 40.60998
target_lon = -122.432530
#upstream
#target_lat = 40.700252
#target_lon = -122.620575
#more upstream
#target_lat = 40.713240
#target_lon = -122.717847
#on the coast
#target_lat = 40.74555
#target_lon = -124.192123

time_index = 21
zmax = 20000
#zmax = 2000
# -------------------------

# Open WRF: use xarray for convenience and netCDF4 for wrf-python where required
ds = xr.open_dataset(wrf_file)
nc = Dataset(wrf_file)

# Get nearest grid index (wrf-python expects a netCDF4 Dataset)
ij = ll_to_xy(nc, target_lat, target_lon)
# ll_to_xy returns (i, j) or (x,y) depending on version; robustly convert:
try:
    i_index, j_index = int(ij[0]), int(ij[1])
except Exception:
    # If it's returned as (y,x) or as a scalar-array, try swapping
    i_index, j_index = int(ij[1]), int(ij[0])

# Extract basic variables (wrf-python getvar returns arrays in sensible units)
p = getvar(nc, "pressure", timeidx=time_index)   # hPa
T = getvar(nc, "tc",       timeidx=time_index)   # degC
Td= getvar(nc, "td",       timeidx=time_index)   # degC
z = getvar(nc, "z",        timeidx=time_index)   # m (geopotential or geopotential height)
u = getvar(nc, "ua",       timeidx=time_index)   # m/s
v = getvar(nc, "va",       timeidx=time_index)   # m/s

# Index the vertical profile at the grid cell (some wrf versions return [bottom->top] ordering)
p_vals  = p[:, j_index, i_index].values
T_vals  = T[:, j_index, i_index].values
Td_vals = Td[:, j_index, i_index].values
z_vals  = z[:, j_index, i_index].values
u_vals  = u[:, j_index, i_index].values
v_vals  = v[:, j_index, i_index].values

# Optional: mask to z <= zmax (keeps pressure ordering)
mask = z_vals <= zmax
p_vals  = p_vals[mask]
T_vals  = T_vals[mask]
Td_vals = Td_vals[mask]
z_vals  = z_vals[mask]
u_vals  = u_vals[mask]
v_vals  = v_vals[mask]

# Attach MetPy units
p_q   = p_vals * units.hPa
T_q   = T_vals * units.degC
Td_q  = Td_vals * units.degC
u_q   = u_vals * units('m/s')
v_q   = v_vals * units('m/s')

# -------------------------
# Compute parcel profile, LCL, LFC, EL, CAPE/CIN
# -------------------------
# Surface (lowest model level) as parcel source
p_sfc = p_q[0]
T_sfc = T_q[0]
Td_sfc= Td_q[0]

# LCL
lcl_pressure, lcl_temperature = mpcalc.lcl(p_sfc, T_sfc, Td_sfc)

# Parcel profile (temperature of parcel lifted dry then moist)
parcel_prof = mpcalc.parcel_profile(p_q, T_sfc, Td_sfc)

# CAPE/CIN (returns (cape, cin) in J/kg)
cape, cin = mpcalc.cape_cin(p_q, T_q, Td_q, parcel_prof)

# Find LFC and EL (MetPy has lfc and el helpers)
try:
    lfc_pressure = mpcalc.lfc(p_q, T_q, Td_q, parcel_prof)
except Exception:
    lfc_pressure = None
try:
    el_pressure = mpcalc.el(p_q, T_q, Td_q, parcel_prof)
except Exception:
    el_pressure = None

# -------------------------
# Create Skew-T plot
# -------------------------
fig = plt.figure(figsize=(9, 9))
skew = SkewT(fig, rotation=45)

# Plot temperature and dewpoint
skew.plot(p_q, T_q, 'r', linewidth=2, label='Temperature')
skew.plot(p_q, Td_q, 'g', linewidth=2, label='Dewpoint')

# Plot parcel ascent
skew.plot(p_q, parcel_prof, 'k', linewidth=2, linestyle='--', label='Parcel Path')

# Add wind barbs (reduce number of barbs by slicing)
skew.plot_barbs(p_q[::1], u_q[::1], v_q[::1], length=6)

# Add special lines
skew.plot_dry_adiabats()
skew.plot_moist_adiabats()
skew.plot_mixing_lines()

# Mark LCL, LFC, EL on the plot (vertical markers)
skew.plot(lcl_pressure, lcl_temperature, marker='o', color='purple', label='LCL')
if lfc_pressure is not None and hasattr(lfc_pressure, 'magnitude'):
    # compute parcel temp at LFC pressure for plotting point location
    try:
        t_at_lfc = np.interp(lfc_pressure.magnitude, p_q.magnitude[::-1], parcel_prof.magnitude[::-1]) * units.degC
        skew.plot(lfc_pressure, t_at_lfc, marker='D', color='blue', label='LFC')
    except Exception:
        pass
if el_pressure is not None and hasattr(el_pressure, 'magnitude'):
    try:
        t_at_el = np.interp(el_pressure.magnitude, p_q.magnitude[::-1], parcel_prof.magnitude[::-1]) * units.degC
        skew.plot(el_pressure, t_at_el, marker='D', color='orange', label='EL')
    except Exception:
        pass

# Add legend, labels and title
skew.ax.set_xlabel('Temperature (°C)', fontsize=22)
skew.ax.set_ylabel('Pressure (hPa)', fontsize=22)
#skew.ax.set_ylim(100, 1000)        # typical Skew-T limits (adjust as needed)
skew.ax.set_ylim(400, 1000)        # typical Skew-T limits (adjust as needed)
skew.ax.set_xlim(-40, 50)
skew.ax.invert_yaxis()
skew.ax.tick_params(axis='both', labelsize=22)

#plt.title(f"0200 UTC Skew-T at {target_lat:.2f}, {target_lon:.2f}")

# Add MetPy logo (optional)
#add_metpy_logo(fig, 115, 100)

# Print CAPE/CIN values
print(f"CAPE = {cape:.1f} J/kg, CIN = {cin:.1f} J/kg")

plt.legend(loc='upper right')
plt.tight_layout()
plt.show()

