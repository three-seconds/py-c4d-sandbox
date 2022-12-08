import c4d, math
from c4d.modules import mograph as mo
from c4d import utils
#Effector grabs every seconds clone and rotates it in opposite directions
#Works fine in viewport, but not on rendertime.
#If you figure out what i did wrong - please let me know!

#Thomas Gugel // three-seconds.de

#Needs User Data:
#Group: Settings
#Color
#    Datatype: Boolean, Interface: Boolean
#Group: Helper
#Helper 
#    Datatype: Link, Interface: Link
#Helper Clone Nr
#    Datatype: Integer, Interface: Integer
#Group: Tranform Position
#X #Y #Z
#    Datatype: Float, Interface: Float, Unit: Length Unit
#Group: Transform Rotation
#H #P #B
#    Datatype: Float, Interface: Float, Unit: Degree

#Version: 0.9

def main():
    md = mo.GeGetMoData(op)
    if md is None: return False

    #Get UserData
    inX = op[c4d.ID_USERDATA,8]
    inY = op[c4d.ID_USERDATA,9]
    inZ = op[c4d.ID_USERDATA,10]
    inH = op[c4d.ID_USERDATA,12]
    inP = op[c4d.ID_USERDATA,13]
    inB = op[c4d.ID_USERDATA,14]

    helper = op[c4d.ID_USERDATA,1]
    hCloneNr = op[c4d.ID_USERDATA,5]

    bC = op[c4d.ID_USERDATA,7]

    cnt = md.GetCount()
    marr = md.GetArray(c4d.MODATA_MATRIX)
    if bC == True: mcol = md.GetArray(c4d.MODATA_COLOR)
    fall = md.GetFalloffs()

    for i in reversed(xrange(0, cnt)):

        #Calculate Position
        x = marr[i].off.x + inX
        y = marr[i].off.y + inY
        z = marr[i].off.z + inZ

        #Safe Scale from Matrix
        scale = c4d.Vector(marr[i].v1.GetLength(), marr[i].v2.GetLength(), marr[i].v3.GetLength())

        #GetRotation from Matrix:
        rot = utils.MatrixToHPB(marr[i])

        #New Rotation
        if i % 2 == 0:
            inH = inH * -1

        h = rot.x + inH
        p = rot.y + inP
        b = rot.z + inB

        rotNew = c4d.Vector(h,p,b)

        #Build a updated Matrix
        marr[i] = utils.HPBToMatrix(rotNew)

        marr[i].off = c4d.Vector(x,y,z)
        marr[i].v1 = marr[i].v1.GetNormalized() * scale.x
        marr[i].v2 = marr[i].v2.GetNormalized() * scale.y
        marr[i].v3 = marr[i].v3.GetNormalized() * scale.z

        #Set color
        if bC == True: mcol[i] = c4d.Vector(0,0,0)

        #Set Helper Object
        if not helper is None:
            if i == hCloneNr and hCloneNr <= cnt:
                helper.SetMg(marr[i])
                helper.SetRelScale(c4d.Vector(1,1,1))


    md.SetArray(c4d.MODATA_MATRIX, marr, True)
    if bC == True: md.SetArray(c4d.MODATA_COLOR, mcol, True)
    return True