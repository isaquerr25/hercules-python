terraform {
  backend "s3" {
    bucket = "terraform-deploy-isaque"
    key    = "devops-ninja-eks"
    region = "us-west-1"
  }
}

