/**
 * Watchtower Windows - Custom Productivity Tools
 * MCP-style tools for task management and tracking
 */

import dayjs from 'dayjs';
import {
  loadTasks,
  saveTasks,
  addTask as stateAddTask,
  completeTask,
  rollForwardTask,
  getTasksByPriority,
  getAvoidedTasks,
  logEnergy as stateLogEnergy,
  getTodayEntry,
  updateTodayEntry,
  addFieldReport,
  getSprintStatus,
  recordRestDay,
  startSession,
  endSession,
  analyzePatterns,
  getDataSummary,
} from '../core/state.js';
import { getConfig } from '../core/config.js';
import type { Task, TaskPriority, EnergyLevel } from '../types.js';

/**
 * Tool response type
 */
interface ToolResponse {
  success: boolean;
  message: string;
  data?: Record<string, unknown>;
}

// ============================================
// TASK MANAGEMENT TOOLS
// ============================================

/**
 * Add a new task to the system
 */
export function toolAddTask(
  content: string,
  priority: TaskPriority = 'standard',
  notes?: string
): ToolResponse {
  try {
    const task = stateAddTask(content, priority);
    if (notes) {
      const tasks = loadTasks();
      const t = tasks.find((x) => x.id === task.id);
      if (t) {
        t.notes = [notes];
        saveTasks(tasks);
      }
    }

    const config = getConfig();
    const categoryName = config.categories[priority];

    return {
      success: true,
      message: `Task added to ${categoryName}: "${content}"`,
      data: { taskId: task.id, priority, category: categoryName },
    };
  } catch (error) {
    return {
      success: false,
      message: `Failed to add task: ${error instanceof Error ? error.message : 'Unknown error'}`,
    };
  }
}

/**
 * Mark a task as completed
 */
export function toolCompleteTask(taskIdOrContent: string): ToolResponse {
  try {
    const tasks = loadTasks();
    // Find by ID or by content match
    let task = tasks.find((t) => t.id === taskIdOrContent);
    if (!task) {
      task = tasks.find((t) =>
        t.content.toLowerCase().includes(taskIdOrContent.toLowerCase())
      );
    }

    if (!task) {
      return {
        success: false,
        message: `Task not found: "${taskIdOrContent}"`,
      };
    }

    if (task.completedAt) {
      return {
        success: false,
        message: `Task already completed: "${task.content}"`,
      };
    }

    completeTask(task.id);

    // Update today's entry
    const entry = getTodayEntry();
    entry.tasksCompleted.push(task.id);
    updateTodayEntry(entry);

    return {
      success: true,
      message: `Completed: "${task.content}"`,
      data: { taskId: task.id, completedAt: dayjs().toISOString() },
    };
  } catch (error) {
    return {
      success: false,
      message: `Failed to complete task: ${error instanceof Error ? error.message : 'Unknown error'}`,
    };
  }
}

/**
 * Roll forward an incomplete task
 */
export function toolRollForwardTask(taskIdOrContent: string): ToolResponse {
  try {
    const tasks = loadTasks();
    let task = tasks.find((t) => t.id === taskIdOrContent);
    if (!task) {
      task = tasks.find((t) =>
        t.content.toLowerCase().includes(taskIdOrContent.toLowerCase())
      );
    }

    if (!task) {
      return {
        success: false,
        message: `Task not found: "${taskIdOrContent}"`,
      };
    }

    const updated = rollForwardTask(task.id);
    if (!updated) {
      return {
        success: false,
        message: `Failed to roll forward task`,
      };
    }

    // Update today's entry
    const entry = getTodayEntry();
    entry.tasksRolledForward.push(task.id);
    updateTodayEntry(entry);

    const isAvoided = updated.rollForwardCount >= 3;

    return {
      success: true,
      message: isAvoided
        ? `⚠️ AVOIDANCE PATTERN: "${task.content}" has been rolled forward ${updated.rollForwardCount} times`
        : `Rolled forward: "${task.content}" (${updated.rollForwardCount}x)`,
      data: {
        taskId: task.id,
        rollCount: updated.rollForwardCount,
        isAvoidancePattern: isAvoided,
      },
    };
  } catch (error) {
    return {
      success: false,
      message: `Failed to roll forward task: ${error instanceof Error ? error.message : 'Unknown error'}`,
    };
  }
}

/**
 * Get tasks by priority/category
 */
