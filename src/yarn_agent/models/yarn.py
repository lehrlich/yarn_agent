"""Data models for yarn and trend information."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class YarnMetrics:
    """Metrics about a yarn's popularity and characteristics."""

    project_count: int
    favorites: int
    rating: Optional[float]
    comments: int
    queued: int  # Number of people who queued this yarn
    in_stash: int  # Number of people with this in their stash

    @property
    def popularity_score(self) -> float:
        """Calculate a composite popularity score."""
        # Weighted score: projects matter most, then queued, favorites, stash
        return (
            self.project_count * 3.0 +
            self.queued * 1.5 +
            self.favorites * 1.0 +
            self.in_stash * 0.5
        )


@dataclass
class Yarn:
    """Represents a yarn with its metadata and metrics."""

    id: str
    name: str
    brand: str
    yarn_weight: str  # e.g., "Fingering", "Worsted", "Bulky"
    fiber_type: str  # e.g., "Wool", "Cotton", "Acrylic Blend"
    metrics: YarnMetrics
    scraped_at: datetime
    permalink: Optional[str] = None

    # Optional detailed info
    yardage: Optional[int] = None
    grams: Optional[int] = None
    texture: Optional[str] = None
    discontinued: bool = False


@dataclass
class TrendData:
    """Represents trend analysis results."""

    category: str  # e.g., "yarn_weight:Fingering", "fiber:Wool", "brand:Malabrigo"
    time_period: str
    total_projects: int
    avg_popularity_score: float
    yarn_count: int
    sample_yarns: List[Yarn]

    # Comparative metrics (if comparing time periods)
    growth_rate: Optional[float] = None  # Percentage change
    trend_direction: Optional[str] = None  # "rising", "falling", "stable"

    def __repr__(self):
        return (
            f"TrendData(category={self.category}, "
            f"projects={self.total_projects}, "
            f"trend={self.trend_direction})"
        )
