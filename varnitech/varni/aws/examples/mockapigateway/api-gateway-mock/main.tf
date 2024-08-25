provider "aws" {
  region = "us-east-2"
}

resource "aws_lambda_function" "mock_api_lambda_1" {
  function_name = "MockAPILambda1"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "index.lambda_handler"
  runtime       = "python3.8"
  source_code_hash = filebase64sha256("mock_api_1.zip")

  filename = "mock_api_1.zip"
}

resource "aws_lambda_function" "mock_api_lambda_2" {
  function_name = "MockAPILambda2"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "index.lambda_handler"
  runtime       = "python3.8"
  source_code_hash = filebase64sha256("mock_api_2.zip")

  filename = "mock_api_2.zip"
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_apigatewayv2_api" "mock_api_1" {
  name          = "MockAPI1"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "mock_api_1_lambda" {
  api_id           = aws_apigatewayv2_api.mock_api_1.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.mock_api_lambda_1.invoke_arn
}

resource "aws_apigatewayv2_route" "mock_api_1_route" {
  api_id    = aws_apigatewayv2_api.mock_api_1.id
  route_key = "POST /api1"

  target = "integrations/${aws_apigatewayv2_integration.mock_api_1_lambda.id}"
}

resource "aws_apigatewayv2_stage" "mock_api_1_stage" {
  api_id = aws_apigatewayv2_api.mock_api_1.id
  name   = "$default"
  auto_deploy = true
}

resource "aws_apigatewayv2_api" "mock_api_2" {
  name          = "MockAPI2"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "mock_api_2_lambda" {
  api_id           = aws_apigatewayv2_api.mock_api_2.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.mock_api_lambda_2.invoke_arn
}

resource "aws_apigatewayv2_route" "mock_api_2_route" {
  api_id    = aws_apigatewayv2_api.mock_api_2.id
  route_key = "POST /api2"

  target = "integrations/${aws_apigatewayv2_integration.mock_api_2_lambda.id}"
}

resource "aws_apigatewayv2_stage" "mock_api_2_stage" {
  api_id = aws_apigatewayv2_api.mock_api_2.id
  name   = "$default"
  auto_deploy = true
}
