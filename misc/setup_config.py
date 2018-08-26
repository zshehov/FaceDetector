import sns_manager
import sqs_manager
import upload_manager


topicArn = createSNSTopic('rekog-sns')

if topicArn not in listSNSTopics():
    print "Topic wasn't created"
    exit(1)


sqsUrl = createSQS('rekog-sqs')

if sqsUrl not in listSQS():
    print "Sqs wasn't created"
    exit(2)

sqsArn = getQueueArn(sqsUrl)

addPermissions(topicArn, sqsArn, sqsUrl)

subscribeQueueToSNSTopic(topicArn, sqsArn)

createBucket('rekog-bucket')



