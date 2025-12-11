"""
Basic usage examples for the Yarn Trend Agent.

This demonstrates how to use the agent programmatically.
"""

import os
from dotenv import load_dotenv
from src.yarn_agent.agents.trend_agent import TrendAgent

# Load credentials
load_dotenv()


def example_1_comprehensive_trends():
    """Example 1: Get a comprehensive trend report."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Comprehensive Trend Analysis")
    print("="*60)

    agent = TrendAgent(
        ravelry_access_key=os.getenv("RAVELRY_ACCESS_KEY"),
        ravelry_personal_key=os.getenv("RAVELRY_PERSONAL_KEY"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
    )

    query = "What are the current yarn trends on Ravelry?"
    report = agent.analyze(query)
    print(report)


def example_2_rising_trends():
    """Example 2: Find rising trends and emerging yarns."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Rising Trends")
    print("="*60)

    agent = TrendAgent(
        ravelry_access_key=os.getenv("RAVELRY_ACCESS_KEY"),
        ravelry_personal_key=os.getenv("RAVELRY_PERSONAL_KEY"),
    )

    query = "What yarn trends are emerging in 2024?"
    report = agent.analyze(query)
    print(report)


def example_3_brand_analysis():
    """Example 3: Analyze trends by brand."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Brand Analysis")
    print("="*60)

    agent = TrendAgent(
        ravelry_access_key=os.getenv("RAVELRY_ACCESS_KEY"),
        ravelry_personal_key=os.getenv("RAVELRY_PERSONAL_KEY"),
    )

    query = "Which yarn brands are most popular?"
    report = agent.analyze(query)
    print(report)


def example_4_specific_category():
    """Example 4: Focus on a specific yarn category."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Specific Category Analysis")
    print("="*60)

    agent = TrendAgent(
        ravelry_access_key=os.getenv("RAVELRY_ACCESS_KEY"),
        ravelry_personal_key=os.getenv("RAVELRY_PERSONAL_KEY"),
    )

    query = "What are the trends for fingering weight yarns?"
    report = agent.analyze(query)
    print(report)


def example_5_direct_tool_usage():
    """Example 5: Use tools directly (non-agentic)."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Direct Tool Usage (Non-Agentic)")
    print("="*60)

    from src.yarn_agent.tools.ravelry_client import RavelryClient
    from src.yarn_agent.tools.trend_analyzer import TrendAnalyzer
    from src.yarn_agent.tools.report_generator import ReportGenerator

    # Initialize tools
    client = RavelryClient(
        access_key=os.getenv("RAVELRY_ACCESS_KEY"),
        personal_key=os.getenv("RAVELRY_PERSONAL_KEY"),
    )
    analyzer = TrendAnalyzer()
    reporter = ReportGenerator()

    # Manually orchestrate (non-agentic approach)
    print("Fetching fingering weight yarns...")
    yarns = client.get_popular_yarns(limit=50, weight="Fingering")

    print("Analyzing trends...")
    insights = analyzer.generate_insights(yarns)
    rising = analyzer.identify_rising_stars(yarns, min_projects=50)

    print("Generating report...")
    report = reporter.generate_simple_report(yarns, "Fingering Weight Yarns")

    print(report)
    print("\nInsights:")
    for insight in insights:
        print(f"- {insight}")


if __name__ == "__main__":
    # Check for credentials
    if not os.getenv("RAVELRY_ACCESS_KEY") or not os.getenv("RAVELRY_PERSONAL_KEY"):
        print("❌ Error: Please set up your .env file with Ravelry credentials")
        print("Copy .env.example to .env and fill in your credentials")
        exit(1)

    # Run examples
    print("\n🧶 Yarn Trend Agent - Usage Examples")
    print("====================================\n")

    # You can run individual examples by uncommenting:
    # example_1_comprehensive_trends()
    # example_2_rising_trends()
    # example_3_brand_analysis()
    # example_4_specific_category()
    example_5_direct_tool_usage()

    print("\n✓ Examples complete!")
