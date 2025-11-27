"""Add namespace columns for per-user Kubernetes namespaces

Revision ID: 001_add_namespaces
Revises:
Create Date: 2025-11-27

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_add_namespaces'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add k8s_namespace column to users table
    op.add_column('users', sa.Column('k8s_namespace', sa.String(length=63), nullable=True))

    # Add namespace column to servers table
    op.add_column('servers', sa.Column('namespace', sa.String(length=63), nullable=True))

    # Update existing users to generate their namespace
    op.execute("UPDATE users SET k8s_namespace = 'user-' || id WHERE k8s_namespace IS NULL")

    # Update existing servers to use the legacy game-servers namespace
    op.execute("UPDATE servers SET namespace = 'game-servers' WHERE namespace IS NULL")


def downgrade():
    # Remove namespace column from servers table
    op.drop_column('servers', 'namespace')

    # Remove k8s_namespace column from users table
    op.drop_column('users', 'k8s_namespace')
