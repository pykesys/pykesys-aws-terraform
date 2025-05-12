# Re-execute after environment reset to recreate the ZIP package for Terraform + SSM + CloudWatch agent config

import os
import zipfile

# Recreate directory and files
os.makedirs("/mnt/data/terraform_ssm_cwagent", exist_ok=True)

main_tf = """
provider "aws" {
  region = "us-west-2"
}

resource "aws_ssm_parameter" "cloudwatch_config" {
  name  = "/myapp/cloudwatch-agent-config"
  type  = "String"
  value = file("${path.module}/cwagent-config.json")
}

resource "aws_instance" "example" {
  ami           = "ami-0c55b159cbfafe1f0" # Example Amazon Linux 2
  instance_type = "t2.micro"

  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name
  user_data = <<EOF
#!/bin/bash
yum install -y amazon-cloudwatch-agent
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c ssm:/myapp/cloudwatch-agent-config -s
EOF

  tags = {
    Name = "SSM-CloudWatch-Example"
  }
}

resource "aws_iam_role" "ec2_role" {
  name = "ec2_ssm_cloudwatch_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action    = "sts:AssumeRole",
      Effect    = "Allow",
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ssm_attach" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_role_policy_attachment" "cw_attach" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "ec2_ssm_profile"
  role = aws_iam_role.ec2_role.name
}
"""

cwagent_config = """
{
  "agent": {
    "metrics_collection_interval": 60,
    "run_as_user": "root"
  },
  "metrics": {
    "namespace": "MyApp",
    "metrics_collected": {
      "cpu": {
        "measurement": ["cpu_usage_idle", "cpu_usage_user", "cpu_usage_system"],
        "metrics_collection_interval": 60,
        "totalcpu": true
      },
      "mem": {
        "measurement": ["mem_used_percent"]
      }
    }
  }
}
"""

# Write the files
with open("/mnt/data/terraform_ssm_cwagent/main.tf", "w") as f:
    f.write(main_tf)
with open("/mnt/data/terraform_ssm_cwagent/cwagent-config.json", "w") as f:
    f.write(cwagent_config)

# Create the zip archive
zip_path = "/mnt/data/terraform_ssm_cwagent.zip"
with zipfile.ZipFile(zip_path, 'w') as zipf:
    zipf.write("/mnt/data/terraform_ssm_cwagent/main.tf", arcname="main.tf")
    zipf.write("/mnt/data/terraform_ssm_cwagent/cwagent-config.json", arcname="cwagent-config.json")

zip_path

Result
'/mnt/data/terraform_ssm_cwagent.zip'
Here is your downloadable, ready-to-use Terraform module:

📦 Download terraform_ssm_cwagent.zip

This archive contains:

main.tf: A full Terraform setup that:

Creates a CloudWatch Agent config in SSM Parameter Store

Launches an EC2 instance

Installs and configures the CloudWatch Agent at boot

cwagent-config.json: A basic CPU and memory monitoring config

Let me know if you'd like to add alarms, dashboards, or auto-scaling hooks to this setup! ​


