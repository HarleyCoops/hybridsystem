# Watchtower Windows - Architecture

Technical architecture and design decisions for the Windows productivity system.

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    WATCHTOWER WINDOWS                           │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  CLI Layer (src/cli.ts)                                  │  │
│  │  - Commander.js for argument parsing                     │  │
│  │  - Chalk for colored output                              │  │
│  │  - Ora for spinners                                      │  │
│  └────────────────────────┬─────────────────────────────────┘  │
│                           │                                     │
│  ┌────────────────────────▼─────────────────────────────────┐  │
│  │  Agent Layer (src/core/agent.ts)                         │  │
│  │  - Claude Agent SDK integration                          │  │
│  │  - System prompt construction                            │  │
│  │  - Coaching voice selection                              │  │
│  │  - Pattern-aware context building                        │  │
│  └────────────────────────┬─────────────────────────────────┘  │
│                           │                                     │
│  ┌────────────────────────▼─────────────────────────────────┐  │
│  │  Tools Layer (src/tools/productivity.ts)                 │  │
│  │  - Task management (add, complete, roll forward)         │  │
│  │  - Energy tracking                                       │  │
│  │  - Sprint management                                     │  │
│  │  - Pattern analysis                                      │  │
│  └────────────────────────┬─────────────────────────────────┘  │
│                           │                                     │
│  ┌────────────────────────▼─────────────────────────────────┐  │
│  │  State Layer (src/core/state.ts)                         │  │
│  │  - JSON file persistence                                 │  │
│  │  - Task CRUD operations                                  │  │
│  │  - Daily entry management                                │  │
│  │  - Sprint tracking                                       │  │
│  └────────────────────────┬─────────────────────────────────┘  │
│                           │                                     │
│  ┌────────────────────────▼─────────────────────────────────┐  │
│  │  Config Layer (src/core/config.ts)                       │  │
│  │  - Conf package for persistent config                    │  │
│  │  - JSON schema validation                                │  │
│  │  - Default values                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Platform Layer (src/utils/windows.ts)                   │  │
│  │  - Windows notifications                                 │  │
│  │  - Task Scheduler integration                            │  │
│  │  - Clipboard operations                                  │  │
│  │  - System detection                                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  EXTERNAL SERVICES                                              │
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────────┐  │
│  │  Claude API     │  │  Craft MCP      │  │  File System   │  │
│  │  (via SDK)      │  │  (optional)     │  │  (local JSON)  │  │
│  └─────────────────┘  └─────────────────┘  └────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### CLI Layer (`src/cli.ts`)

**Purpose**: Entry point for all user interactions

**Key Responsibilities**:
- Parse command-line arguments
- Route to appropriate handlers
- Display formatted output
- Handle errors gracefully

**Technology Choices**:
- **Commander.js**: Industry-standard CLI framework
- **Chalk**: Cross-platform terminal colors
- **Ora**: Elegant loading spinners
- **Inquirer**: Interactive prompts (future)

### Agent Layer (`src/core/agent.ts`)

**Purpose**: Orchestrate AI-powered analysis and responses

**Key Responsibilities**:
- Build context-aware system prompts
- Select appropriate coaching voice based on patterns
- Invoke Claude SDK with proper configuration
- Handle streaming responses

**Design Patterns**:
- **Prompt Engineering**: Dynamic prompts based on state
- **Voice Selection**: Pattern-to-voice mapping
- **Context Injection**: State summary included in prompts

### Tools Layer (`src/tools/productivity.ts`)

**Purpose**: Provide structured operations the agent can invoke

**Key Responsibilities**:
- Task CRUD operations with validation
- Energy level tracking with recommendations
- Sprint management with status assessment
- Pattern analysis calculations

**Design Patterns**:
- **Command Pattern**: Each tool is a self-contained operation
- **Response Objects**: Consistent `ToolResponse` structure

### State Layer (`src/core/state.ts`)

**Purpose**: Manage persistent data storage

**Key Responsibilities**:
- Load/save JSON files atomically
- Provide typed access to data structures
- Calculate derived metrics
- Maintain data integrity

