"""Tests standard tap features using the built-in SDK tests library."""

import datetime

from singer_sdk.testing import SuiteConfig, get_tap_test_class

from tap_instantly_ai.tap import TapInstantlyAI

SAMPLE_CONFIG = {
    "start_date": datetime.datetime.now().strftime("%Y-%m-%d"),
}

TEST_SUITE_CONFIG = SuiteConfig(
    ignore_no_records_for_streams=["analytics_campaign_count"]
)

# Run standard built-in tap tests from the SDK:
TestTapInstantlyAI = get_tap_test_class(
    tap_class=TapInstantlyAI,
    config=SAMPLE_CONFIG,
    suite_config=TEST_SUITE_CONFIG,
)

