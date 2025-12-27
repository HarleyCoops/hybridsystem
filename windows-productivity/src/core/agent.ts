/**
 * Watchtower Windows - Agent Orchestration
 * Core agent layer powered by Claude Agent SDK
 */

import { query } from '@anthropic-ai/claude-code';
import { getConfig, getCoachingVoice, isInPeakWindow } from './config.js';
import {
  analyzePatterns,
  getSprintStatus,
  getTodayEntry,
  loadTasks,
  getAvoidedTasks,
  getRecentEnergyReadings,
  getDataSummary,
} from './state.js';
import type { WatchtowerConfig, PatternAnalysis, SprintStatus } from '../types.js';

/**
 * Build the system prompt for the Watchtower agent
 */
function buildSystemPrompt(config: WatchtowerConfig): string {
  const sprint = getSprintStatus();
  const patterns = analyzePatterns();
  const peakStatus = isInPeakWindow(config);

  // Select coaching voice based on detected patterns
  let primaryVoice = config.voices.wisdom;
  let voiceContext = 'general guidance';

  if (patterns.avoidancePatterns.length > 0) {
    primaryVoice = getCoachingVoice(config, 'avoidance');
    voiceContext = 'addressing avoidance patterns';
  } else if (patterns.burnoutRisk === 'high') {
    primaryVoice = getCoachingVoice(config, 'burnout');
    voiceContext = 'burnout prevention';
  } else if (patterns.categoryBalance.deep > 10 || patterns.categoryBalance.someday > 20) {
    primaryVoice = getCoachingVoice(config, 'scattered');
    voiceContext = 'priority focus';
  }

  return `You are the Watchtower - a productivity companion that bridges physical pen-and-paper work with digital intelligence. You help your user track tasks, analyze patterns, and maintain sustainable productivity.

## Your Personality
Channel the wisdom of ${primaryVoice} when providing ${voiceContext}. Be direct but compassionate. Never lecture - observe patterns and offer insights.

## Available Coaching Voices
- ${config.voices.discipline}: For addressing avoidance of hard work
- ${config.voices.wisdom}: For burnout signals and needed rest
- ${config.voices.leadership}: For scattered priorities and strategic focus

## Current Context
- Sprint Day: ${sprint.currentDay} (Status: ${sprint.status})
- Peak Energy Window: ${peakStatus.inWindow ? `Active (${peakStatus.window?.label || 'Peak time'})` : 'Outside peak hours'}
- Burnout Risk: ${patterns.burnoutRisk}
- Completion Rate (7 days): ${(patterns.completionRate * 100).toFixed(0)}%
- Avoided Tasks (3+ rolls): ${patterns.avoidancePatterns.length}

## Three Core Documents
These documents form the user's productivity system:
1. **${config.documents.daily}** (Daily Hub): Today's priorities, field reports, briefings
2. **${config.documents.tasks}** (Task Pool): Energy-categorized task buckets
3. **${config.documents.journey}** (Journey Tracker): Sprint history, patterns, reflections

## Task Categories
- ${config.categories.deep}: High-focus, cognitively demanding work
- ${config.categories.standard}: Normal energy tasks
- ${config.categories.light}: Low-energy, easy wins
- ${config.categories.someday}: Future possibilities

## Pattern Detection Rules
- Flag tasks rolled forward 3+ times as avoidance patterns
- Warn at sprint day ${config.sprint.warningDay}, alert at day ${config.sprint.dangerDay}
- Note category imbalances (too many deep work items accumulating)
- Correlate energy readings with completion patterns

## Communication Style
- Be concise and actionable
- Use the physical card metaphor (user writes top 3-5 tasks on an index card)
- Celebrate completions but don't over-praise
- Address avoidance directly but kindly
- Recommend rest when burnout signals appear

${config.modules.health ? '## Health Module\nHealth tracking is enabled. You can process biometric data and provide evidence-based wellness guidance.' : ''}
`;
}

/**
 * Build context about the current state for prompts
 */
