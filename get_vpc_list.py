import boto3
import os
import csv
import jmespath

# update aws profile name
os.environ['AWS_PROFILE'] = "default"
data = []
client = boto3.client('ec2')
ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
for region in ec2_regions:
    ec2 = boto3.resource('ec2', region_name=region)
    response = client.describe_vpcs()
    for vpc_response in response['Vpcs']:
        print(region, vpc_response['VpcId'], vpc_response['CidrBlock'])
        for tag in vpc_response.get('Tags', []):
            if tag['Key'] == 'Name':
                #ignore default VPC
                if tag['Value'] != 'default':
                    data.append([region, tag['Value'], vpc_response['VpcId'], vpc_response['CidrBlock']])
                break

with open("vpc-inventory.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(['Region', 'Name', 'VPC ID', 'CidrBlock'])
    writer.writerows(data)
