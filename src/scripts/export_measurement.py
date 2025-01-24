# Exports a measurement from the databases to a single json file
# execute as module with python -m helper_scripts.export_measurement
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from model.create_dataset import create_dataset  # noqa: E402
from helpers.s3 import enable_local_dev as s3_enable_local_dev  # noqa: E402
from helpers.influx import enable_local_dev as influx_enable_local_dev  # noqa: E402 E501


measurement = "env_beige_default"

s3_enable_local_dev()
influx_enable_local_dev()

# Run create dataset function from model code
images, labels, uids = create_dataset(
    measurements=[measurement],
    img_size=(None, 75, 100, 3)
)

# store the dataset as json
output_data = {
    "images": images.tolist(),
    "labels": labels.tolist(),
    "uids": uids.tolist()
}

with open(f"src/scripts/simdata/{measurement}.json", "w") as file:
    json.dump(output_data, file)
