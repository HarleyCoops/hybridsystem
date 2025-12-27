/**
 * Watchtower Windows - State Management
 * Handles persistent state for tasks, sessions, and productivity tracking
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import dayjs from 'dayjs';
import { getConfig } from './config.js';
import type {
  Task,
  DailyEntry,
  EnergyReading,
  SprintStatus,
  Session,
  TaskPriority,
  EnergyLevel,
  PatternAnalysis,
  AvoidancePattern,
} from '../types.js';

// State file paths
function getStatePath(filename: string): string {
  const config = getConfig();
  return join(config.system.dataDir, filename);
}

/**
 * Generic state file operations
 */
function loadState<T>(filename: string, defaultValue: T): T {
  const path = getStatePath(filename);
  if (!existsSync(path)) {
    return defaultValue;
  }
  try {
    return JSON.parse(readFileSync(path, 'utf-8'));
  } catch {
    return defaultValue;
  }
}

function saveState<T>(filename: string, data: T): void {
  const path = getStatePath(filename);
  const dir = dirname(path);
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }
  writeFileSync(path, JSON.stringify(data, null, 2));
}

// ============================================
// TASK MANAGEMENT
// ============================================

interface TaskStore {
  tasks: Task[];
  lastUpdated: string;
}

export function loadTasks(): Task[] {
  const store = loadState<TaskStore>('tasks.json', { tasks: [], lastUpdated: '' });
  return store.tasks;
}

export function saveTasks(tasks: Task[]): void {
  saveState<TaskStore>('tasks.json', {
    tasks,
    lastUpdated: dayjs().toISOString(),
  });
}

export function addTask(content: string, priority: TaskPriority = 'standard'): Task {
  const tasks = loadTasks();
  const newTask: Task = {
    id: generateId(),
    content,
    priority,
    createdAt: dayjs().toISOString(),
    rollForwardCount: 0,
  };
  tasks.push(newTask);
  saveTasks(tasks);
  return newTask;
}

export function completeTask(taskId: string): Task | null {
  const tasks = loadTasks();
  const task = tasks.find((t) => t.id === taskId);
  if (task) {
    task.completedAt = dayjs().toISOString();
    saveTasks(tasks);
  }
  return task || null;
}

export function rollForwardTask(taskId: string): Task | null {
  const tasks = loadTasks();
  const task = tasks.find((t) => t.id === taskId);
  if (task) {
    task.rollForwardCount += 1;
    if (!task.notes) task.notes = [];
    task.notes.push(`Rolled forward on ${dayjs().format('YYYY-MM-DD')}`);
    saveTasks(tasks);
  }
  return task || null;
}

export function getTasksByPriority(priority: TaskPriority): Task[] {
  return loadTasks().filter((t) => t.priority === priority && !t.completedAt);
}

export function getAvoidedTasks(minRollCount: number = 3): Task[] {
  return loadTasks().filter((t) => t.rollForwardCount >= minRollCount && !t.completedAt);
}

// ============================================
// DAILY ENTRIES
// ============================================

interface DailyStore {
  entries: Record<string, DailyEntry>;
}

export function loadDailyEntries(): Record<string, DailyEntry> {
  const store = loadState<DailyStore>('daily.json', { entries: {} });
  return store.entries;
}

export function saveDailyEntries(entries: Record<string, DailyEntry>): void {
  saveState<DailyStore>('daily.json', { entries });
}

export function getTodayEntry(): DailyEntry {
  const today = dayjs().format('YYYY-MM-DD');
  const entries = loadDailyEntries();

  if (!entries[today]) {
    const sprint = getSprintStatus();
    entries[today] = {
      date: today,
      sprintDay: sprint.currentDay,
      energyReadings: [],
      tasksCompleted: [],
      tasksRolledForward: [],
      fieldReports: [],
    };
    saveDailyEntries(entries);
  }

  return entries[today];
}

export function updateTodayEntry(updates: Partial<DailyEntry>): DailyEntry {
  const today = dayjs().format('YYYY-MM-DD');
  const entries = loadDailyEntries();
  const current = getTodayEntry();

  entries[today] = { ...current, ...updates };
  saveDailyEntries(entries);

  return entries[today];
}

export function addFieldReport(report: string): void {
  const entry = getTodayEntry();
  entry.fieldReports.push(`[${dayjs().format('HH:mm')}] ${report}`);
  updateTodayEntry(entry);
}

// ============================================
// ENERGY TRACKING
// ============================================