export function toolGetTasks(priority?: TaskPriority): ToolResponse {
  try {
    const config = getConfig();
    const tasks = priority ? getTasksByPriority(priority) : loadTasks().filter((t) => !t.completedAt);

    const groupedTasks = {
      deep: tasks.filter((t) => t.priority === 'deep'),
      standard: tasks.filter((t) => t.priority === 'standard'),
      light: tasks.filter((t) => t.priority === 'light'),
      someday: tasks.filter((t) => t.priority === 'someday'),
    };

    const formatTasks = (taskList: Task[]): string[] =>
      taskList.map((t) => {
        const rollInfo = t.rollForwardCount > 0 ? ` [rolled ${t.rollForwardCount}x]` : '';
        return `• ${t.content}${rollInfo}`;
      });

    let message = '';
    if (priority) {
      message = `${config.categories[priority]}:\n${formatTasks(groupedTasks[priority]).join('\n') || 'No tasks'}`;
    } else {
      message = Object.entries(groupedTasks)
        .filter(([, list]) => list.length > 0)
        .map(([p, list]) => `${config.categories[p as TaskPriority]}:\n${formatTasks(list).join('\n')}`)
        .join('\n\n');
    }

    return {
      success: true,
      message: message || 'No active tasks',
      data: { tasks: priority ? groupedTasks[priority] : tasks, count: tasks.length },
    };
  } catch (error) {
    return {
      success: false,
      message: `Failed to get tasks: ${error instanceof Error ? error.message : 'Unknown error'}`,
    };
  }
}

/**
 * Get avoided tasks (rolled 3+ times)
 */
export function toolGetAvoidedTasks(): ToolResponse {
  try {
    const avoided = getAvoidedTasks();

    if (avoided.length === 0) {
      return {
        success: true,
        message: 'No avoidance patterns detected. Great job staying on top of tasks!',
        data: { tasks: [], count: 0 },
      };
    }

    const list = avoided
      .sort((a, b) => b.rollForwardCount - a.rollForwardCount)
      .map((t) => `• "${t.content}" - rolled ${t.rollForwardCount}x (${t.priority})`)
      .join('\n');

    return {
      success: true,
      message: `⚠️ Avoidance Patterns Detected:\n${list}`,
      data: { tasks: avoided, count: avoided.length },
    };
  } catch (error) {
    return {
      success: false,
      message: `Failed to get avoided tasks: ${error instanceof Error ? error.message : 'Unknown error'}`,
    };
  }
}

// ============================================
// ENERGY TRACKING TOOLS
// ============================================

/**
 * Log an energy reading
 */
export function toolLogEnergy(level: EnergyLevel, context?: string): ToolResponse {
  try {
    const reading = stateLogEnergy(level, context);
    const sprint = getSprintStatus();

    let recommendation = '';
    switch (level) {
      case 'high':
        recommendation = 'Perfect time for deep work!';
        break;
      case 'medium':
        recommendation = 'Good for standard tasks.';
        break;
      case 'low':
        recommendation = 'Focus on light tasks or take a break.';
        break;
      case 'depleted':
        recommendation = 'Consider stopping for today. Rest is productive.';
        break;
      case 'recovery':
        recommendation = 'Take it easy. Gentle tasks only.';
        break;
    }

    if (sprint.status === 'danger') {
      recommendation += ' ⚠️ Sprint day ' + sprint.currentDay + ' - consider a rest day soon.';
    }

    return {
      success: true,
      message: `Energy logged: ${level}. ${recommendation}`,
      data: { reading, sprintDay: sprint.currentDay, sprintStatus: sprint.status },
    };
  } catch (error) {
    return {
      success: false,
      message: `Failed to log energy: ${error instanceof Error ? error.message : 'Unknown error'}`,
    };
  }
}

// ============================================
// SPRINT & SESSION TOOLS
// ============================================

/**
 * Get sprint status
 */
export function toolGetSprintStatus(): ToolResponse {
  try {
    const sprint = getSprintStatus();
    const config = getConfig();

    let message = `Sprint Day ${sprint.currentDay}`;

    if (sprint.status === 'danger') {
      message += ` ⚠️ DANGER - You've worked ${sprint.currentDay} consecutive days. Take a rest day!`;
    } else if (sprint.status === 'warning') {
      message += ` ⚡ Warning - Day ${sprint.currentDay}. Rest day recommended within ${config.sprint.dangerDay - sprint.currentDay} days.`;
    } else {
      message += ` ✓ Healthy sprint (warning at day ${config.sprint.warningDay})`;
    }

    if (sprint.lastRestDay) {
      message += `\nLast rest day: ${sprint.lastRestDay}`;
    }

    return {
      success: true,
      message,
      data: sprint,
    };
  } catch (error) {
    return {
      success: false,
      message: `Failed to get sprint status: ${error instanceof Error ? error.message : 'Unknown error'}`,
    };
  }
}

/**
 * Record a rest day
 */
export function toolRecordRestDay(): ToolResponse {
  try {
    recordRestDay();
    return {
      success: true,
      message: '🌙 Rest day recorded. Sprint counter reset. Enjoy your recovery!',
      data: { restDay: dayjs().format('YYYY-MM-DD') },
    };
  } catch (error) {
    return {
      success: false,
      message: `Failed to record rest day: ${error instanceof Error ? error.message : 'Unknown error'}`,
    };
  }
}

/**
 * Start a deep work session
 */
