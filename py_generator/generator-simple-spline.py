import c4d
#Connects two objects with a spline
#Python Generator. Needs two child objects
#Thomas Gugel // three-seconds.de


def main():
    objA = op.GetDown()
    objB = objA.GetNext()

    #Create Spline Objects
    spline = c4d.BaseObject(c4d.Ospline)
    #Define Points and Segments
    spline.ResizeObject(2, 1)

    #Set Point Position Data
    spline.SetPoint(0, objA.GetMg().off)
    spline.SetPoint(1, objB.GetMg().off)

    #Set Segment
    spline.SetSegment(0, 2, False)

    return spline