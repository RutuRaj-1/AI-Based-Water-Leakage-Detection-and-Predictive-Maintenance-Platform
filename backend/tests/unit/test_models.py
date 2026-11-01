"""
Unit tests for ORM models.

Verifies model structure, relationships, and audit column mixins.
"""

from uuid import uuid4

import pytest
from sqlalchemy.inspection import inspect

from app.db import (
    Network, Node, Pipe, Sensor, Observation, Anomaly,
    HealthAssessment, RiskPrediction, MaintenanceRecommendation,
    SimulationRun, Base, AuditMixin,
    NodeType, SensorType, AnomalySeverity,
    SimulationStatus, MaintenanceStatus
)


class TestAuditColumns:
    """Test that all models inherit audit columns from AuditMixin."""

    AUDIT_COLUMNS = {'created_at', 'updated_at', 'created_by', 'updated_by', 'is_deleted'}
    
    @pytest.mark.parametrize('model', [
        Network, Node, Pipe, Sensor, Observation, Anomaly,
        HealthAssessment, RiskPrediction, MaintenanceRecommendation,
        SimulationRun
    ])
    def test_model_has_audit_columns(self, model):
        """Verify model has all audit columns."""
        mapper = inspect(model)
        model_columns = {c.name for c in mapper.columns}
        assert self.AUDIT_COLUMNS.issubset(model_columns), \
            f"Model {model.__name__} missing audit columns. Has: {model_columns}"

    @pytest.mark.parametrize('model', [
        Network, Node, Pipe, Sensor, Observation, Anomaly,
        HealthAssessment, RiskPrediction, MaintenanceRecommendation,
        SimulationRun
    ])
    def test_model_has_uuid_primary_key(self, model):
        """Verify model has UUID primary key."""
        mapper = inspect(model)
        pk_columns = mapper.primary_key
        assert len(pk_columns) == 1, f"Model {model.__name__} should have single PK"
        assert pk_columns[0].name == 'id'


class TestNetworkModel:
    """Test Network model."""

    def test_network_tablename(self):
        """Verify table name."""
        assert Network.__tablename__ == 'networks'

    def test_network_required_columns(self):
        """Verify required columns exist."""
        mapper = inspect(Network)
        columns = {c.name for c in mapper.columns}
        assert 'name' in columns
        assert 'srid' in columns


class TestNodeModel:
    """Test Node model."""

    def test_node_tablename(self):
        """Verify table name."""
        assert Node.__tablename__ == 'nodes'

    def test_node_relationships(self):
        """Verify relationships are defined."""
        mapper = inspect(Node)
        relationships = {r.key for r in mapper.relationships}
        assert 'network' in relationships
        assert 'sensors' in relationships


class TestPipeModel:
    """Test Pipe model."""

    def test_pipe_tablename(self):
        """Verify table name."""
        assert Pipe.__tablename__ == 'pipes'

    def test_pipe_relationships(self):
        """Verify relationships are defined."""
        mapper = inspect(Pipe)
        relationships = {r.key for r in mapper.relationships}
        assert 'network' in relationships
        assert 'start_node' in relationships
        assert 'end_node' in relationships
        assert 'sensors' in relationships
        assert 'anomalies' in relationships
        assert 'health_assessments' in relationships
        assert 'risk_predictions' in relationships


class TestSensorModel:
    """Test Sensor model."""

    def test_sensor_tablename(self):
        """Verify table name."""
        assert Sensor.__tablename__ == 'sensors'

    def test_sensor_type_enum_values(self):
        """Verify sensor type enum has expected values."""
        assert SensorType.PRESSURE.value == 'pressure'
        assert SensorType.FLOW.value == 'flow'
        assert SensorType.QUALITY.value == 'quality'
        assert SensorType.TEMPERATURE.value == 'temperature'


class TestObservationModel:
    """Test Observation model."""

    def test_observation_tablename(self):
        """Verify table name."""
        assert Observation.__tablename__ == 'observations'

    def test_observation_relationships(self):
        """Verify relationships are defined."""
        mapper = inspect(Observation)
        relationships = {r.key for r in mapper.relationships}
        assert 'sensor' in relationships
        assert 'simulation_run' in relationships


class TestAnomalyModel:
    """Test Anomaly model."""

    def test_anomaly_tablename(self):
        """Verify table name."""
        assert Anomaly.__tablename__ == 'anomalies'

    def test_anomaly_severity_enum_values(self):
        """Verify severity enum has expected values."""
        assert AnomalySeverity.LOW.value == 'low'
        assert AnomalySeverity.MEDIUM.value == 'medium'
        assert AnomalySeverity.HIGH.value == 'high'
        assert AnomalySeverity.CRITICAL.value == 'critical'


class TestHealthAssessmentModel:
    """Test HealthAssessment model."""

    def test_health_assessment_tablename(self):
        """Verify table name."""
        assert HealthAssessment.__tablename__ == 'health_assessments'


class TestRiskPredictionModel:
    """Test RiskPrediction model."""

    def test_risk_prediction_tablename(self):
        """Verify table name."""
        assert RiskPrediction.__tablename__ == 'risk_predictions'


class TestMaintenanceRecommendationModel:
    """Test MaintenanceRecommendation model."""

    def test_maintenance_recommendation_tablename(self):
        """Verify table name."""
        assert MaintenanceRecommendation.__tablename__ == 'maintenance_recommendations'

    def test_maintenance_status_enum_values(self):
        """Verify status enum has expected values."""
        assert MaintenanceStatus.OPEN.value == 'open'
        assert MaintenanceStatus.IN_PROGRESS.value == 'in_progress'
        assert MaintenanceStatus.COMPLETED.value == 'completed'
        assert MaintenanceStatus.DEFERRED.value == 'deferred'


class TestSimulationRunModel:
    """Test SimulationRun model."""

    def test_simulation_run_tablename(self):
        """Verify table name."""
        assert SimulationRun.__tablename__ == 'simulation_runs'

    def test_simulation_status_enum_values(self):
        """Verify status enum has expected values."""
        assert SimulationStatus.PENDING.value == 'pending'
        assert SimulationStatus.RUNNING.value == 'running'
        assert SimulationStatus.COMPLETED.value == 'completed'
        assert SimulationStatus.FAILED.value == 'failed'


class TestModelInstantiation:
    """Test that models can be instantiated (without DB hit)."""

    def test_network_instantiation(self):
        """Test creating a Network object."""
        network = Network(name="Test Network", srid=4326)
        assert network.id is not None
        assert network.name == "Test Network"
        assert network.srid == 4326
        assert network.is_deleted is False

    def test_node_instantiation(self):
        """Test creating a Node object."""
        node = Node(
            network_id=uuid4(),
            node_type=NodeType.JUNCTION,
            label="Junction 1",
            elevation_m=100.0
        )
        assert node.id is not None
        assert node.label == "Junction 1"

    def test_pipe_instantiation(self):
        """Test creating a Pipe object."""
        pipe = Pipe(
            network_id=uuid4(),
            start_node_id=uuid4(),
            end_node_id=uuid4(),
            label="Pipe 1",
            length_m=500.0,
            diameter_mm=100.0
        )
        assert pipe.id is not None
        assert pipe.length_m == 500.0
