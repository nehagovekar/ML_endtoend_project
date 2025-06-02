import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

# Add parent directories to path to access src modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.extend([current_dir, parent_dir, grandparent_dir])

try:
    from exception import CustomException
    from logger import logging
except ImportError:
    # Fallback to basic logging if custom modules not found
    import logging
    logging.basicConfig(level=logging.INFO)
    
    class CustomException(Exception):
        def __init__(self, error_message, error_detail):
            super().__init__(error_message)
            self.error_message = error_message

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', "train.csv")
    test_data_path: str = os.path.join('artifacts', "test.csv")
    raw_data_path: str = os.path.join('artifacts', "data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            # Try different possible paths for the data file
            possible_paths = [
                'notebook/data/stud.csv',
                '../../notebook/data/stud.csv',
                os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'notebook', 'data', 'stud.csv')
            ]
            
            df = None
            for path in possible_paths:
                if os.path.exists(path):
                    df = pd.read_csv(path)
                    logging.info(f"Successfully read data from: {path}")
                    break
            
            if df is None:
                raise FileNotFoundError("Could not find stud.csv in any expected location")
            
            logging.info(f"Read dataframe with shape: {df.shape}")
            
            # Create artifacts directory if it doesn't exist
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            
            # Save raw data
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            
            logging.info("Train Test Split Initiated")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            
            # Save train and test sets
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            
            logging.info("Ingestion of the data completed")
            
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            logging.error(f"Error in data ingestion: {str(e)}")
            raise CustomException(e, sys)

if __name__ == "__main__":
    try:
        obj = DataIngestion()
        train_data, test_data = obj.initiate_data_ingestion()
        print(f"Train data saved to: {train_data}")
        print(f"Test data saved to: {test_data}")
    except Exception as e:
        print(f"Error: {e}")