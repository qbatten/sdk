"""Sample tap test for tap-google-analytics."""

import json
from pathlib import Path
from typing import List

from samples.sample_tap_google_analytics.ga_tap_stream import (
    GASimpleSampleStream,
    SampleGoogleAnalyticsStream,
)
from singer_sdk.tap_base import Tap
from singer_sdk.typing import PropertiesList, Property, StringType

REPORT_DEFS_FILE = (
    "samples/sample_tap_google_analytics/resources/default_report_definitions.json"
)
REPORT_DEFS = json.loads(Path(REPORT_DEFS_FILE).read_text())


class SampleTapGoogleAnalytics(Tap):
    """Sample tap for GoogleAnalytics."""

    name: str = "sample-tap-google-analytics"
    config_jsonschema = PropertiesList(
        Property("view_id", StringType(), required=True),
        Property(
            "client_email", StringType(), required=True, examples=["me@example.com"]
        ),
        Property("private_key", StringType(), required=True, secret=True),
    ).to_dict()

    def discover_streams(self) -> List[SampleGoogleAnalyticsStream]:
        """Return a list of all streams."""
        return [GASimpleSampleStream(tap=self)]
