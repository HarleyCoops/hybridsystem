"""
Watchtower Windows - Agent Orchestration
Core agent layer powered by Claude Code SDK.
"""

import asyncio
from typing import Optional

from claude_code_sdk import query, ClaudeCodeOptions, Message

from watchtower.core.config import (
    get_config,
    get_coaching_voice,
    is_in_peak_window,
    get_data_dir,
)
from watchtower.core.state import (
    analyze_patterns,
    get_sprint_status,
    get_today_entry,
    get_avoided_tasks,
    get_data_summary,
)
from watchtower.types import (
    AgentResponse,
    WatchtowerConfig,
    PatternAnalysis,
)


def build_system_prompt(config: WatchtowerConfig) -> str:
    """Build the system prompt for the Watchtower agent."""
    sprint = get_sprint_status()
    patterns = analyze_patterns()
    in_peak, peak_window = is_in_peak_window(config)

    # Select coaching voice based on detected patterns
    primary_voice = config.voices.wisdom
    voice_context = "general guidance"

    if patterns.avoidance_patterns:
        primary_voice = get_coaching_voice("avoidance", config)
        voice_context = "addressing avoidance patterns"
    elif patterns.burnout_risk.value == "high":
        primary_voice = get_coaching_voice("burnout", config)
        voice_context = "burnout prevention"
    elif patterns.category_balance.deep > 10 or patterns.category_balance.someday > 20:
        primary_voice = get_coaching_voice("scattered", config)
        voice_context = "priority focus"

    peak_status = (
        f"Active ({peak_window.label or 'Peak time'})"
        if in_peak and peak_window
        else "Outside peak hours"
    )

    return f"""You are the Watchtower - a productivity companion that bridges physical pen-and-paper work with digital intelligence. You help your user track tasks, analyze patterns, and maintain sustainable productivity.

## Your Personality
Channel the wisdom of {primary_voice} when providing {voice_context}. Be direct but compassionate. Never lecture - observe patterns and offer insights.

## Available Coaching Voices
- {config.voices.discipline}: For addressing avoidance of hard work
- {config.voices.wisdom}: For burnout signals and needed rest
- {config.voices.leadership}: For scattered priorities and strategic focus

## Current Context
- Sprint Day: {sprint.current_day} (Status: {sprint.status.value})
- Peak Energy Window: {peak_status}
- Burnout Risk: {patterns.burnout_risk.value}
- Completion Rate (7 days): {patterns.completion_rate * 100:.0f}%
- Avoided Tasks (3+ rolls): {len(patterns.avoidance_patterns)}

## Three Core Documents
These documents form the user's productivity system:
1. **{config.documents.daily}** (Daily Hub): Today's priorities, field reports, briefings
2. **{config.documents.tasks}** (Task Pool): Energy-categorized task buckets
3. **{config.documents.journey}** (Journey Tracker): Sprint history, patterns, reflections

## Task Categories
- {config.categories.deep}: High-focus, cognitively demanding work
- {config.categories.standard}: Normal energy tasks
- {config.categories.light}: Low-energy, easy wins
- {config.categories.someday}: Future possibilities

## Pattern Detection Rules
- Flag tasks rolled forward 3+ times as avoidance patterns
- Warn at sprint day {config.sprint.warning_day}, alert at day {config.sprint.danger_day}
- Note category imbalances (too many deep work items accumulating)
- Correlate energy readings with completion patterns

## Communication Style
- Be concise and actionable
- Use the physical card metaphor (user writes top 3-5 tasks on an index card)
- Celebrate completions but don't over-praise
- Address avoidance directly but kindly
- Recommend rest when burnout signals appear

{"## Health Module" + chr(10) + "Health tracking is enabled. You can process biometric data and provide evidence-based wellness guidance." if config.modules.health else ""}
"""


def build_state_context() -> str:
    """Build context about the current state for prompts."""
    sprint = get_sprint_status()
    patterns = analyze_patterns()
    today = get_today_entry()
    avoided = get_avoided_tasks()
    summary = get_data_summary()

    avoided_list = (
        "\n".join(f'  - "{t.content}" (rolled {t.roll_forward_count}x)' for t in avoided)
        if avoided
        else "  None detected"
    )

    return f"""
## Current State Summary
- Active Tasks: {summary['active_tasks']}
- Completed Today: {len(today.tasks_completed)}
- Rolled Forward Today: {len(today.tasks_rolled_forward)}
- Energy Readings Today: {len(today.energy_readings)}
- Sprint Day: {sprint.current_day} ({sprint.status.value})
- 7-Day Completion Rate: {summary['completion_rate']}

## Avoided Tasks (3+ Rolls)
{avoided_list}

## Category Distribution
- Deep Work: {patterns.category_balance.deep}
- Standard: {patterns.category_balance.standard}
- Light: {patterns.category_balance.light}
- Someday: {patterns.category_balance.someday}

## Energy Trends (7-day averages)
{chr(10).join(f"- {t.period}: {t.average_level:.1f}/5 ({t.sample_count} readings)" for t in patterns.energy_trends)}
"""


