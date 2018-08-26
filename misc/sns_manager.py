import boto3

def createSNSTopic(name):
    client = boto3.client('sns')

    resp = client.create_topic(Name = name)

    return resp['TopicArn']

def listSNSTopics():
    client = boto3.client('sns')
    result = []

    resp = client.list_topics()

    while True:
        topics = resp['Topics']

        for topic in topics:
            result.append(topic['TopicArn'])

        if 'NextToken' in resp:
            resp = client.list_topics(resp['NextToken'])
        else:
            break
    
    return result

def deleteSNSTopic(topicArn):
    client = boto3.client('sns')

    print('Deleting topic with Arn: ' + topicArn)
    client.delete_topic(TopicArn = topicArn)
    print('Done')

def subscribeQueueToSNSTopic(topicArn, sqsArn):
    client = boto3.client('sns')

    resp = client.subscribe(TopicArn = topicArn,
                            Protocol = 'sqs',
                            Endpoint = sqsArn,
                            ReturnSubscriptionArn = True)

    print(resp['SubscriptionArn'])

def subscribeQueueToSNSTopicByUrl(topicArn, sqsUrl):
    client = boto3.client('sns')

    resp = client.subscribe(TopicArn = topicArn,
                            Protocol = 'https',
                            Endpoint = sqsUrl,
                            ReturnSubscriptionArn = False)

    print(resp['SubscriptionArn'])

def postMessage(topicArn, message):
    client = boto3.client('sns')

    resp = client.publish(TopicArn = topicArn,
                          Message = message)





#createSNSTopic('this-sns')
listSNSTopics()
#subscribeQueueToSNSTopic(sns_arn, sqs_arn)
#subscribeQueueToSNSTopicByUrl('arn:aws:sns:eu-west-1:492907116051:test-sns', 'https://eu-west-1.queue.amazonaws.com/492907116051/test-sqs')
#postMessage(sns_arn)
