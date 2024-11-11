from dataclasses import dataclass
from typing import Set


@dataclass
class Config:
    """Configuration settings for feature calculations"""
    EXCLUDED_BANKS: Set[str] = frozenset({'LIZ', 'LOM', 'MKO', 'SUG'})
    DAYS_LOOKBACK: int = 180
    DEFAULT_NO_CLAIMS: int = -3
    DEFAULT_NO_LOANS: int = -1
    DEFAULT_ERROR: str = 'ERROR'
    MIN_VALID_AMOUNT: float = 0.0

    @classmethod
    def is_valid_bank(cls, bank: str) -> bool:
        """Check if a bank is valid"""
        return bank and bank not in cls.EXCLUDED_BANKS

    @classmethod
    def is_valid_amount(cls, amount: float) -> bool:
        """Check if an amount is valid"""
        return amount >= cls.MIN_VALID_AMOUNT


config = Config()
