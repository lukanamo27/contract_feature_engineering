# Contract Feature Engineering

## Introduction
This project processes customer contract data to calculate various features for analysis. It takes a CSV file containing customer contract information in JSON format and generates derived features such as claim counts, loan amounts, and bank-related metrics.

## Features Calculated
The program calculates the following features from the contract data:

1. `tot_claim_cnt_l180d`: Total number of claims in the last 180 days
2. `disb_bank_loan_wo_tbc`: Sum of loan exposures excluding TBC loans
3. `day_sinlastloan`: Number of days since the last loan
4. `most_frequent_bank`: Most frequently occurring bank in customer's contracts
5. `avg_loan_amount`: Average loan amount across all contracts

## Setup and Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd contract_feature_engineering
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your input data file (`data.csv`) in the `data` directory
2. Run the main script:
```bash
python main.py
```
3. The processed features will be saved in `data/contract_features.csv`

## Input Data Format

The input CSV file (`data.csv`) should contain the following columns:
- `id`: Unique identifier for each record
- `application_date`: Date of application
- `contracts`: JSON string containing contract information

## Configuration

Key configurations can be modified in `utils/config.py`:
- `EXCLUDED_BANKS`: Set of bank codes to exclude from calculations
- `DAYS_LOOKBACK`: Number of days to look back for claim calculations
- `DEFAULT_NO_CLAIMS`: Default value when no claims exist
- `DEFAULT_NO_LOANS`: Default value when no loans exist
- `DEFAULT_ERROR`: Value to use in case of processing errors
- `MIN_VALID_AMOUNT`: Minimum valid amount for loan calculations
