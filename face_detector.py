#!/usr/bin/python

import os
import argparse
from collection_manager import CollectionManager
from rekognition_manager import RekognitionManager 
from face_map import FaceMap
import json
faceIdLen = 36

parser = argparse.ArgumentParser(description = 'Look for the given faces in a video stored on S3 and report when they were seen. There is the notion for "and" groups whose members ought to appear simultaniously.')
parser.add_argument('--faces', type=str, nargs='+', required=True, help='File names of images with faces to put in the collection. Should be as much as the names of faces')

parser.add_argument('--names', type=str, nargs='+', required=True,  help='Names of faces to associate with corresponing images. Should be as much as the names of images')

parser.add_argument('--video', type=str, nargs=1, required=True,  help='Key of the video to be analyzed, stored in the given S3 bucket')

parser.add_argument('--group', type=str, nargs="*", required=False,  help='Define an "and" group', action='append')

 # ==== argument handling ====
args = parser.parse_args()

faces = args.faces
# repeating names are not supported since
# a map with name -> id is created later on
names = list(set(args.names))
if len(names) != len(args.names):
    print "Repeating names are not supported"
    exit(4)
groups = args.group

if len(faces) != len(names):
    print "not cool. images should be as much as the names for them"
    exit

if groups:
    for i in [name for group in groups for name in group]:
        if i not in names:
            print "can't have a group with an unkown name"
            exit(33)

try:
    with open('config.json') as f:
        config = json.load(f)
except IOError:
    print 'Please create a config.json file with the following fields:\n\tCollectionId\n\tRoleArn\n\tSnsArn\n\tSqsArn?\n\tSqsUrl\n\tBucketName'
    exit(2)

required = ['CollectionId', 'RoleArn', 'SnsArn', 'SqsArn', 'SqsUrl', 'BucketName']

if not all(r in config for r in required):
    print 'config.json file is incomplete. It should have the following fields:\n\tCollectionId\n\tRoleArn\n\tSnsArn\n\tSqsArn?\n\tSqsUrl\n\tBucketName'
    exit(3)

 # ==== END OF argument handling ====

collectionManager = CollectionManager(config['CollectionId'])
 # ==== persistent cleanup ====
if os.path.isfile("rekog.lok"):
    print "There are leftover faceIds from last run. Deleting them..."
    try:
        with open('rekog.lok') as persistentFile:
            toDelete = []
            while True:
                faceId = persistentFile.read(faceIdLen)
                if len(faceId) != faceIdLen:
                    break
                toDelete.append(faceId)
            collectionManager.removeFacesFromCollection(toDelete)
            os.remove('rekog.lok')
    except IOError:
        print 'Something is really wrong here'
        exit(220)

# ==== building internal structures ====
face_map = FaceMap()
print "Temporarily putting faces into collection:"
try:
    with open('rekog.lok', 'a') as persistentFile:
        for counter, face in enumerate(faces):
            faceId = collectionManager.addImageWithFace(face)
            # right here we leak one faceId if we crash
            persistentFile.write(faceId)
            face_map.addFace(faceId, names[counter])
except:
    print "Couldn't open a persistent file"
    exit(30)


reko = RekognitionManager(config['BucketName'], args.video[0], config['CollectionId'], config['RoleArn'], config['SnsArn'], config['SqsUrl'])

reko.rekognize(face_map.getFaceMapsFromGroups(groups))

print "Removing faces from collection:"
collectionManager.removeFacesFromCollection(face_map.getFaceIds())
os.remove('rekog.lok')

