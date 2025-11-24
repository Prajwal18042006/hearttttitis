import os  
import sys 
import pandas as pd 
import numpy as np 
from src.logger import logging
from src.exception import Heart
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.model_traianer import ModelTrainerConfig
from src.components.model_traianer import ModelTrainer



@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")
    raw_data_path: str = os.path.join("artifacts", "raw.csv")


class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered data ingestion component")

        try:
            # Read dataset from data frame 
            df = pd.read_csv("notebook/data/heart_cleveland_upload.csv")
            logging.info("Dataset read successfully")

            # Create artifacts directory meaning creating a floder 
            os.makedirs(os.path.dirname(self.data_ingestion_config.train_data_path), exist_ok=True)

            # Save raw data for folder artifacts and file is created 
            df.to_csv(self.data_ingestion_config.raw_data_path, index=False, header=True)
            logging.info("Raw data saved")

            # Train-test split for folder name is artifacts and save it in to this  folder 
            logging.info("Initiating train-test split")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # Save train data
            train_set.to_csv(self.data_ingestion_config.train_data_path, index=False, header=True)

            # Save test data
            test_set.to_csv(self.data_ingestion_config.test_data_path, index=False, header=True)

            logging.info("Data ingestion completed successfully")

            return (
                self.data_ingestion_config.train_data_path,
                self.data_ingestion_config.test_data_path,
               
            )

        except Exception as e:
            raise Heart(e, sys)
if __name__=="__main__":
    obj=DataIngestion()
    obj.initiate_data_ingestion()
   