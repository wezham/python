from unittest.mock import patch

import boto3
import pytest
import testfixtures
from page_metrics import lambda_handler

ENDPOINT_URL = "http://localstack:4566"


@pytest.fixture()
def setup_dynamodb_table():
    dynamodb = boto3.client("dynamodb", endpoint_url=ENDPOINT_URL)

    dynamodb.create_table(
        TableName="page_views",
        KeySchema=[
            {"AttributeName": "page_name", "KeyType": "HASH"},
            {"AttributeName": "timestamp", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "page_name", "AttributeType": "S"},
            {"AttributeName": "timestamp", "AttributeType": "S"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
    )

    table_exists_waiter = dynamodb.get_waiter(waiter_name="table_exists")
    table_exists_waiter.wait(TableName="page_views")

    yield dynamodb

    dynamodb.delete_table(TableName="page_views")


@pytest.mark.parametrize(
    "event, exepected_response_code, expected_items_in_dynamodb",
    [
        pytest.param({}, 403, [], id="No page name, should return 403"),
        pytest.param(
            {"page_name": "TestPage"},
            200,
            [
                {
                    "page_name": {"S": "TestPage"},
                    "timestamp": {"S": "2021-01-01 00:00:00"},
                }
            ],
            id="Page name provided, should return 200",
        ),
    ],
)
@pytest.mark.freeze_time("2021-01-01")
def test_lambda_handler(
    setup_dynamodb_table, event, exepected_response_code, expected_items_in_dynamodb
):
    dynamodb_client = setup_dynamodb_table

    with patch("page_metrics.ENDPOINT_URL", ENDPOINT_URL):
        res = lambda_handler(event, {})
        assert res["statusCode"] == exepected_response_code

        items = dynamodb_client.scan(TableName="page_views")["Items"]
        testfixtures.compare(
            expected=expected_items_in_dynamodb,
            actual=items,
        )
