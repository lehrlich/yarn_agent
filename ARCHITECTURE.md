# Yarn Trend Agent - Architecture Deep Dive

## What Makes This System "Agentic"?

An agent is more than automation - it's a system that autonomously decides HOW to achieve a goal, not just executes predefined steps.

### Core Agentic Principles Applied

#### 1. Goal-Oriented Behavior
**Traditional:** Execute specific instructions
```python
scrape("Malabrigo", "Rios")  # User specifies exact steps
```

**Agentic:** Interpret goals and decide approach
```python
analyze("Find affordable merino alternatives")  # Agent decides what to search, compare, filter
```

#### 2. Autonomous Decision-Making
The agent makes decisions at multiple levels:

- **Strategic:** What data to collect? (Sample size, categories, filters)
- **Tactical:** Which analyses are relevant? (Weight vs fiber vs brand)
- **Presentational:** How to format insights? (Comparison table vs trend chart)

#### 3. Multi-Step Reasoning
The agent plans complex workflows:
```
Query: "What's trending in sock yarn?"
  ↓
Agent reasoning:
1. "Sock yarn = fingering weight"
2. "Trending = need popularity metrics + time signals"
3. "Should sample 100+ yarns for statistical significance"
4. "Compare to worsted weight as baseline"
5. "Highlight rising stars in category"
  ↓
Executes plan autonomously
```

#### 4. Tool Orchestration
The agent combines tools intelligently:
- RavelryClient for data collection
- TrendAnalyzer for pattern detection
- ReportGenerator for insights
- Claude (optional) for query interpretation

## Architecture Components

### 1. Agent Orchestrator (`trend_agent.py`)

**Purpose:** The "brain" that plans and executes

**Key Methods:**
- `analyze(query)` - Main entry point
- `_plan_with_claude(query)` - AI-powered planning
- `_plan_with_rules(query)` - Rule-based fallback
- `_collect_data(plan)` - Execute data collection
- `_execute_analyses(yarns, analyses)` - Run analyses
- `_generate_report(results, type)` - Create final output

**Agentic Aspects:**
- Interprets natural language queries
- Decides sampling strategy based on query intent
- Selects relevant analyses autonomously
- Adapts presentation format to data

### 2. Ravelry Client Tool (`ravelry_client.py`)

**Purpose:** Data collection with intelligent defaults

**Key Methods:**
- `search_yarns()` - Flexible search
- `get_popular_yarns()` - Smart sampling by popularity
- `get_yarns_by_category()` - Category-aware collection
- `get_yarn_details()` - Deep dive on specific yarn

**Agentic Aspects:**
- Autonomous pagination (knows when to stop)
- Rate limiting (respects API constraints)
- Category detection (weight vs fiber)
- Deduplication (avoids redundant data)

### 3. Trend Analyzer Tool (`trend_analyzer.py`)

**Purpose:** Pattern detection and insight generation

**Key Methods:**
- `analyze_by_weight()` - Weight category trends
- `analyze_by_fiber()` - Fiber type patterns
- `analyze_by_brand()` - Brand popularity
- `identify_rising_stars()` - Momentum detection
- `identify_classics()` - Established favorites
- `compare_categories()` - Comparative analysis
- `generate_insights()` - Natural language insights

**Agentic Aspects:**
- Autonomously determines significance thresholds
- Calculates composite metrics (popularity score)
- Detects patterns (rising vs established)
- Generates contextual insights

### 4. Report Generator Tool (`report_generator.py`)

**Purpose:** Intelligent formatting and presentation

**Key Methods:**
- `generate_trend_report()` - Comprehensive report
- `generate_comparison_report()` - Side-by-side comparison
- `generate_simple_report()` - List format

**Agentic Aspects:**
- Adapts format to data volume
- Highlights most relevant information
- Provides context (not just numbers)
- Suggests actionable next steps

## Data Flow

```
1. User Query
   ↓
2. Agent Orchestrator interprets query
   - Uses Claude for semantic understanding (if available)
   - Falls back to rule-based intent detection
   ↓
3. Agent creates execution plan
   {
     "strategy": "Analyze rising trends",
     "data_collection": [...],
     "analyses": ["rising_stars", "by_weight"],
     "report_type": "trend_report"
   }
   ↓
4. Ravelry Client collects data
   - Autonomously samples relevant yarns
   - Respects rate limits
   - Deduplicates results
   ↓
5. Trend Analyzer detects patterns
   - Calculates metrics
   - Identifies trends
   - Generates insights
   ↓
6. Report Generator formats output
   - Creates structured report
   - Highlights key findings
   - Provides context
   ↓
7. Return to user
```

