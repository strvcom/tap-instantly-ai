"""InstantlyAI tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th

from tap_instantly_ai import streams


class TapInstantlyAI(Tap):
    """InstantlyAI tap class."""

    name = "tap-instantly-ai"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
            required=True,
            secret=True,
            description="The API key to authenticate against the API service",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            required=True,
            description="The earliest record date to sync",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.InstantlyAIStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.CampaignsStream(self),
            streams.AnalyticsCampaignSummaryStream(self),
            streams.CampaignStatusStream(self),
            streams.AnalyticsCampaignCountStream(self),
        ]


if __name__ == "__main__":
    TapInstantlyAI.cli()
