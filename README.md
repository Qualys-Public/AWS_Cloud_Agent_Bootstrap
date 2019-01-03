# deploy_qualys_bootstap_AWS
(Based on GARLC https://github.com/awslabs/lambda-runcommand-configuration-management)

"""THIS SCRIPT IS PROVIDED TO YOU "AS IS."  TO THE EXTENT PERMITTED BY LAW, QUALYS HEREBY DISCLAIMS ALL WARRANTIES AND LIABILITY FOR THE PROVISION OR USE OF THIS SCRIPT.  IN NO EVENT SHALL THESE SCRIPTS BE DEEMED TO BE CLOUD SERVICES AS PROVIDED BY QUALYS"""

Taking an inspiration from GARLC, we have built this tutorial to help you achieve a state where all your newly launched instances will have QCA installed.
This tutorial makes use of following services:
1.	AWS Lambda
2.	Amazon EC2 Run Command
3.	CloudWatch Events
4.	S3 Bucket

# Logic: 
we start by creating a Rule that invokes an AWS Lambda function when any instance enters the “Running” state. The Lambda function will trigger Run Command on the instance with commands to install QCA.

# Prerequisites:

1.	EC2 instance has the SSM Agent installed and has an IAM role that allows Run Command. For more information:

	Installing and Configuring SSM Agent 
http://docs.aws.amazon.com/systems-manager/latest/userguide/ssm-agent.html

	Configuring Security Roles for System Manager 
http://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-access.html

# Steps for deployment:

# Lambda:
 1.	Create a Lambda function named Invoke-QCA and copy the contents from the file. It does following tasks:

  i)	Checks Whether the SSM agent is installed on the instance and has the instance assigned instance profile for SSM to run.

  ii)	Builds the commands and send it to Run command via an API. It populates the parameters ie ActivationID, CustomerID, AgentLocationWindows, AgentLocationDebian, AgentLocationRPM. 
Agents will be stored at S3 Bucket. Note: don’t FORGET to change the Input parameters titled “REPLACE_ME”.

![Image](parameters.png?raw=true)


# CloudWatch:

 2.	Create a Rule in CloudWatch Events matching the event pattern that describes an instance’s state change to “running”. This can be done while creating a rule with Event Pattern and selecting Service Name as EC2 and Event Type as EC2 Instance State-change Notification as shown in the diagram. Select Specific state(s) and select running. Select the previously created Lambda function as your target.

![eventsources](eventsources.png?raw=true "eventsources")

![eventfilters](eventfilters.png?raw=true "eventfilters")

![eventtargets](eventtargets.png?raw=true "eventtargets")


# NOTE: The cloudformation template named "Bootstart.yml" is uploaded in the same folder and can be used to deploy this setup.


