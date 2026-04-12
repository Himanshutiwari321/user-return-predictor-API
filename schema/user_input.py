from pydantic import BaseModel, Field, ConfigDict, computed_field, field_validator
from typing import Annotated, Literal

#pydantic model to validate input data 
class UserInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    page_views: Annotated[int, Field(..., alias="Page Views", gt=0, lt=25, description="Total number of pages viewed by user")]
    session_duration: Annotated[float, Field(..., alias="Session Duration", gt=0, lt=50, description="Total session duration in minutes")]
    traffic_source: Annotated[str, Field(..., alias="Traffic Source", description="Source of website traffic like Instagram, Google, Direct, Facebook Ads")]
    time_on_page: Annotated[float, Field(..., alias="Time on Page", gt=0, lt=100, description="Average time spent on page in minutes")]
    previous_visits: Annotated[int, Field(..., alias="Previous Visits", ge=0, le=30, description="Number of previous visits by user")]

    @field_validator("traffic_source", mode="before")
    @classmethod
    def clean_traffic_source(cls, v):
        value = str(v).strip()
        lower = value.lower()
        mapping = {
            "instagram": "Instagram",
            "facebook": "Facebook",
            "twitter": "Twitter",
            "linkedin": "LinkedIn",
            "google": "Google",
            "seo": "SEO",
            "organic": "Organic",
            "paid": "Paid",
            "direct": "Direct",
            "referral": "Referral",
            "instagram ads": "Instagram Ads",
            "facebook ads": "Facebook Ads",
            "google ads": "Google Ads",
            "organic search": "Organic Search"
        }
        return mapping.get(lower, value.title())

    @field_validator("session_duration", "time_on_page", mode="before")
    @classmethod
    def convert_to_float(cls, v):
        return float(v)

    @computed_field
    @property
    def source_category(self) -> str:
        source = self.traffic_source.lower().strip()

        if source in ["google", "seo", "organic search"]:
            return "Organic"
        elif source in ["facebook ads", "instagram ads", "google ads"]:
            return "Paid"
        elif source in ["instagram", "facebook", "twitter", "linkedin"]:
            return "Social"
        elif source in ["direct", "url", "bookmark"]:
            return "Direct"
        else:
            return "Referral"

    @computed_field
    @property
    def source_title(self) -> str:
        return f"User came from {self.traffic_source} ({self.source_category})"



