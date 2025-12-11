# 🧶 Yarn Trend Agent

An **agentic system** for analyzing yarn trends on Ravelry. This project demonstrates how to transform a simple web scraping task into an intelligent, autonomous agent that can interpret natural language queries and generate insightful trend reports.

## What Makes This "Agentic"?

Traditional scraping approach:
```python
# You decide everything
scrape_yarn("Malabrigo", "Rios")
# Returns raw data
```

Agentic approach:
```python
# Agent decides HOW to fulfill your goal
agent.analyze("What yarn trends are emerging in 2024?")

# The agent autonomously:
# 1. Interprets your query
# 2. Decides which yarns to sample
# 3. Determines relevant analyses
# 4. Generates actionable insights
```

### Key Agentic Features

1. **Autonomous Decision-Making** - The agent decides what data to collect based on the query
2. **Multi-Step Reasoning** - Plans and executes complex analysis pipelines
3. **Tool Orchestration** - Combines scraping, analysis, and reporting intelligently
4. **Natural Language Interface** - Understands intent, not just commands
5. **Contextual Insights** - Doesn't just show data, explains what it means

## Architecture

```
User Query
    ↓
Agent Orchestrator (Claude-powered)
    ↓
[Plans strategy autonomously]
    ↓
Tools:
  - Ravelry Client (data collection)
  - Trend Analyzer (pattern detection)
  - Report Generator (insights)
    ↓
Formatted Report
```

## Features

- 📊 **Comprehensive Trend Analysis** - Analyze by weight, fiber type, and brand
- ⭐ **Rising Stars Detection** - Find yarns gaining momentum
- 👑 **Established Classics** - Identify time-tested favorites
- 🔍 **Smart Sampling** - Agent autonomously decides what data to collect
- 📝 **Intelligent Reports** - Generates insights, not just data dumps
- 🤖 **AI-Powered Planning** - Uses Claude to interpret queries (optional)

## Setup

### 1. Install Dependencies

```bash
pip install -e .
```

### 2. Get API Credentials

#### Ravelry API (Required)
1. Visit https://www.ravelry.com/pro/developer
2. Create an application
3. Save your **Access Key** and **Personal Key**

#### Anthropic API (Optional - for AI-powered planning)
1. Visit https://console.anthropic.com/
2. Create an API key
3. This enables Claude-powered query interpretation
4. Without it, the agent uses rule-based planning (still works!)

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your credentials
```

## Usage

### Command Line Interface

```bash
# Basic trend analysis
python -m src.yarn_agent.cli "What are the current yarn trends?"

# Find rising trends
python -m src.yarn_agent.cli "What yarn trends are emerging in 2024?"

# Analyze specific category
python -m src.yarn_agent.cli "Show me trends for fingering weight yarns"

# Brand analysis
python -m src.yarn_agent.cli "Which yarn brands are most popular?"

# Save report to file
python -m src.yarn_agent.cli "What are the trends?" -o report.md

# Use rule-based planning (no AI)
python -m src.yarn_agent.cli "What are the trends?" --no-ai
```

### Programmatic Usage

```python
from src.yarn_agent.agents.trend_agent import TrendAgent

# Initialize agent
agent = TrendAgent(
    ravelry_access_key="your_key",
    ravelry_personal_key="your_key",
    anthropic_api_key="your_key"  # Optional
)

# Ask a question in natural language
report = agent.analyze("What yarn trends are emerging in 2024?")
print(report)
```

### Example Queries

The agent understands natural language queries like:

- "What are the current yarn trends?"
- "Which fiber types are most popular?"
- "Show me rising stars in the yarn world"
- "Compare fingering weight vs worsted weight popularity"
- "What brands are trending?"
- "Find me established classics that are still popular"

## Example Output

```markdown
# Yarn Trend Analysis Report

## 📊 Executive Summary
- Analyzed 100 yarns with 1,234,567 total projects (avg: 12,346 per yarn)
- Most popular weight: Fingering (456,789 projects across 35 yarns)
- Most popular fiber: Wool (678,901 projects)
- Rising stars (high buzz ratio): Hedgehog Fibres Skinny Singles, ...

## 🧶 Trends by Yarn Weight
1. **Fingering** - 456,789 projects across 35 yarns
   - Top yarn: Malabrigo Rios (45,678 projects)
2. **Worsted** - 345,678 projects across 28 yarns
   ...

## ⭐ Rising Stars
Yarns showing strong momentum:
- **Hedgehog Fibres Skinny Singles** (Fingering)
  - 12,345 projects, 8,901 queued, 5,678 favorites
  - Buzz ratio: 1.18
...
```

## Project Structure

```
yarn_agent/
├── src/yarn_agent/
│   ├── agents/
│   │   └── trend_agent.py      # Main agentic orchestrator
│   ├── tools/
│   │   ├── ravelry_client.py   # Data collection tool
│   │   ├── trend_analyzer.py   # Analysis tool
│   │   └── report_generator.py # Reporting tool
│   ├── models/
│   │   └── yarn.py             # Data models
│   └── cli.py                  # Command-line interface
├── examples/
│   └── basic_usage.py          # Usage examples
├── pyproject.toml
└── .env.example
```

## How It's Agentic

### Traditional Approach
```python
# You control everything
yarns = scrape_ravelry(brand="Malabrigo")
filtered = [y for y in yarns if y.weight == "Fingering"]
sorted_yarns = sorted(filtered, key=lambda y: y.projects)
print_table(sorted_yarns)
```

### Agentic Approach
```python
# Agent decides the approach
agent.analyze("Show me popular Malabrigo fingering weight yarns")

# Behind the scenes, the agent:
# 1. Parses intent: user wants Malabrigo + fingering weight
# 2. Decides: search by brand + filter by weight
# 3. Determines: popularity metrics matter (not just count)
# 4. Chooses: comparative report format
# 5. Generates: insights like "Malabrigo dominates fingering weight"
```

## Advanced: Direct Tool Usage

You can also use the tools directly (non-agentic):

```python
from src.yarn_agent.tools import RavelryClient, TrendAnalyzer

client = RavelryClient(access_key="...", personal_key="...")
analyzer = TrendAnalyzer()

# Manual control
yarns = client.get_popular_yarns(limit=50, weight="Fingering")
trends = analyzer.analyze_by_brand(yarns)
```

## Why This Is a Great Agentic Example

1. **Clear Value Add** - The agent does more than scripting could
2. **Autonomous Decisions** - Chooses sampling strategy, analysis depth
3. **Complex Orchestration** - Combines multiple tools intelligently
4. **Natural Interface** - Users describe goals, not steps
5. **Contextual Intelligence** - Generates insights, not just data

## Future Enhancements

Potential agentic features to add:

- 🔄 **Time-series Analysis** - Track trends over time
- 🎯 **Personalized Recommendations** - "Find yarns for MY project"
- 📸 **Image Analysis** - Analyze yarn photos for color trends
- 💰 **Price Tracking** - Monitor pricing across retailers
- 🌐 **Multi-source Data** - Combine Ravelry + Instagram + Reddit
- 🤝 **Interactive Mode** - Ask follow-up questions

## Contributing

This is a demonstration project showing agentic architecture. Feel free to:
- Add new analysis types
- Improve the planning logic
- Add more data sources
- Create visualizations

## License

MIT License - see LICENSE file for details

## Credits

- Ravelry API: https://www.ravelry.com/api
- Claude by Anthropic: https://www.anthropic.com/
- Inspired by the question: "How do I make scraping more agentic?"
