"""
Interactive demo showing step-by-step execution with mock data.

This demonstrates the agentic flow without requiring API credentials.
"""

from datetime import datetime
import json
from typing import List, Dict, Any


def print_section(title: str):
    """Print a section header."""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)


def print_step(step_num: int, description: str):
    """Print a step header."""
    print(f"\n{'─'*80}")
    print(f"STEP {step_num}: {description}")
    print(f"{'─'*80}")


def demo_query_interpretation():
    """Demo: How the agent interprets a query."""
    print_section("DEMO: AGENTIC EXECUTION FLOW")

    print("\n📝 USER QUERY:")
    query = "What yarn trends are emerging in 2024?"
    print(f'>>> "{query}"')

    print_step(1, "Agent Receives Query")
    print("\nAgent initialized with 3 tools:")
    print("  ✓ RavelryClient (data collection)")
    print("  ✓ TrendAnalyzer (pattern detection)")
    print("  ✓ ReportGenerator (formatting)")

    print_step(2, "Planning Phase - AGENTIC DECISION MAKING")

    print("\n🤖 Agent reasoning:")
    print('  Query: "What yarn trends are emerging in 2024?"')
    print('  Key words detected: ["trends", "emerging", "2024"]')
    print()
    print("  Semantic interpretation:")
    print('    - "emerging" → Focus on RISING popularity, not established')
    print('    - "trends" → Need MULTIPLE categories, not single yarns')
    print('    - "2024" → Recent data (not historical)')
    print()
    print("  🎯 Decision 1: What data to collect?")
    print("    Reasoning: Need broad sample for trend detection")
    print("    Decision: Fetch 150 popular yarns (statistically significant)")
    print("    Tool: get_popular_yarns() - sorted by projects")
    print()
    print("  🎯 Decision 2: What analyses to run?")
    print("    Reasoning: 'Emerging' suggests momentum")
    print("    Decision: Focus on rising_stars analysis")
    print("    Also: Analyze by weight/fiber to show WHERE trends emerge")
    print()
    print("  🎯 Decision 3: How to present?")
    print("    Reasoning: Comprehensive insights needed")
    print("    Decision: trend_report format with explanations")

    plan = {
        "strategy": "Identify rising trends and emerging yarns",
        "data_collection": [
            {"action": "get_popular_yarns", "params": {"limit": 150}}
        ],
        "analyses": ["rising_stars", "by_weight", "by_fiber"],
        "report_type": "trend_report"
    }

    print("\n📋 Generated Execution Plan:")
    print(json.dumps(plan, indent=2))


def demo_data_collection():
    """Demo: How the agent collects data."""
    print_step(3, "Data Collection - AUTONOMOUS SAMPLING")

    print("\n🌐 Executing: get_popular_yarns(limit=150)")
    print("\nAgent decides HOW to fetch this data:")
    print("  ✓ API has 50-item page limit → Need 3 requests")
    print("  ✓ Must respect rate limits → 1 request/second")
    print("  ✓ Sort by: 'projects' → Most popular first")
    print("  ✓ Deduplicate → Track seen IDs")

    print("\n📡 API Request 1:")
    print("  GET /yarns/search.json?page=1&page_size=50&sort=projects")
    print("  Response: 50 yarns")
    print("  Sample:")
    print("    {")
    print('      "id": 1234,')
    print('      "name": "Rios",')
    print('      "yarn_company": {"name": "Malabrigo"},')
    print('      "yarn_weight": {"name": "Worsted"},')
    print('      "projects": 45678,')
    print('      "favorites": 12345,')
    print('      "queued_projects_count": 8901')
    print("    }")
    print("  Progress: 50/150 yarns ⏳")

    print("\n📡 API Request 2:")
    print("  GET /yarns/search.json?page=2&page_size=50&sort=projects")
    print("  Response: 50 yarns")
    print("  Progress: 100/150 yarns ⏳")

    print("\n📡 API Request 3:")
    print("  GET /yarns/search.json?page=3&page_size=50&sort=projects")
    print("  Response: 50 yarns")
    print("  Progress: 150/150 yarns ✓")

    print("\n✅ Data collection complete!")
    print("   Collected: 150 Yarn objects")
    print("   Time: ~15 seconds (rate-limited)")


