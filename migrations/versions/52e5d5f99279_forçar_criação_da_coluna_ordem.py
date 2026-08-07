"""Forçar criação da coluna ordem"""

from alembic import op

# Identificadores únicos (deixe como o Alembic gerar)
revision = '52e5d5f99279'  # será gerado automaticamente
down_revision = 'd13d1d8b4eff'
branch_labels = None
depends_on = None

def upgrade():
    op.execute("ALTER TABLE resumos_salvos ADD COLUMN ordem INTEGER NOT NULL DEFAULT 0")

def downgrade():
    op.execute("ALTER TABLE resumos_salvos DROP COLUMN ordem")