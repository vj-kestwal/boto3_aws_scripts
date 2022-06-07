import boto3
import os
import csv
import jmespath

os.environ['AWS_PROFILE'] = "default"
data = []
client = boto3.client('ec2')
ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
for region in ec2_regions:
    ec2 = boto3.resource('ec2', region_name=region)
    for instance in ec2.instances.all():
        try:
            if(instance.state['Name']):
                data.append([region, instance.private_ip_address, instance.key_name, instance.image.name,
                     instance.state['Name']])
        except:
            print("Instance Region %s, IP %s" % (region, instance.private_ip_address))

with open("ec2-inventory.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(['Region', 'PrivateIP', 'KeyName', 'ImageName', 'State'])
    writer.writerows(data)