**Data Files**:
- `tasks.json`: Task database
- `daily.json`: Daily entries by date
- `sprint.json`: Sprint tracking
- `sessions.json`: Session history

### Config Layer (`src/core/config.ts`)

**Purpose**: Manage user preferences

**Key Responsibilities**:
- Load configuration with defaults
- Validate configuration schema
- Provide typed access
- Persist changes

**Technology Choice**:
- **Conf**: Electron-style config management with JSON schema

### Platform Layer (`src/utils/windows.ts`)

**Purpose**: Abstract platform-specific functionality

**Key Responsibilities**:
- Windows toast notifications
- Task Scheduler integration
- Clipboard operations
- System information

**Design Patterns**:
- **Platform Detection**: Runtime checks for Windows
- **Graceful Degradation**: Fallbacks for non-Windows

## Data Flow

### Morning Briefing Flow

```
1. User runs: watchtower brief
2. CLI invokes: runMorningBriefing()
3. Agent layer:
   a. Loads current state (tasks, sprint, patterns)
   b. Builds system prompt with coaching voice
   c. Constructs state context
   d. Invokes Claude SDK with prompt
4. Claude processes and returns briefing text
5. CLI displays formatted output
```

### Card Processing Flow

```
1. User runs: watchtower card photo.jpg
2. CLI invokes: processCard(imagePath)
3. Agent layer:
   a. Builds vision-enabled prompt
   b. Attaches image file
   c. Invokes Claude SDK
4. Claude:
   a. Reads handwriting via vision
   b. Identifies completed (●) vs incomplete (○)
   c. Returns structured analysis
5. Tools layer:
   a. Updates task completion status
   b. Increments roll-forward counts
   c. Updates daily entry
6. CLI displays summary
```

### Pattern Analysis Flow

```
1. User runs: watchtower accountability
2. CLI invokes: runAccountabilityCheck()
3. State layer calculates:
   a. Avoidance patterns (tasks rolled 3+)
   b. Energy trends by time of day
   c. Completion rate over 7 days
   d. Category balance
   e. Burnout risk score
4. Agent layer:
   a. Selects coaching voice based on patterns
   b. Includes all pattern data in prompt
   c. Invokes Claude for analysis
5. Claude provides contextual coaching
6. CLI displays formatted analysis
```

## Design Decisions

### Why TypeScript?

1. **Type Safety**: Catch errors at compile time
2. **IDE Support**: Excellent autocomplete and refactoring
3. **Claude SDK**: Native TypeScript support
4. **Cross-Platform**: Node.js runs everywhere

### Why JSON for Storage?

1. **Simplicity**: No database setup required
2. **Portability**: Easy backup and restore
3. **Debuggability**: Human-readable files
4. **Sufficient Scale**: Personal productivity data is small

### Why Commander.js?

1. **Maturity**: Battle-tested in production
2. **Features**: Subcommands, options, help generation
3. **Ecosystem**: Wide adoption, good documentation

### Why Not SQLite?

1. **Overkill**: Simple key-value suffices
2. **Complexity**: Additional dependency
3. **Portability**: JSON files are more portable

## Extension Points

### Adding New Commands

1. Define handler in `src/commands/` (future)
2. Register in `src/cli.ts`
3. Implement business logic in tools/agent layer

### Adding New Tools

1. Create function in `src/tools/productivity.ts`
2. Export in tool registry
3. Document in help text

### Adding Platform Support

1. Add detection in `src/utils/`
2. Implement platform-specific functions
3. Use graceful degradation

## Performance Considerations

### Startup Time

- Lazy loading of state files
- Minimal synchronous operations
- Config cached after first load

### API Calls

- Single Claude call per command (typically)
- Context built from local state
- No redundant API calls

### File I/O

- Atomic writes prevent corruption
- Read-once, cache in memory
- Minimal file operations

## Security Considerations

### Data Privacy

- All data stored locally
- No telemetry or analytics
- Health data explicitly private

### API Key Safety

- Key read from environment only
- Never logged or stored in files
- Clear error messages for missing key

### Input Validation

- Config schema validation
- Path sanitization
- Safe JSON parsing
