
## Step-by Step AWS Challenge Task

### Networking <br />
Requirements <br />
Create a custom VPC (e.g., CIDR: 10.0.0.0/16)<br />
Create two subnets:<br />
PublicSubnet (e.g., 10.0.1.0/24)<br />
PrivateSubnet (e.g., 10.0.2.0/24)<br />
Attach an Internet Gateway to the VPC<br />
Configure route tables:<br />
Public subnet should route to the Internet Gateway<br />
Private subnet should not have internet access<br />
Associate each subnet with the appropriate route table<br />
## 1. Creating VPC with 2 Subnets
![img_1.png](image/create_vpc_and_subnets.png)

## 2. VPC Resource Map
![img.png](image/vpc_resource_map.png)

## 3. Creating Batsion Host
Bastion Host: <br />
Located in the public subnet<br />
Accessible via SSH only from your IP<br />
![img_2.png](image/create_bastion_host.png)


## 4. Creating WebServer
Web Server: <br />
Located in the public subnet<br />
Accessible via HTTP from the internet<br />
SSH access only from the Bastion Host<br />

![img.png](image/create_webserver.png)

# 5. Create a SG for RDS
RDS: Allow MySQL/MariaDB traffic only from the Web Server
![img.png](image/sg_rds.png)

# 6. Creating RDS MySQL DB
Deploy a MySQL or MariaDB RDS instance in the private subnet <br />
RDS should only allow inbound traffic on port 3306 from the Web Server <br />
![img.png](image/rds_mysql_db.png)

## 6.a Setting Network for DB
![img.png](image/rds_network_setting.png)

## 6.b. Troubleshooting: ERROR
An error occured while creating the DB instance<br />
Fix: Use connect to EC2 instance (WebServer)
![img.png](image/error_buildig.png)

# 7. Access to Bastion Server via terminal
Acces with terminal with ssh and public-key.pem
![ssh_to_bation.png](image/ssh_to_bation.png)


# 8. Connect to Webserver from Bastion server via SSH

IMPORTANT !!! Use private ipAdress 
![img.png](image/bastion_to_webserver.png)

# 9. Access to DB
Install mysql on EC2. Look in internet with updated installation

Access DB with your Credentials
![img.png](image/Access_to_mysql.png)