/**
 * Watchtower Windows - Configuration Management
 * Handles loading, saving, and managing user configuration
 */

import Conf from 'conf';
import { homedir } from 'os';
import { join } from 'path';
import { existsSync, mkdirSync } from 'fs';
import type { WatchtowerConfig, EnergyWindow } from '../types.js';

// Default configuration values
const DEFAULT_CONFIG: WatchtowerConfig = {
  documents: {
    daily: 'The Watchtower',
    tasks: 'The Forge',
    journey: 'The Long Road',
  },

  energyWindows: [
    { start: 9, end: 13, label: 'Morning Focus' },
    { start: 15, end: 18, label: 'Afternoon Drive' },
    { start: 20, end: 22, label: 'Evening Flow' },
  ],

  categories: {
    deep: 'Deep Work Forging',
    standard: 'Standard Forge Work',
    light: 'Light Smithing',
    someday: 'The Anvil Awaits',
  },

  sprint: {
    warningDay: 14,
    dangerDay: 21,
  },

  voices: {
    discipline: 'Marcus Aurelius',
    wisdom: 'Gandalf',
    leadership: 'Aragorn',
  },

  modules: {
    health: false,
    weeklyReview: true,
    deepWorkSessions: true,
  },

  system: {
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    dataDir: join(homedir(), '.watchtower'),
    sessionsDir: join(homedir(), '.watchtower', 'sessions'),
    healthLog: join(homedir(), '.watchtower', 'health-log.md'),
  },
};

// Configuration store using Conf
const configStore = new Conf<WatchtowerConfig>({
  projectName: 'watchtower',
  defaults: DEFAULT_CONFIG,
  schema: {
    documents: {
      type: 'object',
      properties: {
        daily: { type: 'string' },
        tasks: { type: 'string' },
        journey: { type: 'string' },
      },
    },
    energyWindows: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          start: { type: 'number', minimum: 0, maximum: 23 },
          end: { type: 'number', minimum: 0, maximum: 23 },
          label: { type: 'string' },
        },
        required: ['start', 'end'],
      },
    },
    categories: {
      type: 'object',
      properties: {
        deep: { type: 'string' },
        standard: { type: 'string' },
        light: { type: 'string' },
        someday: { type: 'string' },
      },
    },
    sprint: {
      type: 'object',
      properties: {
        warningDay: { type: 'number', minimum: 1 },
        dangerDay: { type: 'number', minimum: 1 },
      },
    },
    voices: {
      type: 'object',
      properties: {
        discipline: { type: 'string' },
        wisdom: { type: 'string' },
        leadership: { type: 'string' },
      },
    },
    modules: {
      type: 'object',
      properties: {
        health: { type: 'boolean' },
        weeklyReview: { type: 'boolean' },
        deepWorkSessions: { type: 'boolean' },
      },
    },
    system: {
      type: 'object',
      properties: {
        timezone: { type: 'string' },
        dataDir: { type: 'string' },
        sessionsDir: { type: 'string' },
        healthLog: { type: 'string' },
      },
    },
  },
});

/**
 * Get the current configuration
 */
export function getConfig(): WatchtowerConfig {
  return configStore.store;
}

/**
 * Update configuration values
 */
export function updateConfig(updates: Partial<WatchtowerConfig>): void {
  configStore.set(updates);
}

/**
 * Reset configuration to defaults
 */
export function resetConfig(): void {
  configStore.clear();
}

/**
 * Get the path to the configuration file
 */
export function getConfigPath(): string {
  return configStore.path;
}

/**
 * Ensure all required directories exist
 */
export function ensureDirectories(): void {
  const config = getConfig();

  const dirs = [
    config.system.dataDir,
    config.system.sessionsDir,
  ];

  for (const dir of dirs) {
    if (!existsSync(dir)) {
      mkdirSync(dir, { recursive: true });
    }
  }
}

/**
 * Check if we're currently in a peak energy window
 */
export function isInPeakWindow(config: WatchtowerConfig): { inWindow: boolean; window?: EnergyWindow } {
  const now = new Date();
  const currentHour = now.getHours();

  for (const window of config.energyWindows) {
    if (currentHour >= window.start && currentHour < window.end) {
      return { inWindow: true, window };
    }
  }

  return { inWindow: false };
}

/**
 * Get the appropriate coaching voice based on context
 */
export function getCoachingVoice(
  config: WatchtowerConfig,
  context: 'avoidance' | 'burnout' | 'scattered'
): string {
  switch (context) {
    case 'avoidance':
      return config.voices.discipline;
    case 'burnout':
      return config.voices.wisdom;
    case 'scattered':
      return config.voices.leadership;
    default:
      return config.voices.wisdom;
  }
}

/**
 * Validate configuration structure
 */
export function validateConfig(config: WatchtowerConfig): { valid: boolean; errors: string[] } {
  const errors: string[] = [];

  // Check energy windows
  for (const window of config.energyWindows) {
    if (window.start >= window.end) {
      errors.push(`Invalid energy window: start (${window.start}) must be before end (${window.end})`);
    }
  }

  // Check sprint thresholds
  if (config.sprint.warningDay >= config.sprint.dangerDay) {
    errors.push('Warning day must be less than danger day');
  }

  // Check document names aren't empty
  if (!config.documents.daily || !config.documents.tasks || !config.documents.journey) {
    errors.push('All document names must be specified');
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}

export { DEFAULT_CONFIG };
