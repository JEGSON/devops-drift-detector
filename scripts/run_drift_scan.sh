#!/bin/bash

# Configuration
PROJECT_DIR="/Users/wealth/devops-drift-detector"
LOG_FILE="$PROJECT_DIR/logs/cron.log"
PYTHON_EXEC="$PROJECT_DIR/.venv/bin/python"
SCRIPT="$PROJECT_DIR/enhanced_drift_detector.py"

# Ensure logs directory exists
mkdir -p "$PROJECT_DIR/logs"

# Timestamp
echo "----------------------------------------------------------------" >> "$LOG_FILE"
echo "Starting scan at $(date)" >> "$LOG_FILE"

# Run Detector
cd "$PROJECT_DIR" || exit 1
"$PYTHON_EXEC" "$SCRIPT" --environment dev --terraform-dir ./terraform/environments/dev >> "$LOG_FILE" 2>&1

EXIT_CODE=$?

echo "Scan finished at $(date) with exit code $EXIT_CODE" >> "$LOG_FILE"
echo "----------------------------------------------------------------" >> "$LOG_FILE"

exit $EXIT_CODE
