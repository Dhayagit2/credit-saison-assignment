I've assumed the actual command to find the file is inside /tmp/cronjob.sh.  The script will have command find /etc/myapp -name *.txt which will find all the files with that extension.
It will have a smtp function along with if else conidtion. if file found it should trigger the email. also if the file is found it should create a file called result.txt and echo "file found" >> /tmp/result.txt. if no file is found then it should not crete the result.txt
. Result.txt. This result.txt is going to be used in the python logic to stop the instances.

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

This block will have varibles and the script. script1 will trigger the script to check the files and if present it will store the echoed word to result.txt
script2 will cat the result.txt. if there is no result.txt it will echo as empty


```response = ssm_client.send_command(
    DocumentName ='AWS-RunShellScript',
    Parameters = {'commands': [script]},
    InstanceIds = instanceid
)

for instance in instanceid:
    response1 = ssm_client.send_command(
    DocumentName ='AWS-RunShellScript',
    Parameters = {'commands': [script2]},
    InstanceIds = instanceid
)
if response1 != "empty":
    ec2_client.stop_instances(InstanceIds=[instance])```



this block will be executed to riun the script. first block is execute the cronjob.sh which will find the file and if found it will create the file result.txt.
Second response1 will execute the scrut cat commmand. if the file is not there it will print empty. and if it dont print empty then it'll it will stop the instances.
Also in the end rm /tmp/results.txt should be added ti remove the file everytime as it will be cronjob. 
