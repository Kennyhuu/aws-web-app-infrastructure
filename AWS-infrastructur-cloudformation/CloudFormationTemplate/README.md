# AWS CloudFormation Templates

This directory contains three CloudFormation templates, each representing a different
stage of a web application infrastructure on AWS — from a basic single-server setup,
through a WordPress deployment, to a fully scalable multi-AZ production stack.

---

## Table of Contents

- [Templates at a Glance](#templates-at-a-glance)
- [Template 1 — Base Network & Web Server](#template-1--base-network--web-server)
- [Template 2 — WordPress Stack](#template-2--wordpress-stack)
- [Template 3 — Load Balancer & Auto Scaling](#template-3--load-balancer--auto-scaling)
- [Shared Parameters](#shared-parameters)
- [Deploying with the AWS Toolkit for VS Code](#deploying-with-the-aws-toolkit-for-vs-code)
- [Deploying via AWS CLI](#deploying-via-aws-cli)
- [Deploying via AWS Console](#deploying-via-aws-console)
- [Security Notes](#security-notes)
- [Cleanup](#cleanup)

---

## Templates at a Glance

| File | Purpose | Complexity |
|---|---|---|
| `cloudformation-template.yaml` | Base VPC + single EC2 web server with WordPress install | Beginner |
| `cloudformation-wordpress.yaml` | Production-ready WordPress on EC2 with MariaDB, full Apache config | Intermediate |
| `cloudformation-loadB-and-autoS.yaml` | ALB + Auto Scaling Group with CloudWatch CPU alarms across 2 AZs | Advanced |

---

## Template 1 — Base Network & Web Server

**File:** `cloudformation-template.yaml`

The starting point. Provisions a full VPC with public and private subnets, an Internet
Gateway, routing tables, and a single EC2 instance running a basic WordPress install.

### What it deploys

```
VPC (10.0.0.0/16)
 ├── Public Subnet 1  (10.0.1.0/24)   ← EC2 App Server
 ├── Public Subnet 2  (10.0.2.0/24)
 ├── Private Subnet 1 (10.0.11.0/24)
 └── Private Subnet 2 (10.0.12.0/24)
```

| Resource | Details |
|---|---|
| VPC + IGW | Isolated network with internet access |
| 4 Subnets | 2 public, 2 private across 2 AZs |
| Route Tables | Public routes to IGW; private isolated |
| Security Group | HTTP 80 open; SSH 22 from a fixed IP |
| EC2 Instance | `t3.micro`, Amazon Linux 2023, in Public Subnet 1 |

### UserData — what runs on boot

```bash
yum update -y
yum install -y httpd php wget unzip
amazon-linux-extras enable php8.2
yum install php php-cli php-fpm php-mysqlnd
systemctl enable httpd && systemctl start httpd
wget https://wordpress.org/latest.tar.gz
tar -xzf latest.tar.gz
cp -r wordpress/* /var/www/html/
chown -R apache:apache /var/www/html
systemctl restart httpd
```

> **Note:** This template downloads WordPress but does not configure a database.
> It is intended as a foundation or a quick connectivity test.

### Parameters

| Parameter | Default | Description |
|---|---|---|
| `LabVpcCidr` | `10.0.0.0/16` | VPC CIDR |
| `PublicSubnet1Cidr` | `10.0.1.0/24` | Public Subnet 1 CIDR |
| `PublicSubnet2Cidr` | `10.0.2.0/24` | Public Subnet 2 CIDR |
| `PrivateSubnet1Cidr` | `10.0.11.0/24` | Private Subnet 1 CIDR |
| `PrivateSubnet2Cidr` | `10.0.12.0/24` | Private Subnet 2 CIDR |
| `AmazonLinuxAMIID` | Latest AL2023 (SSM) | Auto-resolved via SSM |
| `PublicKeyName` | `vockey` | EC2 Key Pair for SSH |

---

## Template 2 — WordPress Stack

**File:** `cloudformation-wordpress.yaml`

A complete, self-contained WordPress deployment on a single EC2 instance. Apache, PHP,
and MariaDB are all installed on the same machine. Database credentials are passed as
CloudFormation parameters so no secrets are hardcoded in the template.

### What it deploys

```
VPC (10.0.0.0/16)
 ├── Public Subnet 1  (10.0.1.0/24)   ← EC2 App Server
 │     Apache + PHP + MariaDB
 │     WordPress auto-configured
 └── Private Subnet 1 (10.0.11.0/24)
```

| Resource | Details |
|---|---|
| VPC + IGW | Isolated network |
| Public + Private Subnet | Single AZ, one of each |
| Security Group | HTTP 80 open; SSH 22 from fixed IP |
| EC2 Instance | `t3.micro`, 20 GB gp3 EBS, Amazon Linux 2023 |

### UserData — what runs on boot

The bootstrap script is fully automated and logs everything to `/var/log/wordpress-install.log`:

1. `dnf update` + install Apache, PHP (with mysqlnd, gd, curl, xml), MariaDB
2. Enable and start `httpd` and `mariadb`
3. Set MariaDB root password, create the WordPress database and user
4. Download and extract WordPress, copy files to `/var/www/html`
5. Write `wp-config.php` with DB name, user, and password via `sed`
6. Write an Apache VirtualHost config with `AllowOverride All`
7. Set correct ownership and permissions on `/var/www/html`

### Parameters

| Parameter | Default | Description |
|---|---|---|
| `LabVpcCidr` | `10.0.0.0/16` | VPC CIDR |
| `PublicSubnet1Cidr` | `10.0.1.0/24` | Public Subnet CIDR |
| `PrivateSubnet1Cidr` | `10.0.11.0/24` | Private Subnet CIDR |
| `AmazonLinuxAMIID` | Latest AL2023 (SSM) | Auto-resolved via SSM |
| `PublicKeyName` | `vockey` | EC2 Key Pair |
| `DBName` | `wordpress` | Database name |
| `DBUser` | `wpuser` | Database username |
| `DBPassword` | *(NoEcho)* | MariaDB root password |
| `DBUserPassword` | *(NoEcho)* | WordPress DB user password |

### Outputs

After deployment, CloudFormation exposes:

| Output | Value |
|---|---|
| `WordPressURL` | `http://<PublicDNS>` — open to complete WP setup wizard |
| `PublicIP` | Instance public IP |
| `SSHCommand` | Ready-to-run SSH command |
| `InstallLog` | Command to tail the install log on the instance |

---

## Template 3 — Load Balancer & Auto Scaling

**File:** `cloudformation-loadB-and-autoS.yaml`

The most advanced template. Adds an Application Load Balancer and an Auto Scaling Group
on top of the base network, with CPU-based CloudWatch alarms driving automatic scale-out
and scale-in across two Availability Zones.

### What it deploys

```
Internet
    │
    ▼
Application Load Balancer  (Public Subnet 1 + 2, internet-facing)
    │  HTTP:80
    ▼
Target Group (health check: GET /)
    │
Auto Scaling Group  min:2 / desired:2 / max:4
    ├── EC2 (Public Subnet 1, AZ-a)   ← Launch Template
    └── EC2 (Public Subnet 2, AZ-b)   ← Launch Template

CloudWatch
  ├── CPUHighAlarm  CPU > 70%  →  ScaleOutPolicy (+1 instance)
  └── CPULowAlarm   CPU < 30%  →  ScaleInPolicy  (-1 instance)
```

| Resource | Details |
|---|---|
| VPC + IGW | Full network (same CIDR layout as Template 1) |
| ALB | Internet-facing, HTTP:80, spans 2 AZs |
| Target Group | Instance type, health check on `/` |
| ALB Listener | HTTP:80 → forward to Target Group |
| Launch Template | Amazon Linux 2023, `t3.micro`, UserData with IMDSv2 |
| Auto Scaling Group | Min 2, Desired 2, Max 4, ELB health check, 300s grace |
| ScaleOutPolicy | `ChangeInCapacity: +1` |
| ScaleInPolicy | `ChangeInCapacity: -1` |
| CPUHighAlarm | CPU > 70% for 2 × 5 min periods |
| CPULowAlarm | CPU < 30% for 2 × 5 min periods |

### Parameters

| Parameter | Default | Description |
|---|---|---|
| `LabVpcCidr` | `10.0.0.0/16` | VPC CIDR |
| `PublicSubnet1Cidr` | `10.0.1.0/24` | Public Subnet 1 CIDR |
| `PublicSubnet2Cidr` | `10.0.2.0/24` | Public Subnet 2 CIDR |
| `PrivateSubnet1Cidr` | `10.0.11.0/24` | Private Subnet 1 CIDR |
| `PrivateSubnet2Cidr` | `10.0.12.0/24` | Private Subnet 2 CIDR |
| `AmazonLinuxAMIID` | Latest AL2023 (SSM) | Auto-resolved via SSM |
| `PublicKeyName` | `vockey` | EC2 Key Pair |

---

## Shared Parameters

All three templates share the same core parameters with the same defaults, so you can
reuse the same override values across all stacks:

```bash
--parameter-overrides \
  PublicKeyName=my-key \
  LabVpcCidr=10.0.0.0/16
```

Templates 2 and 3 only differ in their unique additions (`DBName`/`DBPassword` for
Template 2, no extras for Template 3).

---

## Deploying with the AWS Toolkit for VS Code

The AWS Toolkit extension lets you deploy and manage CloudFormation stacks directly
from the editor without touching a terminal.

### Prerequisites

1. Install the **AWS Toolkit** extension from the VS Code Marketplace
   (`amazonwebservices.aws-toolkit-vscode`)
2. Configure your AWS credentials — either via `aws configure` in a terminal or by
   signing in through the Toolkit's credential provider

### Connect to your AWS account

1. Open the **AWS** panel in the VS Code Activity Bar (the AWS logo on the left)
2. Click **Connect to AWS** and select your credential profile (e.g., `default`)
3. Select the target region (e.g., `eu-west-1`) from the region selector

### Deploy a template

**Method 1 — Right-click in the editor**

1. Open one of the YAML template files in VS Code
2. Right-click anywhere in the editor
3. Select **Deploy SAM Application** — or look for **AWS: Deploy CloudFormation Stack**
   in the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)

**Method 2 — AWS Explorer panel**

1. Open the **AWS** panel → expand **CloudFormation**
2. Click the **+** icon or right-click → **Create CloudFormation Stack**
3. Choose **Upload a template** and browse to the YAML file

**Filling in the wizard**

| Field | What to enter |
|---|---|
| Stack name | e.g., `base-network`, `wordpress-stack`, `lb-asg-stack` |
| Template | Select the relevant `.yaml` file |
| Parameters | Fill in any overrides — leave blank to use defaults |
| Capabilities | Acknowledge `CAPABILITY_IAM` if prompted |

4. Click **Deploy** — the Toolkit opens a CloudFormation Events panel showing live
   stack events as resources are created

### Monitor stack progress

- The **CloudFormation** section in the AWS Explorer panel shows stack status in real time
- Click the stack name to expand its resources and events
- `CREATE_COMPLETE` means the stack is ready

### View outputs (Template 2)

1. In the AWS Explorer, expand **CloudFormation** → select your stack
2. Expand **Outputs** to see `WordPressURL`, `PublicIP`, `SSHCommand`, and `InstallLog`

### Delete a stack

1. In the AWS Explorer, right-click the stack
2. Select **Delete CloudFormation Stack**
3. Confirm the deletion — all resources are removed automatically

---

## Deploying via AWS CLI

If you prefer the terminal, use the commands below for each template.

### Template 1 — Base Stack

```bash
aws cloudformation deploy \
  --template-file cloudformation-template.yaml \
  --stack-name base-network-stack \
  --parameter-overrides PublicKeyName=<your-key-pair>
```

### Template 2 — WordPress Stack

```bash
aws cloudformation deploy \
  --template-file cloudformation-wordpress.yaml \
  --stack-name wordpress-stack \
  --parameter-overrides \
    PublicKeyName=<your-key-pair> \
    DBName=wordpress \
    DBUser=wpuser \
    DBPassword=<strong-password> \
    DBUserPassword=<strong-password>
```

Monitor the install log after deployment:

```bash
# Get the instance IP from the stack output
aws cloudformation describe-stacks \
  --stack-name wordpress-stack \
  --query "Stacks[0].Outputs"

# SSH in and watch the log
ssh -i <your-key-pair>.pem ec2-user@<public-ip>
tail -f /var/log/wordpress-install.log
```

### Template 3 — Load Balancer & Auto Scaling

```bash
aws cloudformation deploy \
  --template-file cloudformation-loadB-and-autoS.yaml \
  --stack-name lb-asg-stack \
  --parameter-overrides PublicKeyName=<your-key-pair>
```

Get the ALB DNS name to open in a browser:

```bash
aws cloudformation describe-stack-resources \
  --stack-name lb-asg-stack \
  --logical-resource-id ApplicationLoadBalancer \
  --query "StackResourceDetail.PhysicalResourceId"

# Or query the ALB directly
aws elbv2 describe-load-balancers \
  --query "LoadBalancers[*].DNSName"
```

---

## Deploying via AWS Console

1. Go to **CloudFormation** → **Create stack** → **With new resources (standard)**
2. Choose **Upload a template file** and select the `.yaml` file
3. Enter a unique stack name
4. On the **Specify stack details** page, fill in or override parameters
   - For Template 2: set `DBPassword` and `DBUserPassword` (they are `NoEcho` — values won't be shown again)
5. On the **Configure stack options** page, leave defaults or add tags
6. Review and click **Create stack**

Stack creation times:
- Template 1: ~2 minutes
- Template 2: ~4–6 minutes (MariaDB + WordPress download/config)
- Template 3: ~3–5 minutes

---

## Security Notes

- SSH on port 22 is restricted to `92.208.111.225/32` in all three templates. Update
  this to your own IP before deploying, or remove the rule if SSH is not needed.
- Template 2 uses `NoEcho: true` for database passwords — they are never shown in
  the console or CLI output after stack creation.
- The `DBPassword` and `DBUserPassword` defaults in Template 2 are `secret` — always
  override these with strong, unique values before deploying.
- AMI IDs are resolved dynamically via SSM (`/aws/service/ami-amazon-linux-latest/...`),
  so you always get the latest patched Amazon Linux 2023 image at deploy time.

---

## Cleanup

Delete stacks when no longer needed to avoid ongoing charges:

```bash
# Template 1
aws cloudformation delete-stack --stack-name base-network-stack

# Template 2
aws cloudformation delete-stack --stack-name wordpress-stack

# Template 3
aws cloudformation delete-stack --stack-name lb-asg-stack
```

Or in the AWS Toolkit: right-click the stack in the AWS Explorer → **Delete CloudFormation Stack**.

All resources created by the stack (VPC, subnets, EC2 instances, load balancer, ASG,
security groups) are removed automatically.
