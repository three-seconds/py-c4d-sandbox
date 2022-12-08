import c4d
from c4d import utils
import math
from c4d.modules import mograph as mo

#Connects Points from Matrix-Object, Cloner or TP-Particle-Group by the index of Clone/Particle
#Needs User Data Inputs

#Thomas Gugel // three-seconds.de

def main():

    #UserData
    name = op[c4d.ID_BASELIST_NAME]
    displayNull = op[c4d.ID_USERDATA,5]
    inObjSwitch = op[c4d.ID_USERDATA,6]
    cIndex = op[c4d.ID_USERDATA,8]
    mod = op[c4d.ID_USERDATA,13]

    spline = None

    #-----------------------------------------

    #Check Object Input Type
    typeCheckA = False
    typeCheckB = False

    inObjA = op[c4d.ID_USERDATA,2]
    inObjB = op[c4d.ID_USERDATA,3]

    if not inObjA or not inObjB:
        print (name + ": One or more Input Objects missing")
        return None
    else:

        inTypeA = inObjA.GetType()
        inTypeB = inObjB.GetType()
        typeCheckA = True if inTypeA == 1018545 or inTypeA == 1018544 or inTypeB == 1001381 else False
        typeCheckB = True if inTypeB == 1018545 or inTypeB == 1018544 or inTypeB == 1001381 else False

        if not typeCheckA or not typeCheckB:
            print (name + ": One or more Input Objects aren't Cloners, Matrix-Objects or Particle Groups")
            return None
        else:
            pass

    #-----------------------------------------

    #Grab Position Data from Matrix/Cloner or TP-Particle-Group

    #Init Matrix Array
    matsA = []
    matsB = []

    #If Input is PGroup
    if inTypeA == 1001381:

        inPGroupA = inObjA
        #Null Basecontainer für Positionsberechnung setzen, da PGroup keine Position hat.
        inObjA = c4d.BaseObject(c4d.Onull)

        tpMS = doc.GetParticleSystem()
        tpGroup = tpMS.GetParticleGroups(inPGroupA,c4d.TP_GETPGROUP_WITHPARTICLES, False)
        tP = tpGroup[0].GetParticles()
        tPnum = tpGroup[0].NumParticles()

        #Array füllen aus TPGroup
        for l in xrange(tPnum):
            matsA.append(tpMS.Transform(tP[l]))

    else:
        #Array füllen aus Matrix/Cloner
        dataA = mo.GeGetMoData(inObjA)
        matsA = dataA.GetArray(c4d.MODATA_MATRIX)



    # Wenn Input B eine Particle Group
    if inTypeB == 1001381:

        #inGroup aus user Link.
        inPGroupB = inObjB
        inObjB = c4d.BaseObject(c4d.Onull)

        tpMSB = doc.GetParticleSystem()
        tpGroupB = tpMSB.GetParticleGroups(inPGroupB,c4d.TP_GETPGROUP_WITHPARTICLES, False)
        tPB = tpGroupB[0].GetParticles()
        tPnumB = tpGroupB[0].NumParticles()

        #Fill Array with data from TPGroup
        for l in xrange(tPnumB):
            matsB.append(tpMSB.Transform(tPB[l]))

    else:
        #Fill Array with data from Matrix/Cloner
        dataB = mo.GeGetMoData(inObjB)
        matsB = dataB.GetArray(c4d.MODATA_MATRIX)

    #Check if there is some Data
    if not matsA == None and not matsB == None:
        cA = len(matsA)
        cB = len(matsB)

        cloneAmount = cA if cA <= cB else cB
    else:
        return None


    #Setting Spline Point Amount
    conCount = 0
    for w in xrange(cloneAmount):
        if w % mod == 0:
            conCount = conCount + 1

    splCount = conCount
    ptAmount = 2
    ptCount = (splCount * ptAmount)

    #Create spline if none
    if not spline:
        spline = createSpline(ptCount)
    else:
        if (ptCount != spline.GetPointCount()):
            spline.Remove()
            spline = createSpline(ptCount)

    #Set Spline points and segments
    if not cloneAmount == 0:
        i = 0
        for w in xrange(splCount):

            gPosA = matsA[w].off * inObjA.GetMg()
            gPosB = matsB[w].off * inObjB.GetMg()

            spline.SetPoint((i*(splCount*ptAmount) + (w*ptAmount)), gPosA)
            spline.SetPoint((i*(splCount*ptAmount) + (w*ptAmount))+1, gPosB)

            spline.SetSegment((i*(splCount)) + w, 2, False)

    #-----------------------------------------

    # Display Null Helper Stuff:
    if inObjSwitch:
        inObj = inObjA
        cIndex = cIndex if cIndex < cA else cA-1
        mats = matsA[cIndex]
    else:
        inObj = inObjB
        cIndex = cIndex if cIndex < cB else cB-1
        mats = matsB[cIndex]

    op[c4d.ID_USERDATA,7] = createControlNull(spline, displayNull, inObj, mats)

    #-----------------------------------------

    return spline


#Function for creating the Spline
def createSpline(ptCount):
    spline = c4d.SplineObject(1, c4d.SPLINETYPE_LINEAR)
    spline.ResizeObject(ptCount, ptCount/2)
    spline[c4d.ID_BASELIST_NAME] = "splines"
    return spline

#Function for creating a null Object
def createControlNull(objContainer, displayNull, inObj, lVec):
    tNull = c4d.BaseObject(c4d.Onull)
    globalPos = inObj.GetMg() * lVec
    tNull.SetMg(globalPos)
    tNull[c4d.NULLOBJECT_DISPLAY] = 11 if displayNull == True else 0
    tNull[c4d.NULLOBJECT_RADIUS] = 20
    tNull[c4d.NULLOBJECT_ORIENTATION] = 1
    tNull.InsertUnder(objContainer)
    return globalPos.off