export function toolStartSession(type: 'briefing' | 'card' | 'energy' | 'accountability' | 'general', context?: Record<string, unknown>): ToolResponse {
  try {
    const session = startSession(type);
    if (context) {
      session.context = context;
    }

    return {
      success: true,
      message: `Session started: ${type}`,
      data: { sessionId: session.id, startedAt: session.startedAt },
    };
  } catch (error) {
    return {
      success: false,
      message: `Failed to start session: ${error instanceof Error ? error.message : 'Unknown error'}`,
    };
  }
}

/**
 * End the current session
 */
export function toolEndSession(): ToolResponse {
  try {
    endSession();
    return {
      success: true,
      message: 'Session ended.',
    };
  } catch (error) {
    return {
      success: false,
      message: `Failed to end session: ${error instanceof Error ? error.message : 'Unknown error'}`,
    };
  }
}

// ============================================
// FIELD REPORTS & NOTES
// ============================================

/**
 * Add a field report (quick capture)
 */
export function toolAddFieldReport(report: string): ToolResponse {
  try {
    addFieldReport(report);
    return {
      success: true,
      message: `Field report logged: "${report}"`,
      data: { timestamp: dayjs().format('HH:mm') },
    };
  } catch (error) {
    return {
      success: false,
      message: `Failed to add field report: ${error instanceof Error ? error.message : 'Unknown error'}`,
    };
  }
}

// ============================================
// ANALYSIS TOOLS
// ============================================

/**
 * Get pattern analysis
 */
export function toolGetPatternAnalysis(): ToolResponse {
  try {
    const patterns = analyzePatterns();
    const config = getConfig();

    let message = '## Pattern Analysis\n\n';

    // Avoidance patterns
    if (patterns.avoidancePatterns.length > 0) {
      message += '### ⚠️ Avoidance Patterns\n';
      patterns.avoidancePatterns.forEach((p) => {
        message += `• "${p.taskContent}" - ${p.rollCount}x rolls (${config.categories[p.category]})\n`;
      });
      message += '\n';
    }

    // Energy trends
    message += '### Energy Trends (7 days)\n';
    patterns.energyTrends.forEach((t) => {
      const bar = '█'.repeat(Math.round(t.averageLevel));
      message += `• ${t.period}: ${bar} ${t.averageLevel.toFixed(1)}/5\n`;
    });
    message += '\n';

    // Completion rate
    message += `### Completion Rate: ${(patterns.completionRate * 100).toFixed(0)}%\n\n`;

    // Burnout risk
    const riskEmoji = { low: '✓', medium: '⚡', high: '⚠️' };
    message += `### Burnout Risk: ${riskEmoji[patterns.burnoutRisk]} ${patterns.burnoutRisk}\n`;

    return {
      success: true,
      message,
      data: patterns,
    };
  } catch (error) {
    return {
      success: false,
      message: `Failed to get pattern analysis: ${error instanceof Error ? error.message : 'Unknown error'}`,
    };
  }
}

/**
 * Get overall data summary
 */
export function toolGetSummary(): ToolResponse {
  try {
    const summary = getDataSummary();
    const sprint = getSprintStatus();
    const entry = getTodayEntry();

    let message = '## Watchtower Status\n\n';
    message += `**Sprint:** Day ${sprint.currentDay} (${sprint.status})\n`;
    message += `**Active Tasks:** ${summary.activeTasks}\n`;
    message += `**Completed Today:** ${entry.tasksCompleted.length}\n`;
    message += `**Rolled Today:** ${entry.tasksRolledForward.length}\n`;
    message += `**7-Day Completion:** ${summary.completionRate}\n`;
    message += `**Burnout Risk:** ${summary.burnoutRisk}\n`;

    if ((summary.avoidedTasks as number) > 0) {
      message += `\n⚠️ **${summary.avoidedTasks} tasks** showing avoidance patterns\n`;
    }

    return {
      success: true,
      message,
      data: summary,
    };
  } catch (error) {
    return {
      success: false,
      message: `Failed to get summary: ${error instanceof Error ? error.message : 'Unknown error'}`,
    };
  }
}

// ============================================
// TOOL REGISTRY
// ============================================

export const productivityTools = {
  // Task management
  addTask: toolAddTask,
  completeTask: toolCompleteTask,
  rollForwardTask: toolRollForwardTask,
  getTasks: toolGetTasks,
  getAvoidedTasks: toolGetAvoidedTasks,

  // Energy tracking
  logEnergy: toolLogEnergy,

  // Sprint & sessions
  getSprintStatus: toolGetSprintStatus,
  recordRestDay: toolRecordRestDay,
  startSession: toolStartSession,
  endSession: toolEndSession,

  // Field reports
  addFieldReport: toolAddFieldReport,

  // Analysis
  getPatternAnalysis: toolGetPatternAnalysis,
  getSummary: toolGetSummary,
};

export type ProductivityToolName = keyof typeof productivityTools;
