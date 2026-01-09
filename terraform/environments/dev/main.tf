terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  # Configure remote backend - UPDATE THESE VALUES from Step 3
  backend "s3" {
    bucket         = "terraform-state-drift-detector-1767985182"  
    key            = "dev/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks-drift-detector"                 
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region
}

data "aws_caller_identity" "current" {}

# Networking Module
module "networking" {
  source = "../../modules/networking"
  
  environment          = var.environment
  project_name         = var.project_name
  vpc_cidr             = var.vpc_cidr
  public_subnet_cidr   = var.public_subnet_cidr
  availability_zone    = var.availability_zone
}

# Compute Module
module "compute" {
  source = "../../modules/compute"
  
  environment       = var.environment
  project_name      = var.project_name
  instance_type     = var.instance_type
  subnet_id         = module.networking.public_subnet_id
  security_group_id = module.networking.web_security_group_id
  account_id        = data.aws_caller_identity.current.account_id
}# Test change
