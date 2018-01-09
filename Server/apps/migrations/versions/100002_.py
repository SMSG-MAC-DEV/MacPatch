"""0002 - MP 3.1.0 Schema additions

Revision ID: 100002
Revises: None
Create Date: 2017-03-28

"""

# revision identifiers, used by Alembic.
revision = '100002'
down_revision = '100001'

# revision identifiers, used by Alembic.
revision = '100002'
down_revision = '100001'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


def upgrade():
	### commands auto generated by Alembic - please adjust! ###
	op.create_table('mp_os_migration_status',
		sa.Column('rid', sa.BigInteger(), nullable=False, autoincrement=True),
		sa.Column('cuuid', sa.String(length=50), server_default='', nullable=False),
		sa.Column('startDateTime', sa.DateTime(), server_default='1970-01-01 00:00:00', nullable=False),
		sa.Column('stopDateTime', sa.DateTime(), server_default='1970-01-01 00:00:00', nullable=True),
		sa.Column('preOSVer', sa.String(length=255), server_default='NA', nullable=False),
		sa.Column('postOSVer', sa.String(length=255), server_default='NA', nullable=True),
		sa.Column('label', mysql.MEDIUMTEXT(), nullable=True),
		sa.Column('migrationID', sa.String(length=100), nullable=True),
		sa.PrimaryKeyConstraint('rid')
	)

	op.create_index(op.f('ix_os_migration_status_cuuid'), 'mp_os_migration_status', ['cuuid'], unique=False)

	op.create_table('mp_os_config_profiles_group_policy',
		sa.Column('rid', sa.BigInteger(), nullable=False, autoincrement=True),
		sa.Column('gPolicyID', sa.String(length=50), nullable=False),
		sa.Column('profileID', sa.String(length=50), nullable=False),
		sa.Column('groupID', sa.String(length=50), nullable=False),
		sa.Column('title', sa.String(length=255), server_default='NA', nullable=False),
		sa.Column('description', mysql.LONGTEXT(), nullable=True),
		sa.Column('enabled', mysql.INTEGER(display_width=1, unsigned=True), server_default='1', nullable=True),
		sa.PrimaryKeyConstraint('rid')
	)
	op.create_index(op.f('ix_mp_os_config_profiles_group_policy_gPolicyID'), 'mp_os_config_profiles_group_policy', ['gPolicyID'], unique=False)
	op.create_index(op.f('ix_mp_os_config_profiles_group_policy_profileID'), 'mp_os_config_profiles_group_policy', ['profileID'], unique=False)
	op.create_index(op.f('ix_mp_os_config_profiles_group_policy_groupID'), 'mp_os_config_profiles_group_policy', ['groupID'], unique=False)

	op.create_table('mp_os_config_profiles_criteria',
		sa.Column('rid', sa.BigInteger(), nullable=False, autoincrement=True),
		sa.Column('gPolicyID', sa.String(length=50), nullable=False),
		sa.Column('type', sa.String(length=25), nullable=False),
		sa.Column('type_data', mysql.MEDIUMTEXT(), nullable=True),
		sa.Column('type_action', mysql.INTEGER(display_width=1, unsigned=True), server_default='0', nullable=True),
		sa.Column('type_order', mysql.INTEGER(display_width=1, unsigned=True), server_default='0', nullable=True),
		sa.PrimaryKeyConstraint('rid')
	)
	op.create_index(op.f('ix_mp_os_config_profiles_criteria_gPolicyID'), 'mp_os_config_profiles_criteria', ['gPolicyID'], unique=False)
	op.create_index(op.f('ix_mp_os_config_profiles_criteria_type'), 'mp_os_config_profiles_criteria', ['type'], unique=False)

	op.create_table('mp_inv_reports',
		sa.Column('rid', sa.BigInteger(), nullable=False, autoincrement=True),
		sa.Column('name', sa.String(length=255), nullable=False),
		sa.Column('owner', sa.String(length=255), nullable=False),
		sa.Column('scope', mysql.INTEGER(display_width=1, unsigned=True), server_default='0'),
		sa.Column('rtable', sa.String(length=255), nullable=False),
		sa.Column('rcolumns', mysql.LONGTEXT(), nullable=True),
		sa.Column('rquery', mysql.LONGTEXT(), nullable=True),
		sa.Column('cdate', sa.DateTime(), server_default='1970-01-01 00:00:00', nullable=True),
		sa.Column('mdate', sa.DateTime(), server_default='1970-01-01 00:00:00', nullable=True),
		sa.PrimaryKeyConstraint('rid')
	)

	op.create_table('mp_client_agent_plugins',
		sa.Column('rid', sa.BigInteger(), nullable=False, autoincrement=True),
		sa.Column('puuid', sa.String(length=50), server_default='', nullable=False),
		sa.Column('plugin', sa.String(length=255), nullable=False),
		sa.Column('bundleIdentifier', sa.String(length=255), nullable=True),
		sa.Column('version', sa.String(length=10), nullable=True),
		sa.PrimaryKeyConstraint('rid')
	)
	op.create_index(op.f('ix_client_agent_plugins_puuid'), 'mp_client_agent_plugins', ['puuid'], unique=False)

	op.create_table('mp_client_agent_profiles',
		sa.Column('rid', sa.BigInteger(), nullable=False, autoincrement=True),
		sa.Column('puuid', sa.String(length=50), server_default='', nullable=False),
		sa.Column('displayName', sa.String(length=255), nullable=False),
		sa.Column('identifier', sa.String(length=255), nullable=True),
		sa.Column('organization', sa.String(length=255), nullable=True),
		sa.Column('version', sa.String(length=10), nullable=True),
		sa.Column('fileName', sa.String(length=255), nullable=True),
		sa.PrimaryKeyConstraint('rid')
	)
	op.create_index(op.f('ix_client_agent_profiles_puuid'), 'mp_client_agent_profiles', ['puuid'], unique=False)

	# Update Indexes
	op.create_index(op.f('ix_mp_software_groups_name'), 'mp_software_groups', ['gName'], unique=False)
	op.create_index(op.f('ix_mp_client_agents_type'), 'mp_client_agents', ['type'], unique=False)
	op.create_index(op.f('ix_mp_client_agents_agent_ver'), 'mp_client_agents', ['agent_ver'], unique=False)

	op.drop_index(op.f('ix_mp_client_group_admin_group_admin'), table_name='mp_client_group_admin')
	op.create_index(op.f('ix_mp_client_group_admin_group_admin'), 'mp_client_group_admin', ['group_admin'], unique=False)

	op.drop_index(op.f('ix_mp_client_group_admin_group_id'), table_name='mp_client_group_admin')
	op.create_index(op.f('ix_mp_client_group_admin_group_id'), 'mp_client_group_admin', ['group_id'], unique=False)

	op.drop_index(op.f('ix_mp_client_group_members_cuuid'), table_name='mp_client_group_members')
	op.create_index(op.f('ix_mp_client_group_members_cuuid'), 'mp_client_group_members', ['cuuid'], unique=False)

	### end Alembic commands ###
	u_qstr1="ALTER TABLE `mp_group_config` ADD COLUMN `tasks_version` bigint AFTER `rev_tasks`;"
	op.execute(u_qstr1)

	# MPClients
	op.add_column('mp_clients', sa.Column('fileVaultStatus', sa.String(length=255), nullable=True))
	op.add_column('mp_clients', sa.Column('firmwareStatus', sa.String(length=255), nullable=True))

