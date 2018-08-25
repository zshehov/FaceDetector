class FaceMap:
    def __init__(self):
        self.face_map = {}

    def addFace(self, faceId, name):
        self.face_map[faceId] = name
        print "Added: ", name, "->", faceId 

    def getFaceIds(self):
        return list(self.face_map.keys())

    def getInvertedMap(self):
        return {name : faceId for faceId, name in self.face_map.iteritems()}

    def getFaceMapsFromGroups(self, groups=None):
        inverted = self.getInvertedMap()
        result = []
        if groups:
            # each group has its own face map
            for group in groups:
                result.append({inverted[name] : name for name in group})
        else:
            # present each face as its own group
            for faceId, name in self.face_map.iteritems():
                result.append({faceId : name})

        return result