def demo_parsing():
    """Demo: How raw API data becomes structured objects."""
    print_step(4, "Data Parsing - INTELLIGENT EXTRACTION")

    print("\n🔄 Converting API response to Yarn objects...")
    print("\nRaw API data:")
    raw_data = {
        "id": 1234,
        "name": "Rios",
        "yarn_company": {"name": "Malabrigo"},
        "yarn_weight": {"name": "Worsted"},
        "projects": 45678,
        "favorites": 12345,
        "queued_projects_count": 8901,
        "stash_count": 23456,
        "rating_average": 4.5
    }
    print(json.dumps(raw_data, indent=2))

    print("\n🎯 Agent extracts and calculates:")
    print("  Basic info:")
    print("    - id: 1234")
    print("    - name: 'Rios'")
    print("    - brand: 'Malabrigo'")
    print("    - weight: 'Worsted'")
    print()
    print("  Metrics:")
    print("    - projects: 45,678")
    print("    - queued: 8,901")
    print("    - favorites: 12,345")
    print("    - in_stash: 23,456")
    print("    - rating: 4.5/5.0")
    print()
    print("  🧮 CALCULATED METRIC - Popularity Score:")
    print("    Formula: (projects × 3) + (queued × 1.5) + (favorites × 1) + (stash × 0.5)")
    print("    Calculation:")
    print(f"      = (45,678 × 3) + (8,901 × 1.5) + (12,345 × 1) + (23,456 × 0.5)")
    print(f"      = 137,034 + 13,351.5 + 12,345 + 11,728")
    print(f"      = 174,458.5")
    print()
    print("  💡 This composite score weighs different engagement types!")

    print("\n✅ Result: Yarn object with enriched metrics")


def demo_analysis():
    """Demo: How the agent analyzes patterns."""
    print_step(5, "Trend Analysis - PATTERN DETECTION")

    print("\n📊 Analysis 1: Identify Rising Stars")
    print("\n🎯 Agent's autonomous heuristic:")
    print('  Definition: "Rising star" = high FUTURE interest relative to CURRENT usage')
    print()
    print("  Metric: Buzz Ratio = (queued + favorites) / projects")
    print("  Threshold: min_projects >= 100 (filter noise)")
    print("  Output: Top 10 by buzz ratio")

    print("\n  Example calculations:")
    print()
    print("  Yarn A: 'Hedgehog Fibres Skinny Singles'")
    print("    - projects: 5,234")
    print("    - queued: 3,456")
    print("    - favorites: 2,890")
    print("    - buzz_ratio = (3,456 + 2,890) / 5,234 = 1.21")
    print("    → 💫 RISING STAR! High future interest!")
    print()
    print("  Yarn B: 'Cascade 220' (established classic)")
    print("    - projects: 50,000")
    print("    - queued: 5,000")
    print("    - favorites: 3,000")
    print("    - buzz_ratio = (5,000 + 3,000) / 50,000 = 0.16")
    print("    → 👑 Classic, but not 'emerging'")

    print("\n  ✅ Rising stars identified: 10 yarns with buzz_ratio > 0.8")

    print("\n📊 Analysis 2: Trends by Weight")
    print("\n  Agent groups 150 yarns by weight category:")

    categories = [
        ("Fingering", 45, 450000, 35000),
        ("Worsted", 35, 380000, 28000),
        ("DK", 28, 290000, 22000),
        ("Bulky", 18, 180000, 18000),
    ]

    for weight, count, total_proj, avg_pop in categories:
        print(f"    {weight:12} → {count:2} yarns, {total_proj:7,} projects, avg popularity: {avg_pop:,}")

    print("\n  💡 Agent insight: 'Fingering weight dominates!'")

    print("\n📊 Analysis 3: Trends by Fiber")
    print("\n  Agent groups by fiber type:")

    fibers = [
        ("Wool", 78, 600000),
        ("Alpaca", 32, 180000),
        ("Cotton", 24, 120000),
        ("Silk", 16, 90000),
    ]

    for fiber, count, total_proj in fibers:
        print(f"    {fiber:12} → {count:2} yarns, {total_proj:7,} projects")

    print("\n  💡 Agent insight: 'Wool is most popular by far'")

    print("\n📊 Analysis 4: Generate Natural Language Insights")
    print("\n  Agent autonomously identifies what's INTERESTING:")
    insights = [
        "Analyzed 150 yarns with 1,823,456 total projects (avg: 12,156 per yarn)",
        "Most popular weight: Fingering (450,000 projects across 45 yarns)",
        "Most popular fiber: Wool (600,000 projects)",
        "Rising stars: Hedgehog Fibres Skinny Singles, Manos del Uruguay Merino Cloud"
    ]
    for i, insight in enumerate(insights, 1):
        print(f"    {i}. {insight}")

    print("\n✅ All analyses complete with contextual insights!")


