import boto3

script = """
bash /tmp/cronjob.sh
"""

script2 = """
cat /tmp/result.txt || echo "empty"
"""

#Define the tag possessed by the EC2 instances that we want to execute the script on
tag='Test'
instanceid = "i--ijndfjndn", "instance-2", "instance-3"
ec2_client = boto3.client("ec2", region_name='us-east-1')
ssm_client = boto3.client('ssm')
#Gather of instances with tag defined earlier
filtered_instances = ec2_client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [instanceid]}])



#Run shell script
response = ssm_client.send_command(
    DocumentName ='AWS-RunShellScript',
    Parameters = {'commands': [script]},
    InstanceIds = instanceid
)

for instance in InstanceIds:
    response1 = ssm_client.send_command(
    DocumentName ='AWS-RunShellScript',
    Parameters = {'commands': [script2]},
    InstanceIds = instanceid
)
if response1 != "empty":
    ec2_client.stop_instances(InstanceIds=[instance])

