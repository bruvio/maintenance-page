provider "aws" {
  region = "eu-west-2"
  assume_role {
    role_arn = "arn:aws:iam::${var.account_id}:role/YOURROLE"
  }
  default_tags {
    tags = tomap(merge(var.default_tags))
  }
}
terraform {
  backend "s3" {
    encrypt = true
    region  = "eu-west-2"
    key     = "maintenance-page/tfstate.tf"
  }
  required_providers {
    aws = {
      source = "hashicorp/aws"
      # version = "= 5.23.0"
    }
  }
}



