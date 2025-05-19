"""Add ordem to ResumoSalvo"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd13d1d8b4eff'
down_revision = None  # já resolvemos o ponteiro
branch_labels = None
depends_on = None

    
def upgrade():
    op.execute("ALTER TABLE resumos_salvos ADD COLUMN ordem INTEGER NOT NULL DEFAULT 0")

def downgrade():
    op.execute("ALTER TABLE resumos_salvos DROP COLUMN ordem")