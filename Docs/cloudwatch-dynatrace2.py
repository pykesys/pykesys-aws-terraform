add alarms, dashboards, and auto-scaling hooks to this setup

# Augment the existing Terraform files with CloudWatch alarms, dashboard, and autoscaling group
additional_tf = """
resource "aws_launch_template" "example" {
  name_prefix   = "cwagent-launch-"
  image_id      = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  iam_instance_profile {
    name = aws_iam_instance_profile.ec2_profile.name
  }

  user_data = base64encode(<<EOF
#!/bin/bash
yum install -y amazon-cloudwatch-agent
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c ssm:/myapp/cloudwatch-agent-config -s
EOF
  )
}

resource "aws_autoscaling_group" "example" {
  desired_capacity     = 1
  max_size             = 2
  min_size             = 1
  vpc_zone_identifier  = ["subnet-xxxxxxxx"] # <-- Replace with your subnet ID
  launch_template {
    id      = aws_launch_template.example.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "cwagent-asg"
    propagate_at_launch = true
  }
}

resource "aws_cloudwatch_metric_alarm" "cpu_high" {
  alarm_name          = "HighCPUUtilization"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 300
  statistic           = "Average"
  threshold           = 70
  alarm_description   = "This alarm triggers when average CPU exceeds 70%"
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.example.name
  }
  alarm_actions = []
}

resource "aws_cloudwatch_dashboard" "example" {
  dashboard_name = "cwagent-dashboard"
  dashboard_body = jsonencode({
    widgets = [
      {
        type = "metric",
        x = 0,
        y = 0,
        width = 12,
        height = 6,
        properties = {
          metrics = [
            [ "AWS/EC2", "CPUUtilization", "AutoScalingGroupName", aws_autoscaling_group.example.name ]
          ],
          period = 300,
          stat = "Average",
          region = "us-west-2",
          title = "EC2 CPU Utilization"
        }
      }
    ]
  })
}
"""

# Write this to a new file in the existing directory
with open("/mnt/data/terraform_ssm_cwagent/alarms_dashboard_autoscaling.tf", "w") as f:
    f.write(additional_tf)

# Update the zip with the new file
with zipfile.ZipFile("/mnt/data/terraform_ssm_cwagent.zip", 'a') as zipf:
    zipf.write("/mnt/data/terraform_ssm_cwagent/alarms_dashboard_autoscaling.tf", arcname="alarms_dashboard_autoscaling.tf")

"/mnt/data/terraform_ssm_cwagent.zip"
Result
'/mnt/data/terraform_ssm_cwagent.zip'
Your Terraform module has been updated! 🎯

📦 Download Updated terraform_ssm_cwagent.zip

✅ New Additions:
CloudWatch Alarm: Triggers if average CPU > 70% over two periods

CloudWatch Dashboard: Visualizes CPU usage for the autoscaling group

Auto Scaling Group (ASG):

Launches EC2 instances from a template

Includes CloudWatch agent configuration via SSM

🔧 IMPORTANT: Update the vpc_zone_identifier with your real subnet ID (subnet-xxxxxxxx).

Would you like to add:

Scale-out/in policies based on the alarm?

Integration with an SNS topic for notifications? 📩 ​


