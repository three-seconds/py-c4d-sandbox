import c4d
#Hide TP by Matrix visiblity flag
#Thomas Gugel // three-seconds.de

#Nees User Data:

#pGroup 
#    DataType: Link, Interface: Link
#View Type 
#    DataType: Integer, Interface: Cycle
#    Cycle Option: 0;None 1;Flakes 2;Dots 3;Ticks 4;Drops 5;Box 6;Global 


def main():
    obj = op.GetObject()

    visE = obj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR]
    inPGroup = op[c4d.ID_USERDATA,1]
    viewType = op[c4d.ID_USERDATA,2]

    if not inPGroup == None:
        if visE == 1:
            inPGroup.SetViewType(0)
        else:
            inPGroup.SetViewType(viewType)