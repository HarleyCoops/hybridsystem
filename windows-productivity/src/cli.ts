#!/usr/bin/env node
/**
 * Watchtower Windows - CLI Entry Point
 * Command-line interface for the productivity system
 */

import { Command } from 'commander';
import chalk from 'chalk';
import ora from 'ora';
import { createRequire } from 'module';

import { ensureDirectories, getConfig, updateConfig, getConfigPath } from './core/config.js';
import {
  runMorningBriefing,
  processCard,
  checkEnergy,
  runAccountabilityCheck,
  getStatus,
  addTask,
  processJournal,
  runWeeklyReview,
  startDeepWork,
  processHealthData,
  healthCoaching,
} from './core/agent.js';
import {
  toolLogEnergy,
  toolGetSummary,
  toolAddTask,
  toolGetTasks,
  toolRecordRestDay,
} from './tools/productivity.js';

const require = createRequire(import.meta.url);
const packageJson = require('../package.json');

// Initialize directories on startup
ensureDirectories();

const program = new Command();

program
  .name('watchtower')
  .description('Windows productivity system powered by Claude Agent SDK')
  .version(packageJson.version);

// ============================================
// CORE COMMANDS
// ============================================

program
  .command('brief')
  .alias('b')
  .description('Generate morning briefing with pattern analysis')
  .action(async () => {
    const spinner = ora('Generating morning briefing...').start();
    try {
      const result = await runMorningBriefing();
      spinner.succeed('Morning briefing ready');
      console.log('\n' + chalk.cyan('═'.repeat(60)));
      console.log(chalk.bold.cyan('  THE WATCHTOWER - Daily Briefing'));
      console.log(chalk.cyan('═'.repeat(60)) + '\n');
      console.log(result.text);
      console.log('\n' + chalk.dim('─'.repeat(60)));
    } catch (error) {
      spinner.fail('Failed to generate briefing');
      console.error(chalk.red(error instanceof Error ? error.message : 'Unknown error'));
      process.exit(1);
    }
  });

program
  .command('card <imagePath>')
  .alias('c')
  .description('Process a photographed index card')
  .action(async (imagePath: string) => {
    const spinner = ora('Processing card image...').start();
    try {
      const result = await processCard(imagePath);
      spinner.succeed('Card processed');
      console.log('\n' + chalk.yellow('═'.repeat(60)));
      console.log(chalk.bold.yellow('  CARD PROCESSING COMPLETE'));
      console.log(chalk.yellow('═'.repeat(60)) + '\n');
      console.log(result.text);
      console.log('\n' + chalk.dim('─'.repeat(60)));
    } catch (error) {
      spinner.fail('Failed to process card');
      console.error(chalk.red(error instanceof Error ? error.message : 'Unknown error'));
      process.exit(1);
    }
  });

program
  .command('energy [level]')
  .alias('e')
  .description('Log and analyze energy level (high/medium/low/depleted/recovery)')
  .action(async (level?: string) => {
    if (level) {
      const validLevels = ['high', 'medium', 'low', 'depleted', 'recovery'];
      if (!validLevels.includes(level.toLowerCase())) {
        console.error(chalk.red(`Invalid energy level. Choose from: ${validLevels.join(', ')}`));
        process.exit(1);
      }
      const result = toolLogEnergy(level.toLowerCase() as any);
      console.log(chalk.green(result.message));
    } else {
      const spinner = ora('Analyzing energy patterns...').start();
      try {
        const result = await checkEnergy();
        spinner.succeed('Energy analysis complete');
        console.log('\n' + result.text);
      } catch (error) {
        spinner.fail('Failed to analyze energy');
        console.error(chalk.red(error instanceof Error ? error.message : 'Unknown error'));
        process.exit(1);
      }
    }
  });

program
  .command('status')
  .alias('s')
  .description('Quick status overview')
  .action(async () => {
    const spinner = ora('Getting status...').start();
    try {
      const result = await getStatus();
      spinner.stop();
      console.log('\n' + result.text);
    } catch (error) {
      spinner.fail('Failed to get status');
      console.error(chalk.red(error instanceof Error ? error.message : 'Unknown error'));
      process.exit(1);
    }
  });

program
  .command('add <task>')
  .alias('a')
  .description('Add a new task')
  .option('-p, --priority <level>', 'Priority: deep, standard, light, someday', 'standard')
  .action(async (task: string, options: { priority: string }) => {
    const validPriorities = ['deep', 'standard', 'light', 'someday'];
    if (!validPriorities.includes(options.priority)) {
      console.error(chalk.red(`Invalid priority. Choose from: ${validPriorities.join(', ')}`));
      process.exit(1);
    }

    const result = toolAddTask(task, options.priority as any);
    if (result.success) {
      console.log(chalk.green('✓ ' + result.message));
    } else {
      console.error(chalk.red('✗ ' + result.message));
      process.exit(1);
    }
  });

