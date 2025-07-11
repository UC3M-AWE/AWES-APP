import netCDF4
import numpy as np

def get_location_data(nc_path, lat, lon):
    """
    Given a NetCDF file, latitude, and longitude, return the closest roughness length and altitude (geopotential/9.80665).
    """
    ds = netCDF4.Dataset(nc_path)
    lats = ds.variables['latitude'][:]
    lons = ds.variables['longitude'][:]
    # ERA5 lons: 0..360, user may give -180..180
    lon_wrapped = lon if lon >= 0 else lon + 360
    lat_idx = np.abs(lats - lat).argmin()
    lon_idx = np.abs(lons - lon_wrapped).argmin()
    # Use first time index (monthly means, so 0=Jan)
    roughness = ds.variables['fsr'][0, lat_idx, lon_idx]
    geopotential = ds.variables['z'][0, lat_idx, lon_idx]
    altitude = geopotential / 9.80665
    ds.close()
    return float(roughness), float(altitude)
