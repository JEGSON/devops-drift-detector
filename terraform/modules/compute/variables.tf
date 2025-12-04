variable "environment" {
  description = "Environment name"
  type        = string
}

variable "project_name" {
  description = "Project name"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "subnet_id" {
  description = "Subnet ID for EC2 instance"
  type        = string
}

variable "security_group_id" {
  description = "Security group ID for EC2 instance"
  type        = string
}

variable "account_id" {
  description = "AWS Account ID"
  type        = string
}