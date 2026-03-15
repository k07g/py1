terraform {
  required_version = ">= 1.14.7"
  required_providers {
    aws = {
        source = "hashicorp/aws"
        version = ">= 5.0"
    }
  }
  cloud {
    organization = "ko07ga-jp"
    hostname = "app.terraform.io"
    workspaces {
      name = "py1"
    }
  }
}