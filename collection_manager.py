#!/usr/bin/python
import boto3
import json

class CollectionManager:
    client = boto3.client('rekognition')
    def __init__(self, collectionName):
        self.collectionId = collectionName
        # make call idempotent
        existingCollections = listCollections()

        if collectionName in existingCollections:
            # collection already exists
            pass
        else:
            resp = self.client.create_collection(CollectionId = collectionName)
            print "Collection ARN: ", resp['CollectionArn']


    def addImageWithFace(self, imageFile):
        with open(imageFile, 'rb') as image:
            global resp
            resp = self.client.index_faces(CollectionId=self.collectionId,
                                           Image={'Bytes' : image.read()})

        # return only id of the biggest face
        return resp['FaceRecords'][0]['Face']['FaceId']

                                                      
    


    def listFacesInCollection(self, maxResults = 5):
        resp = self.client.list_faces(CollectionId = self.collectionId, MaxResults = maxResults)
        
        result= []
        while True:
            faces = resp['Faces']

            for face in faces:
                result.append(face['FaceId'])
            if 'NextToken' in resp:
                nextToken = resp['NextToken']
                resp = self.client.list_faces(CollectionId = self.collectionId,
                                              NextToken = nextToken,
                                              MaxResults = maxResults)
            else:
                break
        return result


    def removeFacesFromCollection(self, faceIds):
        if len(faceIds) < 1:
            print "Nothing to delete"
            return
        resp = self.client.delete_faces(CollectionId=self.collectionId,
                                   FaceIds=faceIds)

        deletedFaces = resp['DeletedFaces']

        print "Deleted faces:"

        for face in deletedFaces:
            print face

        remainingFaces = [face for face in faceIds if face not in deletedFaces]
        
        if len(remainingFaces) > 0:
            print "Couldn't delete:"
            for face in remainingFaces:
                print face

def listCollections(maxResults = 5) :
    client = boto3.client('rekognition')
    resp = client.list_collections(MaxResults = maxResults)
    resultList = []

    while True:
        collections = resp['CollectionIds']

        for collection in collections:
            resultList.append(collection)
        if 'NextToken' in resp:
            nextToken = resp['NextToken']
            resp = client.list_collections(NextToken = nextToken, MaxResults = maxResults)
        else:
            break

    return resultList

if __name__ == '__main__':
    collection = CollectionManager("TestCollection")
    #print listCollections(2)
    faces = collection.listFacesInCollection()
    collection.removeFacesFromCollection(faces)
