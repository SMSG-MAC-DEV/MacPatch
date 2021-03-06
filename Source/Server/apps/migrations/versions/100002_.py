"""0002 - Base

Revision ID: 8e25a122fa51
Revises: None
Create Date: 2016-07-11 14:38:58.898031

"""

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

def downgrade():
	### commands auto generated by Alembic - please adjust! ###
	op.drop_index(op.f('ix_os_migration_status_cuuid'), table_name='mp_os_migration_status')
	op.drop_table('mp_os_migration_status')
