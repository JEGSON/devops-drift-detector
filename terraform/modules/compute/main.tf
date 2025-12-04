# Get latest Amazon Linux 2 AMI
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]
  
  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# EC2 Instance
resource "aws_instance" "web" {
  ami                    = data.aws_ami.amazon_linux_2.id
  instance_type          = var.instance_type
  subnet_id              = var.subnet_id
  vpc_security_group_ids = [var.security_group_id]
  
  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y httpd
              systemctl start httpd
              systemctl enable httpd
              echo "<h1>Hello from ${var.environment} environment</h1>" > /var/www/html/index.html
              EOF
  
  tags = {
    Name        = "${var.environment}-web-server"
    Environment = var.environment
    Project     = var.project_name
  }
}

# S3 Bucket for application data
resource "aws_s3_bucket" "app_data" {
  bucket = "${var.project_name}-${var.environment}-data-${var.account_id}"
  
  tags = {
    Name        = "${var.environment}-app-data"
    Environment = var.environment
    Project     = var.project_name
  }
}