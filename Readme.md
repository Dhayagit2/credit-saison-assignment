I've assumed the actual command to find the file is inside /tmp/cronjob.sh.  The script will have command find /etc/myapp -name *.txt which will find all the files with that extension.
It will have a smtp function along with if else conidtion. if file found it should trigger the email. also if the file is found it should echo "file found" >> /tmp/result.txt
This result.txt is going to be used in the python logic to stop the instances.

Python code:
``` script = """
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
filtered_instances = ec2_client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [instanceid]}])```
