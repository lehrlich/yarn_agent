"""
The main Trend Agent - the orchestrator that makes this system "agentic".

This agent uses Claude to interpret user queries and autonomously decide:
- What data to collect
- How to analyze it
- What insights to surface
- How to present the results
"""

import os
from typing import List, Dict, Any, Optional
from anthropic import Anthropic

from ..tools.ravelry_client import RavelryClient
from ..tools.trend_analyzer import TrendAnalyzer
from ..tools.report_generator import ReportGenerator
from ..models.yarn import Yarn


class TrendAgent:
    """
    An agentic system for analyzing yarn trends.

    This agent autonomously:
    1. Interprets natural language queries
    2. Plans data collection strategies
    3. Executes analysis
    4. Generates insights and reports
    """

    SYSTEM_PROMPT = """You are an expert yarn trend analyst agent. Your job is to help users understand trends in the yarn crafting community by analyzing data from Ravelry.

You have access to these tools:
1. **ravelry_client**: Fetch yarn data from Ravelry
   - search_yarns(query, weight, fiber, sort)
   - get_popular_yarns(limit, weight, fiber)
   - get_yarns_by_category(category, limit)

2. **trend_analyzer**: Analyze yarn data for patterns
   - analyze_by_weight(yarns)
   - analyze_by_fiber(yarns)
   - analyze_by_brand(yarns)
   - identify_rising_stars(yarns)
   - identify_classics(yarns)
   - compare_categories(category_a, category_b)
   - generate_insights(yarns)

3. **report_generator**: Create formatted reports
   - generate_trend_report(...)
   - generate_comparison_report(...)
   - generate_simple_report(yarns, title)

When given a user query, you should:
1. Determine what data to collect (which categories, how many samples)
2. Decide which analyses are relevant
3. Generate actionable insights

Be autonomous - make decisions about sampling strategy, analysis depth, and presentation.
Focus on finding interesting patterns and actionable recommendations.

Respond with a JSON plan that specifies:
{
  "strategy": "brief description of your approach",
  "data_collection": [
    {"action": "get_popular_yarns", "params": {"limit": 100}},
    {"action": "get_yarns_by_category", "params": {"category": "Fingering", "limit": 50}}
  ],
  "analyses": ["by_weight", "by_fiber", "rising_stars", "classics"],
  "report_type": "trend_report"
}
"""

    def __init__(
        self,
        ravelry_access_key: str,
        ravelry_personal_key: str,
        anthropic_api_key: Optional[str] = None,
    ):
        """
        Initialize the Trend Agent.

        Args:
            ravelry_access_key: Ravelry API access key
            ravelry_personal_key: Ravelry API personal key
            anthropic_api_key: Anthropic API key (uses ANTHROPIC_API_KEY env var if not provided)
        """
        self.ravelry_client = RavelryClient(ravelry_access_key, ravelry_personal_key)
        self.trend_analyzer = TrendAnalyzer()
        self.report_generator = ReportGenerator()

        # Initialize Claude client for agentic reasoning
        api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        if api_key:
            self.anthropic = Anthropic(api_key=api_key)
        else:
            self.anthropic = None
            print("⚠️ No Anthropic API key provided - using rule-based planning instead")

    def analyze(self, query: str) -> str:
        """
        Main entry point - analyze a user query and return a report.

        This is the agentic magic: the agent interprets the query and
        autonomously decides how to fulfill it.

        Args:
            query: User's natural language query

        Returns:
            Formatted report as a string
        """
        print(f"\n🤖 Agent received query: '{query}'")
        print("📝 Planning analysis strategy...\n")

        # Get analysis plan (agentic decision-making)
        if self.anthropic:
            plan = self._plan_with_claude(query)
        else:
            plan = self._plan_with_rules(query)

        print(f"📋 Strategy: {plan.get('strategy', 'Analyzing yarn trends')}\n")

        # Execute data collection
        print("📊 Collecting data from Ravelry...")
        yarns = self._collect_data(plan["data_collection"])
        print(f"✓ Collected {len(yarns)} yarns\n")

        # Execute analyses
        print("🔍 Analyzing trends...")
        results = self._execute_analyses(yarns, plan["analyses"])
        print("✓ Analysis complete\n")

        # Generate report
        print("📝 Generating report...")
        report = self._generate_report(results, plan["report_type"])
        print("✓ Report generated\n")

        return report

    def _plan_with_claude(self, query: str) -> Dict[str, Any]:
        """
        Use Claude to create an analysis plan (agentic reasoning).

        Args:
            query: User query

        Returns:
            Analysis plan dictionary
        """
        try:
            response = self.anthropic.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                system=self.SYSTEM_PROMPT,
                messages=[
                    {
                        "role": "user",
                        "content": f"Create an analysis plan for this query: {query}"
                    }
                ]
            )

            # Parse Claude's response (should be JSON)
            import json
            plan_text = response.content[0].text

            # Extract JSON from response (might be in markdown code block)
            if "```json" in plan_text:
                plan_text = plan_text.split("```json")[1].split("```")[0].strip()
            elif "```" in plan_text:
                plan_text = plan_text.split("```")[1].split("```")[0].strip()

            plan = json.loads(plan_text)
            return plan

        except Exception as e:
            print(f"⚠️ Error using Claude for planning: {e}")
            print("Falling back to rule-based planning\n")
            return self._plan_with_rules(query)

    def _plan_with_rules(self, query: str) -> Dict[str, Any]:
        """
        Create an analysis plan using rules (fallback if no Claude API).

        Args:
            query: User query

        Returns:
            Analysis plan dictionary
        """
        query_lower = query.lower()

        # Detect intent from query keywords
        if "compare" in query_lower or "vs" in query_lower:
            return {
                "strategy": "Compare two yarn categories",
                "data_collection": [
                    {"action": "get_popular_yarns", "params": {"limit": 100}}
                ],
                "analyses": ["by_weight", "by_fiber", "compare"],
                "report_type": "comparison_report"
            }
        elif "rising" in query_lower or "trending" in query_lower or "emerging" in query_lower:
            return {
                "strategy": "Identify rising trends and emerging yarns",
                "data_collection": [
                    {"action": "get_popular_yarns", "params": {"limit": 150}}
                ],
                "analyses": ["rising_stars", "by_weight", "by_fiber"],
                "report_type": "trend_report"
            }
        elif "brand" in query_lower or "company" in query_lower:
            return {
                "strategy": "Analyze trends by yarn brand",
                "data_collection": [
                    {"action": "get_popular_yarns", "params": {"limit": 200}}
                ],
                "analyses": ["by_brand", "classics"],
                "report_type": "trend_report"
            }
        else:
            # Default comprehensive analysis
            return {
                "strategy": "Comprehensive trend analysis across all categories",
                "data_collection": [
                    {"action": "get_popular_yarns", "params": {"limit": 100}}
                ],
                "analyses": ["by_weight", "by_fiber", "by_brand", "rising_stars", "classics"],
                "report_type": "trend_report"
            }

    def _collect_data(self, collection_plan: List[Dict[str, Any]]) -> List[Yarn]:
        """
        Execute data collection according to plan.

        Args:
            collection_plan: List of data collection actions

        Returns:
            List of collected Yarn objects
        """
        all_yarns = []
        seen_ids = set()

        for action in collection_plan:
            action_name = action["action"]
            params = action.get("params", {})

            try:
                if action_name == "get_popular_yarns":
                    yarns = self.ravelry_client.get_popular_yarns(**params)
                elif action_name == "get_yarns_by_category":
                    yarns = self.ravelry_client.get_yarns_by_category(**params)
                elif action_name == "search_yarns":
                    yarns = self.ravelry_client.search_yarns(**params)
                else:
                    print(f"⚠️ Unknown action: {action_name}")
                    continue

                # Deduplicate
                for yarn in yarns:
                    if yarn.id not in seen_ids:
                        all_yarns.append(yarn)
                        seen_ids.add(yarn.id)

            except Exception as e:
                print(f"⚠️ Error in {action_name}: {e}")
                continue

        return all_yarns

    def _execute_analyses(
        self,
        yarns: List[Yarn],
        analyses: List[str]
    ) -> Dict[str, Any]:
        """
        Execute the specified analyses.

        Args:
            yarns: List of yarns to analyze
            analyses: List of analysis types to perform

        Returns:
            Dictionary of analysis results
        """
        results = {"yarns": yarns}

        if "by_weight" in analyses:
            results["weight_trends"] = self.trend_analyzer.analyze_by_weight(yarns)

        if "by_fiber" in analyses:
            results["fiber_trends"] = self.trend_analyzer.analyze_by_fiber(yarns)

        if "by_brand" in analyses:
            results["brand_trends"] = self.trend_analyzer.analyze_by_brand(yarns)

        if "rising_stars" in analyses:
            results["rising_stars"] = self.trend_analyzer.identify_rising_stars(yarns)

        if "classics" in analyses:
            results["classics"] = self.trend_analyzer.identify_classics(yarns, min_projects=500)

        # Always generate insights
        results["insights"] = self.trend_analyzer.generate_insights(yarns)

        return results

    def _generate_report(
        self,
        results: Dict[str, Any],
        report_type: str
    ) -> str:
        """
        Generate the final report.

        Args:
            results: Analysis results
            report_type: Type of report to generate

        Returns:
            Formatted report string
        """
        if report_type == "trend_report":
            return self.report_generator.generate_trend_report(
                insights=results.get("insights", []),
                weight_trends=results.get("weight_trends", []),
                fiber_trends=results.get("fiber_trends", []),
                brand_trends=results.get("brand_trends", []),
                rising_stars=results.get("rising_stars", []),
                classics=results.get("classics", []),
            )
        elif report_type == "simple_report":
            return self.report_generator.generate_simple_report(
                yarns=results["yarns"],
                title="Yarn Analysis Report"
            )
        else:
            # Default to simple report
            return self.report_generator.generate_simple_report(
                yarns=results["yarns"],
                title="Yarn Trend Report"
            )
