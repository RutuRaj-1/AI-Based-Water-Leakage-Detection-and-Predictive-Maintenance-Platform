"""
SQLAlchemy ORM models for the Pune Water Network AI system.

This module defines all 10 entities:
1. Network: Top-level water distribution network container
2. Node: Junctions, reservoirs, tanks in the network
3. Pipe: Segments connecting nodes
4. Sensor: Logical sensor definitions on nodes/pipes
5. Observation: Time-series pressure/flow readings (TimescaleDB hypertable)
6. Anomaly: Detected anomalous events
7. HealthAssessment: Composite health scores per pipe
8. RiskPrediction: Failure probability estimates
9. MaintenanceRecommendation: Ranked work orders
10. SimulationRun: Metadata for simulation executions

All models inherit from AuditMixin for full audit trail (created_at, updated_at, 
created_by, updated_by, is_deleted) and use UUID primary keys.

Relationships respect FK dependencies and use CASCADE delete where appropriate.
Time-series data (observations) uses JSONB for extensibility.
Geometric data uses PostGIS types (Point, LineString).
"""

from datetime import datetime
from enum import Enum as PyEnum
from uuid import UUID, uuid4

from geoalchemy2 import Geometry
from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import AuditMixin, Base


# ============================================================================
# ENUMS
# ============================================================================


class NodeType(str, PyEnum):
    """Types of nodes in the water network."""

    JUNCTION = "junction"
    RESERVOIR = "reservoir"
    TANK = "tank"


class SensorType(str, PyEnum):
    """Types of sensors in the network."""

    PRESSURE = "pressure"
    FLOW = "flow"
    QUALITY = "quality"
    TEMPERATURE = "temperature"


class AnomalySeverity(str, PyEnum):
    """Severity levels for detected anomalies."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SimulationStatus(str, PyEnum):
    """Status of a simulation run."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class MaintenanceStatus(str, PyEnum):
    """Status of a maintenance recommendation."""

    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DEFERRED = "deferred"


# ============================================================================
# MODELS
# ============================================================================


class Network(AuditMixin, Base):
    """
    Top-level container for a water distribution network.

    Represents a named Pune water zone or service area.
    All other entities (nodes, pipes, sensors, observations) belong to a network.

    Example:
        Pune Zone A (Synthetic), Pune Zone B (Real), etc.

    Indexes:
        - name (for lookups)
        - is_deleted (for soft-delete filtering)
    """

    __tablename__ = "networks"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    srid: Mapped[int] = mapped_column(
        Integer, default=4326, nullable=False, comment="Spatial reference ID (e.g., 4326=WGS84)"
    )

    # Relationships
    nodes: Mapped[list["Node"]] = relationship(
        "Node",
        back_populates="network",
        cascade="all, delete-orphan",
        foreign_keys="Node.network_id",
    )
    pipes: Mapped[list["Pipe"]] = relationship(
        "Pipe",
        back_populates="network",
        cascade="all, delete-orphan",
        foreign_keys="Pipe.network_id",
    )
    sensors: Mapped[list["Sensor"]] = relationship(
        "Sensor",
        back_populates="network",
        cascade="all, delete-orphan",
        foreign_keys="Sensor.network_id",
    )
    simulation_runs: Mapped[list["SimulationRun"]] = relationship(
        "SimulationRun",
        back_populates="network",
        cascade="all, delete-orphan",
        foreign_keys="SimulationRun.network_id",
    )

    def __repr__(self) -> str:
        return f"<Network(id={self.id}, name='{self.name}')>"


