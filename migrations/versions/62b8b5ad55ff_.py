"""empty message

Revision ID: 62b8b5ad55ff
Revises: 
Create Date: 2023-04-23 18:04:18.092905

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62b8b5ad55ff'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=150), nullable=True),
    sa.Column('last_name', sa.String(length=150), nullable=True),
    sa.Column('unique_email', sa.String(length=150), nullable=True),
    sa.Column('password_hash', sa.String(length=150), nullable=True),
    sa.Column('unique_reset_password_token', sa.String(length=150), nullable=True),
    sa.Column('reset_password_token_expiration', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('unique_email'),
    sa.UniqueConstraint('unique_reset_password_token')
    )
    op.create_table('calculator_user_inputs',
    sa.Column('income', sa.Integer(), nullable=False),
    sa.Column('home_val', sa.Integer(), nullable=True),
    sa.Column('down_pay', sa.Integer(), nullable=True),
    sa.Column('loan_amt', sa.Integer(), nullable=False),
    sa.Column('interest_rate', sa.Numeric(precision=2, scale=2), nullable=False),
    sa.Column('loan_term', sa.Integer(), nullable=False),
    sa.Column('property_tax', sa.Integer(), nullable=True),
    sa.Column('home_insurance', sa.Integer(), nullable=True),
    sa.Column('monthly_hoa', sa.Integer(), nullable=True),
    sa.Column('pmi', sa.Numeric(precision=2, scale=2), nullable=True),
    sa.Column('credit_card_payments', sa.Integer(), nullable=True),
    sa.Column('car_payments', sa.Integer(), nullable=True),
    sa.Column('student_payments', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('calendar_events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('notes', sa.String(length=500), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('end_time', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('checklist_items',
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('detail', sa.String(length=255), nullable=True),
    sa.Column('order_no', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('order_no', 'user_id')
    )
    op.create_table('property',
    sa.Column('propId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('street', sa.String(length=100), nullable=True),
    sa.Column('city', sa.String(length=25), nullable=True),
    sa.Column('state', sa.String(length=2), nullable=True),
    sa.Column('zcode', sa.Integer(), nullable=True),
    sa.Column('county', sa.String(length=25), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('yearBuilt', sa.Integer(), nullable=True),
    sa.Column('numBeds', sa.Integer(), nullable=True),
    sa.Column('numBaths', sa.Integer(), nullable=True),
    sa.Column('favorite', sa.Boolean(), nullable=True),
    sa.Column('image_filename', sa.String(length=255), nullable=True),
    sa.Column('propUrl', sa.String(length=255), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('propId')
    )
    with op.batch_alter_table('property', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_property_city'), ['city'], unique=False)
        batch_op.create_index(batch_op.f('ix_property_county'), ['county'], unique=False)
        batch_op.create_index(batch_op.f('ix_property_zcode'), ['zcode'], unique=False)

    op.create_table('user_favorite',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('property_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['property_id'], ['property.propId'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'property_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_favorite')
    with op.batch_alter_table('property', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_property_zcode'))
        batch_op.drop_index(batch_op.f('ix_property_county'))
        batch_op.drop_index(batch_op.f('ix_property_city'))

    op.drop_table('property')
    op.drop_table('checklist_items')
    op.drop_table('calendar_events')
    op.drop_table('calculator_user_inputs')
    op.drop_table('users')
    # ### end Alembic commands ###
