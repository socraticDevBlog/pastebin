variable "routes_read" {
  type        = set(string)
  description = "list of API GET routes to be configured in API Gateway"
  default     = ["GET /paste", "GET /paste/api", "GET /paste/api/pastes","OPTIONS /paste"]
}

variable "routes_write" {
  type        = set(string)
  description = "list of API POST routes to be configured in API Gateway"
  default     = ["POST /paste", "POST /paste/api"]
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
  default   = "maximebonin@outlook.com"
}

variable "zipped_files" {
  type = map(string)
  default = {
    "app"   = "src.zip"
    "layer" = "layer.zip"
  }
}