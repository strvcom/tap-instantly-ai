"""Tests standard tap features using the built-in SDK tests library."""


from singer_sdk.testing import get_tap_test_class

from tap_instantly_ai.tap import TapInstantlyAI

SAMPLE_CONFIG = {
    "start_date": "2024-01-01",
}

# Run standard built-in tap tests from the SDK:
TestTapInstantlyAI = get_tap_test_class(
    tap_class=TapInstantlyAI,
    config=SAMPLE_CONFIG,
)

