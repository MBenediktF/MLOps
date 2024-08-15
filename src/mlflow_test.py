import mlflow
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_diabetes
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
experiment_name = f"experiment_{timestamp}"

# set the experiment id
mlflow.set_experiment(experiment_name)

mlflow.autolog()
db = load_diabetes()

X_train, X_test, y_train, y_test = train_test_split(db.data, db.target)

# Create and train models.
rf = RandomForestRegressor(n_estimators=100, max_depth=6, max_features=3)
rf.fit(X_train, y_train)

# Use the model to make predictions on the test dataset.
predictions = rf.predict(X_test)

# Modell als Artefakt loggen
model_path = 'model.h5'
rf.save(model_path)
mlflow.log_artifact(model_path)

# TensorFlow-Modell als MLflow-Artifact loggen (kann besser von MLFlow gelesen und angezeigt werden)
mlflow.tensorflow.log_model(rf, "model")
