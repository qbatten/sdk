"""Tests discovery features for Parquet."""

import json
from pathlib import Path
from typing import Optional

from singer_sdk.samples.sample_tap_gitlab.gitlab_tap import SampleTapGitlab

CONFIG_FILE = "singer_sdk/tests/.secrets/gitlab-config.json"


def test_gitlab_tap_discovery():
    """Test class creation."""
    config: Optional[dict] = None
    if Path(CONFIG_FILE).exists():
        config = json.loads(Path(CONFIG_FILE).read_text())
    tap = SampleTapGitlab(config=config, state=None)
    catalog_json = tap.run_discovery()
    assert catalog_json

def test_gitlab_replication_keys():
    stream_name = "issues"
    expected_replication_key = "updated_at"
    config: Optional[dict] = None
    if Path(CONFIG_FILE).exists():
        config = json.loads(Path(CONFIG_FILE).read_text())
    tap = SampleTapGitlab(config=config, state=None)
    catalog = json.loads(tap.get_catalog_json())
    catalog_entries = catalog["streams"]
    for catalog_entry in [c for c in catalog_entries if c["stream"] == stream_name]:
        metadata_root = [md for md in catalog_entry["metadata"] if md["breadcrumb"] == []][0]
        key_props_1 = metadata_root["metadata"].get("valid-replication-keys")[0]
        key_props_2 = catalog_entry.get("replication_key")
        assert key_props_1 == expected_replication_key, (
            f"Incorrect 'valid-replication-keys' in catalog: ({key_props_1})\n\nRoot metadata was: {metadata_root}\n\nCatalog entry was: {catalog_entry}"
            )
        assert key_props_2 == expected_replication_key, (
            f"Incorrect 'replication_key' in catalog: ({key_props_2})\n\nCatalog entry was: {catalog_entry}"
            )
