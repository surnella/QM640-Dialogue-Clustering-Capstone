"""
Two-Tier Canonical Slot Schema for Goal-Oriented Dialogue Trajectories.
Formalizes Tier-1 (Universal Core Slots) and Tier-2 (Enterprise Operational Extension Slots).
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class Tier1UniversalSlots(BaseModel):
    """
    Tier 1: Universal Core Slots present across academic benchmarks
    (Microsoft Frames and MultiWOZ 2.2) and enterprise travel consultations.
    """
    origin_city: Optional[str] = Field(None, description="Departure or origin city/airport")
    destination_city: Optional[str] = Field(None, description="Target destination city/resort")
    departure_date: Optional[str] = Field(None, description="Start date of journey")
    return_date: Optional[str] = Field(None, description="Return date of journey")
    duration_nights: Optional[int] = Field(None, description="Length of stay in nights")
    traveler_count_adults: Optional[int] = Field(1, description="Number of adult travelers")
    traveler_count_children: Optional[int] = Field(0, description="Number of child travelers")
    budget_amount: Optional[float] = Field(None, description="Total or per-person budget ceiling")
    accommodation_tier: Optional[str] = Field(None, description="Star rating or tier (3-star, 4-star, 5-star, luxury)")
    booking_status: Optional[str] = Field("inquiry", description="State: inquiry, exploring, shortlisted, confirmed")


class Tier2EnterpriseSlots(BaseModel):
    """
    Tier 2: Enterprise Extension Slots evaluating operational policy
    and business rule adherence (tested in RQ3 and RQ4).
    """
    visa_processing_window_days: Optional[int] = Field(None, description="Days between inquiry and departure for visa issuance")
    passport_expiry_months: Optional[int] = Field(None, description="Remaining validity of passport in months")
    package_type: Optional[str] = Field("FIT", description="Tour format: FIT (Free Independent Traveler) or Group")
    sharing_basis: Optional[str] = Field("Twin", description="Room occupancy: Single, Twin, Double, Triple")
    discount_applied_percentage: Optional[float] = Field(0.0, description="Authorized sales promotion discount percentage")


class CanonicalTurn(BaseModel):
    """
    A single turn within a goal-oriented conversation trajectory.
    """
    turn_id: int
    speaker: str  # 'user' or 'system' / 'wizard'
    utterance: str
    acts: List[str] = Field(default_factory=list)
    slots_mentioned: Dict[str, Any] = Field(default_factory=dict)
    revisions: List[str] = Field(default_factory=list, description="Slots modified in this turn")


class CanonicalDialogueTrajectory(BaseModel):
    """
    Complete dialogue session normalized into canonical trajectory format.
    """
    dialogue_id: str
    source_dataset: str  # 'frames', 'multiwoz', or 'enterprise'
    total_turns: int
    user_turns: int
    wizard_turns: int
    canonical_tier1: Tier1UniversalSlots = Field(default_factory=Tier1UniversalSlots)
    canonical_tier2: Tier2EnterpriseSlots = Field(default_factory=Tier2EnterpriseSlots)
    turns: List[CanonicalTurn] = Field(default_factory=list)
    revisions_count: int = 0
    budget_specified: bool = False
    hesitation_markers_count: int = 0
    assigned_archetype: Optional[str] = None  # Populated during RQ1 clustering
