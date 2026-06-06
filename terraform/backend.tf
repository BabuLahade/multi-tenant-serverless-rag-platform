terraform {
  backend "s3" {
    bucket         = "nova-rag-tf-state-babulahade"
    key            = "dev/terraform.tfstate"
    region         = "ap-south-1"
    dynamodb_table = "nova-rag-tf-locks"
    encrypt        = true
  }
}