async def run_agent(
    prompt: str,
    include_state: bool = True,
    attachments: Optional[list[str]] = None,
    allowed_tools: Optional[list[str]] = None,
) -> AgentResponse:
    """Run a query through the Watchtower agent."""
    config = get_config()
    system_prompt = build_system_prompt(config)
    state_context = build_state_context() if include_state else ""

    full_prompt = (
        f"{state_context}\n\n---\n\nUser Request:\n{prompt}"
        if state_context
        else prompt
    )

    tools = allowed_tools or ["Read", "Write", "Glob", "Grep"]

    options = ClaudeCodeOptions(
        system_prompt=system_prompt,
        allowed_tools=tools,
        cwd=str(get_data_dir()),
    )

    result_text = ""
    tools_used: list[str] = []
    session_id: Optional[str] = None

    try:
        async for message in query(prompt=full_prompt, options=options):
            if isinstance(message, Message):
                if message.type == "text":
                    result_text += message.content
                elif message.type == "tool_use":
                    tools_used.append(message.tool_name)
                elif message.type == "result":
                    if hasattr(message, "content"):
                        result_text = message.content or result_text
                    if hasattr(message, "session_id"):
                        session_id = message.session_id
    except Exception as e:
        raise RuntimeError(f"Agent error: {e}") from e

    return AgentResponse(
        text=result_text,
        tools_used=tools_used,
        session_id=session_id,
    )


async def run_morning_briefing() -> AgentResponse:
    """Run the morning briefing flow."""
    config = get_config()

    prompt = f"""Generate the morning briefing for {config.documents.daily}.

Analyze the current state and provide:
1. Sprint status and health check
2. Pattern alerts (any tasks rolled 3+ times)
3. Today's energy forecast based on recent trends
4. Suggested focus for the physical card (3-5 priority items)
5. Any coaching insights based on detected patterns

Format as a structured briefing the user can reference throughout the day."""

    return await run_agent(prompt, include_state=True)


async def process_card(image_path: str) -> AgentResponse:
    """Process a photographed index card."""
    prompt = f"""Process this photographed index card.

The card uses a simple notation:
- ● (filled circle) or checkmark = completed task
- ○ (empty circle) or dash = incomplete task
- Handwritten text describes each task

Please:
1. Read and transcribe all items from the card image
2. Identify which tasks are completed vs incomplete
3. For completed tasks: Mark them done in the system
4. For incomplete tasks:
   - Check if they already exist in the task pool
   - Increment their "rolled forward" count
   - Flag any hitting 3+ rolls as avoidance patterns
5. Note any new tasks that should be added
6. Provide a brief end-of-day summary

Use vision to carefully read the handwriting. If uncertain about text, make your best interpretation and note the uncertainty.

Image path: {image_path}"""

    return await run_agent(prompt, include_state=True, attachments=[image_path])


async def check_energy(level: Optional[str] = None) -> AgentResponse:
    """Log and analyze energy level."""
    sprint = get_sprint_status()

    level_prompt = (
        f"The user reports their energy level as: {level}"
        if level
        else "Ask the user about their current energy level (high/medium/low/depleted/recovery)"
    )

    prompt = f"""{level_prompt}

Current sprint context:
- Sprint Day: {sprint.current_day}
- Sprint Status: {sprint.status.value}

Based on the energy level and sprint status:
1. Log the energy reading
2. Provide brief, contextual feedback
3. If burnout signals detected, gently suggest rest
4. Recommend appropriate task type for current energy"""

    return await run_agent(prompt, include_state=True)


async def run_accountability_check() -> AgentResponse:
    """Run accountability check with deep pattern analysis."""
    prompt = """Perform a deep accountability check and pattern analysis.

Review:
1. All avoided tasks (rolled 3+ times) - what's the underlying resistance?
2. Sprint health - are we pushing too hard or coasting?
3. Energy patterns - when is the user most/least productive?
4. Category balance - is important work being avoided for easy wins?
5. Completion trends - improving or declining?

Provide:
- Honest assessment of current patterns (use appropriate coaching voice)
- Specific, actionable recommendations
- Recognition of what's working well
- One key insight the user might not see themselves

Be direct but compassionate. This is a check-in, not a lecture."""

    return await run_agent(prompt, include_state=True)


