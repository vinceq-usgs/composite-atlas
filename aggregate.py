import math
import geojson

from utm import from_latlon,to_latlon,OutOfRangeError

PRECISION = 4    # How many decimal places to output lat/lon coords
#---------------------
# UTM Helper Functions
#---------------------

def getUtmFromCoordinates(lat,lon,span=None):
    """

    :synopsis: Convert lat/lon coordinates to UTM string
    :param float lat: Latitude
    :param float lon: Longitude
    :param span: (optional) Size of the UTM box (see below)
    :returns: UTM string with the correct resolution

    Convert lat/lon coordinates into a UTM string using the :py:obj:`UTM` package. If :py:obj:`span` is specified, the output resolution is degraded via the :py:obj:`floor` function.

    :py:obj:`span` accepts the values 'geo_10km', 'geo_1km', or the size of the UTM box in meters (should be a power of 10).

    This will NOT filter the location based on precision of the input coordinates.

    """

    span=_floatSpan(span)

    try:
        loc=from_latlon(lat,lon)
    except OutOfRangeError:
        # Catchall for any location that cannot be geocoded
        return None

    x,y,zonenum,zoneletter=loc
    x=myFloor(x,span)
    y=myFloor(y,span)

    utm='{} {} {} {}'.format(x,y,zonenum,zoneletter)
    return utm


def _floatSpan(span):

    if span=='geo_1km' or span=='1km' or span==1000:
        span=1000
    elif span=='geo_10km' or span=='10km' or span==10000:
        span=10000
    elif span=='geo_100km' or span=='100km' or span==100000:
        span=100000
    else:
        raise TypeError('Invalid span value '+str(span))

    return span


def getUtmPolyFromString(utm,span):
    """

    :synopsis: Compute the (lat/lon) bounds and center from a UTM string
    :param utm: A UTM string
    :param int span: The size of the UTM box in meters
    :return: :py:obj:`dict`, see below

    Get the bounding box polygon and center point for a UTM string suitable for plotting.

    The return value has two keys:

    ======    ========================
    center    A GeoJSON Point object
    bounds    A GeoJSON Polygon object
    ======    ========================

    """

    x,y,zone,zoneletter=utm.split()
    x=int(x)
    y=int(y)
    zone=int(zone)

    # Compute bounds. Need to reverse-tuple here because the
    # to_latlon function returns lat/lon and geojson requires lon/lat.
    # Rounding needed otherwise lat/lon coordinates are arbitrarily long

    ebound=zone*6-180
    wbound=ebound-6

    def _reverse(tup,eastborder=None):

        (y,x)=tup
        if eastborder and x>ebound:
            x=ebound
        elif x<wbound:
            x=wbound
        x=round(x,PRECISION)
        y=round(y,PRECISION)
        return (x,y)

    p1=_reverse(to_latlon(x,y,zone,zoneletter))
    p2=_reverse(to_latlon(x,y+span,zone,zoneletter))
    p3=_reverse(to_latlon(x+span,y+span,zone,zoneletter),'e')
    p4=_reverse(to_latlon(x+span,y,zone,zoneletter),'e')
    bounds=geojson.Polygon([[p1,p2,p3,p4,p1]])

    # Compute center
    cx=int(x)+span/2
    cy=int(y)+span/2
    clat,clon=to_latlon(cx,cy,zone,zoneletter)
    clat=round(clat,PRECISION)
    clon=round(clon,PRECISION)
    center=geojson.Point((clon,clat))

    return ({'center':center,'bounds':bounds})


#-------------------------
# Utility Functions
#-------------------------

def myFloor(x,multiple):
    """

    :synopsis: Round down to a multiple of 10/100/1000...
    :param float x: A number
    :param int multiple: Power of 10 indicating how many places to round
    :returns: int

    This emulates the `math.floor` function but
    rounding down a positive power of 10 (i.e. 10, 100, 1000...)

    For example, myFloor(1975,100) returns 1900.

    """

    y=x/multiple
    return int(math.floor(y) * multiple)


def myCeil(x,multiple):
    """

    :synopsis: Round up to a multiple of 10/100/etc.
    :param float x: A number
    :param int multiple: Power of 10 indicating how many places to round
    :returns: int

    This emulates the `math.ceil` function but
    rounding up a positive power of 10 (i.e. 10, 100, 1000...)

    For example, myCeil(1975,100) returns 2000.

    """

    return int(math.ceil(x/multiple) * multiple)

