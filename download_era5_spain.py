import cdsapi

c = cdsapi.Client()
c.retrieve(
    'reanalysis-era5-single-levels-monthly-means',
    {
      'product_type': 'reanalysis',
      'format': 'netcdf',
      'variable': [
        '10m wind speed',
        'surface roughness',
        'geopotential'
      ],
      'year':  ['2022'],
      'month': [f"{m:02d}" for m in range(1,13)],
      'time':  ['00:00'],
      'area':  [45, -11, 35, 5],   # N, W, S, E
    },
    'era5_spain_monthly.nc'
)
print("✅ Download complete: era5_spain_monthly.nc")