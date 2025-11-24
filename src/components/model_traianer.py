from imblearn.over_sampling import SMOTE
from sklearn.metrics import accuracy_score

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression

from sklearn.model_selection import GridSearchCV

import os
import sys
import pickle
from dataclasses import dataclass

from src.exception import Heart
from src.logger import logging


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_training(self, x_train, y_train, x_test, y_test):
        try:
            logging.info("Applying SMOTE to balance dataset")

            smote = SMOTE(random_state=42)
            x_train, y_train = smote.fit_resample(x_train, y_train)

            logging.info(f"Training data after SMOTE: {x_train.shape}, {y_train.shape}")

            # ============ HYPERPARAMETER TUNING ============= #

            param_grid = {
                "Logistic Regression": {
                    "model": LogisticRegression(),
                    "params": {
                        "max_iter": [200, 500, 800],
                        "C": [0.1, 1, 5, 10],
                        "solver": ["liblinear", "lbfgs"]
                    }
                },

                "Decision Tree": {
                    "model": DecisionTreeClassifier(),
                    "params": {
                        "criterion": ["gini", "entropy"],
                        "max_depth": [3, 5, 10, None],
                        "min_samples_split": [2, 5, 10]
                    }
                },

                "Random Forest": {
                    "model": RandomForestClassifier(),
                    "params": {
                        "n_estimators": [100, 200, 300],
                        "max_depth": [5, 10, 20, None],
                        "min_samples_split": [2, 5],
                        "min_samples_leaf": [1, 2]
                    }
                }
            }

            best_model = None
            best_score = 0
            best_model_name = None

            # Iterate through models
            for name, mp in param_grid.items():
                logging.info(f"Tuning hyperparameters for: {name}")

                grid = GridSearchCV(mp["model"], mp["params"], cv=5, scoring="accuracy", n_jobs=-1)
                grid.fit(x_train, y_train)

                best_params = grid.best_params_
                best_grid_model = grid.best_estimator_

                logging.info(f"Best Params for {name}: {best_params}")

                y_pred = best_grid_model.predict(x_test)
                score = accuracy_score(y_test, y_pred)

                logging.info(f"{name} Accuracy after tuning: {score}")

                if score > best_score:
                    best_score = score
                    best_model = best_grid_model
                    best_model_name = name

            # Save best model
            os.makedirs(os.path.dirname(self.model_trainer_config.trained_model_file_path), exist_ok=True)
            with open(self.model_trainer_config.trained_model_file_path, "wb") as f:
                pickle.dump(best_model, f)

            logging.info("Best model saved successfully after hyperparameter tuning.")

            return best_model_name, best_score

        except Exception as e:
            raise Heart(e, sys) from e
