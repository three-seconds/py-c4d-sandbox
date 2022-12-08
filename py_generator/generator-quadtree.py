

import c4d
from c4d import utils
from c4d.utils import noise
from c4d.modules import mograph as mo
import random
#Quadtree Generator: Distributes Instances on given Points from Base Matrix Object
#Divides Grid in max 3 Levels. Even works with Rigid-Body Dynamics and Effectors
#on the Base Matrix Object.

#It developed from some playaround stuff. So it is still a work-in-progress thing.
#Anyway: Feel free to use it, learn from it or revise it.

#Script needs UserData Inputs. 

#If you need help. Drop me a line.
#Thomas Gugel // three-seconds.de

#Version: 1.0


def main():

    oInstMode = 1
    container = c4d.BaseObject(c4d.Onull)
    cloner = op[c4d.ID_USERDATA,7]

    uSc = op[c4d.ID_USERDATA,11]
    offset = 0

    uTh = op[c4d.ID_USERDATA,5]
    uRObjSwitch = op[c4d.ID_USERDATA,8]
    uRRotSwitch = op[c4d.ID_USERDATA,9]

    global uUseInstance
    uUseInstance = op[c4d.ID_USERDATA,10]

    global cube

    cCount = 0

    if uUseInstance == False:
        uRObjSwitch = 0
        uRRotSwitch = None

        cube = c4d.BaseObject(c4d.Ocube)
        cube[c4d.PRIM_CUBE_DOFILLET] = 1
        cube[c4d.PRIM_CUBE_FRAD] = 5
        cube[c4d.PRIM_CUBE_SUBF] = 5
        #cube[c4d.ID_BASEOBJECT_USECOLOR] = 1
        #cube[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(.5,.5,.5)
        cube.InsertUnder(container)



    oInst = [op[c4d.ID_USERDATA,1], op[c4d.ID_USERDATA,2], op[c4d.ID_USERDATA,3], op[c4d.ID_USERDATA,4]]


    global uOctaves
    global uContrast
    global uBrightness
    global uNoiseinvert
    global uNoisetype
    uOctaves = op[c4d.ID_USERDATA,6]
    uContrast = op[c4d.ID_USERDATA,17]
    uBrightness = op[c4d.ID_USERDATA,18]
    uNoiseinvert = op[c4d.ID_USERDATA,19]
    uNoisetype = op[c4d.ID_USERDATA,20]


    uTf = 100 #May not be 0

    global uT
    uT = c4d.Vector((op[c4d.ID_USERDATA,22]), (op[c4d.ID_USERDATA,23]), (op[c4d.ID_USERDATA,24]))
    global uR
    uR = c4d.Vector(op[c4d.ID_USERDATA,27], op[c4d.ID_USERDATA,28], op[c4d.ID_USERDATA,29])

    global uS
    uNoisescale = op[c4d.ID_USERDATA,35]

    sV = utils.RangeMap(uNoisescale, 0,1,0,float(1)/uTf, False)
    uS = c4d.Vector(sV, sV, sV)


    #Get Clone position from Matrix Object
    dC = mo.GeGetMoData(cloner)
    dCmat = dC.GetArray(c4d.MODATA_MATRIX)
    dCcol = dC.GetArray(c4d.MODATA_COLOR)
    dCflag = dC.GetArray(c4d.MODATA_FLAGS)
    dCstart = dC.GetArray(c4d.MODATA_STARTMAT)

    #Clone count
    if not dCmat == None:
        cCount = len(dCmat)

    #Position Array
    arrB4 = [c4d.Vector(-1,-1,-1), c4d.Vector(1,-1,-1), c4d.Vector(-1,1,-1), c4d.Vector(1,1,-1), c4d.Vector(-1,-1,1), c4d.Vector(1,-1,1), c4d.Vector(-1,1,1), c4d.Vector(1,1,1)]

    #Generate RANDOM Value for rotation
    rand = random.Random()
    rand.seed(3)

    #Noise instance
    nObj = noise.C4DNoise(1234)
    nObj.InitFbm(21, 2.1, 0.5)

    for i in xrange(cCount):

        if dCflag[i] == 1:
            dCmatScale = dCmat[i].GetScale().x
            dCmatRotation = utils.MatrixToHPB(dCmat[i])

            #Current Position (for using effectors in Matrix)
            pPcur = c4d.Vector((dCmat[i].off).x, (dCmat[i].off).y, (dCmat[i].off).z)
            #Initial clone Start position
            pP = c4d.Vector((dCstart[i].off).x, (dCstart[i].off).y, (dCstart[i].off).z)

            #Noise Noise:
            pTurb = createNoiseValue(nObj, pP)

            if pTurb > uTh:
                for w in xrange(8):
                    pP2 = c4d.Vector(pP.x+((uSc/4+offset/2)*arrB4[w].x),pP.y+((uSc/4+offset/2)*arrB4[w].y),pP.z+((uSc/4+offset/2)*arrB4[w].z))
                    pP2cur = c4d.Vector(pPcur.x+((uSc/4+offset/2)*arrB4[w].x),pPcur.y+((uSc/4+offset/2)*arrB4[w].y),pPcur.z+((uSc/4+offset/2)*arrB4[w].z))
                    pTurb2 = createNoiseValue(nObj, pP2)

                    if pTurb2 > uTh:
                        for u in xrange(8):
                            pP3 = c4d.Vector(pP2.x+((uSc/8+offset/2)*arrB4[u].x),pP2.y+((uSc/8+offset/2)*arrB4[u].y),pP2.z+((uSc/8+offset/2)*arrB4[u].z))
                            pP3cur = c4d.Vector(pP2cur.x+((uSc/8+offset/2)*arrB4[u].x),pP2cur.y+((uSc/8+offset/2)*arrB4[u].y),pP2cur.z+((uSc/8+offset/2)*arrB4[u].z))
                            pTurb3 = createNoiseValue(nObj, pP3)

                            createObj(container, oInst[randomInstance(pTurb3, rand, uRObjSwitch)], oInstMode, 0.25*dCmatScale, dCmatRotation, pP3cur, 1, pTurb3, rand, uRRotSwitch)
                    else:
                        createObj(container, oInst[randomInstance(pTurb2, rand, uRObjSwitch)], oInstMode, 0.5*dCmatScale, dCmatRotation, pP2cur, 1, pTurb2, rand, uRRotSwitch)
            else:
                createObj(container, oInst[randomInstance(pTurb, rand, uRObjSwitch)], oInstMode, 1*dCmatScale, dCmatRotation, pPcur, 1, pTurb, rand, uRRotSwitch)

    return container


