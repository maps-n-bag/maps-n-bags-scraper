from openlocationcode import openlocationcode as olc

code = 'P9WC+9F Dhaka'
code = code.split(' ')
shortPlus, plus_ext = code[0], code[1]

# ignoring plus_ext for now
# 23.6943, 90.3444 are coordinate of somewhat the middle point of bd
completePlus = olc.recoverNearest(shortPlus, 23.6943, 90.3444)
print(completePlus)

latlong = olc.decode(completePlus)
lat, long = latlong.latitudeCenter, latlong.longitudeCenter
print(lat, long)