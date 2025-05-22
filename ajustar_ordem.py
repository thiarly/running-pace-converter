from main import app, db
from conversor.models import ResumoSalvo

with app.app_context():
    resumos = ResumoSalvo.query.order_by(ResumoSalvo.id.desc()).all()
    for i, resumo in enumerate(resumos):
        resumo.ordem = len(resumos) - i
    db.session.commit()
    print("✅ Ordem ajustada com sucesso!")