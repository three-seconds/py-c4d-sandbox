import c4d
#Writes your data to string and into the text-object
#Note: Tag needs to be placed on a text-object
#Thomas Gugel // three-seconds.de



def main():
    #Get current Frame
    frame = doc.GetTime().GetFrame(doc.GetFps())

    #Get Text Object
    text = op.GetObject()
    name = text.GetName()
    pos = text.GetAbsPos()

    #Prepare String. '\n' within is a linebreak
    strOut = name + " Position-X: " + str(round(pos.x,3)) + " \n" \
         + "Frame: " + str(frame).zfill(5) +  "\n" \

    #Set as Text
    text[c4d.PRIM_TEXT_TEXT] = strOut