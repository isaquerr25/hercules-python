module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = local.cluster_name
  cluster_version = "1.18"
  subnet_ids            = module.vpc.public_subnets
  tags = {
    Environment = "training"
    GithubRepo  = "terraform-aws-eks"
    GithubOrg   = "terraform-aws-modules"
  }

  vpc_id = module.vpc.vpc_id

  eks_managed_node_group_defaults  = {
    root_volume_type = "gp2"
  }
  eks_managed_node_groups = {
    one = {
      name = "worker-group-1"
      additional_security_group_ids = [aws_security_group.worker_group_mgmt_one.id]
      instance_types = ["t2.small"]
      additional_userdata           = "echo foo bar"

      //min_size     = 1
      //max_size     = 3
      desired_size = 1
    }

    two = {
      name = "worker-group-2"
      additional_security_group_ids = [aws_security_group.worker_group_mgmt_two.id]
      instance_types = ["t2.medium"]
      additional_userdata           = "echo foo bar"
      //min_size     = 1
      //max_size     = 3
      desired_size = 1
    }
  }
}

data "aws_eks_cluster" "cluster" {
  name = module.eks.cluster_id
}

data "aws_eks_cluster_auth" "cluster" {
  name = module.eks.cluster_id
}

provider "kubernetes" {
  host                   = data.aws_eks_cluster.cluster.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority.0.data)
  token                  = data.aws_eks_cluster_auth.cluster.token
}