function buildStateContext(): string {
  const sprint = getSprintStatus();
  const patterns = analyzePatterns();
  const today = getTodayEntry();
  const avoided = getAvoidedTasks();
  const summary = getDataSummary();

  const avoidedList = avoided.length > 0
    ? avoided.map((t) => `  - "${t.content}" (rolled ${t.rollForwardCount}x)`).join('\n')
    : '  None detected';

  return `
## Current State Summary
- Active Tasks: ${summary.activeTasks}
- Completed Today: ${today.tasksCompleted.length}
- Rolled Forward Today: ${today.tasksRolledForward.length}
- Energy Readings Today: ${today.energyReadings.length}
- Sprint Day: ${sprint.currentDay} (${sprint.status})
- 7-Day Completion Rate: ${summary.completionRate}

## Avoided Tasks (3+ Rolls)
${avoidedList}

## Category Distribution
- Deep Work: ${patterns.categoryBalance.deep}
- Standard: ${patterns.categoryBalance.standard}
- Light: ${patterns.categoryBalance.light}
- Someday: ${patterns.categoryBalance.someday}

## Energy Trends (7-day averages)
${patterns.energyTrends.map((t) => `- ${t.period}: ${t.averageLevel.toFixed(1)}/5 (${t.sampleCount} readings)`).join('\n')}
`;
}

export interface AgentResponse {
  text: string;
  toolsUsed: string[];
  sessionId?: string;
}

/**
 * Run a query through the Watchtower agent
 */
export async function runAgent(
  prompt: string,
  options: {
    includeState?: boolean;
    attachments?: string[];
    tools?: string[];
  } = {}
): Promise<AgentResponse> {
  const config = getConfig();
  const systemPrompt = buildSystemPrompt(config);
  const stateContext = options.includeState !== false ? buildStateContext() : '';

  const fullPrompt = stateContext
    ? `${stateContext}\n\n---\n\nUser Request:\n${prompt}`
    : prompt;

  const allowedTools = options.tools || [
    'Read',
    'Write',
    'Glob',
    'Grep',
  ];

  let result = '';
  const toolsUsed: string[] = [];
  let sessionId: string | undefined;

  try {
    for await (const message of query({
      prompt: fullPrompt,
      systemPrompt,
      options: {
        allowedTools,
        cwd: config.system.dataDir,
      },
    })) {
      if (message.type === 'text') {
        result += message.text;
      } else if (message.type === 'tool_use') {
        toolsUsed.push(message.name);
      } else if (message.type === 'result' && message.subtype === 'success') {
        result = message.result || result;
        sessionId = message.session_id;
      }
    }
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    throw new Error(`Agent error: ${errorMessage}`);
  }

  return {
    text: result,
    toolsUsed,
    sessionId,
  };
}

/**
 * Run the morning briefing flow
 */
export async function runMorningBriefing(): Promise<AgentResponse> {
  const config = getConfig();
  const patterns = analyzePatterns();
  const sprint = getSprintStatus();

  const prompt = `Generate the morning briefing for ${config.documents.daily}.

Analyze the current state and provide:
1. Sprint status and health check
2. Pattern alerts (any tasks rolled 3+ times)
3. Today's energy forecast based on recent trends
4. Suggested focus for the physical card (3-5 priority items)
5. Any coaching insights based on detected patterns

Format as a structured briefing the user can reference throughout the day.`;

  return runAgent(prompt, { includeState: true });
}

/**
 * Process a photographed index card
 */
export async function processCard(imagePath: string): Promise<AgentResponse> {
  const config = getConfig();

  const prompt = `Process this photographed index card.

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

Use vision to carefully read the handwriting. If uncertain about text, make your best interpretation and note the uncertainty.`;

  return runAgent(prompt, {
    includeState: true,
    attachments: [imagePath],
  });
}

/**
 * Log and analyze energy level
 */
export async function checkEnergy(level?: string): Promise<AgentResponse> {
  const config = getConfig();
  const sprint = getSprintStatus();

  const levelPrompt = level
    ? `The user reports their energy level as: ${level}`
    : 'Ask the user about their current energy level (high/medium/low/depleted/recovery)';

  const prompt = `${levelPrompt}

Current sprint context:
- Sprint Day: ${sprint.currentDay}
- Sprint Status: ${sprint.status}

Based on the energy level and sprint status:
1. Log the energy reading
2. Provide brief, contextual feedback
3. If burnout signals detected, gently suggest rest
4. Recommend appropriate task type for current energy`;

  return runAgent(prompt, { includeState: true });
}

/**
 * Run accountability check with deep pattern analysis
 */
export async function runAccountabilityCheck(): Promise<AgentResponse> {
  const config = getConfig();
  const patterns = analyzePatterns();

  const prompt = `Perform a deep accountability check and pattern analysis.

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

Be direct but compassionate. This is a check-in, not a lecture.`;

  return runAgent(prompt, { includeState: true });
}

