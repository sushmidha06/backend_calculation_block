from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Constants
CF = 0.475       # Carbon Fraction
CO2_CON = 3.67   # CO2 Conversion factor
PIXEL_AREA_DEFAULT = 0.09  # 30m x 30m pixel in hectares

# Input models
class NDVIInputFixed(BaseModel):
    ndvi: float
    a: float
    b: float

class NDVIInputFlexible(BaseModel):
    ndvi: float
    a: float
    b: float
    pixel_area: float  # in hectares

# Endpoint 1: Fixed pixel area (0.09 ha)
@app.post("/calculate_credits_fixed/")
def calculate_credits_fixed(data: NDVIInputFixed):
    # Step 1: Biomass per hectare
    biomass_per_hectare = data.a * data.ndvi + data.b

    # Step 2: Biomass per pixel (fixed pixel area)
    biomass_per_pixel = biomass_per_hectare * PIXEL_AREA_DEFAULT

    # Step 3: Carbon stock
    carbon_stock = biomass_per_pixel * CF

    # Step 4: CO2 equivalent
    co2_eq = carbon_stock * CO2_CON

    # Step 5: Credits (1 credit = 1 ton CO2eq)
    credits = co2_eq / 1000

    return {
        "NDVI": data.ndvi,
        "biomass_per_hectare": biomass_per_hectare,
        "biomass_per_pixel": biomass_per_pixel,
        "carbon_stock": carbon_stock,
        "co2_equivalent": co2_eq,
        "carbon_credits": credits
    }

# Endpoint 2: Flexible pixel area (user input)
@app.post("/calculate_credits_flexible/")
def calculate_credits_flexible(data: NDVIInputFlexible):
    # Step 1: Biomass per hectare
    biomass_per_hectare = data.a * data.ndvi + data.b

    # Step 2: Biomass per pixel (user-defined pixel area)
    biomass_per_pixel = biomass_per_hectare * data.pixel_area

    # Step 3: Carbon stock
    carbon_stock = biomass_per_pixel * CF

    # Step 4: CO2 equivalent
    co2_eq = carbon_stock * CO2_CON

    # Step 5: Credits (1 credit = 1 ton CO2eq)
    credits = co2_eq / 1000

    return {
        "NDVI": data.ndvi,
        "pixel_area": data.pixel_area,
        "biomass_per_hectare": biomass_per_hectare,
        "biomass_per_pixel": biomass_per_pixel,
        "carbon_stock": carbon_stock,
        "co2_equivalent": co2_eq,
        "carbon_credits": credits
    }
