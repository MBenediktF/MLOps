import mlflow
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_diabetes
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime
import numpy as np

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
experiment_name = f"experiment_{timestamp}"

# set the experiment id
mlflow.set_experiment(experiment_name)

mlflow.autolog()
db = load_diabetes()

X_train, X_test, y_train, y_test = train_test_split(db.data, db.target)

# Save a subset of the data as artefakt
# (subset is created for demo purposes in order to keep the size small)
x_train_sub = X_train[:5]
y_train_sub = y_train[:5]
x_test_sub = X_test[:5]
y_test_sub = y_test[:5]
subset_path = 'mnist_subset.npz'
np.savez_compressed(
    subset_path,
    x_train=x_train_sub,
    y_train=y_train_sub,
    x_test=x_test_sub,
    y_test=y_test_sub)

# Create and train models.
rf = RandomForestRegressor(n_estimators=100, max_depth=6, max_features=3)
rf.fit(X_train, y_train)

# Use the model to make predictions on the test dataset.
predictions = rf.predict(X_test)

# Modell als Artefakt loggen (it tensorflow used)
# model_path = 'model.h5'
# rf.save(model_path)
# mlflow.log_artifact(model_path)

# TensorFlow-Modell als MLflow-Artifact loggen
# (kann besser von MLFlow gelesen und angezeigt werden)
mlflow.tensorflow.log_model(rf, "model")
