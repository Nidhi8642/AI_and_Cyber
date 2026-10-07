# AI-Powered Cybersecurity Threat Detection & Response Platform

An AI-powered cybersecurity platform that ingests security logs, normalizes events, detects threats using rule-based and machine-learning techniques, generates alerts, provides SIEM-style monitoring, and assists analysts using RAG and Google Gemini.

## Overview

The platform combines traditional cybersecurity detection with machine learning and generative AI.

Security events flow through the following pipeline:

Security Data Sources
        ↓
Log Ingestion
        ↓
Parsing & Normalization
        ↓
Rule-Based Detection + ML Anomaly Detection
        ↓
Alert Generation
        ↓
SIEM Dashboard
        ↓
Investigation
        ↓
RAG Knowledge Retrieval
        ↓
Google Gemini Security Analysis
        ↓
Incident Response Workflow

## Key Features

### Log Ingestion & Normalization

- Accepts individual security logs and batches of logs.
- Parses raw security log fields.
- Converts raw events into a normalized `SecurityEvent` model.
- Validates timestamps and required fields.

### Rule-Based Threat Detection

Implemented detection rules for:

- Brute-force authentication attacks
- Privilege escalation

Alerts include:

- Unique alert ID
- Severity
- Detection reason
- Supporting evidence
- Alert status

### ML Anomaly Detection

Uses Scikit-learn's `IsolationForest` for anomaly detection.

The ML pipeline:

1. Extracts numerical features from security events.
2. Trains an Isolation Forest model.
3. Generates anomaly predictions.
4. Calculates anomaly and risk scores.
5. Converts detected anomalies into security alerts.

### SIEM Dashboard

The React dashboard provides:

- Total security events
- Open alerts
- Critical alerts
- ML anomalies
- Event severity analytics
- Alert severity analytics
- Event type distribution
- Recent security alerts
- Recent security events
- Severity and event-type filtering

### RAG Knowledge Base

The platform contains a cybersecurity knowledge base covering:

- Brute-force attacks
- Privilege escalation
- Authentication attacks
- Incident response

The RAG layer retrieves relevant knowledge based on the security event before AI analysis.

### AI Security Assistant

Google Gemini is integrated to assist security analysts with:

- Threat explanation
- Suspicious-event analysis
- Investigation steps
- Defensive recommendations
- Risk assessment

The assistant is designed to distinguish observed evidence from possible scenarios and does not perform destructive or irreversible actions.

### Incident Response

The incident response workflow covers:

1. Identify
2. Investigate
3. Correlate
4. Contain
5. Recover
6. Document

High-impact containment and recovery actions require human approval.

## Technology Stack

### Backend

- Python
- FastAPI
- Pydantic
- Uvicorn

### Machine Learning

- Scikit-learn
- Isolation Forest

### AI

- Google Gemini
- RAG-based knowledge retrieval

### Frontend

- React
- Vite

### Testing

- Pytest
- FastAPI TestClient

### Deployment

- Docker
- Docker Compose

## Project Structure

```text
AI_and_Cyber/
│
├── backend/
│   ├── app/
│   │   ├── detection/
│   │   │   ├── anomaly.py
│   │   │   ├── features.py
│   │   │   └── rules.py
│   │   │
│   │   ├── ingestion/
│   │   │   ├── parser.py
│   │   │   └── normalizer.py
│   │   │
│   │   ├── models/
│   │   │   └── schemas.py
│   │   │
│   │   ├── rag/
│   │   │   ├── ingest.py
│   │   │   └── retriever.py
│   │   │
│   │   ├── routes/
│   │   │   ├── events.py
│   │   │   ├── alerts.py
│   │   │   ├── ingestion.py
│   │   │   ├── dashboard.py
│   │   │   ├── rag.py
│   │   │   ├── assistant.py
│   │   │   └── incidents.py
│   │   │
│   │   ├── services/
│   │   │   ├── ingestion_service.py
│   │   │   ├── alert_service.py
│   │   │   ├── anomaly_service.py
│   │   │   ├── detection_service.py
│   │   │   ├── ml_alert_service.py
│   │   │   ├── dashboard_service.py
│   │   │   ├── ai_assistant_service.py
│   │   │   ├── alert_analysis_service.py
│   │   │   ├── gemini_service.py
│   │   │   └── incident_response_service.py
│   │   │
│   │   └── main.py
│   │
│   ├── knowledge_base/
│   ├── sample_data/
│   ├── tests/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   └── React/Vite dashboard
│
└── docker-compose.yml