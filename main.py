from utils.config import config
from utils.logger import logger
from utils.data_manager import DataManager
from data_processing.contract_processor import ContractProcessor


def main():
    try:
        path_to_data = 'data/data.csv'
        output_path = 'data/contract_features.csv'
        data_manager = DataManager(logger=logger)

        df = data_manager.load_data(path_to_data)

        result_df = ContractProcessor(config=config,
                                      logger=logger).process_data(df)

        data_manager.save_data(result_df, output_path)
    except Exception as e:
        logger.error(f'Error in main process: {e}')
        raise


if __name__ == '__main__':
    main()
