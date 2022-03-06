from xmlrpc.client import Boolean
from pydantic import BaseModel

class userData(BaseModel):
    tier: float
    family_planning: Boolean
    mental_health: Boolean
    dental_care: Boolean
    telemedicine_service: Boolean
    cashback_benefit: Boolean
    anc_delivery_coverage: Boolean
    eye_care_cost: Boolean
    gym_membership: Boolean
    annual_medical_screening: Boolean
    location: str