export function logEnergy(level: EnergyLevel, context?: string): EnergyReading {
  const reading: EnergyReading = {
    timestamp: dayjs().toISOString(),
    level,
    context,
  };

  const entry = getTodayEntry();
  entry.energyReadings.push(reading);
  updateTodayEntry(entry);

  return reading;
}

export function getRecentEnergyReadings(days: number = 7): EnergyReading[] {
  const entries = loadDailyEntries();
  const cutoff = dayjs().subtract(days, 'day');
  const readings: EnergyReading[] = [];

  for (const [date, entry] of Object.entries(entries)) {
    if (dayjs(date).isAfter(cutoff)) {
      readings.push(...entry.energyReadings);
    }
  }

  return readings.sort((a, b) => dayjs(a.timestamp).unix() - dayjs(b.timestamp).unix());
}

export function calculateAverageEnergy(readings: EnergyReading[]): number {
  if (readings.length === 0) return 0;

  const levelValues: Record<EnergyLevel, number> = {
    high: 5,
    medium: 4,
    low: 3,
    depleted: 2,
    recovery: 1,
  };

  const sum = readings.reduce((acc, r) => acc + levelValues[r.level], 0);
  return sum / readings.length;
}

// ============================================
// SPRINT TRACKING
// ============================================

interface SprintStore {
  currentDay: number;
  startDate: string;
  lastWorkDay: string;
  restDays: string[];
}

export function getSprintStatus(): SprintStatus {
  const store = loadState<SprintStore>('sprint.json', {
    currentDay: 1,
    startDate: dayjs().format('YYYY-MM-DD'),
    lastWorkDay: dayjs().format('YYYY-MM-DD'),
    restDays: [],
  });

  const config = getConfig();
  const today = dayjs().format('YYYY-MM-DD');

  // Check if we need to increment the day
  if (store.lastWorkDay !== today) {
    const daysSinceLastWork = dayjs(today).diff(dayjs(store.lastWorkDay), 'day');

    if (daysSinceLastWork > 1) {
      // Rest day(s) detected - reset sprint
      store.currentDay = 1;
      store.startDate = today;
    } else {
      store.currentDay += 1;
    }

    store.lastWorkDay = today;
    saveState('sprint.json', store);
  }

  // Determine status
  let status: 'healthy' | 'warning' | 'danger' = 'healthy';
  if (store.currentDay >= config.sprint.dangerDay) {
    status = 'danger';
  } else if (store.currentDay >= config.sprint.warningDay) {
    status = 'warning';
  }

  return {
    currentDay: store.currentDay,
    startDate: store.startDate,
    status,
    lastRestDay: store.restDays[store.restDays.length - 1],
  };
}

export function recordRestDay(): void {
  const store = loadState<SprintStore>('sprint.json', {
    currentDay: 0,
    startDate: dayjs().format('YYYY-MM-DD'),
    lastWorkDay: dayjs().format('YYYY-MM-DD'),
    restDays: [],
  });

  store.restDays.push(dayjs().format('YYYY-MM-DD'));
  store.currentDay = 0;
  store.startDate = dayjs().add(1, 'day').format('YYYY-MM-DD');
  saveState('sprint.json', store);
}

// ============================================
// SESSION MANAGEMENT
// ============================================

interface SessionStore {
  currentSession?: Session;
  history: Session[];
}

export function getCurrentSession(): Session | null {
  const store = loadState<SessionStore>('sessions.json', { history: [] });
  return store.currentSession || null;
}

export function startSession(type: Session['type']): Session {
  const store = loadState<SessionStore>('sessions.json', { history: [] });

  // Archive current session if exists
  if (store.currentSession) {
    store.history.push(store.currentSession);
  }

  const session: Session = {
    id: generateId(),
    startedAt: dayjs().toISOString(),
    lastActivity: dayjs().toISOString(),
    type,
  };

  store.currentSession = session;
  saveState('sessions.json', store);

  return session;
}

export function updateSession(updates: Partial<Session>): void {
  const store = loadState<SessionStore>('sessions.json', { history: [] });

  if (store.currentSession) {
    store.currentSession = {
      ...store.currentSession,
      ...updates,
      lastActivity: dayjs().toISOString(),
    };
    saveState('sessions.json', store);
  }
}

export function endSession(): void {
  const store = loadState<SessionStore>('sessions.json', { history: [] });

  if (store.currentSession) {
    store.history.push(store.currentSession);
    store.currentSession = undefined;
    saveState('sessions.json', store);
  }
}

