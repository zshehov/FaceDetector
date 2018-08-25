Simple python command line tool over AWS that reports when input named faces from images are seen in a given video in a "from - to" manner.
It is possible define a group which will be considered seen only if all the members are in the shot simultaniously

A conifg file must be provided either by putting "config.json" in the script's dir, or by --configFile.
The config file must contain:
- CollectionId -> the name of the collection into which faces will be put
- SnsArn       -> ARN of a SNS topic that the Rekognition service will publish stats to
- SqsUrl       -> URL of a SQS, that has 'Allow' permission for the SNS topic and is subscribed to the SNS topic above
- RoleArn      -> ARN of an IAM role that gives Rekognition publishing permissions to the SNS topic above
- BucketName   -> the name of the S3 bucket that contains the video to be analyzed 

Example config file:

{
   "CollectionId" : "TestCollection",
   "SnsArn" : "arn:aws:sns:eu-west-1:123123123123:test-sns",
   "SqsUrl" : "https://eu-west-1.queue.amazonaws.com/123123123123/test-sqs",
   "RoleArn" : "arn:aws:iam::123123123123:role/rekognitionRole",
   "BucketName" : "some-s3-bucket-name"
}
