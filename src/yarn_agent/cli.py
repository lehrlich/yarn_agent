"""
Command-line interface for the Yarn Trend Agent.
"""

import os
import argparse
from dotenv import load_dotenv

from .agents.trend_agent import TrendAgent


def main():
    """Main CLI entry point."""
    # Load environment variables
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Yarn Trend Agent - Analyze yarn trends on Ravelry"
    )
    parser.add_argument(
        "query",
        nargs="+",
        help="Natural language query about yarn trends"
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output file for the report (default: stdout)"
    )
    parser.add_argument(
        "--no-ai",
        action="store_true",
        help="Use rule-based planning instead of AI (no Anthropic API key needed)"
    )

    args = parser.parse_args()
    query = " ".join(args.query)

    # Get credentials
    ravelry_access = os.getenv("RAVELRY_ACCESS_KEY")
    ravelry_personal = os.getenv("RAVELRY_PERSONAL_KEY")
    anthropic_key = None if args.no_ai else os.getenv("ANTHROPIC_API_KEY")

    if not ravelry_access or not ravelry_personal:
        print("❌ Error: Ravelry API credentials not found!")
        print("Please set RAVELRY_ACCESS_KEY and RAVELRY_PERSONAL_KEY in .env file")
        print("Get credentials at: https://www.ravelry.com/pro/developer")
        return 1

    # Initialize agent
    print("🧶 Yarn Trend Agent")
    print("=" * 60)
    agent = TrendAgent(
        ravelry_access_key=ravelry_access,
        ravelry_personal_key=ravelry_personal,
        anthropic_api_key=anthropic_key,
    )

    # Run analysis
    try:
        report = agent.analyze(query)

        # Output report
        if args.output:
            with open(args.output, "w") as f:
                f.write(report)
            print(f"✓ Report saved to: {args.output}")
        else:
            print("=" * 60)
            print(report)

        return 0

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
