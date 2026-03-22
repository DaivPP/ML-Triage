# ML Assisted Triage System

An AI-powered emergency triage web application that analyzes patient vital signs and symptoms to classify cases as **Non-Urgent**, **Urgent**, or **Critical** — helping healthcare teams prioritize response in emergency or hostile environments.

Built as a Final Year Project using **Scikit-learn**, **Flask**, and deployed on **Vercel**.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Input Parameters](#input-parameters)
- [Triage Classification](#triage-classification)
- [Local Setup](#local-setup)
- [Deployment on Vercel](#deployment-on-vercel)
- [Disclaimer](#disclaimer)

---

## Overview

This system is designed for use in scenarios where rapid patient prioritization is critical — such as remote emergencies, disaster response, or situations where a medical professional is not immediately available. It accepts either **precise vital sign readings** (from a device) or **observed/felt descriptions** (e.g. "breathing fast", "skin feels cold") and returns a triage level with a confidence score.

---

## Features

- **Dual input modes** — precise numeric readings or plain-language observed descriptions for each vital sign
- **ML-powered prediction** — trained Random Forest classifier with probability-based confidence scoring
- **Three triage levels** — Non-Urgent, Urgent, and Critical with color-coded results
- **Doctor consultation link** — shown automatically for Urgent and Critical cases
- **Dark / Light mode** — toggle with preference saved across sessions
- **Form validation** — catches missing or out-of-range values before submission
- **Responsive design** — works on desktop and mobile

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Python, Flask |
| ML Model | Scikit-learn (Random Forest Classifier) |
| Data Scaling | Scikit-learn StandardScaler |
| Deployment | Vercel |
| Fonts | Rajdhani, Inter, Share Tech Mono (Google Fonts) |

---

## Project Structure

```
your-repo/
├── app.py                  # Flask backend & /predict endpoint
├── triage_model.pkl        # Trained ML model (Random Forest)
├── scaler.pkl              # Fitted StandardScaler for numeric features
├── requirements.txt        # Python dependencies
├── vercel.json             # Vercel deployment configuration
├── templates/
│   └── index.html          # Main frontend UI
└── static/
    ├── drone.mp4.mp4       # Background video
    └── logo197.png         # Logo image
```

---

## How It Works

1. The user enters patient information via the web form — either using the **Observed / Feel** dropdowns or **Precise Readings** number inputs.
2. The frontend sends a `POST` request to `/predict` with all 12 features as JSON.
3. The Flask backend scales the 6 continuous vitals using the pre-fitted `scaler.pkl`, then runs inference using `triage_model.pkl`.
4. The model returns a predicted triage class and probability scores. The highest probability is shown as the confidence percentage.
5. The result is displayed on the page with the appropriate urgency color and recommended action.

```
User Form  →  POST /predict (JSON)  →  Scaler  →  ML Model  →  Triage Label + Confidence  →  UI
```

---

## Input Parameters

### Patient Information

| Field | Type | Description |
|---|---|---|
| `age` | Number | Patient age in years (0–120) |

### Vital Signs (Numeric)

| Field | Normal Range | Description |
|---|---|---|
| `heart_rate` | 60–100 bpm | Heart rate in beats per minute |
| `spo2` | 95–100% | Blood oxygen saturation |
| `systolic_bp` | 90–120 mmHg | Systolic blood pressure |
| `respiratory_rate` | 12–20 br/min | Breathing rate per minute |
| `temperature` | 36–37 °C | Body temperature in Celsius |

### Symptoms & Conditions (Binary: 0 or 1)

| Field | Description |
|---|---|
| `chest_pain` | Patient reports chest pain |
| `shortness_of_breath` | Difficulty breathing observed |
| `severe_bleeding` | Active severe bleeding present |
| `loss_of_consciousness` | Patient is or was unconscious |
| `diabetes` | Known diabetic |
| `heart_disease` | Known heart condition |

### Observed Mode — Dropdown Mappings

When precise readings are unavailable, the dropdowns map descriptions to representative values:

**Heart Rate**
| Option | Value Sent |
|---|---|
| Dangerously Slow | 38 bpm |
| Slow / Weak | 52 bpm |
| Normal | 80 bpm |
| Fast / Racing | 115 bpm |
| Very Fast / Pounding | 150 bpm |

**Temperature**
| Option | Value Sent |
|---|---|
| Dangerously Cold (Hypothermia) | 32 °C |
| Cold — Shivering | 35 °C |
| Normal | 36.6 °C |
| Mild Fever | 38.3 °C |
| High Fever | 40 °C |
| Dangerous Fever | 41.5 °C |

*(Similar mappings apply for SpO₂, Blood Pressure, and Breathing Rate)*

---

## Triage Classification

| Level | Color | Recommended Action |
|---|---|---|
| 🟢 Non-Urgent | Green | Monitor vitals, schedule follow-up |
| 🟠 Urgent | Orange | Teleconsultation within 30 minutes |
| 🔴 Critical | Red | Immediate intervention, drone dispatch |

---

## Local Setup

### Prerequisites

- Python 3.8+
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the Flask development server
python app.py
```

Then open `http://localhost:5000` in your browser.

> Make sure `triage_model.pkl` and `scaler.pkl` are present in the root directory before running.

---

## Deployment on Vercel

This project is configured for one-click deployment on Vercel via `vercel.json`.

### Steps

1. Push all files to your GitHub repository (including `vercel.json` and `requirements.txt`)
2. Go to [vercel.com](https://vercel.com) and click **Add New Project**
3. Import your GitHub repository
4. Vercel will auto-detect the configuration — click **Deploy**

### Required files for Vercel

| File | Purpose |
|---|---|
| `vercel.json` | Tells Vercel to use the Python runtime and route all traffic to `app.py` |
| `requirements.txt` | Lists all Python packages Vercel needs to install |

> ⚠️ **Size limit**: Vercel has a 250 MB deployment limit. Check your `.pkl` file sizes with `ls -lh *.pkl` before deploying.

### `vercel.json`

```json
{
  "version": 2,
  "builds": [{ "src": "app.py", "use": "@vercel/python" }],
  "routes": [{ "src": "/(.*)", "dest": "app.py" }]
}
```

### `requirements.txt`

```
flask
scikit-learn
pandas
numpy
joblib
```

---

## Disclaimer

> This system is intended as a **clinical decision support tool** only. It is **not a substitute for professional medical advice, diagnosis, or treatment**. Always consult a qualified healthcare professional for medical decisions.
