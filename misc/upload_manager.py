#!/usr/bin/python
import os
import sys
import threading
import argparse
import boto3


class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()
    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()

def createBucket(name):
    s3 = boto3.client('s3')
    resp = client.create_bucket(name)
    
    return resp['Location']

def uploadFile(bucketName, fileName):
    s3 = boto3.client('s3')

    s3.upload_file(
        fileName, bucketName, fileName,
        Callback=ProgressPercentage(fileName))

    print(' -> Done')

def listBuckets():
    s3 = boto3.client('s3')

    resp = s3.list_buckets()

    print(resp['Owner'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Create a collection for AWS Rekognize with local images. Number of input images of faces should be the same as the number of input names')
    parser.add_argument('--video', type=str, nargs=1, required=True, help='name of local video file to be uploaded to S3')
    args = parser.parse_args()

    video = args.video[0]
    print "Uploading: ", video
    uploadFile('big-data-61963', video)
