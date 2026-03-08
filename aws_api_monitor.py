import json
import boto3
import requests
import os
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3client = boto3.client("s3")


def lambda_handler(event, context):

    logger.info("API monitor started")

    bucket_name = os.environ["CONFIG_BUCKET"]
    config_filename = os.environ["CONFIG_FILE"]

    response = s3client.get_object(
        Bucket=bucket_name,
        Key=config_filename
    )

    config_text = response["Body"].read().decode("utf-8")
    config_json = json.loads(config_text)

    timeout = config_json["timeout"]
    apis = config_json["apis"]

    results = []

    for api in apis:
        name = api["name"]
        url = api["url"]
        params = api["params"]

        try:
            start_time = time.time()

            response = requests.get(url, params=params, timeout=timeout)

            response.raise_for_status()

            end_time = time.time()
            response_time = round((end_time - start_time) * 1000, 2)

            results.append({
                "name": name,
                "url": url,
                "status": "SUCCESS",
                "status_code": response.status_code,
                "response_time": response_time,
                "error": None
            })

        except requests.exceptions.RequestException as e:
            end_time = time.time()
            response_time = round((end_time - start_time) * 1000, 2)

            logger.error(f"{name} FAILED: {str(e)}")

            results.append({
                "name": name,
                "url": url,
                "status": "FAILED",
                "status_code": None,
                "response_time": response_time,
                "error": str(e)
            })

    total_apis = len(results)
    successful = 0
    failed = 0
    total_response_time = 0

    for result in results:
        if result["status"] == "SUCCESS":
            successful += 1
            total_response_time += result["response_time"]
        else:
            failed += 1

    if successful > 0:
        average_response_time = round(total_response_time / successful, 2)
    else:
        average_response_time = None

    summary = {
        "total_apis": total_apis,
        "successful": successful,
        "failed": failed,
        "average_response_time": average_response_time
    }

    logger.info(f"Summary: {summary}")

    report = {
        "summary": summary,
        "results": results
    }

    report_json = json.dumps(report, indent=2)
    report_key = f"reports/api_report_{int(time.time())}.json"

    s3client.put_object(
        Bucket=bucket_name,
        Key=report_key,
        Body=report_json,
        ContentType="application/json"
    )

    logger.info(f"Report uploaded to S3: {report_key}")
    logger.info("API monitor completed")

    return {
        "message": "API monitor completed",
        "report_file": report_key,
        "summary": summary
    }