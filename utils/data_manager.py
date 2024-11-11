import pandas as pd
from pathlib import Path
import logging


class DataManager:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def load_data(self, path_to_data: str) -> pd.DataFrame:
        """Load data from a csv file"""
        file_path = Path(path_to_data)
        if not file_path.exists():
            raise FileNotFoundError(f'Data file not found at {path_to_data}')

        try:
            df = pd.read_csv(path_to_data)
            self.logger.info(
                f'Successfully loaded {len(df)} rows from {path_to_data}')
            return df
        except pd.errors.EmptyDataError:
            self.logger.error(f'Empty file found at {path_to_data}')
            raise

    def save_data(self, df: pd.DataFrame, output_path: str):
        """Save dataframe to a csv file"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(output_path, index=False)
        self.logger.info(f'Successfully saved {len(df)} rows to {output_path}')

