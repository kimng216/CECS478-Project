import pandas as pd
import pytest

from src.pipeline import build_features, detect_anomalies


def test_build_features_happy_path():
    logon = pd.DataFrame(
        {
            "date": ["01/02/2010 08:00:00", "01/02/2010 20:00:00"],
            "user": ["U1", "U1"],
            "pc": ["PC-1", "PC-1"],
            "activity": ["Logon", "Logon"],
        }
    )

    file_df = pd.DataFrame(
        {
            "date": ["01/02/2010 09:00:00"],
            "user": ["U1"],
            "pc": ["PC-1"],
            "filename": ["file1.txt"],
            "activity": ["File Open"],
            "to_removable_media": [False],
            "from_removable_media": [False],
            "content": ["x"],
        }
    )

    device = pd.DataFrame(
        {
            "date": ["01/02/2010 10:00:00"],
            "user": ["U1"],
            "pc": ["PC-1"],
            "file_tree": ["R:\\"],
            "activity": ["Connect"],
        }
    )

    features = build_features(logon, file_df, device)

    assert not features.empty
    assert "logon_count" in features.columns
    assert "file_event_count" in features.columns
    assert "device_event_count" in features.columns


def test_detect_anomalies_negative_empty_input():
    features = pd.DataFrame(
        columns=[
            "logon_count",
            "unique_pcs",
            "after_hours_logons",
            "file_event_count",
            "to_removable_count",
            "from_removable_count",
            "device_event_count",
            "device_connect_count",
        ]
    )

    with pytest.raises(ValueError):
        detect_anomalies(features)


def test_build_features_missing_required_column():
    logon = pd.DataFrame(
        {
            "date": ["01/02/2010 08:00:00"],
            "user": ["U1"],
            "activity": ["Logon"],
        }
    )

    file_df = pd.DataFrame(
        {
            "date": ["01/02/2010 09:00:00"],
            "user": ["U1"],
            "pc": ["PC-1"],
            "filename": ["file1.txt"],
            "activity": ["File Open"],
            "to_removable_media": [False],
            "from_removable_media": [False],
            "content": ["x"],
        }
    )

    device = pd.DataFrame(
        {
            "date": ["01/02/2010 10:00:00"],
            "user": ["U1"],
            "pc": ["PC-1"],
            "file_tree": ["R:\\"],
            "activity": ["Connect"],
        }
    )

    with pytest.raises(KeyError):
        build_features(logon, file_df, device)


def test_build_features_invalid_dates():
    logon = pd.DataFrame(
        {
            "date": ["not-a-date"],
            "user": ["U1"],
            "pc": ["PC-1"],
            "activity": ["Logon"],
        }
    )

    file_df = pd.DataFrame(
        {
            "date": ["not-a-date"],
            "user": ["U1"],
            "pc": ["PC-1"],
            "filename": ["file1.txt"],
            "activity": ["File Open"],
            "to_removable_media": [False],
            "from_removable_media": [False],
            "content": ["x"],
        }
    )

    device = pd.DataFrame(
        {
            "date": ["not-a-date"],
            "user": ["U1"],
            "pc": ["PC-1"],
            "file_tree": ["R:\\"],
            "activity": ["Connect"],
        }
    )

    features = build_features(logon, file_df, device)
    assert isinstance(features, pd.DataFrame)