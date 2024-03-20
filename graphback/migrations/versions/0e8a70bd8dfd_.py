"""empty message

Revision ID: 0e8a70bd8dfd
Revises: 
Create Date: 2024-03-20 15:15:00.148890

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0e8a70bd8dfd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('log')
    op.drop_table('file')
    with op.batch_alter_table('dataset', schema=None) as batch_op:
        batch_op.alter_column('createtime',
               existing_type=mysql.DATETIME(),
               nullable=True)
        batch_op.alter_column('userid',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
        batch_op.drop_constraint('dataset_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'user', ['userid'], ['userid'])

    with op.batch_alter_table('graph', schema=None) as batch_op:
        batch_op.alter_column('updatatime',
               existing_type=mysql.DATETIME(),
               nullable=True)

    with op.batch_alter_table('graphcount', schema=None) as batch_op:
        batch_op.alter_column('updatatime',
               existing_type=mysql.DATETIME(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('graphcount', schema=None) as batch_op:
        batch_op.alter_column('updatatime',
               existing_type=mysql.DATETIME(),
               nullable=False)

    with op.batch_alter_table('graph', schema=None) as batch_op:
        batch_op.alter_column('updatatime',
               existing_type=mysql.DATETIME(),
               nullable=False)

    with op.batch_alter_table('dataset', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('dataset_ibfk_1', 'user', ['userid'], ['userid'], onupdate='RESTRICT', ondelete='RESTRICT')
        batch_op.alter_column('userid',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
        batch_op.alter_column('createtime',
               existing_type=mysql.DATETIME(),
               nullable=False)

    op.create_table('file',
    sa.Column('fileid', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('dataid', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('filepath', mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_0900_ai_ci', length=50), nullable=False),
    sa.Column('filename', mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_0900_ai_ci', length=20), nullable=False),
    sa.Column('creattime', mysql.DATETIME(), nullable=False),
    sa.ForeignKeyConstraint(['dataid'], ['dataset.dataid'], name='file_ibfk_1', onupdate='RESTRICT', ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('fileid'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB',
    mysql_row_format='DYNAMIC'
    )
    op.create_table('log',
    sa.Column('logid', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('ip', mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_0900_ai_ci', length=20), nullable=False),
    sa.Column('request', mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_0900_ai_ci', length=200), nullable=False),
    sa.Column('response', mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_0900_ai_ci', length=200), nullable=False),
    sa.Column('type', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('request_time', mysql.DATETIME(), nullable=False),
    sa.Column('userid', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['userid'], ['user.userid'], name='log_ibfk_1', onupdate='RESTRICT', ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('logid'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB',
    mysql_row_format='DYNAMIC'
    )
    # ### end Alembic commands ###
