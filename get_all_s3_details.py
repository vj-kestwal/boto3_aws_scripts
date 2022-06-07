import boto3
import os
import csv
from botocore.exceptions import ClientError

os.environ['AWS_PROFILE'] = "default"
s3 = boto3.client('s3')
response = s3.list_buckets()
data = []

for bucket in response['Buckets']:
    temp = []
    try:
        temp.insert(0, bucket['Name'])
        location = s3.get_bucket_location(Bucket=bucket['Name'])['LocationConstraint']
        temp.insert(1, location)
        enc = s3.get_bucket_encryption(Bucket=bucket['Name'])
        rules = enc['ServerSideEncryptionConfiguration']['Rules']
        temp.insert(2, "SSE_YES")
        temp.insert(3, rules)
        print('Bucket: %s,region: %s, Encryption: %s' % (bucket['Name'], location, rules))
    except ClientError as e:
        if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
            print('Bucket: %s, no server-side encryption' % (bucket['Name']))
            temp.insert(2, 'NO_SSE')
            temp.insert(3, 'NONE')
        else:
            print("Bucket: %s, unexpected error: %s" % (bucket['Name'], e))
    data.append(temp)


with open("s3.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Region', 'SSE', 'SSE RULE'])
    writer.writerows(data)