class Node(AuditMixin, Base):
    """
    Junctions, reservoirs, and tanks in the water network graph.

    A node is a vertex in the network topology. It can be a junction (pipe
    connection point), a reservoir (source), or a tank (storage).

    Indexes:
        - network_id (for filtering by network)
        - geometry (PostGIS spatial index, automatic)
        - is_deleted (for soft-delete)

    Spatial:
        - location: WGS84 point (EPSG:4326)
    """

    __tablename__ = "nodes"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    network_id: Mapped[UUID] = mapped_column(
        ForeignKey("networks.id", ondelete="CASCADE"), nullable=False, index=True
    )
    node_type: Mapped[NodeType] = mapped_column(Enum(NodeType), nullable=False)
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    elevation_m: Mapped[float] = mapped_column(Float, nullable=True, comment="Elevation in metres")
    location: Mapped[Geometry] = mapped_column(
        Geometry("POINT", srid=4326), nullable=False, comment="WGS84 geographic point"
    )
    attributes: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="Extensible metadata")

    # Relationships
    network: Mapped["Network"] = relationship("Network", back_populates="nodes")
    sensors: Mapped[list["Sensor"]] = relationship(
        "Sensor",
        back_populates="node",
        cascade="all, delete-orphan",
        foreign_keys="Sensor.node_id",
    )
    pipes_as_start: Mapped[list["Pipe"]] = relationship(
        "Pipe",
        back_populates="start_node",
        foreign_keys="Pipe.start_node_id",
        cascade="all, delete-orphan",
    )
    pipes_as_end: Mapped[list["Pipe"]] = relationship(
        "Pipe",
        back_populates="end_node",
        foreign_keys="Pipe.end_node_id",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Node(id={self.id}, label='{self.label}', type={self.node_type})>"


class Pipe(AuditMixin, Base):
    """
    Pipe segments connecting pairs of nodes in the network.

    A pipe is an edge in the network graph with hydraulic properties
    (length, diameter, material, roughness). Observations and anomalies
    are tracked per pipe.

    Indexes:
        - network_id (for filtering by network)
        - start_node_id, end_node_id (for topology queries)
        - geometry (PostGIS spatial index, automatic)
        - is_deleted (for soft-delete)

    Spatial:
        - geometry: WGS84 linestring (EPSG:4326)

    Open questions:
        - Should we store calculated flow direction? (currently directional via start/end)
    """

    __tablename__ = "pipes"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    network_id: Mapped[UUID] = mapped_column(
        ForeignKey("networks.id", ondelete="CASCADE"), nullable=False, index=True
    )
    start_node_id: Mapped[UUID] = mapped_column(
        ForeignKey("nodes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    end_node_id: Mapped[UUID] = mapped_column(
        ForeignKey("nodes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    length_m: Mapped[float] = mapped_column(Float, nullable=False, comment="Length in metres")
    diameter_mm: Mapped[float] = mapped_column(Float, nullable=False, comment="Diameter in millimetres")
    material: Mapped[str] = mapped_column(
        String(50), nullable=True, comment="Material type (e.g., CI, PVC, DI, AC)"
    )
    roughness: Mapped[float] = mapped_column(
        Float, nullable=True, comment="Hazen-Williams or Darcy-Weisbach coefficient"
    )
    installation_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    geometry: Mapped[Geometry] = mapped_column(
        Geometry("LINESTRING", srid=4326), nullable=False, comment="WGS84 linestring"
    )
    attributes: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="Extensible metadata")

    # Relationships
    network: Mapped["Network"] = relationship("Network", back_populates="pipes")
    start_node: Mapped["Node"] = relationship(
        "Node", back_populates="pipes_as_start", foreign_keys=[start_node_id]
    )
    end_node: Mapped["Node"] = relationship(
        "Node", back_populates="pipes_as_end", foreign_keys=[end_node_id]
    )
    sensors: Mapped[list["Sensor"]] = relationship(
        "Sensor",
        back_populates="pipe",
        cascade="all, delete-orphan",
        foreign_keys="Sensor.pipe_id",
    )
    anomalies: Mapped[list["Anomaly"]] = relationship(
        "Anomaly",
        back_populates="pipe",
        cascade="all, delete-orphan",
        foreign_keys="Anomaly.pipe_id",
    )
    health_assessments: Mapped[list["HealthAssessment"]] = relationship(
        "HealthAssessment",
        back_populates="pipe",
        cascade="all, delete-orphan",
        foreign_keys="HealthAssessment.pipe_id",
    )
    risk_predictions: Mapped[list["RiskPrediction"]] = relationship(
        "RiskPrediction",
        back_populates="pipe",
        cascade="all, delete-orphan",
        foreign_keys="RiskPrediction.pipe_id",
    )
    maintenance_recommendations: Mapped[list["MaintenanceRecommendation"]] = relationship(
        "MaintenanceRecommendation",
        back_populates="pipe",
        cascade="all, delete-orphan",
        foreign_keys="MaintenanceRecommendation.pipe_id",
    )

    __table_args__ = (
        CheckConstraint("length_m > 0", name="check_pipe_length_positive"),
        CheckConstraint("diameter_mm > 0", name="check_pipe_diameter_positive"),
    )

    def __repr__(self) -> str:
        return f"<Pipe(id={self.id}, label='{self.label}', length={self.length_m}m)>"


class Sensor(AuditMixin, Base):
    """
    Logical sensor definitions attached to nodes or pipes.

    A sensor is a measurement device that produces observations (pressure, flow, etc.).
    It can be attached to either a node (junction pressure) or a pipe (flow/quality).

    Constraint:
        - Exactly one of node_id or pipe_id must be non-null (not both, not neither).

    Indexes:
        - network_id (for filtering)
        - node_id, pipe_id (for sensor location)
        - is_deleted (for soft-delete)
    """

    __tablename__ = "sensors"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    network_id: Mapped[UUID] = mapped_column(
        ForeignKey("networks.id", ondelete="CASCADE"), nullable=False, index=True
    )
    node_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("nodes.id", ondelete="CASCADE"), nullable=True, index=True
    )
    pipe_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("pipes.id", ondelete="CASCADE"), nullable=True, index=True
    )
    sensor_type: Mapped[SensorType] = mapped_column(Enum(SensorType), nullable=False)
    label: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relationships
    network: Mapped["Network"] = relationship("Network", back_populates="sensors")
    node: Mapped["Node | None"] = relationship("Node", back_populates="sensors")
    pipe: Mapped["Pipe | None"] = relationship("Pipe", back_populates="sensors")
    observations: Mapped[list["Observation"]] = relationship(
        "Observation",
        back_populates="sensor",
        cascade="all, delete-orphan",
        foreign_keys="Observation.sensor_id",
    )

    __table_args__ = (
        CheckConstraint(
            "(node_id IS NOT NULL AND pipe_id IS NULL) OR (node_id IS NULL AND pipe_id IS NOT NULL)",
            name="check_sensor_location",
        ),
    )

    def __repr__(self) -> str:
        return f"<Sensor(id={self.id}, label='{self.label}', type={self.sensor_type})>"


class Observation(AuditMixin, Base):
    """
    Time-series pressure and flow readings from sensors (real or synthetic).

    This table is backed by a TimescaleDB hypertable, automatically partitioned
    by the observed_at timestamp. This enables efficient querying and compression
    of high-volume sensor data.

    Indexes:
        - observed_at (primary time index, automatic via hypertable)
        - sensor_id (for filtering by sensor)
        - simulation_run_id (for grouping by scenario run)
        - is_deleted (for soft-delete)

    Note:
        - pressure_kpa: nullable (not all sensors measure pressure)
        - flow_lps: nullable (not all sensors measure flow)
        - quality_flag: 0=ok, 1=suspect, 2=bad (for data QA)
        - simulation_run_id: null for real readings, non-null for synthetic

    TimescaleDB:
        - Hypertable on (observed_at, sensor_id) enables efficient compression
          of old data (e.g., compress after 7 days).
    """

    __tablename__ = "observations"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    sensor_id: Mapped[UUID] = mapped_column(
        ForeignKey("sensors.id", ondelete="CASCADE"), nullable=False, index=True
    )
    simulation_run_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("simulation_runs.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="NULL for real readings; non-NULL for synthetic",
    )
    observed_at: Mapped[datetime] = mapped_column(
        nullable=False, index=True, comment="Observation timestamp (time-series key)"
    )
    pressure_kpa: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Pressure in kPa")
    flow_lps: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Flow in litres/second")
    quality_flag: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False, comment="0=ok, 1=suspect, 2=bad"
    )

    # Relationships
    sensor: Mapped["Sensor"] = relationship("Sensor", back_populates="observations")
    simulation_run: Mapped["SimulationRun | None"] = relationship(
        "SimulationRun", back_populates="observations"
    )

    __table_args__ = (
        CheckConstraint("quality_flag IN (0, 1, 2)", name="check_observation_quality_flag"),
    )

    def __repr__(self) -> str:
        return (
            f"<Observation(id={self.id}, sensor_id={self.sensor_id}, "
            f"observed_at={self.observed_at}, pressure={self.pressure_kpa}, flow={self.flow_lps})>"
        )


