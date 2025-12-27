/**
 * Watchtower Windows - Type Definitions
 * Core types for the productivity system
 */

export interface WatchtowerConfig {
  // Document names (for Craft MCP or alternative note systems)
  documents: {
    daily: string;      // The Watchtower - Daily hub
    tasks: string;      // The Forge - Task pool
    journey: string;    // The Long Road - Journey tracker
  };

  // Energy windows (up to 3 peak productivity periods)
  energyWindows: EnergyWindow[];

  // Task categories with energy levels
  categories: {
    deep: string;       // High energy work
    standard: string;   // Normal energy work
    light: string;      // Low energy work
    someday: string;    // Future/someday tasks
  };

  // Sprint thresholds for burnout detection
  sprint: {
    warningDay: number;   // Days before warning (default: 14)
    dangerDay: number;    // Days before danger alert (default: 21)
  };

  // Coaching voices (archetypal personas)
  voices: {
    discipline: string;   // For avoidance patterns
    wisdom: string;       // For burnout signals
    leadership: string;   // For scattered priorities
  };

  // Optional modules
  modules: {
    health: boolean;
    weeklyReview: boolean;
    deepWorkSessions: boolean;
  };

  // System settings
  system: {
    timezone: string;
    dataDir: string;
    sessionsDir: string;
    healthLog: string;
  };
}

export interface EnergyWindow {
  start: number;  // Hour (0-23)
  end: number;    // Hour (0-23)
  label?: string; // Optional label (e.g., "Morning Focus")
}

export type EnergyLevel = 'high' | 'medium' | 'low' | 'depleted' | 'recovery';

export type TaskPriority = 'deep' | 'standard' | 'light' | 'someday';

export interface Task {
  id: string;
  content: string;
  priority: TaskPriority;
  createdAt: string;
  completedAt?: string;
  rollForwardCount: number;
  notes?: string[];
}

export interface DailyEntry {
  date: string;
  sprintDay: number;
  energyReadings: EnergyReading[];
  tasksCompleted: string[];
  tasksRolledForward: string[];
  fieldReports: string[];
  briefing?: string;
}

export interface EnergyReading {
  timestamp: string;
  level: EnergyLevel;
  context?: string;
}

export interface SprintStatus {
  currentDay: number;
  startDate: string;
  status: 'healthy' | 'warning' | 'danger';
  lastRestDay?: string;
}

export interface PatternAnalysis {
  avoidancePatterns: AvoidancePattern[];
  energyTrends: EnergyTrend[];
  completionRate: number;
  categoryBalance: CategoryBalance;
  burnoutRisk: 'low' | 'medium' | 'high';
}

export interface AvoidancePattern {
  taskId: string;
  taskContent: string;
  rollCount: number;
  firstRolled: string;
  category: TaskPriority;
}

export interface EnergyTrend {
  period: 'morning' | 'afternoon' | 'evening';
  averageLevel: number;
  sampleCount: number;
}

export interface CategoryBalance {
  deep: number;
  standard: number;
  light: number;
  someday: number;
}

export interface Session {
  id: string;
  startedAt: string;
  lastActivity: string;
  type: 'briefing' | 'card' | 'energy' | 'accountability' | 'general';
  context?: Record<string, unknown>;
}

export interface CardProcessingResult {
  completedTasks: string[];
  incompleteTasks: string[];
  newTasks: string[];
  notes: string[];
  rawText?: string;
}

export interface JournalEntry {
  date: string;
  content: string;
  insights?: string[];
  mood?: string;
}

// Command types
export type WatchtowerCommand =
  | 'brief'
  | 'card'
  | 'energy'
  | 'status'
  | 'add'
  | 'journal'
  | 'accountability'
  | 'weekly'
  | 'work'
  | 'health'
  | 'coach'
  | 'config';

export interface CommandContext {
  config: WatchtowerConfig;
  dataDir: string;
  args: string[];
  flags: Record<string, boolean | string>;
}
