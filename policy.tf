resource "aws_iam_role" "glue" {
  name        = "AWSGlueServiceRoleDefault"
  description = "Role able to execute Glue Jobs"

  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : "sts:AssumeRole",
        "Principal" : {
          "Service" : "glue.amazonaws.com"
        },
        "Condition" : {}
      }
    ]
  })
}

data "aws_iam_policy" "AmazonS3FullAccess" {
  arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "glue_s3" {
  role       = aws_iam_role.glue.name
  policy_arn = data.aws_iam_policy.AmazonS3FullAccess.arn
}

data "aws_iam_policy" "AWSGlueServiceRole" {
  arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

resource "aws_iam_role_policy_attachment" "glue_service" {
  role       = aws_iam_role.glue.name
  policy_arn = data.aws_iam_policy.AWSGlueServiceRole.arn
}

resource "aws_iam_user" "airflow" {
  name = "airflow"
}

resource "aws_iam_user_policy" "airflow_glue_jobs" {
  name = "RunGlueJobs"
  user = aws_iam_user.airflow.name

  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Sid" : "ID0",
        "Effect" : "Allow",
        "Action" : [
          "iam:GetRole",
          "iam:PassRole"
        ],
        "Resource" : [
          "arn:aws:iam::*:role/AWSGlueServiceRoleDefault"
        ]
      },
      {
        "Sid" : "ID1",
        "Effect" : "Allow",
        "Action" : [
          "glue:GetJob",
          "glue:CreateJob",
          "glue:StartJobRun",
          "glue:GetJobRun"
        ],
        "Resource" : [
          "arn:aws:glue:*:*:job/*"
        ]
      }
    ]
  })
}