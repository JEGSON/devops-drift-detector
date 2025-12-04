output "vpc_id" {
  value       = module.networking.vpc_id
  description = "VPC ID"
}

output "web_server_public_ip" {
  value       = module.compute.instance_public_ip
  description = "Public IP of web server"
}

output "web_server_url" {
  value       = "http://${module.compute.instance_public_ip}"
  description = "URL to access web server"
}

output "s3_bucket_name" {
  value       = module.compute.s3_bucket_name
  description = "S3 bucket for app data"
}