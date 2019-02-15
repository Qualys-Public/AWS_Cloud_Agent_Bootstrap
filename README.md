# AWS_Cloud_Agent_Bootstrap
(Based on [GARLC](https://github.com/awslabs/lambda-runcommand-configuration-management))

# License
_**THIS SCRIPT IS PROVIDED TO YOU "AS IS."  TO THE EXTENT PERMITTED BY LAW, QUALYS HEREBY DISCLAIMS ALL WARRANTIES AND LIABILITY FOR THE PROVISION OR USE OF THIS SCRIPT.  IN NO EVENT SHALL THESE SCRIPTS BE DEEMED TO BE CLOUD SERVICES AS PROVIDED BY QUALYS**_

# Usage:
Taking an inspiration from GARLC, we have built this tutorial to help you achieve a state where all your newly launched instances will have Qualys Cloud Agent(CA) installed.
This tutorial makes use of following services:
1.	AWS Lambda
2.	Amazon EC2 Run Command
3.	CloudWatch Events
4.	S3 Bucket

## Logic: 
We start by creating a Rule that invokes an AWS Lambda function when any instance enters the “Running” state. The Lambda function will trigger the Run command on the instance to install Qualys Cloud Agent(CA).

## Prerequisites:

**EC2 instance has the AWS Systems Manager Agent (SSM agent) installed and has an IAM role that allows Run Command. For more information, refer to the following links:**

* [Installing and Configuring SSM Agent](http://docs.aws.amazon.com/systems-manager/latest/userguide/ssm-agent.html)

* [Configuring Security Roles for System Manager](http://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-access.html)

# Deployment:

## Lambda:
 1.	Create a Lambda function named Invoke-QCA and copy the contents from the file. It performs the following tasks:

* Checks whether the AWS Systems Manager Agent (SSM agent) is installed on the instance and has the instance assigned instance profile for SSM to run.

* Builds the commands and send it to Run command via an API. It populates the parameters: _ActivationID, CustomerID, AgentLocationWindows, AgentLocationDebian, AgentLocationRPM_. 
Agents will be stored at S3 Bucket. 

**_Note: Ensure that you insert the apt Input parameters titled _“REPLACE_ME”_._**

![Image](parameters.png?raw=true)


## CloudWatch:

 2.	Create a Rule in CloudWatch Events matching the event pattern that describes an instance’s state change to “running”. This can be done while creating a rule with Event Pattern and selecting Service Name as EC2 and Event Type as EC2 Instance State-change Notification as shown in the diagram. Select Specific state(s) and select running. Select the previously created Lambda function as your target.

![eventsources|100x100,30%](eventsources.png?raw=true "eventsources")

![eventfilters|100x100,30%](eventfilters.png?raw=true "eventfilters")

![eventtargets |100x100,30%](eventtargets.png?raw=true "eventtargets")


**NOTE: The cloudformation template named "Bootstrap.yml" is uploaded in the same folder and can be used to deploy this setup.**