def downgrade():
	### commands auto generated by Alembic - please adjust! ###
	op.drop_index(op.f('ix_mp_software_groups_name'), table_name='mp_software_groups')
	op.drop_index(op.f('ix_mp_client_agents_type'), table_name='mp_client_agents')
	op.drop_index(op.f('ix_mp_client_agents_agent_ver'), table_name='mp_client_agents')

	op.drop_index(op.f('ix_os_migration_status_cuuid'), table_name='mp_os_migration_status')
	op.drop_table('mp_os_migration_status')

	op.drop_table('mp_inv_reports')
	op.drop_table('mp_os_config_profiles_criteria')
	op.drop_table('mp_os_config_profiles_group_policy')

	op.drop_index(op.f('ix_client_agent_plugins_puuid'), table_name='mp_client_agent_plugins')
	op.drop_table('mp_client_agent_plugins')

	op.drop_index(op.f('ix_client_agent_profiles_puuid'), table_name='mp_client_agent_profiles')
	op.drop_table('mp_client_agent_profiles')

	### end Alembic commands ###
	d_qstr1 = "ALTER TABLE `mp_group_config` DROP COLUMN `tasks_version`;"
	op.execute(d_qstr1)

	# MPClients
	op.drop_column('mp_clients', 'fileVaultStatus')
	op.drop_column('mp_clients', 'firmwareStatus')
