import logging
import os

import pandas as pd
from sklearn.ensemble import IsolationForest


ARTIFACT_DIR = "artifacts/release"
os.makedirs(ARTIFACT_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(ARTIFACT_DIR, "pipeline.log"),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logging.info("Starting pipeline")


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    logging.info("Loading CSV files")
    logon = pd.read_csv("data/raw/logon.csv")
    file_df = pd.read_csv("data/raw/file.csv")
    device = pd.read_csv("data/raw/device.csv")
    return logon, file_df, device


def build_features(
    logon: pd.DataFrame, file_df: pd.DataFrame, device: pd.DataFrame
) -> pd.DataFrame:
    logging.info("Building features")

    for df in [logon, file_df, device]:
        df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y %H:%M:%S", errors="coerce")
        df["day"] = df["date"].dt.date

    logon_events = logon[logon["activity"] == "Logon"].copy()
    logon_events["hour"] = logon_events["date"].dt.hour
    logon_events["after_hours"] = ((logon_events["hour"] < 6) | (logon_events["hour"] > 18)).astype(int)

    logon_features = (
        logon_events.groupby(["user", "day"])
        .agg(
            logon_count=("activity", "count"),
            unique_pcs=("pc", "nunique"),
            after_hours_logons=("after_hours", "sum"),
        )
        .reset_index()
    )

    file_features = (
        file_df.groupby(["user", "day"])
        .agg(
            file_event_count=("activity", "count"),
            to_removable_count=("to_removable_media", lambda x: (x == True).sum()),
            from_removable_count=("from_removable_media", lambda x: (x == True).sum()),
        )
        .reset_index()
    )

    device_features = (
        device.groupby(["user", "day"])
        .agg(
            device_event_count=("activity", "count"),
            device_connect_count=("activity", lambda x: (x == "Connect").sum()),
        )
        .reset_index()
    )

    features = logon_features.merge(file_features, on=["user", "day"], how="outer")
    features = features.merge(device_features, on=["user", "day"], how="outer")
    features = features.fillna(0)

    logging.info("Built feature table with %s rows", len(features))
    return features


def detect_anomalies(features: pd.DataFrame) -> pd.DataFrame:
    logging.info("Running Isolation Forest")

    numeric_cols = [
        "logon_count",
        "unique_pcs",
        "after_hours_logons",
        "file_event_count",
        "to_removable_count",
        "from_removable_count",
        "device_event_count",
        "device_connect_count",
    ]

    X = features[numeric_cols]

    model = IsolationForest(
        contamination=0.02,
        random_state=42,
    )
    model.fit(X)

    features["anomaly_score"] = model.decision_function(X)
    features["prediction"] = model.predict(X)
    features["is_anomaly"] = (features["prediction"] == -1).astype(int)

    logging.info("Detected %s anomalies", int(features["is_anomaly"].sum()))
    return features


def save_outputs(results: pd.DataFrame) -> None:
    logging.info("Saving outputs")

    alerts = results[results["is_anomaly"] == 1].copy()
    alerts.to_csv(os.path.join(ARTIFACT_DIR, "alerts.csv"), index=False)

    metrics = {
        "total_rows": int(len(results)),
        "total_alerts": int(results["is_anomaly"].sum()),
    }
    pd.DataFrame([metrics]).to_json(os.path.join(ARTIFACT_DIR, "metrics.json"), orient="records", indent=2)

    results.head(20).to_csv(os.path.join(ARTIFACT_DIR, "feature_preview.csv"), index=False)


def main() -> None:
    logon, file_df, device = load_data()
    features = build_features(logon, file_df, device)
    results = detect_anomalies(features)
    save_outputs(results)
    logging.info("Pipeline completed successfully")
    print("Pipeline complete. Outputs saved to artifacts/release/")


if __name__ == "__main__":
    main()