import boto3

# returns the url of the newly created queue
def createSQS(name):
    client = boto3.client('sqs')

    resp = client.create_queue(QueueName = name)

    return resp['QueueUrl']

def listSQS():
    client = boto3.client('sqs')

    resp = client.list_queues()

    urls = resp['QueueUrls']
    
    return urls

def deleteSQS(url):
    client = boto3.client('sqs')

    print('Deleting SQS: ' + url)
    client.delete_queue(url)
    print('Done')

def getQueueArn(url):
    client = boto3.client('sqs')

    resp = client.get_queue_attributes(QueueUrl = url, AttributeNames = ['QueueArn'])

    return resp['Attributes']['QueueArn']
    
def addPermissions(topicArn, queueArn, queueUrl):
    policy_json = """{{
  "Version":"2012-10-17",
  "Statement":[
    {{
      "Sid":"MyPolicy",
      "Effect":"Allow",
      "Principal" : {{"AWS" : "*"}},
      "Action":"SQS:SendMessage",
      "Resource": "{}",
      "Condition":{{
        "ArnEquals":{{
          "aws:SourceArn": "{}"
        }}
      }}
    }}
  ]
}}""".format(queueArn, topicArn)

    client = boto3.client('sqs')
    response = client.set_queue_attributes(
        QueueUrl = queueUrl,
        Attributes = {
            'Policy' : policy_json
        }
    )
    print(response)

def receiveMessage(url):
    client = boto3.client('sqs')

    resp = client.receive_message(QueueUrl = url)

    print(resp['Messages'])

sqs_url = 'https://eu-west-1.queue.amazonaws.com/492907116051/lstChance-sqs'
sns_arn = 'arn:aws:sns:eu-west-1:492907116051:this-sns'
sqs_arn = 'arn:aws:sqs:eu-west-1:492907116051:lstChance-sqs'
#createSQS('lstChance-sqs')
listSQS()
getQueueArn("https://eu-west-1.queue.amazonaws.com/492907116051/proj-sqs")
#receiveMessage(queue_url)
#addPermissions(sns_arn, sqs_arn, sqs_url)


