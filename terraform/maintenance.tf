variable "hosts" {
  description = "List of hosts to be redirected to the maintenance page"
  type        = map(number)
}

variable "maintenance_mode" {
  description = "Enable maintenance mode (true/false)"
  type        = bool
  default     = false
}

locals {
  maintenance_page_content = file("${path.module}/../assets/maintenance_page.html")
}

resource "null_resource" "maintenance" {
  triggers = {
    maintenance_mode = var.maintenance_mode ? "enable" : "disable"
  }

  provisioner "local-exec" {
    command = "pip install boto3 && python3 maintenance.py ${var.external_ssl_listener_arn} ${var.maintenance_mode ? "true" : "false"}"
  }
}

resource "aws_lb_listener_rule" "fixed_response_maintenance" {
  for_each     = var.maintenance_mode ? var.hosts : {}
  listener_arn = var.external_ssl_listener_arn
  priority     = each.value
  action {
    type = "fixed-response"
    fixed_response {
      content_type = "text/html"
      message_body = local.maintenance_page_content
      status_code  = "503"
    }
  }

  condition {
    host_header {
      values = [each.key]
    }
  }
  depends_on = [null_resource.maintenance]
  tags = merge(
    var.default_tags, module.tags.tags, var.map_tags
  )
}