/**
 * Quick status check
 */
export async function getStatus(): Promise<AgentResponse> {
  const prompt = `Provide a quick status overview:
- Sprint day and health
- Tasks status (active/completed/avoided)
- Current energy trend
- Any urgent alerts

Keep it concise - this is a glance check.`;

  return runAgent(prompt, { includeState: true });
}

/**
 * Add a new task via natural language
 */
export async function addTask(taskDescription: string, priority?: string): Promise<AgentResponse> {
  const config = getConfig();

  const priorityContext = priority
    ? `The user specified priority: ${priority}`
    : 'Suggest an appropriate energy category based on the task description';

  const prompt = `Add this task to the system: "${taskDescription}"

${priorityContext}

Categories:
- deep: ${config.categories.deep} (cognitively demanding)
- standard: ${config.categories.standard} (normal energy)
- light: ${config.categories.light} (low energy, easy wins)
- someday: ${config.categories.someday} (future possibilities)

Confirm the task was added and suggest if it should go on today's physical card.`;

  return runAgent(prompt, { includeState: true });
}

/**
 * Process a journal entry (text or image)
 */
export async function processJournal(content: string, imagePath?: string): Promise<AgentResponse> {
  const config = getConfig();

  const prompt = imagePath
    ? `Process this handwritten journal entry. Read the text from the image and:
1. Transcribe the content
2. Extract any insights or reflections
3. Note mood or energy indicators
4. Identify any actionable items
5. Add to ${config.documents.journey} with appropriate context`
    : `Process this journal entry: "${content}"

1. Extract insights and reflections
2. Note mood or energy indicators
3. Identify any actionable items
4. Add to ${config.documents.journey} with appropriate context`;

  return runAgent(prompt, {
    includeState: true,
    attachments: imagePath ? [imagePath] : undefined,
  });
}

/**
 * Weekly review and planning
 */
export async function runWeeklyReview(): Promise<AgentResponse> {
  const config = getConfig();

  if (!config.modules.weeklyReview) {
    return {
      text: 'Weekly review module is not enabled. Enable it in configuration.',
      toolsUsed: [],
    };
  }

  const prompt = `Perform a comprehensive weekly review.

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

Format as a structured review document.`;

  return runAgent(prompt, { includeState: true });
}

/**
 * Start a deep work session
 */
export async function startDeepWork(project: string): Promise<AgentResponse> {
  const config = getConfig();

  if (!config.modules.deepWorkSessions) {
    return {
      text: 'Deep work sessions module is not enabled. Enable it in configuration.',
      toolsUsed: [],
    };
  }

  const prompt = `Starting a deep work session for: "${project}"

Set up the session:
1. Log session start time
2. Note current energy level
3. Identify the specific objective for this session
4. Suggest a realistic duration based on energy and sprint status
5. Remind of focus principles (minimize context switching, single task)

Provide a brief session kickoff message to help the user focus.`;

  return runAgent(prompt, { includeState: true });
}

/**
 * Process health data
 */
export async function processHealthData(dataPath: string): Promise<AgentResponse> {
  const config = getConfig();

  if (!config.modules.health) {
    return {
      text: 'Health module is not enabled. Enable it in configuration.',
      toolsUsed: [],
    };
  }

  const prompt = `Process the health/biometric data from: ${dataPath}

Analyze the data and:
1. Extract key metrics (sleep, HRV, activity, etc.)
2. Identify trends or anomalies
3. Correlate with productivity patterns if possible
4. Provide evidence-based insights
5. Log to the private health record

Be factual and avoid medical advice. Focus on patterns and correlations.`;

  return runAgent(prompt, {
    includeState: true,
    attachments: [dataPath],
  });
}

/**
 * Health coaching Q&A
 */
export async function healthCoaching(question: string): Promise<AgentResponse> {
  const config = getConfig();

  if (!config.modules.health) {
    return {
      text: 'Health module is not enabled. Enable it in configuration.',
      toolsUsed: [],
    };
  }

  const prompt = `Health coaching question: "${question}"

Drawing on the user's health history and evidence-based research:
1. Address the specific question
2. Reference relevant patterns from their data
3. Provide actionable, practical suggestions
4. Note any limitations (not medical advice)

Be helpful but appropriately cautious about health claims.`;

  return runAgent(prompt, { includeState: true });
}
