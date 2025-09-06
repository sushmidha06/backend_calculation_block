from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

# Constants
CF = 0.475       # Carbon Fraction
CO2_CON = 3.67   # CO2 Conversion factor
PIXEL_AREA_DEFAULT = 0.09  # 30m x 30m pixel in hectares

# Input models
class NDVIInputFixed(BaseModel):
    ndvi: float = Field(..., ge=-1.0, le=1.0, description="NDVI value between -1 and 1")
    a: float
    b: float

class NDVIInputFlexible(BaseModel):
    ndvi: float = Field(..., ge=-1.0, le=1.0, description="NDVI value between -1 and 1")
    a: float
    b: float
    pixel_area: float = Field(..., gt=0, description="Pixel area in hectares (must be > 0)")

# Response model
class CreditsResponse(BaseModel):
    NDVI: float
    pixel_area: float | None = None
    biomass_per_hectare: float
    biomass_per_pixel: float
    carbon_stock: float
    co2_equivalent: float
    carbon_credits: float

# Endpoint 1: Fixed pixel area (0.09 ha)
@app.post("/calculate_credits_fixed/", response_model=CreditsResponse)
def calculate_credits_fixed(data: NDVIInputFixed):
    """
    Calculate carbon credits for a fixed pixel area (0.09 ha).
    """
    biomass_per_hectare = data.a * data.ndvi + data.b
    biomass_per_pixel = biomass_per_hectare * PIXEL_AREA_DEFAULT
    carbon_stock = biomass_per_pixel * CF
    co2_eq = carbon_stock * CO2_CON
    credits = co2_eq / 1000

    return CreditsResponse(
        NDVI=data.ndvi,
        biomass_per_hectare=biomass_per_hectare,
        biomass_per_pixel=biomass_per_pixel,
        carbon_stock=carbon_stock,
        co2_equivalent=co2_eq,
        carbon_credits=credits
    )

# Endpoint 2: Flexible pixel area (user input)
@app.post("/calculate_credits_flexible/", response_model=CreditsResponse)
def calculate_credits_flexible(data: NDVIInputFlexible):
    """
    Calculate carbon credits for a user-defined pixel area.
    """
    biomass_per_hectare = data.a * data.ndvi + data.b
    biomass_per_pixel = biomass_per_hectare * data.pixel_area
    carbon_stock = biomass_per_pixel * CF
    co2_eq = carbon_stock * CO2_CON
    credits = co2_eq / 1000

    return CreditsResponse(
        NDVI=data.ndvi,
        pixel_area=data.pixel_area,
        biomass_per_hectare=biomass_per_hectare,
        biomass_per_pixel=biomass_per_pixel,
        carbon_stock=carbon_stock,
        co2_equivalent=co2_eq,
        carbon_credits=credits
        )