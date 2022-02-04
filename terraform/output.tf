output "internal_ip_address" {
  value = aws_instance.web-test.private_ip
}

output "external_ip_address" {
  value = aws_instance.web-test.public_ip
}

output "subnet_id" {
  value = aws_instance.web-test.subnet_id
}

output "aws-reg" {
  value = "${data.aws_region.current.name}"
}

output "account_id" {
  value = "${data.aws_caller_identity.current.account_id}"
}

output "user_id" {
  value = "${data.aws_caller_identity.current.user_id}"
}

output "caller_arn" {
  value = "${data.aws_caller_identity.current.arn}"
}

