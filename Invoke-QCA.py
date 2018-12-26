#THIS SCRIPT IS PROVIDED TO YOU "AS IS." TO THE EXTENT PERMITTED BY LAW, QUALYS HEREBY DISCLAIMS ALL WARRANTIES AND LIABILITY FOR THE PROVISION OR USE OF THIS SCRIPT. IN NO EVENT SHALL THESE SCRIPTS BE DEEMED TO BE CLOUD SERVICES AS PROVIDED BY QUALYS
import datetime
import time
import logging
import boto3
from botocore.exceptions import ClientError

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def is_a_garlc_instance(instance_id):
    try:
        ec2 = boto3.client('ec2')
        instance = ec2.describe_instances(InstanceIds=[str(instance_id)])
    except ClientError as err:
        LOGGER.error(str(err))
        return False

    if instance:
        return True
    else:
        LOGGER.error(str(instance_id) + " is not a GARLC instance!")
        return False

def send_run_command(instance_id):
    """
    Sends the Run Command API Call
    """
    try:
        ssm = boto3.client('ssm')
    except ClientError as err:
        LOGGER.error("Run Command Failed!\n%s", str(err))
        return False

    try:
        ssm.send_command(
            InstanceIds=[instance_id],
            DocumentName='QualysCloudAgent-Install',
            TimeoutSeconds=900,
            Parameters={
                'ActivationID': ['REPLACE_ME-xxxx-xxxx'],
		'CustomerID': ['REPLACE_ME-xxxx-xxxx'],
		'AgentLocationWindows': ['REPLACE_ME-xxxx-xxxx'] ,
		'AgentLocationDebian': ['REPLACE_ME-xxxx-xxxx'] ,
		'AgentLocationRPM': ['REPLACE_ME-xxxx-xxxx'] ,
		'LogLevel': ['5']
            }
        )
        return True
    except ClientError as err:
        if 'ThrottlingException' in str(err):
            LOGGER.info("RunCommand throttled, automatically retrying...")
            send_run_command(instance_id)
        else:
            LOGGER.error("Run Command Failed!\n%s", str(err))
            return False

def log_event(event):
    """Logs event information for debugging"""
    LOGGER.info("====================================================")
    LOGGER.info(event)
    LOGGER.info("====================================================")

def get_instance_id(event):
    """ Grab the instance ID out of the "event" dict sent by cloudwatch events """
    try:
        return str(event['detail']['instance-id'])
    except (TypeError, KeyError) as err:
        LOGGER.error(err)
        return False

def resources_exist(instance_id):
    """
    Validates instance_id have values
    """
    if not instance_id:
        LOGGER.error('Unable to retrieve Instance ID!')
        return False
    else: return True


def lambda_handler(event, _context):
    """ Lambda Handler """
    log_event(event)
    instance_id = get_instance_id(event)

    if resources_exist(instance_id) and is_a_garlc_instance(instance_id):
        time.sleep(60)
        send_run_command(instance_id)
        LOGGER.info('===SUCCESS===')
        return True
    else:
        return False