async def get_status() -> AgentResponse:
    """Quick status check."""
    prompt = """Provide a quick status overview:
- Sprint day and health
- Tasks status (active/completed/avoided)
- Current energy trend
- Any urgent alerts

Keep it concise - this is a glance check."""

    return await run_agent(prompt, include_state=True)


async def add_task_via_agent(task_description: str, priority: Optional[str] = None) -> AgentResponse:
    """Add a new task via natural language."""
    config = get_config()

    priority_context = (
        f"The user specified priority: {priority}"
        if priority
        else "Suggest an appropriate energy category based on the task description"
    )

    prompt = f"""Add this task to the system: "{task_description}"

{priority_context}

Categories:
- deep: {config.categories.deep} (cognitively demanding)
- standard: {config.categories.standard} (normal energy)
- light: {config.categories.light} (low energy, easy wins)
- someday: {config.categories.someday} (future possibilities)

Confirm the task was added and suggest if it should go on today's physical card."""

    return await run_agent(prompt, include_state=True)


async def process_journal(content: str, image_path: Optional[str] = None) -> AgentResponse:
    """Process a journal entry (text or image)."""
    config = get_config()

    if image_path:
        prompt = f"""Process this handwritten journal entry. Read the text from the image and:
1. Transcribe the content
2. Extract any insights or reflections
3. Note mood or energy indicators
4. Identify any actionable items
5. Add to {config.documents.journey} with appropriate context

Image path: {image_path}"""
    else:
        prompt = f"""Process this journal entry: "{content}"

1. Extract insights and reflections
2. Note mood or energy indicators
3. Identify any actionable items
4. Add to {config.documents.journey} with appropriate context"""

    return await run_agent(
        prompt,
        include_state=True,
        attachments=[image_path] if image_path else None,
    )


async def run_weekly_review() -> AgentResponse:
    """Weekly review and planning."""
    config = get_config()

    if not config.modules.weekly_review:
        return AgentResponse(
            text="Weekly review module is not enabled. Enable it in configuration.",
            tools_used=[],
        )

    prompt = """Perform a comprehensive weekly review.

Analyze the past 7 days:
1. Completion statistics and trends
2. Energy patterns across the week
3. Tasks that persisted (avoidance patterns)
4. Sprint health trajectory
5. Category balance over time

Provide:
- Week summary with key accomplishments
- Patterns that helped or hindered progress
- Specific recommendations for next week
- One strategic insight for improvement

Format as a structured review document."""

    return await run_agent(prompt, include_state=True)


async def start_deep_work(project: str) -> AgentResponse:
    """Start a deep work session."""
    config = get_config()

    if not config.modules.deep_work_sessions:
        return AgentResponse(
            text="Deep work sessions module is not enabled. Enable it in configuration.",
            tools_used=[],
        )

    prompt = f"""Starting a deep work session for: "{project}"

Set up the session:
1. Log session start time
2. Note current energy level
3. Identify the specific objective for this session
4. Suggest a realistic duration based on energy and sprint status
5. Remind of focus principles (minimize context switching, single task)

Provide a brief session kickoff message to help the user focus."""

    return await run_agent(prompt, include_state=True)


async def process_health_data(data_path: str) -> AgentResponse:
    """Process health data."""
    config = get_config()

    if not config.modules.health:
        return AgentResponse(
            text="Health module is not enabled. Enable it in configuration.",
            tools_used=[],
        )

    prompt = f"""Process the health/biometric data from: {data_path}

Analyze the data and:
1. Extract key metrics (sleep, HRV, activity, etc.)
2. Identify trends or anomalies
3. Correlate with productivity patterns if possible
4. Provide evidence-based insights
5. Log to the private health record

Be factual and avoid medical advice. Focus on patterns and correlations."""

    return await run_agent(prompt, include_state=True, attachments=[data_path])


async def health_coaching(question: str) -> AgentResponse:
    """Health coaching Q&A."""
    config = get_config()

    if not config.modules.health:
        return AgentResponse(
            text="Health module is not enabled. Enable it in configuration.",
            tools_used=[],
        )

    prompt = f"""Health coaching question: "{question}"

Drawing on the user's health history and evidence-based research:
1. Address the specific question
2. Reference relevant patterns from their data
3. Provide actionable, practical suggestions
4. Note any limitations (not medical advice)

Be helpful but appropriately cautious about health claims."""

    return await run_agent(prompt, include_state=True)


def run_sync(coro):
    """Run an async function synchronously."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # We're in an async context, create a new thread
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as pool:
            return pool.submit(asyncio.run, coro).result()
    else:
        return asyncio.run(coro)
