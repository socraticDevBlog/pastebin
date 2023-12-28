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

variable "compressed_dependencies_layer_filename" {
  type        = string
  default     = "layer.zip"
  description = "a python layer are external dependencies modules lambda app requires to run (ex.: boto3)"
}

variable "compressed_app_filename" {
  type    = string
  default = "src.zip"
}

variable "cors_allow_origins" {
  type    = set(string)
  default = ["*"]
}