// ============================================
// PATTERN ANALYSIS
// ============================================

export function analyzePatterns(): PatternAnalysis {
  const tasks = loadTasks();
  const entries = loadDailyEntries();
  const sprint = getSprintStatus();

  // Avoidance patterns
  const avoidancePatterns: AvoidancePattern[] = tasks
    .filter((t) => t.rollForwardCount >= 3 && !t.completedAt)
    .map((t) => ({
      taskId: t.id,
      taskContent: t.content,
      rollCount: t.rollForwardCount,
      firstRolled: t.notes?.[0]?.replace('Rolled forward on ', '') || t.createdAt,
      category: t.priority,
    }));

  // Energy trends by time of day
  const allReadings = getRecentEnergyReadings(7);
  const morningReadings = allReadings.filter((r) => {
    const hour = dayjs(r.timestamp).hour();
    return hour >= 6 && hour < 12;
  });
  const afternoonReadings = allReadings.filter((r) => {
    const hour = dayjs(r.timestamp).hour();
    return hour >= 12 && hour < 18;
  });
  const eveningReadings = allReadings.filter((r) => {
    const hour = dayjs(r.timestamp).hour();
    return hour >= 18 || hour < 6;
  });

  const energyTrends = [
    {
      period: 'morning' as const,
      averageLevel: calculateAverageEnergy(morningReadings),
      sampleCount: morningReadings.length,
    },
    {
      period: 'afternoon' as const,
      averageLevel: calculateAverageEnergy(afternoonReadings),
      sampleCount: afternoonReadings.length,
    },
    {
      period: 'evening' as const,
      averageLevel: calculateAverageEnergy(eveningReadings),
      sampleCount: eveningReadings.length,
    },
  ];

  // Completion rate
  const recentDays = Object.values(entries)
    .filter((e) => dayjs(e.date).isAfter(dayjs().subtract(7, 'day')));
  const totalCompleted = recentDays.reduce((acc, e) => acc + e.tasksCompleted.length, 0);
  const totalRolled = recentDays.reduce((acc, e) => acc + e.tasksRolledForward.length, 0);
  const completionRate = totalCompleted + totalRolled > 0
    ? totalCompleted / (totalCompleted + totalRolled)
    : 0;

  // Category balance
  const activeTasks = tasks.filter((t) => !t.completedAt);
  const categoryBalance = {
    deep: activeTasks.filter((t) => t.priority === 'deep').length,
    standard: activeTasks.filter((t) => t.priority === 'standard').length,
    light: activeTasks.filter((t) => t.priority === 'light').length,
    someday: activeTasks.filter((t) => t.priority === 'someday').length,
  };

  // Burnout risk assessment
  let burnoutRisk: 'low' | 'medium' | 'high' = 'low';
  const avgEnergy = calculateAverageEnergy(allReadings);

  if (sprint.status === 'danger' || avgEnergy < 2.5) {
    burnoutRisk = 'high';
  } else if (sprint.status === 'warning' || avgEnergy < 3.5) {
    burnoutRisk = 'medium';
  }

  return {
    avoidancePatterns,
    energyTrends,
    completionRate,
    categoryBalance,
    burnoutRisk,
  };
}

// ============================================
// UTILITIES
// ============================================

function generateId(): string {
  return `${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
}

export function formatTaskList(tasks: Task[]): string {
  if (tasks.length === 0) return 'No tasks';

  return tasks
    .map((t) => {
      const rollIndicator = t.rollForwardCount > 0 ? ` [rolled ${t.rollForwardCount}x]` : '';
      const status = t.completedAt ? '[x]' : '[ ]';
      return `${status} ${t.content}${rollIndicator}`;
    })
    .join('\n');
}

export function getDataSummary(): Record<string, unknown> {
  const tasks = loadTasks();
  const entries = loadDailyEntries();
  const sprint = getSprintStatus();
  const patterns = analyzePatterns();

  return {
    totalTasks: tasks.length,
    activeTasks: tasks.filter((t) => !t.completedAt).length,
    completedTasks: tasks.filter((t) => t.completedAt).length,
    avoidedTasks: patterns.avoidancePatterns.length,
    dailyEntries: Object.keys(entries).length,
    sprintDay: sprint.currentDay,
    sprintStatus: sprint.status,
    burnoutRisk: patterns.burnoutRisk,
    completionRate: `${(patterns.completionRate * 100).toFixed(1)}%`,
  };
}
