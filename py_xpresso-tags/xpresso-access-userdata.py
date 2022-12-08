import c4d
#Just a little example how you can access the Object, the xpresso tag is attached to
#Thomas Gugel // three-seconds.de

def main():
    global color

    #Grab the host-object to the xpresso Tag
    cube = op.GetNodeMaster().GetOwner().GetObject()

    #Get the UserData
    colorA = cube[c4d.ID_USERDATA,1]
    colorB = cube[c4d.ID_USERDATA,2]

    if posX > 0:
        out = colorA
    else:
        out = colorB

    color = out