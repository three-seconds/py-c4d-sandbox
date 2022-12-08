import c4d
#Simple Renamer Tag
#Thomas Gugel // three-seconds.de


def main():
    main = op.GetObject()
    obj = main.GetDown()

    for i in xrange(200):
        if obj == None:
            break

        obj[c4d.ID_BASELIST_NAME] = "Cube " + str(i+1).zfill(2)
        obj = obj.GetNext()