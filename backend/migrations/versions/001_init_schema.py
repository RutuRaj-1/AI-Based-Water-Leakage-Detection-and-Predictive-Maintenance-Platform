"""init: create initial schema with 10 entities, enums, and indexes

Revision ID: 001
Revises: 
Create Date: 2024-11-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: Create all tables, enums, and indexes."""
    
    # Create ENUM types
    node_type = postgresql.ENUM('junction', 'reservoir', 'tank', name='node_type')
    node_type.create(op.get_bind(), checkfirst=True)
    
    sensor_type = postgresql.ENUM('pressure', 'flow', 'quality', 'temperature', name='sensor_type')
    sensor_type.create(op.get_bind(), checkfirst=True)
    
    anomaly_severity = postgresql.ENUM('low', 'medium', 'high', 'critical', name='anomaly_severity')
    anomaly_severity.create(op.get_bind(), checkfirst=True)
    
    simulation_status = postgresql.ENUM('pending', 'running', 'completed', 'failed', name='simulation_status')
    simulation_status.create(op.get_bind(), checkfirst=True)
    
    maintenance_status = postgresql.ENUM('open', 'in_progress', 'completed', 'deferred', name='maintenance_status')
    maintenance_status.create(op.get_bind(), checkfirst=True)
    
    # Create networks table
    op.create_table(
        'networks',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('srid', sa.Integer(), nullable=False, server_default='4326'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('created_by', sa.String(255), nullable=True),
        sa.Column('updated_by', sa.String(255), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_networks_name', 'networks', ['name'])
    op.create_index('ix_networks_is_deleted', 'networks', ['is_deleted'])
    
    # Create nodes table
    op.create_table(
        'nodes',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('network_id', sa.UUID(), nullable=False),
        sa.Column('node_type', node_type, nullable=False),
        sa.Column('label', sa.String(255), nullable=False),
        sa.Column('elevation_m', sa.Float(), nullable=True),
        sa.Column('location', sa.sql.sqltypes.Geometry('POINT', srid=4326), nullable=False),
        sa.Column('attributes', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('created_by', sa.String(255), nullable=True),
        sa.Column('updated_by', sa.String(255), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
        sa.ForeignKeyConstraint(['network_id'], ['networks.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_nodes_network_id', 'nodes', ['network_id'])
    op.create_index('ix_nodes_is_deleted', 'nodes', ['is_deleted'])
    
    # Create pipes table
    op.create_table(
        'pipes',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('network_id', sa.UUID(), nullable=False),
        sa.Column('start_node_id', sa.UUID(), nullable=False),
        sa.Column('end_node_id', sa.UUID(), nullable=False),
        sa.Column('label', sa.String(255), nullable=False),
        sa.Column('length_m', sa.Float(), nullable=False),
        sa.Column('diameter_mm', sa.Float(), nullable=False),
        sa.Column('material', sa.String(50), nullable=True),
        sa.Column('roughness', sa.Float(), nullable=True),
        sa.Column('installation_year', sa.Integer(), nullable=True),
        sa.Column('geometry', sa.sql.sqltypes.Geometry('LINESTRING', srid=4326), nullable=False),
        sa.Column('attributes', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('created_by', sa.String(255), nullable=True),
        sa.Column('updated_by', sa.String(255), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
        sa.CheckConstraint('length_m > 0', name='check_pipe_length_positive'),
        sa.CheckConstraint('diameter_mm > 0', name='check_pipe_diameter_positive'),
        sa.ForeignKeyConstraint(['network_id'], ['networks.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['start_node_id'], ['nodes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['end_node_id'], ['nodes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_pipes_network_id', 'pipes', ['network_id'])
    op.create_index('ix_pipes_start_node_id', 'pipes', ['start_node_id'])
    op.create_index('ix_pipes_end_node_id', 'pipes', ['end_node_id'])
    op.create_index('ix_pipes_is_deleted', 'pipes', ['is_deleted'])
    
    # Create sensors table
    op.create_table(
        'sensors',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('network_id', sa.UUID(), nullable=False),
        sa.Column('node_id', sa.UUID(), nullable=True),
        sa.Column('pipe_id', sa.UUID(), nullable=True),
        sa.Column('sensor_type', sensor_type, nullable=False),
        sa.Column('label', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('created_by', sa.String(255), nullable=True),
        sa.Column('updated_by', sa.String(255), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
        sa.CheckConstraint('(node_id IS NOT NULL AND pipe_id IS NULL) OR (node_id IS NULL AND pipe_id IS NOT NULL)', name='check_sensor_location'),
        sa.ForeignKeyConstraint(['network_id'], ['networks.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['node_id'], ['nodes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['pipe_id'], ['pipes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_sensors_network_id', 'sensors', ['network_id'])
    op.create_index('ix_sensors_node_id', 'sensors', ['node_id'])
    op.create_index('ix_sensors_pipe_id', 'sensors', ['pipe_id'])
    op.create_index('ix_sensors_is_deleted', 'sensors', ['is_deleted'])
    
    # Create simulation_runs table
    op.create_table(
        'simulation_runs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('network_id', sa.UUID(), nullable=False),
        sa.Column('scenario_name', sa.String(255), nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', simulation_status, nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('created_by', sa.String(255), nullable=True),
        sa.Column('updated_by', sa.String(255), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
        sa.ForeignKeyConstraint(['network_id'], ['networks.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_simulation_runs_network_id', 'simulation_runs', ['network_id'])
    op.create_index('ix_simulation_runs_started_at', 'simulation_runs', ['started_at'])
    op.create_index('ix_simulation_runs_completed_at', 'simulation_runs', ['completed_at'])
    op.create_index('ix_simulation_runs_status', 'simulation_runs', ['status'])
    op.create_index('ix_simulation_runs_is_deleted', 'simulation_runs', ['is_deleted'])
    
    # Create observations table (will be converted to TimescaleDB hypertable)
    op.create_table(
        'observations',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('sensor_id', sa.UUID(), nullable=False),
        sa.Column('simulation_run_id', sa.UUID(), nullable=True),
        sa.Column('observed_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('pressure_kpa', sa.Float(), nullable=True),
        sa.Column('flow_lps', sa.Float(), nullable=True),
        sa.Column('quality_flag', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('created_by', sa.String(255), nullable=True),
        sa.Column('updated_by', sa.String(255), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
        sa.CheckConstraint('quality_flag IN (0, 1, 2)', name='check_observation_quality_flag'),
        sa.ForeignKeyConstraint(['sensor_id'], ['sensors.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['simulation_run_id'], ['simulation_runs.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_observations_observed_at', 'observations', ['observed_at'])
    op.create_index('ix_observations_sensor_id', 'observations', ['sensor_id'])
    op.create_index('ix_observations_simulation_run_id', 'observations', ['simulation_run_id'])
    op.create_index('ix_observations_is_deleted', 'observations', ['is_deleted'])
    
    # Create anomalies table
    op.create_table(
        'anomalies',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('pipe_id', sa.UUID(), nullable=False),
        sa.Column('detected_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('anomaly_type', sa.String(100), nullable=False),
        sa.Column('severity', anomaly_severity, nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False),
        sa.Column('details', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('created_by', sa.String(255), nullable=True),
        sa.Column('updated_by', sa.String(255), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
        sa.CheckConstraint('confidence >= 0.0 AND confidence <= 1.0', name='check_anomaly_confidence'),
        sa.ForeignKeyConstraint(['pipe_id'], ['pipes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_anomalies_pipe_id', 'anomalies', ['pipe_id'])
    op.create_index('ix_anomalies_detected_at', 'anomalies', ['detected_at'])
    op.create_index('ix_anomalies_severity', 'anomalies', ['severity'])
    op.create_index('ix_anomalies_is_deleted', 'anomalies', ['is_deleted'])
    
    # Create health_assessments table
    op.create_table(
        'health_assessments',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('pipe_id', sa.UUID(), nullable=False),
        sa.Column('assessed_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('health_score', sa.Float(), nullable=False),
        sa.Column('component_scores', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('created_by', sa.String(255), nullable=True),
        sa.Column('updated_by', sa.String(255), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
        sa.CheckConstraint('health_score >= 0.0 AND health_score <= 100.0', name='check_health_score_range'),
        sa.ForeignKeyConstraint(['pipe_id'], ['pipes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_health_assessments_pipe_id', 'health_assessments', ['pipe_id'])
    op.create_index('ix_health_assessments_assessed_at', 'health_assessments', ['assessed_at'])
    op.create_index('ix_health_assessments_health_score', 'health_assessments', ['health_score'])
    op.create_index('ix_health_assessments_is_deleted', 'health_assessments', ['is_deleted'])
    
    # Create risk_predictions table
    op.create_table(
        'risk_predictions',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('pipe_id', sa.UUID(), nullable=False),
        sa.Column('predicted_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('horizon_days', sa.Integer(), nullable=False),
        sa.Column('failure_probability', sa.Float(), nullable=False),
        sa.Column('model_version', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('created_by', sa.String(255), nullable=True),
        sa.Column('updated_by', sa.String(255), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
        sa.CheckConstraint('failure_probability >= 0.0 AND failure_probability <= 1.0', name='check_failure_probability'),
        sa.ForeignKeyConstraint(['pipe_id'], ['pipes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_risk_predictions_pipe_id', 'risk_predictions', ['pipe_id'])
    op.create_index('ix_risk_predictions_predicted_at', 'risk_predictions', ['predicted_at'])
    op.create_index('ix_risk_predictions_failure_probability', 'risk_predictions', ['failure_probability'])
    op.create_index('ix_risk_predictions_is_deleted', 'risk_predictions', ['is_deleted'])
    
    # Create maintenance_recommendations table
    op.create_table(
        'maintenance_recommendations',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('risk_prediction_id', sa.UUID(), nullable=False),
        sa.Column('pipe_id', sa.UUID(), nullable=False),
        sa.Column('priority_rank', sa.Integer(), nullable=False),
        sa.Column('recommended_action', sa.String(100), nullable=False),
        sa.Column('estimated_cost_inr', sa.Float(), nullable=True),
        sa.Column('status', maintenance_status, nullable=False, server_default='open'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('created_by', sa.String(255), nullable=True),
        sa.Column('updated_by', sa.String(255), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
        sa.CheckConstraint('priority_rank > 0', name='check_maintenance_priority_positive'),
        sa.ForeignKeyConstraint(['pipe_id'], ['pipes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['risk_prediction_id'], ['risk_predictions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('risk_prediction_id'),
    )
    op.create_index('ix_maintenance_recommendations_pipe_id', 'maintenance_recommendations', ['pipe_id'])
    op.create_index('ix_maintenance_recommendations_priority_rank', 'maintenance_recommendations', ['priority_rank'])
    op.create_index('ix_maintenance_recommendations_status', 'maintenance_recommendations', ['status'])
    op.create_index('ix_maintenance_recommendations_is_deleted', 'maintenance_recommendations', ['is_deleted'])
    
    # Enable TimescaleDB extension and create hypertable for observations
    op.execute('CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;')
    op.execute("""
        SELECT create_hypertable('observations', 'observed_at', if_not_exists => TRUE);
    """)
    # Enable compression for observations older than 7 days
    op.execute("""
        ALTER TABLE observations SET (
            timescaledb.compress = true,
            timescaledb.compress_orderby = 'observed_at DESC',
            timescaledb.compress_segmentby = 'sensor_id'
        );
        SELECT add_compression_policy('observations', INTERVAL '7 days', if_not_exists => true);
    """)


def downgrade() -> None:
    """Downgrade schema: Drop all tables and enums."""
    
    # Drop TimescaleDB hypertable extension (if exists)
    op.execute('DROP EXTENSION IF EXISTS timescaledb CASCADE;')
    
    # Drop tables in reverse order of creation (respecting FKs)
    op.drop_table('maintenance_recommendations')
    op.drop_table('risk_predictions')
    op.drop_table('health_assessments')
    op.drop_table('anomalies')
    op.drop_table('observations')
    op.drop_table('simulation_runs')
    op.drop_table('sensors')
    op.drop_table('pipes')
    op.drop_table('nodes')
    op.drop_table('networks')
    
    # Drop ENUMs
    op.execute('DROP TYPE IF EXISTS maintenance_status;')
    op.execute('DROP TYPE IF EXISTS simulation_status;')
    op.execute('DROP TYPE IF EXISTS anomaly_severity;')
    op.execute('DROP TYPE IF EXISTS sensor_type;')
    op.execute('DROP TYPE IF EXISTS node_type;')
