import logging
from collections import Counter
import pandas as pd
from datetime import timedelta
from utils.types import Contracts


class FeatureCalculator:
    def __init__(
            self,
            contracts: Contracts,
            application_date: str,
            config,
            logger: logging.Logger
    ):
        self.contracts = contracts
        self.application_date = pd.to_datetime(application_date).tz_localize(
            None)
        self.config = config
        self.logger = logger

    def calculate_tot_claim_cnt_l180d(self) -> int:
        """Calculate the number of claims for last 180 days"""
        if not self.contracts:
            return self.config.DEFAULT_NO_CLAIMS

        try:
            app_date = pd.to_datetime(self.application_date).tz_localize(None)
            cutoff_date = app_date - timedelta(days=self.config.DAYS_LOOKBACK)

            claim_count = 0
            for contract in self.contracts:
                claim_date = contract.get('claim_date')
                if claim_date:
                    claim_date = pd.to_datetime(claim_date, format='%d.%m.%Y')
                    if cutoff_date <= claim_date <= app_date:
                        claim_count += 1

            return claim_count
        except (ValueError, pd.errors.OutOfBoundsDatetime) as e:
            self.logger.error(f'Error calculating claim count: {e}')
            return self.config.DEFAULT_ERROR

    def calculate_disb_bank_loan_wo_tbc(self) -> float:
        """Calculate the sum of exposure of loans without TBC loans"""
        if not self.contracts:
            return self.config.DEFAULT_NO_CLAIMS

        total_exposure = 0
        has_loans = False

        for contract in self.contracts:
            bank = contract.get('bank')
            loan_summa = contract.get('loan_summa')
            contract_date = contract.get('contract_date')

            if self.config.is_valid_bank(bank) and contract_date:
                has_loans = True
                if loan_summa and loan_summa != '':
                    try:
                        amount = float(loan_summa)
                        if self.config.is_valid_amount(amount):
                            total_exposure += amount
                    except:
                        continue

        return total_exposure if has_loans else self.config.DEFAULT_NO_LOANS

    def calculate_day_sinlastloan(self) -> int:
        """Calculate the number of days since last loan."""
        if not self.contracts:
            return self.config.DEFAULT_NO_CLAIMS

        try:
            app_date = pd.to_datetime(self.application_date).tz_localize(None)
            latest_loan_date = None
            has_loans = False

            for contract in self.contracts:
                contract_date = contract.get('contract_date')
                summa = contract.get('summa')

                if contract_date and summa and summa != '':
                    has_loans = True
                    loan_date = pd.to_datetime(contract_date,
                                               format='%d.%m.%Y')
                    if latest_loan_date is None or loan_date > latest_loan_date:
                        latest_loan_date = loan_date

            if not has_loans:
                return self.config.DEFAULT_NO_LOANS

            return (app_date - latest_loan_date).days

        except (ValueError, pd.errors.OutOfBoundsDatetime) as e:
            self.logger.error(f'Error calculating days since last loan: {e}')
            return self.config.DEFAULT_ERROR

    def calculate_most_frequent_bank(self) -> str:
        """Calculate the most frequently occurring bank"""
        if not self.contracts:
            return 'NONE'

        bank_counts = Counter(
            contract.get('bank') for contract in self.contracts
            if contract.get('bank')
        )

        if not bank_counts:
            return 'NONE'

        return bank_counts.most_common(1)[0][0]

    def calculate_avg_loan_amount(self) -> float:
        """Calculate average loan amount"""
        if not self.contracts:
            return self.config.DEFAULT_NO_CLAIMS

        amounts = []
        for contract in self.contracts:
            summa = contract.get('summa')
            if summa and summa != '':
                try:
                    amount = float(summa)
                    if self.config.is_valid_amount(amount):
                        amounts.append(amount)
                except:
                    continue

        return sum(amounts) / len(
            amounts) if amounts else self.config.DEFAULT_NO_LOANS
