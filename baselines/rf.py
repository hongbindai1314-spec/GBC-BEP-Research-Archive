"""Reproduction entry point for Random Forest.

Replace the dataset-loader hook with the final archived experiment loader.
Hyperparameter tuning is performed on the chronological validation block.
"""
METHOD = 'Random Forest'

def build_config():
    return {
        "method": METHOD,
        "tuning": "Optuna",
        "trials": 100,
        "selection_metric": "validation_RMSE",
    }

if __name__ == "__main__":
    print(build_config())