class Anomaly(AuditMixin, Base):
    """
    Detected anomalous events in pipe data (leaks, pressure drops, flow surges, etc.).

    Anomalies are flagged by the ML pipeline and stored with:
    - Type: e.g., "pressure_drop", "flow_surge", "leak_signature"
    - Severity: low, medium, high, critical
    - Confidence: ML model confidence (0.0–1.0)
    - Details: Raw model outputs, feature values, evidence

    Indexes:
        - pipe_id (for querying anomalies on a pipe)
        - detected_at (for time-range queries)
        - severity (for filtering by criticality)
        - is_deleted (for soft-delete)

    Note:
        - Anomalies may overlap in time (multiple events on same pipe).
        - Details (JSONB) stores model-specific evidence for forensics.
    """

    __tablename__ = "anomalies"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    pipe_id: Mapped[UUID] = mapped_column(
        ForeignKey("pipes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    detected_at: Mapped[datetime] = mapped_column(nullable=False, index=True)
    anomaly_type: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="e.g., 'pressure_drop', 'flow_surge', 'leak_signature'"
    )
    severity: Mapped[AnomalySeverity] = mapped_column(Enum(AnomalySeverity), nullable=False, index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, comment="Model confidence 0.0–1.0")
    details: Mapped[dict | None] = mapped_column(
        JSON, nullable=True, comment="Raw model output, feature values, evidence"
    )

    # Relationships
    pipe: Mapped["Pipe"] = relationship("Pipe", back_populates="anomalies")

    __table_args__ = (
        CheckConstraint("confidence >= 0.0 AND confidence <= 1.0", name="check_anomaly_confidence"),
    )

    def __repr__(self) -> str:
        return (
            f"<Anomaly(id={self.id}, pipe_id={self.pipe_id}, "
            f"type='{self.anomaly_type}', severity={self.severity})>"
        )


class HealthAssessment(AuditMixin, Base):
    """
    Composite health score for a pipe at a point in time.

    A health assessment captures the overall condition of a pipe (0=failed, 100=perfect)
    and breaks down the score by contributing factors (age, material, anomaly history, etc.).

    Indexes:
        - pipe_id (for pipe health history)
        - assessed_at (for timeline queries)
        - health_score (for ranking by condition)
        - is_deleted (for soft-delete)

    Note:
        - component_scores (JSONB) stores the breakdown:
          {"age_factor": 0.8, "material_factor": 0.9, "anomaly_factor": 0.7, ...}
        - Useful for maintenance prioritization and trend analysis.
    """

    __tablename__ = "health_assessments"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    pipe_id: Mapped[UUID] = mapped_column(
        ForeignKey("pipes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    assessed_at: Mapped[datetime] = mapped_column(nullable=False, index=True)
    health_score: Mapped[float] = mapped_column(Float, nullable=False, index=True, comment="0 (failed) – 100 (perfect)")
    component_scores: Mapped[dict | None] = mapped_column(
        JSON, nullable=True, comment="Breakdown by contributing factor (e.g., age, material, anomalies)"
    )

    # Relationships
    pipe: Mapped["Pipe"] = relationship("Pipe", back_populates="health_assessments")

    __table_args__ = (
        CheckConstraint("health_score >= 0.0 AND health_score <= 100.0", name="check_health_score_range"),
    )

    def __repr__(self) -> str:
        return (
            f"<HealthAssessment(id={self.id}, pipe_id={self.pipe_id}, "
            f"health_score={self.health_score}, assessed_at={self.assessed_at})>"
        )


class RiskPrediction(AuditMixin, Base):
    """
    Failure probability estimate for a pipe over a planning horizon.

    Risk predictions are generated by the ML pipeline to estimate the likelihood
    of pipe failure in the next N days. Used for maintenance prioritization.

    Indexes:
        - pipe_id (for pipe risk history)
        - predicted_at (for forecast timeline)
        - failure_probability (for ranking by risk)
        - is_deleted (for soft-delete)

    Note:
        - horizon_days: planning window (e.g., 30, 90, 365)
        - model_version: tracks which model generated the prediction
    """

    __tablename__ = "risk_predictions"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    pipe_id: Mapped[UUID] = mapped_column(
        ForeignKey("pipes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    predicted_at: Mapped[datetime] = mapped_column(nullable=False, index=True)
    horizon_days: Mapped[int] = mapped_column(Integer, nullable=False, comment="Planning horizon (e.g., 30, 90, 365)")
    failure_probability: Mapped[float] = mapped_column(
        Float, nullable=False, index=True, comment="Predicted failure probability 0.0–1.0"
    )
    model_version: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="Model version identifier")

    # Relationships
    pipe: Mapped["Pipe"] = relationship("Pipe", back_populates="risk_predictions")
    maintenance_recommendation: Mapped["MaintenanceRecommendation | None"] = relationship(
        "MaintenanceRecommendation",
        back_populates="risk_prediction",
        uselist=False,
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        CheckConstraint("failure_probability >= 0.0 AND failure_probability <= 1.0", name="check_failure_probability"),
    )

    def __repr__(self) -> str:
        return (
            f"<RiskPrediction(id={self.id}, pipe_id={self.pipe_id}, "
            f"failure_prob={self.failure_probability}, horizon={self.horizon_days}d)>"
        )


class MaintenanceRecommendation(AuditMixin, Base):
    """
    Ranked work orders derived from risk predictions and health assessments.

    Maintenance recommendations are prioritized actions (inspect, repair, replace)
    with estimated costs and status tracking.

    Indexes:
        - pipe_id (for pipe work order history)
        - risk_prediction_id (for linking to risk forecast)
        - priority_rank (for work queue ordering)
        - status (for filtering open/in-progress/completed)
        - is_deleted (for soft-delete)

    Note:
        - priority_rank: lower number = higher priority (1 is most urgent)
        - status: open, in_progress, completed, deferred
        - Linked to RiskPrediction (1-to-1 via risk_prediction_id)
    """

    __tablename__ = "maintenance_recommendations"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    risk_prediction_id: Mapped[UUID] = mapped_column(
        ForeignKey("risk_predictions.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    pipe_id: Mapped[UUID] = mapped_column(
        ForeignKey("pipes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    priority_rank: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment="Lower = higher priority")
    recommended_action: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="e.g., 'inspect', 'repair', 'replace'"
    )
    estimated_cost_inr: Mapped[float | None] = mapped_column(Float, nullable=True, comment="Estimated cost in INR")
    status: Mapped[MaintenanceStatus] = mapped_column(Enum(MaintenanceStatus), default=MaintenanceStatus.OPEN, nullable=False, index=True)

    # Relationships
    risk_prediction: Mapped["RiskPrediction"] = relationship(
        "RiskPrediction", back_populates="maintenance_recommendation"
    )
    pipe: Mapped["Pipe"] = relationship("Pipe", back_populates="maintenance_recommendations")

    __table_args__ = (
        CheckConstraint("priority_rank > 0", name="check_maintenance_priority_positive"),
    )

    def __repr__(self) -> str:
        return (
            f"<MaintenanceRecommendation(id={self.id}, pipe_id={self.pipe_id}, "
            f"priority={self.priority_rank}, status={self.status})>"
        )


class SimulationRun(AuditMixin, Base):
    """
    Metadata for a hydraulic simulation execution.

    A simulation run represents a single WNTR/EPANET scenario execution with
    injected faults (leaks, pump failures, etc.), generating synthetic observations
    and test data for model training/evaluation.

    Indexes:
        - network_id (for filtering by network)
        - status (for finding active/completed runs)
        - started_at, completed_at (for temporal queries)
        - is_deleted (for soft-delete)

    Note:
        - scenario_name: describes the fault injection (e.g., "leak_node_N1_t500-t700")
        - started_at, completed_at: timestamps in UTC
        - status: pending, running, completed, failed
        - Observations linked to this run (via observation.simulation_run_id)
    """

    __tablename__ = "simulation_runs"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    network_id: Mapped[UUID] = mapped_column(
        ForeignKey("networks.id", ondelete="CASCADE"), nullable=False, index=True
    )
    scenario_name: Mapped[str] = mapped_column(String(255), nullable=False, comment="Scenario description (e.g., 'leak_node_N1')")
    started_at: Mapped[datetime] = mapped_column(nullable=False, index=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    status: Mapped[SimulationStatus] = mapped_column(Enum(SimulationStatus), default=SimulationStatus.PENDING, nullable=False, index=True)

    # Relationships
    network: Mapped["Network"] = relationship("Network", back_populates="simulation_runs")
    observations: Mapped[list["Observation"]] = relationship(
        "Observation",
        back_populates="simulation_run",
        cascade="all, delete-orphan",
        foreign_keys="Observation.simulation_run_id",
    )

    def __repr__(self) -> str:
        return (
            f"<SimulationRun(id={self.id}, network_id={self.network_id}, "
            f"scenario='{self.scenario_name}', status={self.status})>"
        )

