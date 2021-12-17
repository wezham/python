from unittest.mock import MagicMock, patch

import pytest
from page_metrics import lambda_handler


@pytest.mark.parametrize(
    "event, exepected_response_code",
    [
        pytest.param({}, 403, id="No page name, should return 403"),
        pytest.param(
            {"page_name": "TestPage"}, 200, id="Page name provided, should return 200"
        ),
    ],
)
def test_lambda_hanlder(event, exepected_response_code):
    with patch("page_metrics.put_item_in_dynamodb", MagicMock()):
        res = lambda_handler(event, {})
        assert res["statusCode"] == exepected_response_code
