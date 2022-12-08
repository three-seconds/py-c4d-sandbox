import c4d
#Disable-Enable all objects and tags by visibility flag
#Thomas Gugel // three-seconds.de


def main():
    root = op.GetObject()
    queue = []
    disable = False

    #Read visibility flag of root object
    visE = root[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR]
    visR = root[c4d.ID_BASEOBJECT_VISIBILITY_RENDER]
    if visE == 1 or visR == 1:
        disable = True

    #First fill of "queue" list
    queue = addToQueue(queue, root, True)
    count = 0

    #Loop as long as you have objects in queue list
    while len(queue) > 0:
        count += 1

        #Disable-Enable first object in Queue
        if disable == True:
            checkObjToDisable(queue[0])
        else:
            checkObjToEnable(queue[0])

        #Get all tags from current object
        tags = queue[0].GetTags()
        for tag in tags:
            if disable == True:
                checkTagToDisable(tag)
            else:
                checkTagToEnable(tag)

        #Add Children to queue list
        queue = addToQueue(queue, queue[0], False)
        #delete current object from queue list
        queue.pop(0)


#Function To add Objects to Queue
def addToQueue(queue, root, starttree):
    childs = root.GetChildren()

    if starttree == True:
        for child in childs:
            queue.append(child)
    else:
        for child in reversed(childs):
            queue.insert(1, child)

    return queue


#Function To Disable Tags
def checkTagToDisable(tag):
    if tag.GetType() == 180000102:
        tag[c4d.RIGID_BODY_ENABLED] = False

    tag[c4d.EXPRESSION_ENABLE] = False

#Function To Enable Tags
def checkTagToEnable(tag):
    if tag.GetType() == 180000102:
        tag[c4d.RIGID_BODY_ENABLED] = True

    tag[c4d.EXPRESSION_ENABLE] = True

#Function To Disable Objects
def checkObjToDisable(obj):
    obj[c4d.ID_BASEOBJECT_GENERATOR_FLAG] = False

#Function To Enable Objects
def checkObjToEnable(obj):
    obj[c4d.ID_BASEOBJECT_GENERATOR_FLAG] = True