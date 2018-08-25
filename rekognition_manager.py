import boto3
import json
import sys

from group import Group

class RekognitionManager:
    
    client = boto3.client('rekognition')
    sqs = boto3.client('sqs')
    def __init__(self, bucketName, videoName, collectionId, roleArn, snsTopicArn, queueUrl):
        self.bucketName = bucketName
        self.videoName = videoName
        self.collectionId = collectionId
        self.roleArn = roleArn
        self.snsTopicArn = snsTopicArn
        self.queueUrl = queueUrl

    def rekognize(self, idToNameMaps):
        jobFound = False

        #=====================================
        response = self.client.start_face_search(Video={'S3Object':{'Bucket':self.bucketName,'Name':self.videoName}},
        CollectionId=self.collectionId,
        NotificationChannel={'RoleArn':self.roleArn, 'SNSTopicArn': self.snsTopicArn})

        #=====================================
        # print('Start Job Id: ' + response['JobId'])
        dotLine=0
        while jobFound == False:
            sqsResponse = self.sqs.receive_message(QueueUrl=self.queueUrl, MessageAttributeNames=['ALL'],
                                          MaxNumberOfMessages=10)

            if sqsResponse:
                
                if 'Messages' not in sqsResponse:
                    if dotLine<20:
                        sys.stdout.write('.') 
                        dotLine=dotLine+1
                    else:
                        sys.stdout.write("\b" * dotLine + " " * dotLine + "\b" * dotLine)
                        dotLine=0    
                    sys.stdout.flush()
                    continue

                print
                for message in sqsResponse['Messages']:
                    notification = json.loads(message['Body'])
                    # print(notification)
                    clientMessage = json.loads(notification['Message'])
                    # print(clientMessage['JobId'])
                    print(clientMessage['Status'])
                    if str(clientMessage['JobId']) == response['JobId']:
                        # print('Matching Job Found:' + clientMessage['JobId'])
                        jobFound = True

                        self.GetResultsFaceSearchCollection(clientMessage['JobId'], idToNameMaps)

                        self.sqs.delete_message(QueueUrl=self.queueUrl,
                                       ReceiptHandle=message['ReceiptHandle'])
                    else:
                        print("Job didn't match:" +
                              str(clientMessage['JobId']) + ' : ' + str(response['JobId']))
                    # Delete the unknown message. Consider sending to dead letter queue
                    self.sqs.delete_message(QueueUrl=self.queueUrl,
                                   ReceiptHandle=message['ReceiptHandle'])

        print('done')

    def GetResultsFaceSearchCollection(self, jobId, idToNameMaps):
        maxResults = 10
        paginationToken = ''

        finished = False

        groups = []
        for idToNameMap in idToNameMaps:
            groups.append(Group(idToNameMap))

        faceToGroupMap = {}
        for group in groups:
            for faceId in group.getMemberFaceIds():
                if faceId not in faceToGroupMap:
                    faceToGroupMap[faceId] = []
                faceToGroupMap[faceId].append(group)

        
        while finished == False:
            response = self.client.get_face_search(JobId=jobId,
                                        MaxResults=maxResults,
                                        NextToken=paginationToken)

            for personMatch in response['Persons']:
                #print('Person Index: ' + str(personMatch['Person']['Index']))
                #print('Timestamp: ' + str(personMatch['Timestamp']))

                current = personMatch['Timestamp']

                if ('FaceMatches' in personMatch):
                    for faceMatch in personMatch['FaceMatches']:
                        faceId = faceMatch['Face']['FaceId']
                        
                        for group in faceToGroupMap[faceId]:
                            group.faceAppear(faceId, current)

                        #print('Face ID: ' + faceMatch['Face']['FaceId'])
                        #print('Similarity: ' + str(faceMatch['Similarity']))
                #print
            if 'NextToken' in response:
                paginationToken = response['NextToken']
            else:
                finished = True

        group.printLastOccurance()
