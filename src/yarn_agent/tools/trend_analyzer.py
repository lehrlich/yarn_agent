"""
Trend analysis tool for detecting patterns in yarn data.

This is a key component of the agentic system - it autonomously
identifies trends, patterns, and insights from the data.
"""

from typing import List, Dict, Any
from collections import defaultdict
from datetime import datetime
import statistics

from ..models.yarn import Yarn, TrendData


class TrendAnalyzer:
    """Analyzes yarn data to identify trends and patterns."""

    def __init__(self):
        self.analysis_cache = {}

    def analyze_by_weight(self, yarns: List[Yarn]) -> List[TrendData]:
        """
        Analyze trends across different yarn weights.

        Args:
            yarns: List of yarns to analyze

        Returns:
            List of TrendData objects, one per yarn weight category
        """
        weight_groups = self._group_by_attribute(yarns, "yarn_weight")
        trends = []

        for weight, yarn_list in weight_groups.items():
            if len(yarn_list) < 3:  # Skip categories with too few samples
                continue

            trend = TrendData(
                category=f"weight:{weight}",
                time_period="current",
                total_projects=sum(y.metrics.project_count for y in yarn_list),
                avg_popularity_score=statistics.mean(
                    y.metrics.popularity_score for y in yarn_list
                ),
                yarn_count=len(yarn_list),
                sample_yarns=sorted(
                    yarn_list,
                    key=lambda y: y.metrics.popularity_score,
                    reverse=True
                )[:5],  # Top 5 yarns as samples
            )
            trends.append(trend)

        # Sort trends by total popularity
        return sorted(trends, key=lambda t: t.avg_popularity_score, reverse=True)

    def analyze_by_fiber(self, yarns: List[Yarn]) -> List[TrendData]:
        """
        Analyze trends across different fiber types.

        Args:
            yarns: List of yarns to analyze

        Returns:
            List of TrendData objects, one per fiber type
        """
        fiber_groups = self._group_by_attribute(yarns, "fiber_type")
        trends = []

        for fiber, yarn_list in fiber_groups.items():
            if len(yarn_list) < 3:
                continue

            trend = TrendData(
                category=f"fiber:{fiber}",
                time_period="current",
                total_projects=sum(y.metrics.project_count for y in yarn_list),
                avg_popularity_score=statistics.mean(
                    y.metrics.popularity_score for y in yarn_list
                ),
                yarn_count=len(yarn_list),
                sample_yarns=sorted(
                    yarn_list,
                    key=lambda y: y.metrics.popularity_score,
                    reverse=True
                )[:5],
            )
            trends.append(trend)

        return sorted(trends, key=lambda t: t.avg_popularity_score, reverse=True)

    def analyze_by_brand(self, yarns: List[Yarn], top_n: int = 10) -> List[TrendData]:
        """
        Analyze trends across different yarn brands.

        Args:
            yarns: List of yarns to analyze
            top_n: Number of top brands to include

        Returns:
            List of TrendData objects for top brands
        """
        brand_groups = self._group_by_attribute(yarns, "brand")
        trends = []

        for brand, yarn_list in brand_groups.items():
            if len(yarn_list) < 2:
                continue

            trend = TrendData(
                category=f"brand:{brand}",
                time_period="current",
                total_projects=sum(y.metrics.project_count for y in yarn_list),
                avg_popularity_score=statistics.mean(
                    y.metrics.popularity_score for y in yarn_list
                ),
                yarn_count=len(yarn_list),
                sample_yarns=sorted(
                    yarn_list,
                    key=lambda y: y.metrics.popularity_score,
                    reverse=True
                )[:3],
            )
            trends.append(trend)

        # Return top N brands by popularity
        return sorted(trends, key=lambda t: t.total_projects, reverse=True)[:top_n]

    def identify_rising_stars(
        self,
        yarns: List[Yarn],
        min_projects: int = 100,
        top_n: int = 10
    ) -> List[Yarn]:
        """
        Identify yarns that are gaining popularity.

        This uses heuristics to find "rising stars" - yarns with
        high engagement relative to their project count.

        Args:
            yarns: List of yarns to analyze
            min_projects: Minimum project count to consider
            top_n: Number of rising stars to return

        Returns:
            List of Yarn objects that are trending up
        """
        candidates = [y for y in yarns if y.metrics.project_count >= min_projects]

        # Calculate "buzz ratio" - queued + favorites relative to projects
        # High ratio = lots of future interest relative to current usage
        def buzz_ratio(yarn: Yarn) -> float:
            if yarn.metrics.project_count == 0:
                return 0
            return (yarn.metrics.queued + yarn.metrics.favorites) / yarn.metrics.project_count

        # Sort by buzz ratio
        rising = sorted(candidates, key=buzz_ratio, reverse=True)[:top_n]
        return rising

    def identify_classics(
        self,
        yarns: List[Yarn],
        min_projects: int = 1000,
        top_n: int = 10
    ) -> List[Yarn]:
        """
        Identify "classic" yarns with sustained popularity.

        These are established yarns with consistently high usage.

        Args:
            yarns: List of yarns to analyze
            min_projects: Minimum project count for classics
            top_n: Number of classics to return

        Returns:
            List of Yarn objects that are established favorites
        """
        classics = [
            y for y in yarns
            if y.metrics.project_count >= min_projects
            and not y.discontinued
        ]

        # Sort by total popularity score
        return sorted(
            classics,
            key=lambda y: y.metrics.popularity_score,
            reverse=True
        )[:top_n]

    def compare_categories(
        self,
        category_a: List[Yarn],
        category_b: List[Yarn],
        label_a: str,
        label_b: str
    ) -> Dict[str, Any]:
        """
        Compare two categories of yarns.

        Args:
            category_a: First category of yarns
            category_b: Second category of yarns
            label_a: Label for first category
            label_b: Label for second category

        Returns:
            Dictionary with comparative metrics
        """
        def calculate_stats(yarns: List[Yarn]) -> Dict[str, float]:
            if not yarns:
                return {
                    "avg_projects": 0,
                    "avg_popularity": 0,
                    "avg_rating": 0,
                    "total_projects": 0,
                }

            ratings = [y.metrics.rating for y in yarns if y.metrics.rating]

            return {
                "avg_projects": statistics.mean(y.metrics.project_count for y in yarns),
                "avg_popularity": statistics.mean(y.metrics.popularity_score for y in yarns),
                "avg_rating": statistics.mean(ratings) if ratings else 0,
                "total_projects": sum(y.metrics.project_count for y in yarns),
                "count": len(yarns),
            }

        stats_a = calculate_stats(category_a)
        stats_b = calculate_stats(category_b)

        # Calculate percentage differences
        comparison = {
            "category_a": label_a,
            "category_b": label_b,
            "stats_a": stats_a,
            "stats_b": stats_b,
            "differences": {},
        }

        for metric in ["avg_projects", "avg_popularity", "total_projects"]:
            if stats_b[metric] > 0:
                pct_diff = ((stats_a[metric] - stats_b[metric]) / stats_b[metric]) * 100
                comparison["differences"][metric] = pct_diff

        return comparison

    def generate_insights(self, yarns: List[Yarn]) -> List[str]:
        """
        Generate natural language insights from yarn data.

        This is the "intelligent" part - the system autonomously
        identifies what's interesting about the data.

        Args:
            yarns: List of yarns to analyze

        Returns:
            List of insight strings
        """
        insights = []

        if not yarns:
            return ["No yarn data available for analysis."]

        # Overall stats
        total_projects = sum(y.metrics.project_count for y in yarns)
        avg_projects = total_projects / len(yarns)
        insights.append(
            f"Analyzed {len(yarns)} yarns with {total_projects:,} total projects "
            f"(avg: {avg_projects:.0f} per yarn)"
        )

        # Weight distribution
        weight_trends = self.analyze_by_weight(yarns)
        if weight_trends:
            top_weight = weight_trends[0]
            insights.append(
                f"Most popular weight: {top_weight.category.split(':')[1]} "
                f"({top_weight.total_projects:,} projects across {top_weight.yarn_count} yarns)"
            )

        # Fiber trends
        fiber_trends = self.analyze_by_fiber(yarns)
        if fiber_trends:
            top_fiber = fiber_trends[0]
            insights.append(
                f"Most popular fiber: {top_fiber.category.split(':')[1]} "
                f"({top_fiber.total_projects:,} projects)"
            )

        # Rising stars
        rising = self.identify_rising_stars(yarns, min_projects=50, top_n=3)
        if rising:
            rising_names = [f"{y.brand} {y.name}" for y in rising[:3]]
            insights.append(
                f"Rising stars (high buzz ratio): {', '.join(rising_names)}"
            )

        # Discontinued detection
        discontinued = [y for y in yarns if y.discontinued]
        if discontinued:
            insights.append(
                f"⚠️ {len(discontinued)} yarns in dataset are discontinued"
            )

        return insights

    def _group_by_attribute(
        self,
        yarns: List[Yarn],
        attribute: str
    ) -> Dict[str, List[Yarn]]:
        """
        Group yarns by a specific attribute.

        Args:
            yarns: List of yarns
            attribute: Attribute to group by ("yarn_weight", "fiber_type", "brand")

        Returns:
            Dictionary mapping attribute values to lists of yarns
        """
        groups = defaultdict(list)
        for yarn in yarns:
            value = getattr(yarn, attribute, "Unknown")
            groups[value].append(yarn)
        return dict(groups)
