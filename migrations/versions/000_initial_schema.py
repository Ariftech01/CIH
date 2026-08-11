"""initial_schema

Revision ID: 000_initial_schema
Revises: 
Create Date: 2026-08-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '000_initial_schema'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # 1. users
    op.create_table(
        'users',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=100), nullable=True),
        sa.Column('email', sa.String(length=100), nullable=True),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(length=36), nullable=True),
        sa.Column('updated_by', sa.String(length=36), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_id', 'users', ['id'])
    op.create_index('ix_users_username', 'users', ['username'], unique=True)

    # 2. projects
    op.create_table(
        'projects',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('project_name', sa.String(length=100), nullable=False),
        sa.Column('project_code', sa.String(length=20), nullable=False),
        sa.Column('client_name', sa.String(length=100), nullable=True),
        sa.Column('project_location', sa.String(length=200), nullable=True),
        sa.Column('budget', sa.Float(), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('expected_end_date', sa.Date(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('building_type', sa.String(length=50), nullable=True),
        sa.Column('total_builtup_area', sa.Float(), nullable=True),
        sa.Column('site_area', sa.Float(), nullable=True),
        sa.Column('construction_area', sa.Float(), nullable=True),
        sa.Column('number_of_floors', sa.Integer(), nullable=True),
        sa.Column('basement_floors', sa.Integer(), nullable=True),
        sa.Column('terrace_count', sa.Integer(), nullable=True),
        sa.Column('parking_levels', sa.Integer(), nullable=True),
        sa.Column('roof_type', sa.String(length=50), nullable=True),
        sa.Column('building_orientation', sa.String(length=30), nullable=True),
        sa.Column('foundation_type', sa.String(length=50), nullable=True),
        sa.Column('frame_type', sa.String(length=50), nullable=True),
        sa.Column('structural_material', sa.String(length=50), nullable=True),
        sa.Column('concrete_grade', sa.String(length=20), nullable=True),
        sa.Column('steel_grade', sa.String(length=20), nullable=True),
        sa.Column('seismic_zone', sa.String(length=20), nullable=True),
        sa.Column('wind_zone', sa.String(length=20), nullable=True),
        sa.Column('number_of_rooms', sa.Integer(), nullable=True),
        sa.Column('bedrooms', sa.Integer(), nullable=True),
        sa.Column('bathrooms', sa.Integer(), nullable=True),
        sa.Column('living_rooms', sa.Integer(), nullable=True),
        sa.Column('kitchens', sa.Integer(), nullable=True),
        sa.Column('conference_rooms', sa.Integer(), nullable=True),
        sa.Column('office_rooms', sa.Integer(), nullable=True),
        sa.Column('storage_rooms', sa.Integer(), nullable=True),
        sa.Column('corridors', sa.Integer(), nullable=True),
        sa.Column('staircases', sa.Integer(), nullable=True),
        sa.Column('elevators', sa.Integer(), nullable=True),
        sa.Column('emergency_exits', sa.Integer(), nullable=True),
        sa.Column('balconies', sa.Integer(), nullable=True),
        sa.Column('utility_rooms', sa.Integer(), nullable=True),
        sa.Column('construction_phase', sa.String(length=50), nullable=True),
        sa.Column('owner_name', sa.String(length=100), nullable=True),
        sa.Column('contractor_name', sa.String(length=100), nullable=True),
        sa.Column('architect_name', sa.String(length=100), nullable=True),
        sa.Column('consultant_name', sa.String(length=100), nullable=True),
        sa.Column('manager_name', sa.String(length=100), nullable=True),
        sa.Column('site_engineer_name', sa.String(length=100), nullable=True),
        sa.Column('priority', sa.String(length=20), nullable=True),
        sa.Column('model_geometry_json', sa.Text(), nullable=True),
        sa.Column('current_version', sa.String(length=20), nullable=True),
        sa.Column('version_history_json', sa.Text(), nullable=True),
        sa.Column('user_id', sa.String(length=36), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(length=36), nullable=True),
        sa.Column('updated_by', sa.String(length=36), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_projects_id', 'projects', ['id'])
    op.create_index('ix_projects_project_code', 'projects', ['project_code'], unique=True)
    op.create_index('ix_projects_project_name', 'projects', ['project_name'])

    # 3. buildings
    op.create_table(
        'buildings',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('project_id', sa.String(length=36), nullable=False),
        sa.Column('building_name', sa.String(length=100), nullable=False),
        sa.Column('building_code', sa.String(length=30), nullable=False),
        sa.Column('building_type', sa.String(length=50), nullable=True),
        sa.Column('total_floors', sa.Integer(), nullable=True),
        sa.Column('total_area_sqft', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(length=36), nullable=True),
        sa.Column('updated_by', sa.String(length=36), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_buildings_id', 'buildings', ['id'])

    # 4. floors
    op.create_table(
        'floors',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('building_id', sa.String(length=36), nullable=False),
        sa.Column('floor_number', sa.Integer(), nullable=False),
        sa.Column('floor_name', sa.String(length=50), nullable=True),
        sa.Column('floor_type', sa.String(length=50), nullable=True),
        sa.Column('elevation_m', sa.Float(), nullable=True),
        sa.Column('area_sqft', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(length=36), nullable=True),
        sa.Column('updated_by', sa.String(length=36), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['building_id'], ['buildings.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_floors_id', 'floors', ['id'])

    # 5. rooms
    op.create_table(
        'rooms',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('floor_id', sa.String(length=36), nullable=False),
        sa.Column('room_number', sa.String(length=30), nullable=False),
        sa.Column('room_name', sa.String(length=100), nullable=True),
        sa.Column('room_type', sa.String(length=50), nullable=True),
        sa.Column('area_sqft', sa.Float(), nullable=True),
        sa.Column('height_m', sa.Float(), nullable=True),
        sa.Column('capacity', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(length=36), nullable=True),
        sa.Column('updated_by', sa.String(length=36), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['floor_id'], ['floors.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_rooms_id', 'rooms', ['id'])

    # 6. cost_estimations
    op.create_table(
        'cost_estimations',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('project_id', sa.String(length=36), nullable=False),
        sa.Column('estimation_type', sa.String(length=50), nullable=False),
        sa.Column('estimated_cost', sa.Float(), nullable=False),
        sa.Column('actual_cost', sa.Float(), nullable=True),
        sa.Column('currency', sa.String(length=10), nullable=False),
        sa.Column('breakdown_json', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(length=36), nullable=True),
        sa.Column('updated_by', sa.String(length=36), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_cost_estimations_id', 'cost_estimations', ['id'])

    # 7. materials
    op.create_table(
        'materials',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('project_id', sa.String(length=36), nullable=False),
        sa.Column('material_name', sa.String(length=100), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('unit', sa.String(length=20), nullable=False),
        sa.Column('quantity_required', sa.Float(), nullable=False),
        sa.Column('quantity_available', sa.Float(), nullable=False),
        sa.Column('supplier', sa.String(length=100), nullable=True),
        sa.Column('unit_cost', sa.Float(), nullable=False),
        sa.Column('total_cost', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(length=36), nullable=True),
        sa.Column('updated_by', sa.String(length=36), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_materials_id', 'materials', ['id'])

    # 8. workers
    op.create_table(
        'workers',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('project_id', sa.String(length=36), nullable=False),
        sa.Column('worker_name', sa.String(length=100), nullable=False),
        sa.Column('designation', sa.String(length=50), nullable=False),
        sa.Column('contact', sa.String(length=50), nullable=True),
        sa.Column('daily_wage', sa.Float(), nullable=False),
        sa.Column('attendance', sa.String(length=20), nullable=False),
        sa.Column('assigned_task', sa.String(length=200), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(length=36), nullable=True),
        sa.Column('updated_by', sa.String(length=36), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_workers_id', 'workers', ['id'])

    # 9. equipment
    op.create_table(
        'equipment',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('project_id', sa.String(length=36), nullable=False),
        sa.Column('equipment_name', sa.String(length=100), nullable=False),
        sa.Column('equipment_type', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('availability', sa.String(length=20), nullable=False),
        sa.Column('maintenance_date', sa.Date(), nullable=True),
        sa.Column('operator', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(length=36), nullable=True),
        sa.Column('updated_by', sa.String(length=36), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_equipment_id', 'equipment', ['id'])

    # 10. safety_inspections
    op.create_table(
        'safety_inspections',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('project_id', sa.String(length=36), nullable=False),
        sa.Column('inspection_date', sa.Date(), nullable=False),
        sa.Column('risk_level', sa.String(length=20), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('corrective_action', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(length=36), nullable=True),
        sa.Column('updated_by', sa.String(length=36), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_safety_inspections_id', 'safety_inspections', ['id'])

    # 11. project_progress
    op.create_table(
        'project_progress',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('project_id', sa.String(length=36), nullable=False),
        sa.Column('milestone_name', sa.String(length=100), nullable=False),
        sa.Column('completion_percentage', sa.Float(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('updated_date', sa.Date(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(length=36), nullable=True),
        sa.Column('updated_by', sa.String(length=36), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_project_progress_id', 'project_progress', ['id'])

    # 12. reports
    op.create_table(
        'reports',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('project_id', sa.String(length=36), nullable=False),
        sa.Column('report_type', sa.String(length=50), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('generated_by', sa.String(length=100), nullable=False),
        sa.Column('generated_date', sa.DateTime(), nullable=False),
        sa.Column('file_path', sa.String(length=300), nullable=True),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(length=36), nullable=True),
        sa.Column('updated_by', sa.String(length=36), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_reports_id', 'reports', ['id'])

    # 13. ai_conversations
    op.create_table(
        'ai_conversations',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('project_id', sa.String(length=36), nullable=True),
        sa.Column('conversation_title', sa.String(length=200), nullable=False),
        sa.Column('started_at', sa.DateTime(), nullable=False),
        sa.Column('last_message_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(length=36), nullable=True),
        sa.Column('updated_by', sa.String(length=36), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_ai_conversations_id', 'ai_conversations', ['id'])

    # 14. ai_messages
    op.create_table(
        'ai_messages',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('conversation_id', sa.String(length=36), nullable=False),
        sa.Column('sender', sa.String(length=20), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('tokens', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(length=36), nullable=True),
        sa.Column('updated_by', sa.String(length=36), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['ai_conversations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_ai_messages_id', 'ai_messages', ['id'])

    # 15. documents
    op.create_table(
        'documents',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('project_id', sa.String(length=36), nullable=False),
        sa.Column('document_name', sa.String(length=150), nullable=False),
        sa.Column('file_type', sa.String(length=20), nullable=False),
        sa.Column('file_size_mb', sa.Float(), nullable=False),
        sa.Column('uploaded_by', sa.String(length=100), nullable=False),
        sa.Column('file_path', sa.String(length=300), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(length=36), nullable=True),
        sa.Column('updated_by', sa.String(length=36), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_documents_id', 'documents', ['id'])

    # 16. ai_predictions
    op.create_table(
        'ai_predictions',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('project_id', sa.String(length=36), nullable=False),
        sa.Column('prediction_type', sa.String(length=50), nullable=False),
        sa.Column('prediction_result', sa.Text(), nullable=False),
        sa.Column('confidence_score', sa.Float(), nullable=False),
        sa.Column('generated_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(length=36), nullable=True),
        sa.Column('updated_by', sa.String(length=36), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_ai_predictions_id', 'ai_predictions', ['id'])

    # 17. activity_logs
    op.create_table(
        'activity_logs',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=True),
        sa.Column('project_id', sa.String(length=36), nullable=True),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('module', sa.String(length=50), nullable=False),
        sa.Column('details', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(length=36), nullable=True),
        sa.Column('updated_by', sa.String(length=36), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_activity_logs_id', 'activity_logs', ['id'])

    # 18. system_settings
    op.create_table(
        'system_settings',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('setting_key', sa.String(length=100), nullable=False),
        sa.Column('setting_value', sa.Text(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(length=36), nullable=True),
        sa.Column('updated_by', sa.String(length=36), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('setting_key')
    )

    # 19. workflow_states
    op.create_table(
        'workflow_states',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('project_id', sa.String(length=36), nullable=False),
        sa.Column('entity_type', sa.String(length=50), nullable=False),
        sa.Column('entity_id', sa.String(length=36), nullable=False),
        sa.Column('current_state', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(length=36), nullable=True),
        sa.Column('updated_by', sa.String(length=36), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_workflow_states_id', 'workflow_states', ['id'])

    # 20. workflow_histories
    op.create_table(
        'workflow_histories',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('workflow_state_id', sa.String(length=36), nullable=False),
        sa.Column('from_state', sa.String(length=50), nullable=True),
        sa.Column('to_state', sa.String(length=50), nullable=False),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('performed_by', sa.String(length=36), nullable=True),
        sa.Column('comments', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(length=36), nullable=True),
        sa.Column('updated_by', sa.String(length=36), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['workflow_state_id'], ['workflow_states.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_workflow_histories_id', 'workflow_histories', ['id'])

    # 21. tasks
    op.create_table(
        'tasks',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('project_id', sa.String(length=36), nullable=False),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=30), nullable=False),
        sa.Column('priority', sa.String(length=20), nullable=False),
        sa.Column('assignee_id', sa.String(length=36), nullable=True),
        sa.Column('due_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(length=36), nullable=True),
        sa.Column('updated_by', sa.String(length=36), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['assignee_id'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_tasks_id', 'tasks', ['id'])

    # 22. approvals
    op.create_table(
        'approvals',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('project_id', sa.String(length=36), nullable=False),
        sa.Column('approval_type', sa.String(length=50), nullable=False),
        sa.Column('entity_id', sa.String(length=36), nullable=False),
        sa.Column('requested_by', sa.String(length=36), nullable=False),
        sa.Column('approver_id', sa.String(length=36), nullable=True),
        sa.Column('status', sa.String(length=30), nullable=False),
        sa.Column('comments', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(length=36), nullable=True),
        sa.Column('updated_by', sa.String(length=36), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['approver_id'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['requested_by'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_approvals_id', 'approvals', ['id'])

    # 23. notifications
    op.create_table(
        'notifications',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('is_read', sa.Boolean(), nullable=False),
        sa.Column('notification_type', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(length=36), nullable=True),
        sa.Column('updated_by', sa.String(length=36), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_notifications_id', 'notifications', ['id'])

    # 24. project_members
    op.create_table(
        'project_members',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('project_id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('role_in_project', sa.String(length=50), nullable=False),
        sa.Column('assigned_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(length=36), nullable=True),
        sa.Column('updated_by', sa.String(length=36), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_project_members_id', 'project_members', ['id'])

def downgrade() -> None:
    op.drop_index('ix_project_members_id', table_name='project_members')
    op.drop_table('project_members')
    op.drop_index('ix_notifications_id', table_name='notifications')
    op.drop_table('notifications')
    op.drop_index('ix_approvals_id', table_name='approvals')
    op.drop_table('approvals')
    op.drop_index('ix_tasks_id', table_name='tasks')
    op.drop_table('tasks')
    op.drop_index('ix_workflow_histories_id', table_name='workflow_histories')
    op.drop_table('workflow_histories')
    op.drop_index('ix_workflow_states_id', table_name='workflow_states')
    op.drop_table('workflow_states')
    op.drop_table('system_settings')
    op.drop_index('ix_activity_logs_id', table_name='activity_logs')
    op.drop_table('activity_logs')
    op.drop_index('ix_ai_predictions_id', table_name='ai_predictions')
    op.drop_table('ai_predictions')
    op.drop_index('ix_documents_id', table_name='documents')
    op.drop_table('documents')
    op.drop_index('ix_ai_messages_id', table_name='ai_messages')
    op.drop_table('ai_messages')
    op.drop_index('ix_ai_conversations_id', table_name='ai_conversations')
    op.drop_table('ai_conversations')
    op.drop_index('ix_reports_id', table_name='reports')
    op.drop_table('reports')
    op.drop_index('ix_project_progress_id', table_name='project_progress')
    op.drop_table('project_progress')
    op.drop_index('ix_safety_inspections_id', table_name='safety_inspections')
    op.drop_table('safety_inspections')
    op.drop_index('ix_equipment_id', table_name='equipment')
    op.drop_table('equipment')
    op.drop_index('ix_workers_id', table_name='workers')
    op.drop_table('workers')
    op.drop_index('ix_materials_id', table_name='materials')
    op.drop_table('materials')
    op.drop_index('ix_cost_estimations_id', table_name='cost_estimations')
    op.drop_table('cost_estimations')
    op.drop_index('ix_rooms_id', table_name='rooms')
    op.drop_table('rooms')
    op.drop_index('ix_floors_id', table_name='floors')
    op.drop_table('floors')
    op.drop_index('ix_buildings_id', table_name='buildings')
    op.drop_table('buildings')
    op.drop_index('ix_projects_project_name', table_name='projects')
    op.drop_index('ix_projects_project_code', table_name='projects')
    op.drop_index('ix_projects_id', table_name='projects')
    op.drop_table('projects')
    op.drop_index('ix_users_username', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
