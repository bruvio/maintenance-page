variable "account_id" {
}

variable "kms_key_id" {
}

variable "kms_description" {
}

variable "vpc_name" {
  default = "dev"
}



variable "default_tags" {
  description = "Default tags applied to all created resources"
  type        = map(any)
}

variable "map_tags" {
  description = "Default tags applied to all created resources"
  type        = map(any)
}


variable "map_migrated" {
  default = "d-server-01c97d6l20f8bk"
}

variable "aws_migration_project_id" {
  default = "MPE17143"
}

variable "route53_zone_name" {
}

variable "route53_genomic_zone_name" {
}

variable "route53_public_zone_name" {
}

variable "route53_ac_zone_name" {
}

variable "ecs_iam_role_name" {
  default = "ecsTaskExecutionRole"
}

variable "task_execution_role_name" {
  default = "ecsTaskExecutionRole"
}

variable "ecs_cluster_name" {
}

variable "internal_listener_arn" {
}

variable "external_ssl_listener_arn" {
}

variable "lb_arn" {
}

variable "lb_name" {
}





variable "service_version" {
  default = "latest"
}



variable "region" {
  default = "eu-west-2"
}
variable "aws_region" {
  description = "A region the infrastructure will be deployed in."
  type        = string
  default     = "eu-west-2"
}