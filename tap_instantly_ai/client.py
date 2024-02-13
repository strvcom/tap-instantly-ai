"""REST client handling, including InstantlyAIStream base class."""

from __future__ import annotations

import datetime
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.streams import RESTStream


class InstantlyAIStream(RESTStream):
    """InstantlyAI stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return "https://api.instantly.ai/api"

    records_jsonpath = "$[*]"

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="api_key",
            value=self.config.get("api_key"),
            location="params",
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")

        return headers

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
        row["downloaded_at"] = datetime.datetime.now().isoformat()

        return row
