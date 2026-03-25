# 🚀 MLOps Batch Signal Pipeline

## 📌 Overview

This project implements a **minimal MLOps-style batch pipeline** in Python.

It demonstrates:

* ✅ Reproducibility (config + seed)
* ✅ Observability (logs + metrics)
* ✅ Deployment readiness (Dockerized)

The pipeline processes OHLCV data and generates a **binary trading signal** based on a rolling mean.

---
## ⚙️ How It Works

1. Load configuration from YAML
2. Read dataset (`data.csv`)
3. Compute rolling mean on `close`
4. Generate signal:

   * `1` → close > rolling_mean
   * `0` → otherwise
5. Output:

   * `metrics.json` (structured metrics)
   * `run.log` (detailed logs)

---

## 📂 Project Structure

```
mlops-task/
├── run.py
├── config.yaml
├── data.csv
├── requirements.txt
├── Dockerfile
├── README.md
├── metrics.json
├── run.log
```

---

## 🚀 Run Locally

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Run the pipeline

```
python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log
```

---

## 🐳 Run with Docker

### Build image

```
docker build -t mlops-task .
```

### Run container

```
docker run --rm mlops-task
```

---

## 📊 Example Output (`metrics.json`)

```
{
  "version": "v1",
  "rows_processed": 9996,
  "metric": "signal_rate",
  "value": 0.4987,
  "latency_ms": 120,
  "seed": 42,
  "status": "success"
}
```

---

## 📜 Logging (`run.log`)

Logs include:

* Job start/end timestamps
* Config validation
* Data loading info
* Processing steps
* Metrics summary
* Error handling (if any)

---

## 🧪 Error Handling

The pipeline safely handles:

* Missing files
* Invalid CSV format
* Empty dataset
* Missing `close` column
* Invalid config

On failure, `metrics.json` is still generated:

```
{
  "version": "v1",
  "status": "error",
  "error_message": "Description of error"
}
```

---

## 🎯 Key Features

* Deterministic execution using seed
* Robust CSV parsing (handles malformed files)
* Clean logging and observability
* CLI-based execution (no hardcoded paths)
* Dockerized for reproducibility

---

## 🧠 Engineering Highlights

This project simulates a **real-world ML pipeline**:

* Handles messy data ingestion
* Enforces schema consistency
* Produces machine-readable metrics
* Designed for batch processing systems



Designed with production ML pipelines in mind, similar to real-world **trading signal systems**.
