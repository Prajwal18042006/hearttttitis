from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_traianer import ModelTrainer

if __name__ == "__main__":
    # INGESTION
    ingestion = DataIngestion()
    train_path, test_path = ingestion.initiate_data_ingestion()

    # TRANSFORMATION
    transform = DataTransformation()
    x_train, x_test, y_train, y_test, _ = transform.initiate_data_transformation(train_path, test_path)

    # TRAINER
    trainer = ModelTrainer()
    best_model, best_score = trainer.initiate_model_training(
        x_train,
        y_train,
        x_test,
        y_test
    )

    print("Best Model:", best_model)
    print("Best Accuracy:", best_score)
