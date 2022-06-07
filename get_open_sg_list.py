import boto3
import os
import csv
import jmespath

os.environ['AWS_PROFILE'] = "default"
data = []
client = boto3.client('ec2')
ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
for region in ec2_regions:
    client = boto3.client('ec2', region_name=region)
    response = client.describe_security_groups()
    for sg in response['SecurityGroups']:
        for ingress in sg['IpPermissions']:
            for iprange in ingress['IpRanges']:
                if iprange['CidrIp'] == '0.0.0.0/0':
                    try:
                        data.append([region, sg['GroupName'], sg['Description'], ingress['FromPort'], ingress['ToPort'],
                                 iprange['CidrIp']])
                    except:
                        print(region)
                        print(sg)



with open("sg.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(['Region', 'SGroupName', 'Description', 'FromPort', 'ToPort', 'CidrIp'])
    writer.writerows(data)
