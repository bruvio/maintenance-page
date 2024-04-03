data "aws_vpc" "selected" {
  filter {
    name   = "tag:CustomName"
    values = [var.vpc_name]
  }
}

data "aws_lb" "internal" {
  arn  = var.lb_arn
  name = var.lb_name
}

data "aws_route53_zone" "selected" {
  name         = var.route53_zone_name
  private_zone = true
}

data "aws_route53_zone" "public" {
  name = var.route53_public_zone_name
}

data "aws_security_group" "lb" {
  name   = "ecs-alb"
  vpc_id = data.aws_vpc.selected.id
}

data "aws_security_group" "ecs_tasks" {
  name   = "ecs-tasks"
  vpc_id = data.aws_vpc.selected.id
}


data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.selected.id]
  }
}
data "aws_iam_role" "task_role" {
  name = var.ecs_iam_role_name
}

data "aws_iam_role" "task_execution_role" {
  name = var.task_execution_role_name
}

data "aws_ecs_cluster" "fargate_cluster_blue" {
  cluster_name = var.ecs_cluster_name
}

data "aws_lb_listener" "internal" {
  arn = var.internal_listener_arn
}

data "aws_lb_listener" "external_ssl" {
  arn = var.external_ssl_listener_arn
}


data "aws_caller_identity" "current" {}