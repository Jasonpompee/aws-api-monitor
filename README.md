# AWS API Monitor

A serverless API monitoring tool built with **AWS Lambda, Amazon S3, and Python**.

The system reads a configuration file from S3, checks multiple external APIs, records their response time and status, and stores a monitoring report back in S3.

This project demonstrates a **config-driven serverless monitoring system** using AWS services.

## Architecture

S3 (Configuration File)  
↓  
AWS Lambda (Python API Monitor)  
↓  
External APIs are called and monitored  
↓  
Response times and status codes are collected  
↓  
Monitoring report is generated  
↓  
Report is saved to Amazon S3


## Features

- Monitors multiple APIs using a configuration file
- Measures API response times
- Detects API failures and errors
- Generates structured JSON monitoring reports
- Stores reports in Amazon S3
- Uses environment variables for configuration
- Logs execution details to AWS CloudWatch


## Configuration

The Lambda function loads its configuration from a JSON file stored in Amazon S3.

Example configuration file:

```json
{
  "timeout": 5,
  "apis": [
    {
      "name": "GitHub API",
      "url": "https://api.github.com",
      "params": {}
    },
    {
      "name": "Open Meteo Weather",
      "url": "https://api.open-meteo.com/v1/forecast",
      "params": {
        "latitude": 41.76,
        "longitude": -72.67,
        "current_weather": true
      }
    }
  ]
}
```

## Environment Variables

The Lambda function uses environment variables instead of hardcoding configuration values.



Required variables:

CONFIG_BUCKET  
Name of the S3 bucket that stores the configuration file.



CONFIG_FILE  
Name of the JSON configuration file stored in the bucket.








## Example Output Report

After checking all APIs, the Lambda function generates a monitoring report and saves it to S3.


Example report structure:

```json
{
  "summary": {
    "total_apis": 3,
    "successful": 2,
    "failed": 1,
    "average_response_time": 142.8
  },
  "results": [
    {
      "name": "GitHub API",
      "status": "SUCCESS",
      "status_code": 200,
      "response_time": 87.4
    },
    {
      "name": "Example API",
      "status": "FAILED",
      "error": "Connection timeout"
    }
  ]
}
