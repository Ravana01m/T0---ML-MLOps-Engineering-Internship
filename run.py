import argparse
import json
import sys
import time
import logging
from pathlib import Path

import numpy as np
import pandas as pd
import yaml


# ---------- Logger ----------
def setup_logger(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


# ---------- CLI ----------
def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)

    return parser.parse_args()


# ---------- Metrics ----------
def write_metrics(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


# ---------- Config ----------
def load_config(path):
    try:
        with open(path) as f:
            config = yaml.safe_load(f)
    except:
        raise ValueError("Invalid config file")

    if not all(k in config for k in ["seed", "window", "version"]):
        raise ValueError("Config must contain seed, window, version")

    return config


# ---------- Data Loader (FINAL FIX) ----------
def load_data(path):
    try:
        df = pd.read_csv(path)
    except:
        raise ValueError("Invalid CSV")

    # 🔥 If file is broken (everything in one column)
    if len(df.columns) == 1:
        raw = df.iloc[:, 0]

        # split rows into columns
        df = raw.str.split(",", expand=True)

        # assign correct headers manually
        df.columns = [
            "timestamp", "open", "high", "low",
            "close", "volume_btc", "volume_usd"
        ]

    # normalize
    df.columns = df.columns.str.strip().str.lower()

    if "close" not in df.columns:
        raise ValueError(f"close column missing: {df.columns.tolist()}")

    # convert numeric safely
    df["close"] = pd.to_numeric(df["close"], errors="coerce")

    # remove bad rows
    df = df.dropna(subset=["close"])

    return df


# ---------- Main ----------
def main():
    args = parse_args()
    setup_logger(args.log_file)

    start = time.time()

    try:
        logging.info("Job started")

        config = load_config(args.config)
        np.random.seed(config["seed"])

        logging.info(f"Config loaded: {config}")

        df = load_data(args.input)
        logging.info(f"Rows loaded: {len(df)}")

        # Processing
        df["rolling_mean"] = df["close"].rolling(config["window"]).mean()
        df = df.dropna()

        df["signal"] = (df["close"] > df["rolling_mean"]).astype(int)

        # Metrics
        rows = len(df)
        signal_rate = df["signal"].mean()
        latency = int((time.time() - start) * 1000)

        metrics = {
            "version": config["version"],
            "rows_processed": rows,
            "metric": "signal_rate",
            "value": round(float(signal_rate), 4),
            "latency_ms": latency,
            "seed": config["seed"],
            "status": "success"
        }

        write_metrics(args.output, metrics)

        logging.info(f"Metrics: {metrics}")
        logging.info("Job completed")

        print(json.dumps(metrics, indent=4))
        return 0

    except Exception as e:
        error = {
            "version": "v1",
            "status": "error",
            "error_message": str(e)
        }

        write_metrics(args.output, error)

        logging.error(str(e))
        print(json.dumps(error, indent=4))

        return 1


if __name__ == "__main__":
    sys.exit(main())