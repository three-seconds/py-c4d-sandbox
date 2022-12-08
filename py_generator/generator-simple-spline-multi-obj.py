import c4d
#Connects objects with a spline
#Renames all objects and connects them with a spline
#Thomas Gugel // three-seconds.de


def main():
    #Get all Object among op
    objList = op.GetChildren()

    #Object Count
    pC = len(objList)

    spline = c4d.BaseObject(c4d.Ospline)
    spline.ResizeObject(pC, 1)

    #Loop through all objects, rename and set spline point position
    for i in xrange(pC):
        obj = objList[i]
        obj[c4d.ID_BASELIST_NAME] = str(i+1).zfill(2)
        oPos = obj.GetMg().off
        spline.SetPoint(i, oPos)

    spline.SetSegment(0, pC, False)

    return spline