output "vpc_id" {
  value       = aws_vpc.main.id
  description = "ID of the VPC"
}

output "public_subnet_id" {
  value       = aws_subnet.public.id
  description = "ID of the public subnet"
}

output "web_security_group_id" {
  value       = aws_security_group.web.id
  description = "ID of the web security group"
}