# Draft Results

Initial evaluation shows that the anomaly detection pipeline is able to identify a small subset of user-day activity records as anomalous. The flagged records tend to include combinations of unusual login times, elevated file activity, and increased removable media usage.

At this stage, the model appears to successfully separate a minority of higher-risk behavioral patterns from the broader baseline of routine activity. Because this is an unsupervised approach, additional analysis is still needed to determine whether flagged records correspond to meaningful suspicious behavior or false positives.

Next steps include refining feature engineering, tuning the Isolation Forest contamination parameter, and comparing anomaly patterns across users to improve interpretability and reduce unnecessary alerts.