# Configure the AWS Provider
provider "aws" {
  region = "us-east-2"
}


data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_instance" "web-test" {
  ami             = data.aws_ami.ubuntu.id
  instance_type   = "t2.micro"
  key_name        = "BaseSG"
  subnet_id       = "subnet-eed17885"

  tags = {
    Name = "Hello Netology!"
  }
}

data "aws_security_group" "selected" {
  id = "sg-a1969cd2"
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

