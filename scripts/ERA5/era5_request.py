#!/usr/bin/env python3

import cdsapi

c = cdsapi.Client()

print("Downloading data...")

c.retrieve(
    'reanalysis-era5-pressure-levels',
    {
        'product_type': 'reanalysis',
        'variable': [
            'geopotential',
            'temperature',
            'u_component_of_wind',
            'v_component_of_wind',
            'relative_humidity',
        ],
        'pressure_level': [
            '1','2','3','5','7','10','20','30','50','70',
            '100','125','150','175','200','225','250','300',
            '350','400','450','500','550','600','650','700',
            '750','775','800','825','850','875','900','925',
            '950','975','1000'
        ],
        'year': '1949',
        'month': '08',
        'day': ['04','05','06'],
        'time': [
            '00:00','01:00','02:00','03:00','04:00','05:00',
            '06:00','07:00','08:00','09:00','10:00','11:00',
            '12:00','13:00','14:00','15:00','16:00','17:00',
            '18:00','19:00','20:00','21:00','22:00','23:00'
        ],
        'data_format': 'grib',
        'area': [60, -135, 30, -90]
    },
    'era5_pl_19490804_06.grib')

c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',

        'variable': [

            '10m_u_component_of_wind',
            '10m_v_component_of_wind',

            '2m_temperature',
            '2m_dewpoint_temperature',

            'surface_pressure',
            'mean_sea_level_pressure',
            'geopotential',

            'skin_temperature',

            'soil_temperature_level_1',
            'soil_temperature_level_2',
            'soil_temperature_level_3',
            'soil_temperature_level_4',

            'volumetric_soil_water_layer_1',
            'volumetric_soil_water_layer_2',
            'volumetric_soil_water_layer_3',
            'volumetric_soil_water_layer_4',

        ],

        'year': '1949',
        'month': '08',
        'day': ['04','05','06'],

        'time': [
            '00:00','01:00','02:00','03:00',
            '04:00','05:00','06:00','07:00',
            '08:00','09:00','10:00','11:00',
            '12:00','13:00','14:00','15:00',
            '16:00','17:00','18:00','19:00',
            '20:00','21:00','22:00','23:00'
        ],

        'data_format': 'grib',

        'area': [60, -135, 30, -90]

        },

    'era5_sl_19490804_06.grib'
)
