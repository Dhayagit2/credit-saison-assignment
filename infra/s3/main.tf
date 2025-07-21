provider "aws" {
  region = "ap-south-1"
}

# Create KMS key
resource "aws_kms_key" "s3_key" {
  description             = "KMS key for S3 bucket encryption"
  enable_key_rotation     = true
}

# S3 bucket
resource "aws_s3_bucket" "restricted_bucket" {
  bucket = "credit-saison-s3-bucket"
  force_destroy = true

  tags = {
    Name = "IPRestrictedEncryptedBucket"
  }
}

# Enable default encryption using KMS with bucket key
resource "aws_s3_bucket_server_side_encryption_configuration" "bucket_enc" {
  bucket = aws_s3_bucket.restricted_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.s3_key.arn
      sse_algorithm     = "aws:kms"
    }

    bucket_key_enabled = true
  }
}

# Block public access
resource "aws_s3_bucket_public_access_block" "block_public" {
  bucket = aws_s3_bucket.restricted_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# IP Restriction via Bucket Policy
resource "aws_s3_bucket_policy" "ip_restrict" {
  bucket = aws_s3_bucket.restricted_bucket.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid       = "IPAllow",
        Effect    = "Allow",
        Principal = "*",
        Action    = "s3:*",
        Resource  = [
          "${aws_s3_bucket.restricted_bucket.arn}",
          "${aws_s3_bucket.restricted_bucket.arn}/*"
        ],
        Condition = {
          IpAddress = {
            "aws:SourceIp" = "49.207.193.33/32"
          }
        }
      }
    ]
  })
}
