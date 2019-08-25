import json
import boto3
images = []

def lambda_handler(event, context):
    instances = []
    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.all():
        if(instance.tags is not None) and (instance.tags[0]['Key'] == 'GoldAMI'):
            instances.append(instance.id)
        print (instance.id , instance.tags)
    client = boto3.client('ec2')
    for x in instances:
        images.append(client.create_image(InstanceId = x, Name = 'tempImage'))
    client = boto3.client('lambda')
    
    client = boto3.client('ec2')
    response = client.describe_images(
        Filters=[
            {
                'Name': 'name',
                'Values' : [
                    'Windows_Server-2016-English-Full-Base-2019.08.16'
                ]
            }
        ]
        
    )

    imageId = response['Images'][0]['ImageId']
    resource = boto3.resource('ec2')
    instance = resource.create_instances(
          ImageId = imageId,
          InstanceType = 't2.micro',
          MinCount = 1,
          MaxCount = 1
    )
    
    #Powershell
    
    ec2 = boto3.resource('ec2')
    inspector = boto3.client('inspector')
    instance = instance[0]
    response = inspector.create_assessment_target(
        assessmentTargetName = 'securityCheck',
        resourceGroupArn = instance[0].iam_instance_profile['Arn']
    )
    
    #Run Inspector 
    
    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.all():
        if(instance.tags is not None) and (instance.tags[0]['Key'] == 'temp'):
            instances = instance.id
    client = boto3.client('ec2')
    image = client.create_image(InstanceId = instances, Name = 'upImage')
    instance = ec2.Instance(instances)
    instance.terminate()
    client = boto3.client('lambda')

    
    client = boto3.client('ses')
    email = "A new AMI is made with the new Windows update. The ami id is __________"
    response = client.send_email(
        Destination = {
            'ToAddresses': [
                'string',
            ]
        },
        Message={
            'Subject': {
                'Charset': 'UTF-8',
                'Data': 'Windows AMI Update'
            },
            'Body':{
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': email 
                }
            }
        }
    )
    