def demo_report_generation():
    """Demo: How the agent formats the final report."""
    print_step(6, "Report Generation - CONTEXTUAL PRESENTATION")

    print("\n📝 Agent assembles final report:")
    print("\n  🎯 Decision: Use 'trend_report' format")
    print("    Reasoning: Comprehensive insights needed for trend query")
    print()
    print("  Structure chosen:")
    print("    1. Executive Summary (key insights)")
    print("    2. Trends by Weight (ordered by popularity)")
    print("    3. Trends by Fiber (ordered by popularity)")
    print("    4. Rising Stars (with buzz ratios)")
    print("    5. Context and explanations (not just numbers!)")

    print("\n📄 Generated Report Preview:")
    print("\n" + "─"*70)

    report = """# Yarn Trend Analysis Report

**Generated:** 2024-12-11 14:30:45

---

## 📊 Executive Summary

- Analyzed 150 yarns with 1,823,456 total projects (avg: 12,156 per yarn)
- Most popular weight: Fingering (450,000 projects across 45 yarns)
- Most popular fiber: Wool (600,000 projects)
- Rising stars: Hedgehog Fibres Skinny Singles, Manos Merino Cloud

---

## 🧶 Trends by Yarn Weight

1. **Fingering** - 450,000 projects across 45 yarns
   - Top yarn: Malabrigo Rios (45,678 projects)
2. **Worsted** - 380,000 projects across 35 yarns
   - Top yarn: Cascade 220 (38,901 projects)

## ⭐ Rising Stars

Yarns showing strong momentum:
- **Hedgehog Fibres Skinny Singles** (Fingering)
  - 5,234 projects, 3,456 queued, 2,890 favorites
  - Buzz ratio: 1.21 ← HIGH FUTURE INTEREST!

[... full report continues ...]"""

    print(report)
    print("─"*70)

    print("\n💡 Note the agentic qualities:")
    print("  ✓ Contextual explanations (not just numbers)")
    print("  ✓ Prioritized by relevance")
    print("  ✓ Highlights most important findings")
    print("  ✓ Explains WHY trends matter")
    print("\n✅ Report complete and returned to user!")


def demo_comparison():
    """Demo: Traditional vs Agentic approach."""
    print_section("TRADITIONAL vs AGENTIC COMPARISON")

    print("\n❌ TRADITIONAL SCRIPTING APPROACH:")
    print("""
    def get_trending_yarns():
        # YOU make every decision
        response = requests.get("ravelry.com/api/yarns?limit=50")  # Manual limit
        yarns = response.json()["yarns"]

        # YOU define the logic
        filtered = [y for y in yarns if y["projects"] > 1000]  # Manual threshold
        sorted_yarns = sorted(filtered, key=lambda y: y["projects"], reverse=True)

        # YOU format the output
        for yarn in sorted_yarns[:10]:  # Manual limit
            print(f"{yarn['name']}: {yarn['projects']} projects")  # Manual format

    # Problems:
    # - No autonomous decisions
    # - Single fixed approach
    # - No insights, just data
    # - Breaks if requirements change
    """)

    print("\n✅ AGENTIC APPROACH:")
    print("""
    # User specifies GOAL, not HOW
    report = agent.analyze("What yarn trends are emerging?")

    # Agent autonomously decides:
    # 1. Data Collection Strategy:
    #    → Determined 150 yarns needed (not 50, not 500)
    #    → Chose get_popular_yarns() tool
    #    → Handled pagination automatically
    #    → Applied rate limiting

    # 2. Analysis Strategy:
    #    → Defined "emerging" = high buzz ratio
    #    → Compared across multiple dimensions (weight, fiber, brand)
    #    → Calculated composite popularity scores
    #    → Identified patterns autonomously

    # 3. Presentation Strategy:
    #    → Generated contextual insights
    #    → Prioritized most relevant information
    #    → Formatted as comprehensive report
    #    → Explained WHY trends matter

    # Benefits:
    # ✓ Autonomous decisions at every step
    # ✓ Adapts to different queries
    # ✓ Provides insights, not just data
    # ✓ Self-correcting and robust
    """)


