GRANULARITY = 400
class Face:
    def __init__(self, name):
        self.name = name
        self.start = -1.0
        self.last = -1.0

class Group:
    def __init__(self, membersMap):
        self.members = {}
        for faceId, name in membersMap.items():
            self.members[faceId] = Face(name)


    def getMemberFaceIds(self):
        return [faceId for faceId in self.members] 

    def faceAppear(self, faceId, time):
        if self.members[faceId].start == -1.0:
            self.members[faceId].start = time
            self.members[faceId].last = time

        elif time - self.members[faceId].last > GRANULARITY:
            self.printLastOccurance()
            
            self.members[faceId].start = time
            self.members[faceId].last = time
        else:
            self.members[faceId].last = time

    # this should be reworked in python3 with members.items() and obj access
    def printLastOccurance(self):
        latestStart = max([self.members[faceId].start for faceId in self.members])
        earliestEnd = min([self.members[faceId].last for faceId in self.members])

        if latestStart > earliestEnd:
            pass
            # there is no crossection
        else:
            if len(self.members) == 1:
                print "Person: ",
            else:
                print "Group: ", 
            for face in self.members:
                print self.members[face].name,
            print ' -> ',
            timestampToNormal(latestStart)
            print 'to',
            timestampToNormal(earliestEnd) 
            print
            print '==============================='
 
def timestampToNormal(time):

    time, milis = divmod(time, 1000)
    time, seconds = divmod(time, 60)
    time, minutes = divmod(time, 60)

    hours = time

    print "%d:%02d:%02d:%03d" % (hours, minutes, seconds, milis),

if __name__ == '__main__':
    
    face_map = {'a':'cecko', 'b':'mitko', 'c':'petkan'}
    group = Group(face_map)

    group.printLastOccurance()



