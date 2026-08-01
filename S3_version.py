import json
import boto3

s3 = boto3.client("s3")
config = boto3.client("config")

def lambda_handler(event, context):

    print(json.dumps(event, indent=4))

    invoking_event = json.loads(event["invokingEvent"])

    configuration_item = invoking_event["configurationItem"]

    bucket_name = configuration_item["resourceName"]

    result_token = event["resultToken"]

    response = s3.get_bucket_versioning(Bucket=bucket_name)

    status = response.get("Status")

    if status == "Enabled":
        compliance = "COMPLIANT"
    else:
        compliance = "NON_COMPLIANT"

    config.put_evaluations(
        Evaluations=[
            {
                "ComplianceResourceType": "AWS::S3::Bucket",
                "ComplianceResourceId": bucket_name,
                "ComplianceType": compliance,
                "OrderingTimestamp": configuration_item["configurationItemCaptureTime"]
            }
        ],
        ResultToken=result_token
    )

    return {
        "statusCode": 200,
        "body": f"{bucket_name} is {compliance}"
    }