program
  .command('journal [content]')
  .alias('j')
  .description('Process a journal entry (text or image path)')
  .option('-i, --image <path>', 'Path to handwritten journal image')
  .action(async (content?: string, options?: { image?: string }) => {
    if (!content && !options?.image) {
      console.error(chalk.red('Please provide journal content or an image path'));
      process.exit(1);
    }

    const spinner = ora('Processing journal entry...').start();
    try {
      const result = await processJournal(content || '', options?.image);
      spinner.succeed('Journal processed');
      console.log('\n' + result.text);
    } catch (error) {
      spinner.fail('Failed to process journal');
      console.error(chalk.red(error instanceof Error ? error.message : 'Unknown error'));
      process.exit(1);
    }
  });

program
  .command('accountability')
  .alias('acc')
  .description('Deep pattern analysis and coaching')
  .action(async () => {
    const spinner = ora('Running accountability check...').start();
    try {
      const result = await runAccountabilityCheck();
      spinner.succeed('Accountability check complete');
      console.log('\n' + chalk.magenta('═'.repeat(60)));
      console.log(chalk.bold.magenta('  ACCOUNTABILITY CHECK'));
      console.log(chalk.magenta('═'.repeat(60)) + '\n');
      console.log(result.text);
      console.log('\n' + chalk.dim('─'.repeat(60)));
    } catch (error) {
      spinner.fail('Failed to run accountability check');
      console.error(chalk.red(error instanceof Error ? error.message : 'Unknown error'));
      process.exit(1);
    }
  });

// ============================================
// OPTIONAL MODULE COMMANDS
// ============================================

program
  .command('weekly')
  .alias('w')
  .description('Weekly intelligence review')
  .action(async () => {
    const config = getConfig();
    if (!config.modules.weeklyReview) {
      console.log(chalk.yellow('Weekly review module is not enabled.'));
      console.log(chalk.dim('Enable it with: watchtower config --enable-weekly'));
      return;
    }

    const spinner = ora('Generating weekly review...').start();
    try {
      const result = await runWeeklyReview();
      spinner.succeed('Weekly review complete');
      console.log('\n' + chalk.blue('═'.repeat(60)));
      console.log(chalk.bold.blue('  WEEKLY INTELLIGENCE REVIEW'));
      console.log(chalk.blue('═'.repeat(60)) + '\n');
      console.log(result.text);
      console.log('\n' + chalk.dim('─'.repeat(60)));
    } catch (error) {
      spinner.fail('Failed to generate weekly review');
      console.error(chalk.red(error instanceof Error ? error.message : 'Unknown error'));
      process.exit(1);
    }
  });

program
  .command('work <project>')
  .description('Start a deep work session')
  .action(async (project: string) => {
    const config = getConfig();
    if (!config.modules.deepWorkSessions) {
      console.log(chalk.yellow('Deep work sessions module is not enabled.'));
      console.log(chalk.dim('Enable it with: watchtower config --enable-deepwork'));
      return;
    }

    const spinner = ora('Starting deep work session...').start();
    try {
      const result = await startDeepWork(project);
      spinner.succeed('Session started');
      console.log('\n' + chalk.green('═'.repeat(60)));
      console.log(chalk.bold.green(`  DEEP WORK: ${project.toUpperCase()}`));
      console.log(chalk.green('═'.repeat(60)) + '\n');
      console.log(result.text);
      console.log('\n' + chalk.dim('─'.repeat(60)));
    } catch (error) {
      spinner.fail('Failed to start session');
      console.error(chalk.red(error instanceof Error ? error.message : 'Unknown error'));
      process.exit(1);
    }
  });

program
  .command('health <dataPath>')
  .description('Process health/biometric data')
  .action(async (dataPath: string) => {
    const config = getConfig();
    if (!config.modules.health) {
      console.log(chalk.yellow('Health module is not enabled.'));
      console.log(chalk.dim('Enable it with: watchtower config --enable-health'));
      return;
    }

    const spinner = ora('Processing health data...').start();
    try {
      const result = await processHealthData(dataPath);
      spinner.succeed('Health data processed');
      console.log('\n' + result.text);
    } catch (error) {
      spinner.fail('Failed to process health data');
      console.error(chalk.red(error instanceof Error ? error.message : 'Unknown error'));
      process.exit(1);
    }
  });

program
  .command('coach [question]')
  .description('Health coaching Q&A')
  .action(async (question?: string) => {
    const config = getConfig();
    if (!config.modules.health) {
      console.log(chalk.yellow('Health module is not enabled.'));
      console.log(chalk.dim('Enable it with: watchtower config --enable-health'));
      return;
    }

    if (!question) {
      console.error(chalk.red('Please provide a health-related question'));
      process.exit(1);
    }

    const spinner = ora('Consulting health coach...').start();
    try {
      const result = await healthCoaching(question);
      spinner.succeed('Coaching complete');
      console.log('\n' + result.text);
    } catch (error) {
      spinner.fail('Failed to get coaching response');
      console.error(chalk.red(error instanceof Error ? error.message : 'Unknown error'));
      process.exit(1);
    }
  });

// ============================================
// UTILITY COMMANDS
// ============================================

program
  .command('tasks')
  .alias('t')
  .description('List all tasks')
  .option('-p, --priority <level>', 'Filter by priority: deep, standard, light, someday')
  .action((options: { priority?: string }) => {
    const result = toolGetTasks(options.priority as any);
    console.log('\n' + result.message);
  });

