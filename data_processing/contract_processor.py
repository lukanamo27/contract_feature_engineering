import pandas as pd
from data_processing.feature_calculator import FeatureCalculator
from utils.types import Contracts
import json
import logging

class ContractProcessor:
    def __init__(self, config, logger: logging.Logger):
        self.config = config
        self.logger = logger

    def parse_contracts(self, contracts_str: str) -> Contracts:
        """Parse json string containing contact information"""
        if not contracts_str or pd.isna(contracts_str):
            return []
        try:
            contracts = json.loads(contracts_str)
            if isinstance(contracts, dict):
                return [contracts]
            return contracts if isinstance(contracts, list) else []
        except json.JSONDecodeError as e:
            self.logger.error(f'Failed to parse contracts json: {e}')
            return []

    def calculate_features(self, row: pd.Series) -> dict[str, int | float]:
        """Calculate features for a single row of data"""
        try:
            contracts = self.parse_contracts(row['contracts'])
            calculator = FeatureCalculator(
                contracts,
                row['application_date'],
                self.config,
                self.logger
            )
            return {
                'tot_claim_cnt_l180d': calculator.calculate_tot_claim_cnt_l180d(),
                'disb_bank_loan_wo_tbc': calculator.calculate_disb_bank_loan_wo_tbc(),
                'day_sinlastloan': calculator.calculate_day_sinlastloan(),
                'most_frequent_bank': calculator.calculate_most_frequent_bank(),
                'avg_loan_amount': calculator.calculate_avg_loan_amount()
            }
        except Exception as e:
            self.logger.error(
                f'Error calculating features for id {row.get("id", "unknown")}: {e}')
            return {
                'tot_claim_cnt_l180d': self.config.DEFAULT_ERROR,
                'disb_bank_loan_wo_tbc': self.config.DEFAULT_ERROR,
                'day_sinlastloan': self.config.DEFAULT_ERROR,
                'most_frequent_bank': self.config.DEFAULT_ERROR,
                'avg_loan_amount': self.config.DEFAULT_ERROR
            }

    def process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process the input dataframe and calculate features"""
        output_df = df[['id', 'application_date']].copy()
        try:
            features = df.apply(self.calculate_features, axis=1)
            features_df = pd.DataFrame(features.tolist())
            output_df = pd.concat([output_df, features_df], axis=1)

            self.logger.info(f'Successfully processed {len(df)} rows')
            return output_df
        except Exception as e:
            self.logger.error(f'Error processing data: {e}')
            raise
