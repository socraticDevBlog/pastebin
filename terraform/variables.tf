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
