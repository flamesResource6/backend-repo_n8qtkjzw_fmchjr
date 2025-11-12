"""
Database Schemas for the Real Estate Investing SaaS

Each Pydantic model represents one MongoDB collection. The collection name
is the lowercase of the class name (e.g., Property -> "property").
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class Property(BaseModel):
    """
    Properties listed/deal feed items
    Collection: "property"
    """
    title: str = Field(..., description="Listing headline")
    address: str = Field(..., description="Street address")
    city: str = Field(..., description="City")
    state: str = Field(..., description="US state (2-letter)")
    zipcode: str = Field(..., description="ZIP Code")
    price: float = Field(..., ge=0, description="Asking price in USD")
    cap_rate: Optional[float] = Field(None, ge=0, le=100, description="Cap rate percentage")
    cash_on_cash: Optional[float] = Field(None, ge=0, le=100, description="Cash-on-cash return percentage")
    units: Optional[int] = Field(None, ge=0, description="Number of units (multifamily)")
    property_type: str = Field(..., description="Type: SFR, Multifamily, Industrial, Retail, Land, etc.")
    images: Optional[List[str]] = Field(default_factory=list, description="Image URLs")
    source: Optional[str] = Field(None, description="Lead source or marketplace")
    latitude: Optional[float] = Field(None, description="Latitude")
    longitude: Optional[float] = Field(None, description="Longitude")

class Savedsearch(BaseModel):
    """
    Saved Searches for users to monitor markets
    Collection: "savedsearch"
    """
    name: str = Field(..., description="Saved search name")
    email: EmailStr = Field(..., description="Subscriber email")
    markets: List[str] = Field(default_factory=list, description="List of markets like 'Austin, TX'")
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    min_cap_rate: Optional[float] = Field(None, ge=0, le=100)
    property_types: List[str] = Field(default_factory=list)

class Lead(BaseModel):
    """
    Inbound contact/lead submissions
    Collection: "lead"
    """
    name: str
    email: EmailStr
    message: Optional[str] = None
    company: Optional[str] = None
    phone: Optional[str] = None