## Why Traditional Scraping Isn't Agentic

### Traditional Approach
```python
def get_yarn_info(brand, name):
    """Non-agentic: User specifies exact steps"""
    html = requests.get(f"ravelry.com/yarns/{brand}/{name}")
    soup = BeautifulSoup(html)
    projects = int(soup.find("span", class_="projects").text)
    return projects

# User must know exactly what to ask for
result = get_yarn_info("Malabrigo", "Rios")
```

**Problems:**
- No autonomy (user decides everything)
- No reasoning (just executes)
- No context (returns raw number)
- No adaptation (breaks if site changes)

### Agentic Approach
```python
agent = TrendAgent(...)

# User specifies goal, not steps
result = agent.analyze("Show me popular sock yarns")

# Agent autonomously:
# - Interprets "sock yarns" → fingering weight
# - Decides "popular" → sort by projects + favorites
# - Determines sample size → 100 yarns for good coverage
# - Selects analyses → weight trends, rising stars
# - Generates insights → "Fingering weight dominates..."
```

**Benefits:**
- Autonomous (agent makes decisions)
- Reasoning (plans multi-step approach)
- Contextual (provides insights, not just data)
- Adaptive (handles variations gracefully)

## Claude Integration (Optional AI Enhancement)

When Claude API is available, the agent uses it for:

### Query Interpretation
```
User: "What's hot in indie dyed yarns?"
  ↓
Claude interprets:
- "hot" → rising trends
- "indie dyed" → small batch, hand-dyed brands
- Suggests: sample indie brands, focus on recent popularity
```

### Strategy Planning
Claude generates execution plans:
```json
{
  "strategy": "Analyze indie brand trends with focus on recent momentum",
  "data_collection": [
    {"action": "search_yarns", "params": {"query": "hand dyed", "limit": 150}},
    {"action": "get_yarns_by_category", "params": {"category": "Fingering", "limit": 50}}
  ],
  "analyses": ["by_brand", "rising_stars", "by_fiber"],
  "report_type": "trend_report"
}
```

### Insight Generation
Claude can enhance insights with:
- Contextual explanations
- Trend causation hypotheses
- Actionable recommendations

## Fallback: Rule-Based Planning

Without Claude API, the agent uses pattern matching:

```python
if "rising" in query or "trending" in query:
    plan = {
        "strategy": "Identify rising trends",
        "analyses": ["rising_stars", "by_weight"],
        ...
    }
elif "compare" in query:
    plan = {
        "strategy": "Compare categories",
        "analyses": ["compare", "by_weight", "by_fiber"],
        ...
    }
```

Still agentic because:
- Autonomous execution once plan is set
- Intelligent tool orchestration
- Context-aware reporting

## Key Agentic Patterns Used

### 1. Planning Pattern
```
Observe → Orient → Decide → Act
```
- Observe: Parse user query
- Orient: Understand intent and context
- Decide: Create execution plan
- Act: Execute with tools

### 2. Tool Selection Pattern
Agent chooses tools based on:
- Query intent
- Data requirements
- Analysis goals

### 3. Autonomous Sampling Pattern
Agent decides:
- Sample size (statistical significance)
- Categories to compare
- Depth of analysis

### 4. Insight Generation Pattern
Agent doesn't just report data, it:
- Identifies patterns
- Provides context
- Suggests implications

## Future Enhancements for More Agentic Behavior

### 1. Feedback Loop
```
Generate report → Get user feedback → Refine approach → Iterate
```

### 2. Memory System
Remember past queries to improve future responses:
- "Similar to last time but for worsted weight"
- Agent recalls previous preferences

### 3. Proactive Monitoring
Agent autonomously:
- Tracks yarns over time
- Alerts on significant changes
- Suggests analyses

### 4. Multi-Agent Collaboration
Specialized sub-agents:
- Data Collector Agent
- Analysis Agent
- Report Agent
- Monitoring Agent

### 5. Learning from Data
Improve heuristics based on results:
- What makes a "rising star"?
- Which metrics correlate with user interest?

## Conclusion

This project demonstrates agentic architecture by:

✅ **Autonomous decision-making** - Agent plans its own approach
✅ **Multi-step reasoning** - Complex workflow execution
✅ **Tool orchestration** - Intelligent tool selection and combination
✅ **Goal-oriented** - User specifies WHAT, agent decides HOW
✅ **Contextual intelligence** - Generates insights, not just data

The key difference from traditional scripting: The agent has **agency** - the ability to make decisions about how to achieve goals, not just execute predetermined steps.
