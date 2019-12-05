"""0008 - Base

Revision ID: 100008
Revises: 100007a
Create Date: 2019-07-24

"""

# revision identifiers, used by Alembic.
revision = '100008'
down_revision = '100007a'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


def upgrade():
    	### commands auto generated by Alembic - please adjust! ###

	### end Alembic commands ###
	u_qstr1="ALTER TABLE `mp_clients` ADD COLUMN `hasPausedPatching` varchar(1) NULL DEFAULT 0 AFTER `firmwareStatus`;"
	op.execute(u_qstr1)



def downgrade():
	### commands auto generated by Alembic - please adjust! ###

	### end Alembic commands ###
	d_qstr1 = "ALTER TABLE `mp_clients` DROP COLUMN `hasPausedPatching`;"
	op.execute(d_qstr1)



