# Dat-540-Prosjekt
Predicting Gallstone Disease from Clinical + Bioimpedance

## Project Overview

**Domain:** Healthcare | **Task:** Binary Classification | **Data:** Tabular

Predict gallstone status (Yes/No) from 38 features across 3 categories:
- **Demographics:** Age, sex, height, weight, BMI
- **Bioimpedance:** Total/extracellular/intracellular water, muscle/fat mass, protein, visceral fat area, hepatic fat
- **Laboratory values:** Glucose, lipids, AST/ALT/ALP, creatinine, GFR, CRP, hemoglobin, vitamin D

**Dataset:** 319 outpatients from Ankara VM Medical Park (June 2022–June 2023)  
**Target:** Gallstone Status (161 positive, 158 negative - balanced classes)  
**Quality:** No missing values, complete feature set

## Setup (Python environment)

1. Create and activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Upgrade pip and install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```