/**
 * Watchtower Windows - Main Entry Point
 * Windows productivity system powered by Claude Agent SDK
 */

// Core exports
export * from './types.js';
export * from './core/config.js';
export * from './core/state.js';
export * from './core/agent.js';

// Tools
export * from './tools/productivity.js';

// Utilities
export * from './utils/windows.js';

// Version
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const packageJson = require('../package.json');
export const VERSION = packageJson.version;
