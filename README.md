# Rikkeisoft - Documents Chatbot Assistant for Employees | Backend

Language: Python
Framework: FastAPI

## Installation & Launch

1. Ensure you have Python and `venv` package installed.
2. Clone this repository to your local machine.
3. Create a virtual environment:

   ```
   python -m venv venv
   ```
4. Activate the virtual environment:

   - On Windows:

     ```
     .\venv\Scripts\activate
     ```
   - On macOS and Linux:

     ```
     source venv/bin/activate
     ```
5. Install required packages:

```
    pip install -r requirements.txt
```

6. Create a `.env` file in the root dir (where this file is in) and provide these environment variables:

```
    GROQ_API_KEYSS
    UPLOAD_PATH (optional)
```

7. Compose Docker containers with this command:

```
    docker compose up -d
```

This will prepare the Milvus vector database.

8. Launch the FastAPI server:

```
    fastapi dev app/main.py
```

9. Server should be running at [http://127.0.0.1:8000](http://127.0.0.1:8000). APIs can be tested at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Development Guidance

To save tree structure of a directory, run command:

```
    tree /f /a [<drive>:][<path>] > [<drive>:]/[<file_path>]/<file_name>.txt
```

To run server without reloading a certain directory/file, e.g. the embedding model, run command:

```
    uvicorn app.main:app --reload --reload-exclude app/bot/model.py
```

groq.RateLimitError

## AWS Deployment

### Involved Services

- EC2: Bastion Host, NAT Server, load balancer, target group for auto scaling
- VPC: VPC, subnets, route tables, NACLs, security groups
- RDS: subnet group, DB instance
- S3: storing avatars, documents, backend files... and optionally static website hosting
- ECR: pushing Docker images
- ECS: cluster, task definition, service, task (Fargate)
- CloudFront: HTTPS distribution to redirect to HTTP ALB and optionally serve static website
- CloudFormation: create stack from template

### Description:

- User will access the website FE hosted by Vercel, which calls API from the CloudFront distribution (HTTPS)
- IAM roles for secure access management.
- ECS containers belong to WebServerSG security group in the private subnets. They receive requests from ALB, and access internet via NAT server.
- RDS instance belongs to DBServerSG security group in private subnets, only receives traffic from WebServerSG and DevServerSG security group (Bastion Host)
- NAT Server belongs to NATServerSG security group which accepts inbound traffic from WebServerSG security group and directs it to the internet.
- The Application Load Balancer belongs to ELBSG security group which accepts inbound web traffic (HTTP) from the CloudFront distribution and distributes them between the ECS tasks on port 80 in the target group via a listener
- ECS tasks have IAM role to access ECR (pull images) and S3 (read / write files)

### Bastion Host Setup

- AMI: Amazon Linux 2 AMI (HVM), SSD Volume Type
- Subnet: Public subnet, routed to an IGW
- Security Group: Allow SSH (22) and outbound access, ensure DBServerSG allows MySQL traffic from DevServerSG
- User Data:

  ```
  #!/bin/bash
  yum update -y
  amazon-linux-extras install -y lamp-mariadb10.2-php7.2 php7.2
  service httpd start
  yum install -y httpd mariadb-server php-mbstring php-xml
  sed -i "s/upload_max_filesize = 2M/upload_max_filesize = 10M/g" /etc/php.ini
  systemctl start httpd
  systemctl enable httpd
  usermod -a -G apache ec2-user
  chown -R ec2-user:apache /var/www
  chmod 2775 /var/www
  find /var/www -type d -exec sudo chmod 2775 {} \;
  find /var/www -type f -exec sudo chmod 0664 {} \;
  echo "<?php echo '<h2>Welcome to COS80001. Installed PHP version: ' . phpversion() . '</h2>'; ?>" > /var/www/html/phpinfo.php
  wget -P /var/www/html http://files.phpmyadmin.net/phpMyAdmin/5.2.1/phpMyAdmin-5.2.1-english.zip
  unzip /var/www/html/phpMyAdmin-5.2.1-english.zip -d /var/www/html
  mv /var/www/html/phpMyAdmin-5.2.1-english /var/www/html/phpmyadmin
  mv /var/www/html/phpmyadmin/config.sample.inc.php /var/www/html/phpmyadmin/config.inc.php
  sed -i "s/\$cfg\['Servers'\]\[\$i\]\['host'\] = 'localhost';/\$cfg\['Servers'\]\[\$i\]\['host'\] = '<RDS_ENDPOINT>';/" /var/www/html/phpmyadmin/config.inc.php
  ```

### NAT Server Setup

- AMI: Amazon Linux 2 AMI (HVM), SSD Volume Type
- Subnet: Public subnet, routed to an IGW
- Security Group: Allow SSH (22), HTTP (80), HTTPS (443), and outbound access
- Enable IP Forwarding: Go to EC2 Console → Select your instance → Actions → Networking → Change Source/Destination Check → Disable.
- SSH into the instance and run these commands (or pass as user data):

  ```
  sudo sysctl -w net.ipv4.ip_forward=1
  echo "net.ipv4.ip_forward = 1" | sudo tee -a /etc/sysctl.conf

  export PRIVATE_SUBNET_CIDR="10.0.0.0/16"  # Change this to your private subnet CIDR
  sudo iptables -t nat -A POSTROUTING -s $PRIVATE_SUBNET_CIDR -o eth0 -j MASQUERADE

  sudo yum install -y iptables-services
  sudo systemctl enable iptables
  sudo service iptables save
  ```