def demo_decision_points():
    """Highlight where autonomous decisions happen."""
    print_section("KEY AGENTIC DECISION POINTS")

    decisions = [
        {
            "point": "Query Interpretation",
            "input": '"What yarn trends are emerging?"',
            "decision": "Interpret 'emerging' as rising momentum, not established popularity",
            "method": "Semantic understanding (AI) or keyword matching (rules)",
            "impact": "Determines entire analysis strategy"
        },
        {
            "point": "Sample Size",
            "input": "Need trend data",
            "decision": "Collect 150 yarns (statistically significant, not excessive)",
            "method": "Heuristic based on query scope",
            "impact": "Balances accuracy vs API costs"
        },
        {
            "point": "Metric Definition",
            "input": "What makes a yarn 'rising'?",
            "decision": "Buzz ratio = (queued + favorites) / projects",
            "method": "Domain knowledge encoded in analyzer",
            "impact": "Defines what 'rising star' means"
        },
        {
            "point": "Threshold Selection",
            "input": "Filter noise from results",
            "decision": "Minimum 100 projects to qualify",
            "method": "Statistical significance heuristic",
            "impact": "Quality vs quantity tradeoff"
        },
        {
            "point": "Category Comparison",
            "input": "Show WHERE trends emerge",
            "decision": "Analyze by weight, fiber, AND brand",
            "method": "Multi-dimensional analysis",
            "impact": "Richer insights than single dimension"
        },
        {
            "point": "Insight Generation",
            "input": "Raw analysis results",
            "decision": "Identify and explain most significant patterns",
            "method": "Autonomous pattern detection",
            "impact": "Actionable insights vs data dump"
        }
    ]

    for i, d in enumerate(decisions, 1):
        print(f"\n🎯 DECISION {i}: {d['point']}")
        print(f"   Input:    {d['input']}")
        print(f"   Decision: {d['decision']}")
        print(f"   Method:   {d['method']}")
        print(f"   Impact:   {d['impact']}")


def main():
    """Run the complete demo."""
    print("\n" + "╔" + "═"*78 + "╗")
    print("║" + " "*20 + "YARN TREND AGENT - EXECUTION DEMO" + " "*25 + "║")
    print("╚" + "═"*78 + "╝")

    demo_query_interpretation()

    input("\n\n[Press Enter to continue to Data Collection...]")
    demo_data_collection()

    input("\n\n[Press Enter to continue to Data Parsing...]")
    demo_parsing()

    input("\n\n[Press Enter to continue to Trend Analysis...]")
    demo_analysis()

    input("\n\n[Press Enter to continue to Report Generation...]")
    demo_report_generation()

    input("\n\n[Press Enter to see Traditional vs Agentic Comparison...]")
    demo_comparison()

    input("\n\n[Press Enter to see Key Decision Points...]")
    demo_decision_points()

    print_section("DEMO COMPLETE")
    print("\n✨ This demonstrates the 'agency' in the system:")
    print("   • Autonomous decision-making at each step")
    print("   • Multi-step reasoning and planning")
    print("   • Intelligent tool orchestration")
    print("   • Goal-oriented behavior (WHAT, not HOW)")
    print("   • Contextual insight generation")
    print("\n💡 The agent doesn't just execute - it DECIDES how to achieve goals!\n")


if __name__ == "__main__":
    main()
