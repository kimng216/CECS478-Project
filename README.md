# User Activity Monitoring and Anomaly Detection  

## Project Overview and Dataset  
This project addresses the problem of detecting abnormal user activity within enterprise systems by applying automated anomaly detection techniques to activity logs. By analyzing patterns such as login times, file access frequency, device usage, and more, the system aims to identify behavior that significantly deviates from established user baselines. Detecting such anomalies can help security analysts identify potential security risks, unauthorized access, or misuse of system resources. The goal of this project is to design and evaluate an automated system that identifies deviations from normal user behavior in enterprise activity logs using anomaly detection methods. The system will use Isolation Forest, an unsupervised anomaly detection method, to detect abnormal patterns in user activity logs.  

The project uses the [CERT Insider Threat Detection Dataset] (https://www.kaggle.com/datasets/mrajaxnp/cert-insider-threat-detection-research?resource=download) on Kaggle as the primary data source which contains simulated enterprise activity logs including user logins, file access events, device connections, email activity, and web browsing records.

Due to GitHub file size limitations, this repository includes reduced samples (3k–5k rows) of the dataset for testing and demonstration. The full dataset was used locally during development and evaluation.  

Required files (shortened files are in this Github, but for full file, please download from Kaggle):  
- logon.csv  
- file.csv  
- device.csv  

## Architecture
The system follows an end-to-end pipeline: ingest → detect → alert → summarize  
1. **Ingest**: load logon, file, and device activity logs  
2. **Detect**: extract behavioral features (login counts, file activity, device usage) & apply Isolation Forest to identify anomalies  
3. **Alert**: flag anomalous user-day activity  
4. **Summarize**: export alerts, metrics, logs, and evaluation artifacts  

## Run Instructions    
### Run with Docker (recommended)   
make up && make demo  

### Run Tests:  
make test  

### Artifacts  
The pipeline generates outputs in: artifacts/release/    

Example outputs:    
* alerts.csv — detected anomalies  
* metrics.json — summary statistics  
* pipeline.log — execution logs  
* feature_preview.csv — sample feature table  
* top_anomalies.csv — highest anomaly scores  
* anomaly_counts_by_user.csv — anomalies per user  
* anomalies_by_user.png — visualization  
* results.md — draft evaluation  

### Observability  
The system includes:
* logging of key pipeline steps  
* anomaly metrics export  
* structured output files for inspection and analysis  

### Security Evidence
* Input validation ensures required columns exist before processing  
* The system operates on structured CSV inputs only  
* Alerts are treated as indicators, not definitive proof of malicious behavior  
* Execution is containerized for reproducibility  
* Testing  

The project includes:  
* 1 happy-path test  
* multiple negative/edge-case tests  
* coverage reporting via pytest-cov  

Tests validate:  
* feature extraction
* anomaly detection
* handling of invalid or missing input
* What Works
* End-to-end anomaly detection pipeline
* Dockerized execution (make up && make demo)
* Automated testing with coverage
* Output artifacts for evaluation
* Initial anomaly detection results and visualizations