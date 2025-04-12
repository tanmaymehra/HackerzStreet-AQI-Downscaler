import random
from PIL import Image
import os

def predict_aqi_map(lat, lon, output_image=False):
    # Dummy AQI prediction based on coordinates from city_coordinates file
    aqi = round(random.uniform(40, 180), 2)

    if output_image:
        # Use a dummy image
        img_path = os.path.join("data/satellite_sample.png")
        return img_path

    return aqi
