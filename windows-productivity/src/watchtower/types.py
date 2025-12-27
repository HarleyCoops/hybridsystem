"""
Watchtower Windows - Type Definitions
Core types for the productivity system using Pydantic models.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class EnergyLevel(str, Enum):
    """Energy level for productivity tracking."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    DEPLETED = "depleted"
    RECOVERY = "recovery"


class TaskPriority(str, Enum):
    """Task priority based on cognitive energy required."""
    DEEP = "deep"
    STANDARD = "standard"
    LIGHT = "light"
    SOMEDAY = "someday"


class SprintStatusLevel(str, Enum):
    """Sprint health status."""
    HEALTHY = "healthy"
    WARNING = "warning"
    DANGER = "danger"


class BurnoutRisk(str, Enum):
    """Burnout risk assessment."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class SessionType(str, Enum):
    """Type of productivity session."""
    BRIEFING = "briefing"
    CARD = "card"
    ENERGY = "energy"
    ACCOUNTABILITY = "accountability"
    GENERAL = "general"


class EnergyWindow(BaseModel):
    """A peak productivity time window."""
    start: int = Field(ge=0, le=23, description="Start hour (0-23)")
    end: int = Field(ge=0, le=23, description="End hour (0-23)")
    label: Optional[str] = Field(default=None, description="Optional label")


class DocumentNames(BaseModel):
    """Names for the three core documents."""
    daily: str = Field(default="The Watchtower", description="Daily hub document")
    tasks: str = Field(default="The Forge", description="Task pool document")
    journey: str = Field(default="The Long Road", description="Journey tracker document")


class CategoryNames(BaseModel):
    """Names for task categories."""
    deep: str = Field(default="Deep Work Forging", description="High energy work")
    standard: str = Field(default="Standard Forge Work", description="Normal energy work")
    light: str = Field(default="Light Smithing", description="Low energy work")
    someday: str = Field(default="The Anvil Awaits", description="Future tasks")


class SprintThresholds(BaseModel):
    """Sprint thresholds for burnout detection."""
    warning_day: int = Field(default=14, ge=1, description="Days before warning")
    danger_day: int = Field(default=21, ge=1, description="Days before danger alert")


class CoachingVoices(BaseModel):
    """Archetypal coaching personas."""
    discipline: str = Field(default="Marcus Aurelius", description="For avoidance patterns")
    wisdom: str = Field(default="Gandalf", description="For burnout signals")
    leadership: str = Field(default="Aragorn", description="For scattered priorities")


class ModuleSettings(BaseModel):
    """Optional module configuration."""
    health: bool = Field(default=False, description="Enable health tracking")
    weekly_review: bool = Field(default=True, description="Enable weekly reviews")
    deep_work_sessions: bool = Field(default=True, description="Enable deep work sessions")


class SystemSettings(BaseModel):
    """System configuration."""
    timezone: str = Field(default="auto", description="Timezone setting")
    data_dir: str = Field(default="~/.watchtower", description="Data directory")
    sessions_dir: str = Field(default="~/.watchtower/sessions", description="Sessions directory")
    health_log: str = Field(default="~/.watchtower/health-log.md", description="Health log path")


class WatchtowerConfig(BaseModel):
    """Complete Watchtower configuration."""
    documents: DocumentNames = Field(default_factory=DocumentNames)
    energy_windows: list[EnergyWindow] = Field(
        default_factory=lambda: [
            EnergyWindow(start=9, end=13, label="Morning Focus"),
            EnergyWindow(start=15, end=18, label="Afternoon Drive"),
            EnergyWindow(start=20, end=22, label="Evening Flow"),
        ]
    )
    categories: CategoryNames = Field(default_factory=CategoryNames)
    sprint: SprintThresholds = Field(default_factory=SprintThresholds)
    voices: CoachingVoices = Field(default_factory=CoachingVoices)
    modules: ModuleSettings = Field(default_factory=ModuleSettings)
    system: SystemSettings = Field(default_factory=SystemSettings)


class Task(BaseModel):
    """A productivity task."""
    id: str
    content: str
    priority: TaskPriority = TaskPriority.STANDARD
    created_at: datetime
    completed_at: Optional[datetime] = None
    roll_forward_count: int = Field(default=0, ge=0)
    notes: list[str] = Field(default_factory=list)


class EnergyReading(BaseModel):
    """An energy level reading."""
    timestamp: datetime
    level: EnergyLevel
    context: Optional[str] = None


class DailyEntry(BaseModel):
    """A daily productivity entry."""
    date: str
    sprint_day: int
    energy_readings: list[EnergyReading] = Field(default_factory=list)
    tasks_completed: list[str] = Field(default_factory=list)
    tasks_rolled_forward: list[str] = Field(default_factory=list)
    field_reports: list[str] = Field(default_factory=list)
    briefing: Optional[str] = None


class SprintStatus(BaseModel):
    """Current sprint status."""
    current_day: int
    start_date: str
    status: SprintStatusLevel
    last_rest_day: Optional[str] = None


class AvoidancePattern(BaseModel):
    """A detected avoidance pattern."""
    task_id: str
    task_content: str
    roll_count: int
    first_rolled: str
    category: TaskPriority


class EnergyTrend(BaseModel):
    """Energy trend for a time period."""
    period: str  # 'morning', 'afternoon', 'evening'
    average_level: float
    sample_count: int


class CategoryBalance(BaseModel):
    """Distribution of tasks across categories."""
    deep: int = 0
    standard: int = 0
    light: int = 0
    someday: int = 0


class PatternAnalysis(BaseModel):
    """Complete pattern analysis results."""
    avoidance_patterns: list[AvoidancePattern] = Field(default_factory=list)
    energy_trends: list[EnergyTrend] = Field(default_factory=list)
    completion_rate: float = 0.0
    category_balance: CategoryBalance = Field(default_factory=CategoryBalance)
    burnout_risk: BurnoutRisk = BurnoutRisk.LOW


class Session(BaseModel):
    """A productivity session."""
    id: str
    started_at: datetime
    last_activity: datetime
    type: SessionType
    context: Optional[dict] = None


class AgentResponse(BaseModel):
    """Response from the agent."""
    text: str
    tools_used: list[str] = Field(default_factory=list)
    session_id: Optional[str] = None


class ToolResponse(BaseModel):
    """Response from a productivity tool."""
    success: bool
    message: str
    data: Optional[dict] = None
