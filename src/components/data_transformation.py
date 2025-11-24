import os
import sys
import pickle

from dataclasses import dataclass
import pandas as pd
import numpy as np

from src.exception import Heart
from src.logger import logging

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join("artifacts", "preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_transformet_obj(self, numerical_features):
        """
        Preprocessor for numerical features only.
        """
        try:
            logging.info("Creating numerical pipeline for preprocessing")

            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )

            preprocessor = ColumnTransformer(
                transformers=[
                    ("numerical", num_pipeline, numerical_features)
                ]
            )

            return preprocessor

        except Exception as e:
            raise Heart(e, sys) from e

    def initiate_data_transformation(self, train_path, test_path):
        try:
            logging.info("Reading train and test datasets")

            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            target_column = "condition"

            # Split X and Y
            x_train = train_df.drop(columns=[target_column])
            y_train = train_df[target_column]

            x_test = test_df.drop(columns=[target_column])
            y_test = test_df[target_column]

            # Only numerical features
            numerical_features = x_train.columns.tolist()

            preprocessor = self.get_transformet_obj(numerical_features)

            logging.info("Fitting preprocessor on training data")

            preprocessor_obj = preprocessor.fit(x_train)

            logging.info("Transforming datasets")
            x_train_transformed = preprocessor_obj.transform(x_train)
            x_test_transformed = preprocessor_obj.transform(x_test)

            # Save preprocessor.pkl
            path = self.data_transformation_config.preprocessor_obj_file_path
            os.makedirs(os.path.dirname(path), exist_ok=True)

            with open(path, "wb") as f:
                pickle.dump(preprocessor_obj, f)

            logging.info("Data transformation completed. Preprocessor saved successfully.")

            return (
                x_train_transformed,
                x_test_transformed,
                y_train,
                y_test,
                path
            )

        except Exception as e:
            raise Heart(e, sys) from e
if __name__ == "__main__":
    obj = DataTransformation()
    train = "artifacts/train.csv"
    test = "artifacts/test.csv"
    output = obj.initiate_data_transformation(train, test)
    print("Data Transformation Completed")
    print(output)
