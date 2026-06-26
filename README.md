# AWS Web Application Infrastructure

A growing collection of guides and templates for building web application infrastructure
on AWS. Each approach covers the same core concepts — networking, compute, security, and
storage — using a different toolset or method.

---

## Approaches

| # | Approach | Folder | Toolset |
|---|---|---|---|
| 1 | [Visual — AWS Management Console](#approach-1--visual-aws-management-console) | [`Aws-infrastructur-visual-approach/`](./Aws-infrastructur-visual-approach) | AWS Console, click-through |
| 2 | [Infrastructure as Code — CloudFormation](#approach-2--infrastructure-as-code-cloudformation) | [`AWS-infrastructur-cloudformation/`](./AWS-infrastructur-cloudformation) | CloudFormation YAML + AWS Toolkit |
| … | More approaches coming | — | — |

---

## Approach 1 — Visual (AWS Management Console)

**Folder:** [`Aws-infrastructur-visual-approach/`](./Aws-infrastructur-visual-approach)
**Guide:** [`Aws-infrastructur-visual-approach/README.md`](./Aws-infrastructur-visual-approach/README.md)

A step-by-step walkthrough of building the infrastructure manually through the AWS
Management Console. Every step is documented with screenshots.

### Infrastructure built

```
VPC (10.0.0.0/16)
 ├── Public Subnet  (10.0.1.0/24)
 │     ├── Bastion Host  ← SSH from your IP only
 │     └── Web Server    ← HTTP from internet, SSH from Bastion only
 └── Private Subnet (10.0.2.0/24)
       └── RDS MySQL     ← port 3306 from Web Server only
```

### Steps covered

| Step | Description |
|---|---|
| 1 | Create VPC with public and private subnets |
| 2 | Attach Internet Gateway and configure route tables |
| 3 | Launch a Bastion Host in the public subnet |
| 4 | Launch a Web Server (HTTP public, SSH from Bastion) |
| 5 | Create a Security Group for RDS |
| 6 | Deploy an RDS MySQL instance in the private subnet |
| 7 | SSH into the Bastion Host from your terminal |
| 8 | Tunnel from Bastion to Web Server via private IP |
| 9 | Connect to the RDS database from the Web Server |

---

## Approach 2 — Infrastructure as Code (CloudFormation)

**Folder:** [`AWS-infrastructur-cloudformation/`](./AWS-infrastructur-cloudformation)
**Guide:** [`AWS-infrastructur-cloudformation/CloudFormationTemplate/README.md`](AWS-infrastructur-cloudformation/README.md)

Three CloudFormation templates that automate the infrastructure setup progressively.
Deployable via the **AWS Toolkit for VS Code**, the **AWS CLI**, or the **AWS Console**.

### Templates

| Template | Purpose |
|---|---|
| [`cloudformation-template.yaml`](./AWS-infrastructur-cloudformation/CloudFormationTemplate/cloudformation-template.yaml) | VPC, subnets, IGW, single EC2 with WordPress |
| [`cloudformation-wordpress.yaml`](./AWS-infrastructur-cloudformation/CloudFormationTemplate/cloudformation-wordpress.yaml) | Same network + EC2 fully configured with Apache, PHP, MariaDB |
| [`cloudformation-loadB-and-autoS.yaml`](./AWS-infrastructur-cloudformation/CloudFormationTemplate/cloudformation-loadB-and-autoS.yaml) | ALB across 2 AZs + ASG (min 2 / max 4) + CloudWatch CPU alarms |

### Quick deploy

**AWS Toolkit for VS Code:**
1. Install the **AWS Toolkit** extension (`amazonwebservices.aws-toolkit-vscode`)
2. Connect your AWS account via the AWS panel in the Activity Bar
3. Open a template file → Command Palette (`Ctrl+Shift+P`) → **AWS: Deploy CloudFormation Stack**
4. Enter a stack name, fill in parameters, and deploy

**AWS CLI:**
```bash
aws cloudformation deploy \
  --template-file AWS-infrastructur-cloudformation/CloudFormationTemplate/<template-file>.yaml \
  --stack-name <stack-name> \
  --parameter-overrides PublicKeyName=<your-key-pair>
```

---

<!-- 
## Approach 3 — (coming)

Description and link will go here.
-->

---

## Repository Structure

```
aws-web-app-infrastructure/
│
├── README.md                                    ← you are here
│
├── Aws-infrastructur-visual-approach/           # Approach 1: Console guide
│   ├── README.md
│   ├── image/                                   # Screenshots
│   └── Document/
│
└── AWS-infrastructur-cloudformation/            # Approach 2: CloudFormation
    ├── README.md                                # Toolkit deployment guide
    ├── Documentation/                           # Diagrams and docs
    └── CloudFormationTemplate/
        ├── README.md                            # Full template reference
        ├── README-loadbalancer-autoscaling.md   # Deep-dive: ALB + ASG
        ├── cloudformation-template.yaml
        ├── cloudformation-wordpress.yaml
        └── cloudformation-loadB-and-autoS.yaml
```

---

## Choosing an approach

| Goal | Recommended approach |
|---|---|
| Learning AWS concepts hands-on | Approach 1 — Console |
| Repeatable, version-controlled deployments | Approach 2 — CloudFormation |
| CI/CD pipelines or team environments | Approach 2 — CloudFormation |
| Future approaches (e.g. CDK, Terraform, SAM) | See upcoming folders |
