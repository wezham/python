from datetime import datetime

import boto3

ENDPOINT_URL = None


def put_item_in_dynamodb(page_name: str):
    global ENDPOINT_URL
    if ENDPOINT_URL:
        args = {"endpoint_url": ENDPOINT_URL}
    else:
        args = {}

    try:
        dynamodb = boto3.resource("dynamodb", **args)
        page_views_table = dynamodb.Table("page_views")
        page_views_table.put_item(
            Item={"page_name": page_name, "timestamp": str(datetime.utcnow())}
        )
    except Exception:
        print("Failed to strore item")


def lambda_handler(event, context):
    page_name = event.get("page_name", None)

    if page_name is None:
        print("No page name provided")
        status_code = 403
    else:
        put_item_in_dynamodb(page_name)
        status_code = 200

    return {
        "statusCode": status_code,
    }