program
  .command('rest')
  .description('Record a rest day (resets sprint counter)')
  .action(() => {
    const result = toolRecordRestDay();
    console.log(chalk.green(result.message));
  });

program
  .command('summary')
  .description('Get data summary')
  .action(() => {
    const result = toolGetSummary();
    console.log('\n' + result.message);
  });

program
  .command('config')
  .description('View or modify configuration')
  .option('--show', 'Show current configuration')
  .option('--path', 'Show configuration file path')
  .option('--enable-health', 'Enable health module')
  .option('--disable-health', 'Disable health module')
  .option('--enable-weekly', 'Enable weekly review module')
  .option('--disable-weekly', 'Disable weekly review module')
  .option('--enable-deepwork', 'Enable deep work sessions module')
  .option('--disable-deepwork', 'Disable deep work sessions module')
  .option('--set-timezone <tz>', 'Set timezone')
  .action((options: Record<string, boolean | string | undefined>) => {
    const config = getConfig();

    if (options.path) {
      console.log(chalk.dim('Config file:'), getConfigPath());
      return;
    }

    if (options['enable-health']) {
      updateConfig({ modules: { ...config.modules, health: true } });
      console.log(chalk.green('Health module enabled'));
    }
    if (options['disable-health']) {
      updateConfig({ modules: { ...config.modules, health: false } });
      console.log(chalk.yellow('Health module disabled'));
    }
    if (options['enable-weekly']) {
      updateConfig({ modules: { ...config.modules, weeklyReview: true } });
      console.log(chalk.green('Weekly review module enabled'));
    }
    if (options['disable-weekly']) {
      updateConfig({ modules: { ...config.modules, weeklyReview: false } });
      console.log(chalk.yellow('Weekly review module disabled'));
    }
    if (options['enable-deepwork']) {
      updateConfig({ modules: { ...config.modules, deepWorkSessions: true } });
      console.log(chalk.green('Deep work sessions module enabled'));
    }
    if (options['disable-deepwork']) {
      updateConfig({ modules: { ...config.modules, deepWorkSessions: false } });
      console.log(chalk.yellow('Deep work sessions module disabled'));
    }
    if (options['set-timezone']) {
      updateConfig({ system: { ...config.system, timezone: options['set-timezone'] as string } });
      console.log(chalk.green(`Timezone set to: ${options['set-timezone']}`));
    }

    if (options.show || Object.keys(options).length === 0) {
      console.log('\n' + chalk.bold('Current Configuration:'));
      console.log(chalk.dim('─'.repeat(40)));
      console.log(JSON.stringify(getConfig(), null, 2));
    }
  });

// ============================================
// HELP & STARTUP
// ============================================

program
  .command('help-full')
  .description('Show detailed help with examples')
  .action(() => {
    console.log(`
${chalk.bold.cyan('WATCHTOWER - Windows Productivity System')}
${chalk.dim('Powered by Claude Agent SDK')}

${chalk.bold('DAILY WORKFLOW')}
${chalk.dim('─'.repeat(50))}

  ${chalk.yellow('Morning (5 min):')}
    watchtower brief          Generate daily briefing
    → Write top 3-5 tasks on physical index card

  ${chalk.yellow('During the Day:')}
    watchtower add "task"     Quick capture new tasks
    watchtower energy high    Log energy level
    watchtower status         Quick status check

  ${chalk.yellow('Evening (5 min):')}
    watchtower card photo.jpg Process completed card
    → Photos your handwritten card for OCR

${chalk.bold('TASK MANAGEMENT')}
${chalk.dim('─'.repeat(50))}

  watchtower add "task" -p deep       High-focus task
  watchtower add "task" -p standard   Normal energy (default)
  watchtower add "task" -p light      Low energy / easy win
  watchtower add "task" -p someday    Future possibility

  watchtower tasks                    List all active tasks
  watchtower tasks -p deep            Filter by priority

${chalk.bold('PATTERN ANALYSIS')}
${chalk.dim('─'.repeat(50))}

  watchtower accountability   Deep pattern analysis
  watchtower weekly           Weekly intelligence review
  watchtower summary          Quick data summary

${chalk.bold('ENERGY & SPRINT')}
${chalk.dim('─'.repeat(50))}

  Energy levels: high, medium, low, depleted, recovery

  watchtower energy high      Log high energy
  watchtower rest             Record rest day

${chalk.bold('OPTIONAL MODULES')}
${chalk.dim('─'.repeat(50))}

  watchtower work "project"   Start deep work session
  watchtower health data.pdf  Process health data
  watchtower coach "question" Health coaching Q&A

${chalk.bold('CONFIGURATION')}
${chalk.dim('─'.repeat(50))}

  watchtower config --show    View current config
  watchtower config --path    Show config file location

  Enable/disable modules:
    --enable-health, --disable-health
    --enable-weekly, --disable-weekly
    --enable-deepwork, --disable-deepwork

${chalk.dim('For more info: https://github.com/your-repo/watchtower-windows')}
    `);
  });

// Parse and run
program.parse();