def createObj(container, oInst, oInstMode, oInstScale, oInstRotation, Pos, colormode, TurbColor, rand, randRotSwitch):


    if uUseInstance == False:
        oInst = cube

    cubeInst = c4d.BaseObject(c4d.Oinstance)

    cubeInst[c4d.INSTANCEOBJECT_LINK] = oInst
    cubeInst[c4d.INSTANCEOBJECT_RENDERINSTANCE_MODE] = oInstMode
    cubeInst[c4d.ID_BASEOBJECT_REL_SCALE] = c4d.Vector(oInstScale,oInstScale,oInstScale)
    tRrot = randomRotation(TurbColor,rand, randRotSwitch)
    cubeInst[c4d.ID_BASEOBJECT_REL_ROTATION] = c4d.Vector(oInstRotation.x + tRrot, oInstRotation.y + tRrot, oInstRotation.z + tRrot)
    cubeInst.SetRelPos(Pos)
    cubeInst[c4d.ID_BASEOBJECT_USECOLOR] = colormode
    cubeInst[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(TurbColor,TurbColor,TurbColor)

    cubeInst.InsertUnder(container)

    return True


def createNoiseValue(nObj, p):

    pPN = p

    #Rotate and Scale Noise:
    rot_mat = utils.HPBToMatrix(uR)

    rot_mat = c4d.Matrix(c4d.Vector(0,0,0), rot_mat.v1, rot_mat.v2, rot_mat.v3)
    p_rot = pPN * ~rot_mat #global position of Point out of the rotation matrix

    rot_mat.v1 = rot_mat.v1.GetNormalized() * uS.x
    rot_mat.v2 = rot_mat.v2.GetNormalized() * uS.y
    rot_mat.v3 = rot_mat.v3.GetNormalized() * uS.z
    rot_mat = c4d.Matrix(c4d.Vector(0,0,0), rot_mat.v1, rot_mat.v2, rot_mat.v3)
    p_scale = pPN*rot_mat

    pPN = p_scale

    #Transform Noise:
    pPN = c4d.Vector(pPN.x + uT.x, pPN.y + uT.y, pPN.z + uT.z)

    #generate Noise Value :
    pNoise = nObj.Noise(uNoisetype, False, pPN, 0, uOctaves, False, 0.25, 0.25, 0)

    #Brightness+Contrast Adjustement Formula (f(x)=α(x−128)+128+b):
    vColorAdjust = uContrast * (pNoise - 0.5) + 0.5 + uBrightness
    v = utils.ClampValue(vColorAdjust, 0, 1)

    #Color invert:
    if uNoiseinvert == True:
        v = utils.RangeMap(v, 0,1,1,0, False)

    return v



def randomRotation(TurbColor, rand, switch):
    arrRot = [0,90,180,270]

    if switch == 0:
        if (TurbColor < 0.25):
            randRot = 0
        elif(TurbColor >= 0.25 and TurbColor < 0.5):
            randRot = 1
        elif(TurbColor >= 0.5 and TurbColor < 0.75):
            randRot = 2
        else:
            randRot = 3

        r = utils.DegToRad(arrRot[randRot])

    elif switch == 1:
        #Generate Random Value betw. 0 - 1:
        rValue = rand.random()

        #RangeMap to Rotation Array Value 0 - 3:
        randRot = int(utils.RangeMap(rValue, 0,1,0,3, True))
        r = utils.DegToRad(arrRot[randRot])
    else:
        r = 0

    return r




def randomInstance(TurbColor, rand, switch):

    if switch == 0:
        #Return Value 0 - 3 from Turbulence Color for selection of the corresponding Instance Objects
        if (TurbColor < 0.25):
            v = 0
        elif(TurbColor >= 0.25 and TurbColor < 0.5):
            v = 1
        elif(TurbColor >= 0.5 and TurbColor < 0.75):
            v = 2
        else:
            v = 3
    elif switch == 1:
        #Generate Random Value betw 0 - 1:
        rValue = rand.random()

        #RangeMap Value 0 - 3:
        v = int(utils.RangeMap(rValue, 0,1,0,3, True))
    else:
        v = 0

    return v
