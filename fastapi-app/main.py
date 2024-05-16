from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
import pandas as pd
from dotenv import load_dotenv
import pickle, uvicorn, os, logging
from logging_setup import LoggerSetup
from elasticsearch import Elasticsearch

# from draft.src.logging_setup import setup_root_logger

app = FastAPI()

# Load environment variables from .env file
load_dotenv()

# Configure Elasticsearch connection
# Elasticsearch connection parameters
# ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST")
# ELASTICSEARCH_PORT = int(os.getenv("ELASTICSEARCH_PORT"))
# ELASTICSEARCH_USERNAME = os.getenv("ELASTICSEARCH_USERNAME")
# ELASTICSEARCH_PASSWORD = os.getenv("ELASTICSEARCH_PASSWORD")
# ELASTICSEARCH_API = os.getenv("ELASTICSEARCH_API")

# # Print loaded configuration (optional)
# print("Elasticsearch Host:", ELASTICSEARCH_HOST)
# print("Elasticsearch Port:", ELASTICSEARCH_PORT)
# print("Elasticsearch Username:", ELASTICSEARCH_USERNAME)
# print("Elasticsearch Password:", ELASTICSEARCH_PASSWORD)

# es = Elasticsearch(
#     [ELASTICSEARCH_HOST],  # Replace with your Elasticsearch server address in .env
#     http_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD),
#     # timeout=6000000,
#     # api_key=ELASTICSEARCH_API,
# )
# setup root logger
logger_setup = LoggerSetup()

# get logger for module
logger = logging.getLogger(__name__)

logger.info("---Starting App---")


# # Add Elasticsearch logging handler
# es_handler = logging.StreamHandler()
# es_handler.setLevel(logging.DEBUG)
# es_handler.setFormatter(
#     logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# )
# logger.addHandler(es_handler)

# Define filepath for ml_components.pkl
ML_COMPONENTS_FILEPATH = os.path.join("assets", "ml", "ml_components.pkl")

# Load machine learning model and other components
with open(ML_COMPONENTS_FILEPATH, "rb") as file:
    ml_components = pickle.load(file)

# preprocessor = ml_components["preprocessor"]
pipeline = ml_components["pipeline"]


class DeviceSpecs(BaseModel):
    """
    Device specifications.

    - battery_power: Total energy a battery can store in one time measured in mAh
    - blue: Has Bluetooth or not (0 for False, 1 for True)
    - clock_speed: The speed at which the microprocessor executes instructions
    - dual_sim: Has dual sim support or not (0 for False, 1 for True)
    - fc: Front Camera megapixels
    - four_g: Has 4G or not (0 for False, 1 for True)
    - int_memory: Internal Memory in Gigabytes
    - m_dep: Mobile Depth in cm
    - mobile_wt: Weight of mobile phone
    - n_cores: Number of cores of the processor
    - pc: Primary Camera megapixels
    - px_height: Pixel Resolution Height
    - px_width: Pixel Resolution Width
    - ram: Random Access Memory in Megabytes
    - sc_h: Screen Height of mobile in cm
    - sc_w: Screen Width of mobile in cm
    - talk_time: longest time that a single battery charge will last when you are
    - three_g: Has 3G or not (0 for False, 1 for True)
    - touch_screen: Has touch screen or not (0 for False, 1 for True)
    - wifi: Has wifi or not (0 for False, 1 for True)
    """

    battery_power: float
    blue: int
    clock_speed: float
    dual_sim: int
    fc: float
    four_g: int
    int_memory: float
    m_dep: float
    mobile_wt: float
    n_cores: float
    pc: float
    px_height: float
    px_width: float
    ram: float
    sc_h: float
    sc_w: float
    talk_time: float
    three_g: int
    touch_screen: int
    wifi: int

    @validator("blue", "dual_sim", "four_g", "three_g", "touch_screen", "wifi")
    def validate_boolean(cls, v):
        # Ensure the values are either 0 or 1
        if v not in (0, 1):
            raise ValueError("Value must be 0 or 1")
        return v


@app.post("/predict/{device_id}")
async def predict_price(device_id: int, specs: DeviceSpecs):
    """
    Predict the price of a device based on its specifications.

    Args:
        device_id (int): The ID of the device.
        specs (DeviceSpecs): The device specifications.

    Returns:
        dict: A dictionary containing the input data and predicted price.
    """
    try:
        logger.info(f"Input request received...")

        # Preprocess the data
        data = pd.DataFrame([{"device_id": device_id, **specs.dict()}])
        logger.info(f"Input as a dataframe\n{data.to_markdown()}\n")

        # Predict price
        data["predicted_price"] = pipeline.predict(data)

        logger.info(
            f"Predictions made\n{data[['device_id', 'predicted_price']].to_markdown()}\n"
        )

        # Return input data and predicted price
        return data.to_dict("records")
    except Exception as e:
        logger.error(
            f"An error occurred while processing prediction for device ID {device_id}: {str(e)}"
        )
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/", tags=["root"])
def root():

    logger.info("Root endpoint was called")
    return {
        "api": "",
        "description": "",
    }


@app.get("/ping", tags=["health"])
async def ping():
    """
    Health Check Endpoint

    This endpoint can be used to check if the API is up and running.

    Returns:
        dict: A JSON response with a message "pong".
    """
    logger.info("Ping endpoint was called")
    return {"message": "pong"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
