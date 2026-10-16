# AI-Based Email Phishing & Fraud Detection

Final-year graduation project. Detects phishing and fraudulent emails from
their text using three supervised classifiers: Random Forest, Support Vector
Machine, and Naive Bayes.

## Alignment With the Official Proposal

| Proposal Item | Implementation |
|---------------|----------------|
| Random Forest, SVM, Naive Bayes | `src/models.py` |
| NLTK / NLP techniques | `src/preprocessing.py` + `src/nltk_setup.py` |
| TF-IDF | `src/features.py` |
| Jupyter Notebook for experiments | `notebooks/01_experiment.ipynb` |
| Database design (Member 2) | `database/schema.sql` + `database/db.py` (SQLite) |
| Email characteristics | `src/features.py` (signals + TF-IDF) |
| Accuracy / Precision / Recall / F1 | `src/evaluation.py` |
| Interactive prototype (Streamlit) | `app.py` + `views/` |
| Model comparison | `views/comparison.py` |
| Error analysis | `src/error_analysis.py` + `views/errors.py` |
| 7 project stages | This README |
| 6 members tasks | `views/members.py` |

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install --only-binary=:all: -r requirements.txt
python -m src.nltk_setup
python download_data.py
python -m src.training
streamlit run app.py
```

## Project Stages (from Proposal)

1. Requirements and Project Analysis
2. Dataset Collection and Preparation
3. Data Preprocessing and Feature Extraction
4. AI Model Development
5. Model Training and Evaluation
6. System Development and Integration
7. Testing, Comparison, and Documentation

## Group Members (from Proposal)

1. RAYAN ABDULRAHMAN IBRAHIM ALHIRABI
2. ALI ASAAD A ALSUWAYRI
3. ABDULELAH FAHAD HAJRS ALOTAIBI
4. HUSSAM MOHAMMED ALMUTAIRI
5. Faisal Turki Mohammed Alshebaiki
6. FAHAD MUSAAD ALOTAIBI

## Supervisor

DR. FAHAD ALOTAIBI
