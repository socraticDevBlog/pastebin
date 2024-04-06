variable "routes" {
  type        = list(string)
  description = "list of API routes to be configured in API Gateway"
  default     = ["GET /paste", "GET /paste/api", "POST /paste", "POST /paste/api", "OPTIONS /paste"]
}

variable "region" {
  type    = string
  default = "ca-central-1"
}

variable "python_runtime" {
  type        = string
  default     = "python3.9"
  description = "runtime on which lambda python code will run"
}

variable "app_name" {
  type    = string
  default = "pastebin"
}

variable "dynamodb_table" {
  type    = string
  default = "paste"
}

variable "log_retention" {
  default = 7
  type    = number
}

variable "virtualenv_id" {
  type        = string
  default     = "98kiCtZv"
  description = "random ID created by pipenv when installing the project"
}

variable "cors_allow_origins" {
  type    = set(string)
  default = ["*"]
}

variable "notification_email" {
  type      = string
  sensitive = true
}

variable "zipped_files" {
  type = map(string)
  default = {
    "app"   = "src.zip"
    "layer" = "layer.zip"
  }
}