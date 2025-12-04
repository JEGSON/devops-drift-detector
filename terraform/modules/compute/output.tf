output "instance_id" {
  value       = aws_instance.web.id
  description = "ID of the EC2 instance"
}

output "instance_public_ip" {
  value       = aws_instance.web.public_ip
  description = "Public IP of the EC2 instance"
}

output "s3_bucket_name" {
  value       = aws_s3_bucket.app_data.id
  description = "Name of the S3 bucket"
}