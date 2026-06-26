# AWS CloudFormation Guide (AWS Toolkit Only)

This README explains how to work with the CloudFormation template in this folder using **Visual Studio Code** and the **AWS Toolkit**.

## Folder Contents
- `CloudFormationTemplate/` - the YAML template used for deployment
- `Documentation/` - diagrams and project notes

## Main Template File
- `CloudFormationTemplate/cloudformation-template.yaml`

## Step 1: Install AWS Toolkit in VS Code
1. Open **Visual Studio Code**.
2. Go to **Extensions**.
3. Search for **AWS Toolkit**.
4. Click **Install**.
5. Restart VS Code if needed.

## Step 2: Sign in to AWS
1. Click the **AWS** icon in the left side panel.
2. Choose **Sign in** or **Connect to AWS**.
3. Use your preferred sign-in method:
   - AWS credentials
   - SSO / IAM Identity Center
   - Existing AWS profile
4. Complete the login flow.

## Step 3: Open the CloudFormation Template
1. Open the folder [AWS-infrastructur-cloudformation](AWS-infrastructur-cloudformation).
2. Open the template file [AWS-infrastructur-cloudformation/CloudFormationTemplate/cloudformation-template.yaml](AWS-infrastructur-cloudformation/CloudFormationTemplate/cloudformation-template.yaml).
3. Make sure the YAML looks correct and is saved.

## Step 4: Validate the Template
Use the AWS Toolkit options to validate the template:
1. Open the template file.
2. Look for the AWS Toolkit template validation actions.
3. Check for any YAML or CloudFormation validation errors.

## Step 5: Deploy the Stack
1. In the AWS Toolkit, open the CloudFormation section.
2. Select the template you want to deploy.
3. Choose a stack name.
4. Select the correct AWS region.
5. Start the deployment.
6. Watch the stack events in the Toolkit.

## Step 6: Review the Created Resources
After deployment, you can use the Toolkit to:
- view stack resources
- inspect outputs
- check status
- open related AWS services

## Step 7: Delete the Stack
When you no longer need the resources:
1. Open the stack in the AWS Toolkit.
2. Choose the delete option.
3. Confirm the action.
4. Wait for the stack to be fully removed.


### Some sources
[AWS CloudFormation: Creating Load Balancer and Auto Scaling Group - Infrastructure as Code](https://medium.com/@ldmishra/aws-cloudformation-creating-load-balancer-and-auto-scaling-group-infrastructure-as-code-883912f7e24d)

[Using CloudFormation with Boto3](https://github.com/Kennyhuu/Boto3PractieKTH/blob/main/cloudformation.py)