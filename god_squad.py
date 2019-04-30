from pyproj import Proj as ppProj
from pyproj import transform as pptransform
import numpy as np


def jesus_christ(st_point, new_point, z):
    base_x, base_y = anti_christ(st_point)
    x = base_x + 20015077.371242613 / 128 / 2 ** z * new_point[0]
    y = base_y + 19949511.388901856 / 128 / 2 ** z * new_point[1]
    lon0 = 42
    lat0 = -30
    rad_earth = 6371229.0 * np.cos(np.radians(lat0))
    projection_merc_tmp = " ".join(("+proj=merc +lon_0=", str(lon0),
                                    "+k=1 +x_0=0 +y_0=0",
                                    "+ellps=sphere",
                                    "+a=", str(rad_earth),
                                    "+b=", str(rad_earth),
                                    "+units=m +no_defs")
                                   )
    proj_tmp = ppProj(projection_merc_tmp)
    laloProj = ppProj("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")
    lonor, lator = pptransform(proj_tmp, laloProj, x, y)
    lonor = max(lonor, -179.99)
    lonor = min(lonor, 179.99)
    lator = max(lator, -85)
    lator = min(lator, 85)
    return (lonor, -lator)


def anti_christ(st_point):
    lonor, lator = st_point
    lon0 = 42
    lat0 = -30
    rad_earth = 6371229.0 * np.cos(np.radians(lat0))
    projection_merc_tmp = " ".join(("+proj=merc +lon_0=", str(lon0),
                                    "+k=1 +x_0=0 +y_0=0",
                                    "+ellps=sphere",
                                    "+a=", str(rad_earth),
                                    "+b=", str(rad_earth),
                                    "+units=m +no_defs")
                                   )
    proj_tmp = ppProj(projection_merc_tmp)
    laloProj = ppProj("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")
    x, y = pptransform(laloProj, proj_tmp, lonor, lator)
    return (x, -y)
