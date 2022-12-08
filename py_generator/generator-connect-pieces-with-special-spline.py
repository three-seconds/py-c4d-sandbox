import c4d
from c4d import utils
import math
from c4d.modules import mograph as mo

#Connects Clones with Splines depending on the position in space and generates cornerpoints.
#Info: Script works fine for my intended purpose. It is not perfect - still has his flaws.
#Anyway: Feel free to use it, learn from it or revise it.

#Needs UserData Inputs. 
#If you need help. Drop me a line.

#Thomas Gugel // three-seconds.de



def main():

    #Collect user Data:
    name = op[c4d.ID_BASELIST_NAME]

    #Reset some stuff on Frame 0:
    frame = doc.GetTime().GetFrame(doc.GetFps())
    if (frame == 0):
        #Torn
        op[c4d.ID_USERDATA,21] = False


    #Thickness of Pieces
    w = op[c4d.ID_USERDATA,5]
    #Distance to Input Object
    a = op[c4d.ID_USERDATA,6]
    #offset Cornerpoint
    e = op[c4d.ID_USERDATA,7]
    #Tear-of Distance
    d = op[c4d.ID_USERDATA,8]
    torn = op[c4d.ID_USERDATA,21]
    #Generator spline in Object Manager?
    genS = op[c4d.ID_USERDATA,9]
    #Display null on/off?
    display = op[c4d.ID_USERDATA,10]
    dispRadius = op[c4d.ID_USERDATA,18]
    #Slide on/off?
    slide = op[c4d.ID_USERDATA,11]
    slideIL = op[c4d.ID_USERDATA,14]
    slideIU = op[c4d.ID_USERDATA,15]
    slideOL = op[c4d.ID_USERDATA,16]
    slideOU = op[c4d.ID_USERDATA,17]

    #Generate main null in memory
    objContainer = c4d.BaseObject(c4d.Onull)

    #-----------------------------------------

    #Grab generated Spline
    projSpline = op.GetDown()

    #Setting Spline Point Amount
    segCount = 1
    splCount = 1
    ptAmount = 4

    wS = splCount-1
    ptCount = segCount * (splCount * ptAmount)

    # If there is no Spline in Object-Manager
    if not projSpline:
        projSpline = createProjSpline(op, segCount, ptCount)
    else:
        if (ptCount != projSpline.GetPointCount()):
            projSpline.Remove()
            projSpline = createProjSpline(op, segCount, ptCount)


    #-----------------------------------------

    #Grab Cloner Objects as Input from UserData:
    moObjA = op[c4d.ID_USERDATA,1]
    moObjB = op[c4d.ID_USERDATA,2]

    #Clone Index for A and B from UserData:
    cIdA = op[c4d.ID_USERDATA,19]
    cIdB = op[c4d.ID_USERDATA,20]

    #check if Inputs aren't empty
    if not moObjA or not moObjB:
        projSpline[c4d.ID_BASEOBJECT_GENERATOR_FLAG] = False
        print (name + ": One or more Input Objects missing.")
        return None
    else:
        #check if Input Objekt is a Cloner (1018544 = Cloner)
        if not moObjA.GetType() == 1018544 or not moObjB.GetType() == 1018544:
            print (name + ": One or more Input Objects aren't Cloner.")
            return None
        else:
            projSpline[c4d.ID_BASEOBJECT_GENERATOR_FLAG] = True

    #Generate Nulls, for positioning on Input-Clone-Index A and B
    nA = c4d.BaseObject(c4d.Onull)
    nB = c4d.BaseObject(c4d.Onull)

    #Access Cloner Data
    moDataA = mo.GeGetMoData(moObjA)
    moMatsA = moDataA.GetArray(c4d.MODATA_MATRIX)
    moCountA =  len(moMatsA)

    moDataB = mo.GeGetMoData(moObjB)
    moMatsB = moDataB.GetArray(c4d.MODATA_MATRIX)
    moCountB =  len(moMatsB)

    #Set NULL Objects to Clone Position (Matrix)
    nA.SetMg(moMatsA[cIdA if cIdA < moCountA else moCountA-1])
    nB.SetMg(moMatsB[cIdB if cIdB < moCountB else moCountB-1])

    #-----------------------------------------

    # Set Main Objects A und B:
    A = nA
    B = nB

    #-----------------------------------------

    # Create first Cornerpoint A1 + Parenting to Object A
    A1 = c4d.BaseObject(c4d.Onull)

    A1[c4d.NULLOBJECT_DISPLAY] = 11 if display == True else 0
    A1[c4d.NULLOBJECT_RADIUS] = dispRadius
    A1[c4d.NULLOBJECT_ORIENTATION] = 1

    M_T1 = A.GetMg()
    M_T2 = c4d.Matrix()
    M_T2.off = c4d.Vector(a,0,0)
    M_T2 = M_T1 * M_T2

    A1.SetMg(M_T2)

    # Create first Cornerpoint B1 + Parenting to Object B
    B1 = c4d.BaseObject(c4d.Onull)
    B1[c4d.NULLOBJECT_DISPLAY] = 11 if display == True else 0
    B1[c4d.NULLOBJECT_RADIUS] = dispRadius
    B1[c4d.NULLOBJECT_ORIENTATION] = 1

    M_T4 = B.GetMg()
    M_T3 = c4d.Matrix()
    M_T3.off = c4d.Vector(a,0,0)
    M_T3 = M_T4 * M_T3

    B1.SetMg(M_T3)

    #Main principle: Calculate local Vector between the pieces
    mBA = B.GetMg().off * ~A.GetMg()
    mAB = A.GetMg().off * ~B.GetMg()

    #-----------------------------------------

    #Vectors for angle between BA und BC
    BA = A.GetMg().off - B.GetMg().off
    BC = B1.GetMg().off - B.GetMg().off

    #Vectoren für Winkel zwischen AB und AC
    AB = B.GetMg().off - A.GetMg().off
    AC = A1.GetMg().off - A.GetMg().off

    #calculate angle between two vectors
    alphaA = utils.RadToDeg(utils.VectorAngle(AB, AC))
    alphaB = utils.RadToDeg(utils.VectorAngle(BA, BC))
    #Abs Angle difference
    alphaDif = abs(alphaA - alphaB)

    #Area of angle mapping:
    wA = utils.RangeMap(alphaA, 50, 75, 0, w, True)
    wB = utils.RangeMap(alphaB, 50, 75, 0, w, True)

    #Distance between objects
    AB = B.GetMg().off - A.GetMg().off
    dist = AB.GetLength()


    #Spline shift from distance of height (Y):
    bBA = mBA.y
    bAB = mAB.y

    #Slide
    if (slide == True):
        slideFactorA = utils.RangeMap(wA, 0, w, 0, 1, True)
        slideFactorB = utils.RangeMap(wB, 0, w, 0, 1, True)

        bBA = utils.RangeMap(bBA, slideIL, slideIU, slideOL, slideOU, True)
        bAB = utils.RangeMap(bAB, slideIL, slideIU, slideOL, slideOU, True)

        bBA *= slideFactorA
        bAB *= slideFactorB
    else:
        bBA = 0
        bAB = 0


    #-----------------------------------------

    #Calculate Spline Points
    if (not dist >= d):

        if (mBA.z >= 0):
            B[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(1,1,1)
            M_A1 = A1.GetMg()
            M_A2 = c4d.Matrix()
            M_A2.off = c4d.Vector(e,bBA,wA)
            M_A2 = M_A1 * M_A2

        elif (mBA.z < 0):
            B[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(.5,0,0)
            M_A1 = A1.GetMg()
            M_A2 = c4d.Matrix()
            M_A2.off = c4d.Vector(e,bBA,-wA)
            M_A2 = M_A1 * M_A2

        if (mAB.z >= 0):
            A[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(1,1,1)
            M_B1 = B1.GetMg()
            M_B2 = c4d.Matrix()
            M_B2.off = c4d.Vector(e,bAB,wB)
            M_B2 = M_B1 * M_B2
        elif (mAB.z < 0):
            A[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(.5,0,0)
            M_B1 = B1.GetMg()
            M_B2 = c4d.Matrix()
            M_B2.off = c4d.Vector(e,bAB,-wB)
            M_B2 = M_B1 * M_B2

        #Set Points
        projSpline.SetPoint(0, A1.GetMg().off)
        projSpline.SetPoint(1, M_A2.off)
        projSpline.SetPoint(2, M_B2.off)
        projSpline.SetPoint(3, B1.GetMg().off)

        #Set Segements
        i = 0
        projSpline.SetSegment((i*(splCount)) + wS, ptAmount, False)

        #Set Torn Info
        op[c4d.ID_USERDATA,21] = False

    else:
        #Set Torn Info
        op[c4d.ID_USERDATA,21] = True

        projSpline.SetPoint(0, A.GetMg().off)
        projSpline.SetPoint(1, A.GetMg().off)
        projSpline.SetPoint(2, A.GetMg().off)
        projSpline.SetPoint(3, A.GetMg().off)

        #Set Segements
        i = 0
        projSpline.SetSegment((i*(splCount)) + wS, ptAmount, False)


    #-----------------------------------------

    #Fill Container Object with generated Objects
    A1.InsertUnder(objContainer)
    B1.InsertUnder(objContainer)

    #Generate Spline in object Manager?
    if (genS == True):
        projSpline.InsertUnder(op)
        projSpline.Message(c4d.MSG_UPDATE)
    else:
        projSpline.InsertUnder(objContainer)

    return objContainer


#Function: generate Spline
def createProjSpline(op, segCount, ptCount):
    projSpline = c4d.SplineObject(segCount, c4d.SPLINETYPE_LINEAR)
    projSpline.ResizeObject(ptCount, segCount)
    projSpline[c4d.ID_BASELIST_NAME] = "projSpline"
    return projSpline