import geocoder

# Origin location

def get_location_origin(origin):
    g = geocoder.osm(origin)
    if g.ok:
        latitude = g.latlng[0]
        longitude = g.latlng[1]
        return latitude, longitude
    else:
        return None

# Destination location

def get_location_destination(dest):
    g = geocoder.osm(dest)
    if g.ok:
        latitude = g.latlng[0]
        longitude = g.latlng[1]
        return latitude, longitude
    else:
        return None
