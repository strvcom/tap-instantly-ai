"""Stream type classes for tap-instantly-ai."""

from __future__ import annotations

import sys
import typing as t
import datetime

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_instantly_ai.client import InstantlyAIStream
from singer_sdk.pagination import BaseOffsetPaginator

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources


SCHEMAS_DIR = importlib_resources.files(__package__) / "schemas"


class CampaignsStream(InstantlyAIStream):
    """Campaigns stream."""

    name = "campaigns"
    path = "/v1/campaign/list"
    primary_key = "id"
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "campaigns.json"

    def get_new_paginator(self) -> BaseOffsetPaginator:
        """Create a new pagination helper instance."""
        return BaseOffsetPaginator(start_value=0, page_size=100)
    
    def get_url_params(
        self,
        context: dict | None,
        next_page_token: str | None,
    ) -> dict[str, t.Any]:
        """Get URL query parameters.

        Args:
            context: Stream sync context.
            next_page_token: Next offset.

        Returns:
            A dictionary of URL query parameters.
        """
        params = {}
        if next_page_token:
            params["skip"] = next_page_token

        return params
    
    def get_child_context(
        self,
        record: dict,
        context: dict | None,  # noqa: ARG002
    ) -> dict | None:
        """Return a context object for child streams.

        Args:
            record: A record from this stream.
            context: The stream sync context.

        Returns:
            A context object for child streams.
        """
        return {
            "campaign_id": record["id"],
        }

    
class CampaignStatusStream(InstantlyAIStream):
    """Campaign Status stream."""

    name = "campaign_status"
    path = "/v1/campaign/get/status"
    parent_stream_type = CampaignsStream
    schema_filepath = SCHEMAS_DIR / "campaign_status.json"

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: int | None,
    ) -> dict[str, t.Any]:
        """Get URL query parameters.

        Args:
            context: Stream sync context.
            next_page_token: Value used to retrieve next page.

        Returns:
            Dictionary of URL query parameters.
        """
        params = {}
        campaign_id = context.get("campaign_id")
        if campaign_id:
            params["campaign_id"] = campaign_id
        return params

class AnalyticsCampaignSummaryStream(InstantlyAIStream):
    """Analytics Campaign Summary stream."""

    name = "analytics_campaign_summary"
    path = "/v1/analytics/campaign/summary"
    parent_stream_type = CampaignsStream
    schema_filepath = SCHEMAS_DIR / "analytics_campaign_summary.json"

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: int | None,
    ) -> dict[str, t.Any]:
        """Get URL query parameters.

        Args:
            context: Stream sync context.
            next_page_token: Value used to retrieve next page.

        Returns:
            Dictionary of URL query parameters.
        """
        params = {}
        campaign_id = context.get("campaign_id")
        if campaign_id:
            params["campaign_id"] = campaign_id
        return params
    

class AnalyticsCampaignCountStream(InstantlyAIStream):
    """Analytics Campaign Count stream."""

    name = "analytics_campaign_count"
    path = "/v1/analytics/campaign/count"
    schema_filepath = SCHEMAS_DIR / "analytics_campaign_count.json"

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: int | None,
    ) -> dict[str, t.Any]:
        """Get URL query parameters.

        Args:
            context: Stream sync context.
            next_page_token: Value used to retrieve next page.

        Returns:
            Dictionary of URL query parameters.
        """
        params = {}
        params["start_date"] = datetime.datetime.now().strftime("%Y-%m-%d")

        return params
    
    def post_process(
        self,
        row: dict,
        context: dict | None = None,  # noqa: ARG002
    ) -> dict | None:
        """Post-process a row of data.

        Args:
            row: An individual record from the stream.
            context: The stream context.

        Returns:
            The updated record dictionary, or ``None`` to skip the record.
        """
        updated_row = super().post_process(row, context)
        updated_row["start_date"] = datetime.datetime.now().strftime("%Y-%m-%d")

        return updated_row
