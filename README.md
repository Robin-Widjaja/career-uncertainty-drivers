# Career Uncertainty Drivers

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Identifying the key factors that drive young people's career uncertainty using the ASPIRES3 longitudinal dataset.**

![Project Banner](link-to-your-image-optional.png)

---

## 📌 Overview

This project investigates what makes young adults (ages 21‑22) anxious about their future careers. Using data from the **ASPIRES3 longitudinal study** (N = 7,635), I built and validated a regression model that explains **40.2% of the variance** in future concern (`CONCERN_R`). The goal is to provide **actionable insights for edtech companies** seeking to reduce student anxiety through targeted interventions.

**Key findings:**
- Mental health, job perceptions, and financial worry are the strongest actionable predictors
- COVID‑19's impact on aspirations is the single largest contributor
- Access to careers advice plays a significant role

---

## 📊 Dataset

- **Source:** ASPIRES3 – Young People's STEM Aspirations and Trajectories, Age 20‑22, 2020‑2023  
- **Provider:** UK Data Service (Study Number SN 9224)  
- **Sample:** 7,635 respondents in England, born 1998‑99  
- **Outcome variable:** `CONCERN_R` (reverse‑coded concern about future opportunities)

*Note: Due to data licensing, the raw dataset is not included in this repository. Instructions for access are provided below.*

---

## 🔧 Methods

### Data Cleaning & Preparation
- Replaced missing codes (`998`, `999`) with `NaN`
- Created numeric versions of categorical variables
- Engineered composite variables:
  - `mental_health`: average of PHQ2/GAD2 items (Cronbach's α = 0.89)
  - `job_perception`: average of job perception items (α = 0.55 – retained for model stability)

### Modeling
- **Linear regression** with backward elimination
- **Multicollinearity check:** VIF (all final VIFs < 1.6)
- **Validation:** 5‑fold cross‑validation (CV R² = 0.389 ± 0.03)

### Tools Used
- **Python:** pandas, numpy, statsmodels, scikit‑learn, matplotlib, seaborn, pingouin
- **Visualization:** Tableau Public (interactive dashboard)

---

## 📈 Key Results

| Metric | Value |
|--------|-------|
| **R²** | 0.402 |
| **Adjusted R²** | 0.399 |
| **Cross‑validated R²** | 0.389 ± 0.03 |
| **Sample size (final model)** | 3,049 |
| **Number of predictors** | 12 |
| **All VIFs** | < 1.6 |

### Final Model Coefficients

| Predictor | Coefficient | Interpretation |
|-----------|-------------|----------------|
| `COVID_ASP` | -0.28 | COVID impact → higher concern |
| `mental_health` | +0.18 | Higher distress → higher concern |
| `job_perception` | +0.16 | Worse job perceptions → higher concern |
| `PREV_PG_02` | +0.15 | Financial worry → higher concern |
| `NO_CAR_RES_01` | +0.13 | Study break → higher concern |
| `NO_CAR_RES_03` | +0.12 | Difficulty accessing careers advice → higher concern |
| `CONF_FUTJOB` | +0.09 | Lower career confidence → higher concern |
| `JOBPER7` | -0.10 | Needing more qualifications → higher concern |
| `BROAD` | -0.08 | Course choice reason → lower concern |
| `NO_CAR_RES_05` | -0.14 | Advice "not needed" → lower concern |
| `LIFESAT` | -0.05 | Higher life satisfaction → lower concern |
| `RIGHT_DEC_WORK` | +0.04 | Work decision regret → higher concern |

*All predictors significant at p < 0.05. See the full regression output in the [Jupyter notebook](notebooks/analysis.ipynb).*

---

## 🎯 Recommendations for EdTech

Based on the findings, edtech platforms can reduce student career anxiety by:

| Area | Action |
|------|--------|
| **Career confidence** | Success stories, skill‑building, clear pathways |
| **Job perceptions** | Transparent graduate outcomes, career exploration tools |
| **Mental health** | Well‑being resources, stress management |
| **Careers advice** | Reduce barriers, proactive outreach |
| **Financial concerns** | Highlight scholarships, earning potential info |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Required packages: `pip install -r requirements.txt`

## 📁 Repository Structure
├── README.md # Project overview and documentation
├── LICENSE # MIT License
├── requirements.txt # Python dependencies
├── data/ # Data files (not included – see access instructions)
│ └── .gitkeep # Placeholder for empty folder
├── notebooks/
│ └── aspire-3.ipynb # Main analysis notebook
├── scripts/
│ ├── data_cleaning.py # Data preparation functions
│ └── utils.py # Helper functions
├── outputs/
│ ├── figures/ # Generated plots
│ └── final_model_summary.csv
└── tableau/
└── aspires3_dashboard.twb # Tableau dashboard file
*Note: The `data/` folder is not included in the repository due to data licensing restrictions. See the [Dataset](#dataset) section for access instructions.*

### Accessing the Data
1. Register at [UK Data Service](https://ukdataservice.ac.uk/)
2. Apply for access to study **SN 9224** (ASPIRES3)
3. Place the downloaded files in the `data/` folder

### Running the Analysis
```bash
git clone https://github.com/robin-widjaja/career-uncertainty-drivers.git
cd career-uncertainty-drivers
pip install -r requirements.txt
jupyter notebook notebooks/aspire-3.ipynb


