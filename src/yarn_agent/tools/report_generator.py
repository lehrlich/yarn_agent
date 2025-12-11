"""
Report generation tool for creating human-readable trend reports.

This tool takes analysis results and formats them into clear,
actionable insights for users.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

from ..models.yarn import Yarn, TrendData


class ReportGenerator:
    """Generates formatted reports from trend analysis."""

    def generate_trend_report(
        self,
        insights: List[str],
        weight_trends: List[TrendData],
        fiber_trends: List[TrendData],
        brand_trends: List[TrendData],
        rising_stars: List[Yarn],
        classics: List[Yarn],
    ) -> str:
        """
        Generate a comprehensive trend report.

        Args:
            insights: List of generated insights
            weight_trends: Trends by yarn weight
            fiber_trends: Trends by fiber type
            brand_trends: Trends by brand
            rising_stars: Yarns gaining popularity
            classics: Established popular yarns

        Returns:
            Formatted markdown report
        """
        report_lines = []

        # Header
        report_lines.append("# Yarn Trend Analysis Report")
        report_lines.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("\n---\n")

        # Executive Summary
        report_lines.append("## 📊 Executive Summary\n")
        for insight in insights:
            report_lines.append(f"- {insight}")
        report_lines.append("\n---\n")

        # Yarn Weight Trends
        if weight_trends:
            report_lines.append("## 🧶 Trends by Yarn Weight\n")
            report_lines.append("Popularity ranking of yarn weights:\n")
            for i, trend in enumerate(weight_trends[:5], 1):
                weight_name = trend.category.split(':')[1]
                report_lines.append(
                    f"{i}. **{weight_name}** - "
                    f"{trend.total_projects:,} projects across {trend.yarn_count} yarns "
                    f"(avg popularity: {trend.avg_popularity_score:.0f})"
                )
                if trend.sample_yarns:
                    top_yarn = trend.sample_yarns[0]
                    report_lines.append(
                        f"   - Top yarn: {top_yarn.brand} {top_yarn.name} "
                        f"({top_yarn.metrics.project_count:,} projects)"
                    )
            report_lines.append("\n")

        # Fiber Type Trends
        if fiber_trends:
            report_lines.append("## 🐑 Trends by Fiber Type\n")
            report_lines.append("Most popular fiber types:\n")
            for i, trend in enumerate(fiber_trends[:5], 1):
                fiber_name = trend.category.split(':')[1]
                report_lines.append(
                    f"{i}. **{fiber_name}** - "
                    f"{trend.total_projects:,} projects across {trend.yarn_count} yarns"
                )
                if trend.sample_yarns:
                    top_yarn = trend.sample_yarns[0]
                    report_lines.append(
                        f"   - Top yarn: {top_yarn.brand} {top_yarn.name}"
                    )
            report_lines.append("\n")

        # Brand Trends
        if brand_trends:
            report_lines.append("## 🏷️ Top Brands\n")
            report_lines.append("Most popular yarn brands:\n")
            for i, trend in enumerate(brand_trends[:10], 1):
                brand_name = trend.category.split(':')[1]
                report_lines.append(
                    f"{i}. **{brand_name}** - "
                    f"{trend.total_projects:,} projects "
                    f"({trend.yarn_count} yarns in dataset)"
                )
            report_lines.append("\n")

        # Rising Stars
        if rising_stars:
            report_lines.append("## ⭐ Rising Stars\n")
            report_lines.append(
                "Yarns showing strong momentum (high queue/favorites relative to projects):\n"
            )
            for yarn in rising_stars[:5]:
                buzz_ratio = (
                    (yarn.metrics.queued + yarn.metrics.favorites) /
                    yarn.metrics.project_count
                )
                report_lines.append(
                    f"- **{yarn.brand} {yarn.name}** ({yarn.yarn_weight})\n"
                    f"  - {yarn.metrics.project_count:,} projects, "
                    f"{yarn.metrics.queued:,} queued, "
                    f"{yarn.metrics.favorites:,} favorites\n"
                    f"  - Buzz ratio: {buzz_ratio:.2f}"
                )
            report_lines.append("\n")

        # Classics
        if classics:
            report_lines.append("## 👑 Established Classics\n")
            report_lines.append("Time-tested yarns with sustained popularity:\n")
            for yarn in classics[:5]:
                report_lines.append(
                    f"- **{yarn.brand} {yarn.name}** ({yarn.yarn_weight}, {yarn.fiber_type})\n"
                    f"  - {yarn.metrics.project_count:,} projects, "
                    f"{yarn.metrics.in_stash:,} in stash"
                )
                if yarn.metrics.rating:
                    report_lines.append(f"  - Rating: {yarn.metrics.rating:.2f}/5.0")
            report_lines.append("\n")

        # Footer
        report_lines.append("---\n")
        report_lines.append(
            "\n*This report was generated autonomously by the Yarn Trend Agent.*\n"
        )

        return "\n".join(report_lines)

    def generate_comparison_report(
        self,
        comparison: Dict[str, Any],
        category_a_yarns: List[Yarn],
        category_b_yarns: List[Yarn],
    ) -> str:
        """
        Generate a report comparing two yarn categories.

        Args:
            comparison: Comparison statistics
            category_a_yarns: Yarns in first category
            category_b_yarns: Yarns in second category

        Returns:
            Formatted markdown report
        """
        report_lines = []

        report_lines.append("# Yarn Category Comparison Report\n")
        report_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report_lines.append("---\n")

        # Categories being compared
        report_lines.append(f"## Comparing: {comparison['category_a']} vs {comparison['category_b']}\n")

        # Stats table
        report_lines.append("### Key Metrics\n")
        report_lines.append("| Metric | {} | {} | Difference |".format(
            comparison['category_a'],
            comparison['category_b']
        ))
        report_lines.append("|--------|---------|---------|------------|")

        stats_a = comparison['stats_a']
        stats_b = comparison['stats_b']
        diffs = comparison['differences']

        report_lines.append("| Yarn Count | {:,} | {:,} | - |".format(
            stats_a['count'],
            stats_b['count']
        ))

        report_lines.append("| Total Projects | {:,} | {:,} | {:.1f}% |".format(
            int(stats_a['total_projects']),
            int(stats_b['total_projects']),
            diffs.get('total_projects', 0)
        ))

        report_lines.append("| Avg Projects/Yarn | {:.0f} | {:.0f} | {:.1f}% |".format(
            stats_a['avg_projects'],
            stats_b['avg_projects'],
            diffs.get('avg_projects', 0)
        ))

        report_lines.append("| Avg Popularity Score | {:.0f} | {:.0f} | {:.1f}% |\n".format(
            stats_a['avg_popularity'],
            stats_b['avg_popularity'],
            diffs.get('avg_popularity', 0)
        ))

        # Top examples from each category
        report_lines.append(f"### Top Yarns in {comparison['category_a']}\n")
        for yarn in sorted(category_a_yarns, key=lambda y: y.metrics.project_count, reverse=True)[:3]:
            report_lines.append(
                f"- **{yarn.brand} {yarn.name}** - {yarn.metrics.project_count:,} projects"
            )

        report_lines.append(f"\n### Top Yarns in {comparison['category_b']}\n")
        for yarn in sorted(category_b_yarns, key=lambda y: y.metrics.project_count, reverse=True)[:3]:
            report_lines.append(
                f"- **{yarn.brand} {yarn.name}** - {yarn.metrics.project_count:,} projects"
            )

        report_lines.append("\n---\n")
        return "\n".join(report_lines)

    def generate_simple_report(self, yarns: List[Yarn], title: str = "Yarn Report") -> str:
        """
        Generate a simple list report of yarns.

        Args:
            yarns: List of yarns to report on
            title: Report title

        Returns:
            Formatted markdown report
        """
        report_lines = []

        report_lines.append(f"# {title}\n")
        report_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report_lines.append(f"**Total Yarns:** {len(yarns)}\n")
        report_lines.append("---\n")

        # Sort by popularity
        sorted_yarns = sorted(
            yarns,
            key=lambda y: y.metrics.popularity_score,
            reverse=True
        )

        for i, yarn in enumerate(sorted_yarns[:20], 1):
            report_lines.append(f"\n## {i}. {yarn.brand} {yarn.name}\n")
            report_lines.append(f"- **Weight:** {yarn.yarn_weight}")
            report_lines.append(f"- **Fiber:** {yarn.fiber_type}")
            report_lines.append(f"- **Projects:** {yarn.metrics.project_count:,}")
            report_lines.append(f"- **Queued:** {yarn.metrics.queued:,}")
            report_lines.append(f"- **Favorites:** {yarn.metrics.favorites:,}")
            report_lines.append(f"- **In Stash:** {yarn.metrics.in_stash:,}")
            if yarn.metrics.rating:
                report_lines.append(f"- **Rating:** {yarn.metrics.rating:.2f}/5.0")
            report_lines.append(f"- **Popularity Score:** {yarn.metrics.popularity_score:.0f}")

        return "\n".join(report_lines)
