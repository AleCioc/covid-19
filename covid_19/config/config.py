import os

validation_results_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "validation_results"
)
trainer_params_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "trainer",
    "trainer_params"
)
validator_params_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "model_validator",
    "validator_params"
)
