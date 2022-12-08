import c4d
from c4d import utils
import math
import random
from c4d.utils import noise
from c4d.modules import mograph as mo
from c4d.modules import thinkingparticles as tp
#Connects Points from Ground-Matrix-Object or Cloner (INPUT-A) with a
#Cloner/Matrix or TP-Particle-Group (INPUT-B) by grayscale values.

#Info: Script has a pretty unique purpose and works fine there.
#But you run quicky into Errors if some main Input-Parameters are missing.
#Anyway: Feel free to use it, learn from it or revise it.

#Thomas Gugel // three-seconds.de

#Version: 0.5


def main():

    #UserData
    name = op[c4d.ID_BASELIST_NAME]

    displayNull = op[c4d.ID_USERDATA,5]
    inObjSwitch = op[c4d.ID_USERDATA,6]
    cIndex = op[c4d.ID_USERDATA,8]
    grid = op[c4d.ID_USERDATA,11]
    turbAmount = op[c4d.ID_USERDATA,12]
    bErrTh = op[c4d.ID_USERDATA,16]
    errTh = op[c4d.ID_USERDATA,14]
    kill = str(op[c4d.ID_USERDATA,15]).split(" ")
    search = op[c4d.ID_USERDATA,17]

    mod = op[c4d.ID_USERDATA,13]

    spline = None

    #-----------------------------------------

    #check if Input A is Matrix/Cloner and Input-B Matrix/Cloner or Particle Group
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

        typeCheckA = True if inTypeA == 1018545 or inTypeA == 1018544 else False
        typeCheckB = True if inTypeB == 1018545 or inTypeB == 1018544 or inTypeB == 1001381 else False

        if not typeCheckA or not typeCheckB:
            print (name + ":  One or more Input Objects aren't Cloners, Matrix-Objects or Particle Groups.")
            return None
        else:
            pass


    #Prepare Ground Grid:
    #If real clone count is higher as the calculated amount from the grid value in the Userdata (Ground Grid Setup),
    #you probably run into an 'index out of range' Error.
    gridCount = (grid*grid)
    gradientFactor = float(1 / float(gridCount))

    #-----------------------------------------

    #Acces Cloner Data from INPUT-A
    dataA = mo.GeGetMoData(inObjA)
    matsA = dataA.GetArray(c4d.MODATA_MATRIX)

    #Init Position and color Array
    matsB = []
    colorB = []

    #If TP-Group
    if inTypeB == 1001381:

        inPGroup = inObjB
        inObjB = c4d.BaseObject(c4d.Onull)

        tpMS = doc.GetParticleSystem()
        tpGroup = tpMS.GetParticleGroups(inPGroup,c4d.TP_GETPGROUP_WITHPARTICLES, False)
        tP = tpGroup[0].GetParticles()
        tPnum = tpGroup[0].NumParticles()

        #fill Arraylist from TPGroup Data
        for l in xrange(tPnum):
            matsB.append(tpMS.Transform(tP[l]))
            colorB.append(tpMS.Color(tP[l]))

    else:
        #Fill Arraylist from Matrix/Cloner
        dataB = mo.GeGetMoData(inObjB)
        matsB = dataB.GetArray(c4d.MODATA_MATRIX)
        colorB = dataB.GetArray(c4d.MODATA_COLOR)

    #check if there is data
    if not matsA == None and not matsB == None:
        cA = len(matsA)
        cB = len(matsB)
        cloneAmount = cB
    else:
        return None

    #-----------------------------------------

    #Setup and fill 2D Array:
    arrSortClone = []
    conCount = 0
    for i in xrange(gridCount):
        curColor = i*gradientFactor
        arrMatrix = []
        for u in xrange(cB):
            #Just take every X.Clone
            if u % mod == 0:
                if (colorB[u].x >= curColor and colorB[u].x <= (curColor+gradientFactor)):
                    arrMatrix.append(matsB[u])
                    conCount = conCount + 1

        arrSortClone.append(arrMatrix)

    #-----------------------------------------

    #Setting Spline Point Amount
    splCount = conCount
    ptAmount = 2
    ptCount = (splCount * ptAmount)

    #check if there is a spline
    if not spline:
        spline = createSpline(ptCount)
    else:
        if (ptCount != spline.GetPointCount()):
            spline.Remove()
            spline = createSpline(ptCount)

    if not cloneAmount == 0:
        #init Counter
        i = 0
        sC = 0

        for h in xrange(len(arrSortClone)):
            for y in xrange(len(arrSortClone[h])):
                gPosA = matsA[h].off * inObjA.GetMg()
                gPosB = arrSortClone[h][y].off * inObjB.GetMg()

                #randomize once, by Turbulence Noise. Pos = loopIndex:
                p = c4d.Vector(y,y,y)
                tX = noise.Turbulence(p, turbAmount, False, 0.0)
                tZ = noise.Turbulence(p+200, turbAmount, False, 1.0)
                gPosA = c4d.Vector(gPosA.x + tX, gPosA.y, gPosA.z + tZ)

                #Error Spline Handling:
                #This Part is kind of "buggy".
                if bErrTh:

                    tPos = c4d.Vector(gPosB.x,gPosA.y,gPosB.z)
                    #angle between A und B:
                    alpha = utils.RadToDeg(utils.GetAngle((gPosA-gPosB),(gPosA-tPos)))

                    #Check if angle to wide = probably error from reading Gradient. Just ignore Spline
                    if alpha < utils.RadToDeg(errTh):
                        gPosB = gPosA

                    if search:
                        #Find smallest angle, which then is probably wrong connected
                        if alpha <= G.sValue and not valueInKillList(kill, sC):
                            G.sCfound = sC
                            G.sValue = alpha

                    #The 'Kill-List': Write the Number of the spline in the text field
                    #seperated by blanks to remove it
                    for q in xrange(len(kill)):
                        if not len(kill[q].strip()) == 0:
                            #If in Kill-List, don't connect spline
                            if int(kill[q]) == sC:
                                gPosB = gPosA

                spline.SetPoint((i*(splCount*ptAmount) + (sC*ptAmount)), gPosA)
                spline.SetPoint((i*(splCount*ptAmount) + (sC*ptAmount))+1, gPosB)

                spline.SetSegment((i*(splCount)) + sC, 2, False)

                sC = sC + 1

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

    #Print Search result to console
    if search:
        if not bErrTh:
            print "Please enable Error Spline Handling first"
        else:
            print "Search Result: " + str(round(G.sValue, 1)) + "° (Spline Number: " + str(G.sCfound) + ")"
            print "----"

    #-----------------------------------------

    return spline


#Function for creating a spline
def createSpline(ptCount):
    spline = c4d.SplineObject(1, c4d.SPLINETYPE_LINEAR)
    spline.ResizeObject(ptCount, ptCount/2)
    spline[c4d.ID_BASELIST_NAME] = "splines"
    return spline

#Function for creating a null-object
def createControlNull(objContainer, displayNull, inObj, lVec):
    tNull = c4d.BaseObject(c4d.Onull)
    globalPos = inObj.GetMg() * lVec
    tNull.SetMg(globalPos)
    tNull[c4d.NULLOBJECT_DISPLAY] = 11 if displayNull == True else 0
    tNull[c4d.NULLOBJECT_RADIUS] = 20
    tNull[c4d.NULLOBJECT_ORIENTATION] = 1
    tNull.InsertUnder(objContainer)
    return globalPos.off

#Function to search through list
def valueInKillList(killlist, sC):
    r = False
    if len(killlist[0].strip()) == 0:
        r = False
    else:
        for o in xrange(len(killlist)):
            if sC == int(killlist[o]):
                r = True
                break
            else:
                r = False
    return r

#Global Class to safe the search result Data
class G:
    sValue = 150
    sCfound = 0