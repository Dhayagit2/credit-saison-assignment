import boto3
import logging

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

TAG_KEY = "CreatedBy"
TAG_VALUE = "AMILifecycle"
KEEP_LATEST = 2
REGION = "ap-south-1"

ec2 = boto3.client("ec2", region_name=REGION)

def get_amis():
    logger.info("Fetching AMIs with tag CreatedBy=AMILifecycle...")
    response = ec2.describe_images(
        Owners=['self'],
        Filters=[
            {"Name": f"tag:{TAG_KEY}", "Values": [TAG_VALUE]}
        ]
    )
    amis = response['Images']
    logger.info(f"Found {len(amis)} AMIs.")
    return sorted(amis, key=lambda x: x['CreationDate'], reverse=True)

def delete_old_amis(amis):
    if len(amis) <= KEEP_LATEST:
        logger.info("Nothing to delete. AMI count is within retention.")
        return

    to_delete = amis[KEEP_LATEST:]
    for ami in to_delete:
        ami_id = ami['ImageId']
        name = ami.get('Name', 'Unnamed')
        logger.info(f"Deregistering AMI: {ami_id} ({name})")

        try:
            ec2.deregister_image(ImageId=ami_id)
            logger.info(f"Deregistered: {ami_id}")
        except Exception as e:
            logger.error(f"Error deregistering {ami_id}: {e}")

        # Delete snapshots
        for bd in ami.get('BlockDeviceMappings', []):
            if 'Ebs' in bd and 'SnapshotId' in bd['Ebs']:
                snap_id = bd['Ebs']['SnapshotId']
                try:
                    ec2.delete_snapshot(SnapshotId=snap_id)
                    logger.info(f"Deleted snapshot: {snap_id}")
                except Exception as e:
                    logger.error(f"Error deleting snapshot {snap_id}: {e}")

# ✅ Required handler for Lambda
def lambda_handler(event, context):
    amis = get_amis()
    if amis:
        delete_old_amis(amis)
    return {
        "statusCode": 200,
        "body": f"AMI lifecycle cleanup completed. {len(amis)} AMIs found."
    }
#
