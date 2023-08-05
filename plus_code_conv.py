from openlocationcode import openlocationcode as olc

def getLatLongFromShortPlusCode(code):
    code = code.split(' ')
    shortPlus = code[0][:-1] if code[0][-1] == ',' else code[0]
    # ignoring plus_ext for now
    
    # check validity first
    if not olc.isValid(shortPlus):
        print("Invalid Plus Code", shortPlus)
        return None, None
    
    # 23.6943, 90.3444 are coordinate of somewhat the middle point of bd
    completePlus = olc.recoverNearest(shortPlus, 23.6943, 90.3444)

    latlong = olc.decode(completePlus)
    lat, long = latlong.latitudeCenter, latlong.longitudeCenter
    return lat, long