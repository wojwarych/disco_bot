terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = var.region
}

resource "aws_ecr_repository" "disco_bot" {
  name = "disco_bot"
}

resource "aws_ecs_cluster" "cluster" {
  name = "disco_bot"
}

module "container_definition" {
  source          = "cloudposse/ecs-container-definition/aws"
  version         = "0.61.1"
  container_name  = "disco_bot_container"
  container_image = "827878376937.dkr.ecr.eu-central-1.amazonaws.com/disco_bot:latest"
}

data "aws_iam_policy_document" "s3_data_bucket_policy" {
  statement {
    sid = ""
    effect = "Allow"
    actions = [
      "s3:ListBucket",
      "s3:CreateBucket",
    ]
    resources = [
      "arn:aws:s3:::*"
    ]
  }

  statement {
    sid = ""
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:ReadObject",
      "s3:PutObject",
    ]
    resources = [
      "arn:aws:s3:::*/mondrosci.txt"
    ]
  }
}

resource "aws_iam_policy" "s3_policy" {
  name = "disco_bot_s3_policy"
  policy = "${data.aws_iam_policy_document.s3_data_bucket_policy.json}"
}

resource "aws_iam_role_policy_attachment" "ecs_role_s3_data_bucket_policy_attach" {
  role = "${aws_iam_role.ecs_role.name}"
  policy_arn = "${aws_iam_policy.s3_policy.arn}"
}

data "aws_iam_policy_document" "ecs_assume_role_policy" {
  statement {
    sid = ""
    effect = "Allow"
    actions = [
      "sts:AssumeRole",
    ]
    principals {
      type = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ecs_role" {
  name = "disco_bot_ecs_role"
  assume_role_policy = "${data.aws_iam_policy_document.ecs_assume_role_policy.json}"
}
