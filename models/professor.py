from .base import db, BaseModel

class Professor(BaseModel):
    """
    Modelo representativo do Docente/Professor no sistema educacional SENAI/FIESC.
    """
    __tablename__ = 'professores'

    nome = db.Column(db.String(150), nullable=False)
    registro_docente = db.Column(db.String(30), unique=True, nullable=False, index=True)
    cpf = db.Column(db.String(14), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    area_atuacao = db.Column(db.String(100), nullable=True)  # ex: Tecnologia da Informação, Mecânica, Gestão
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    # Relacionamentos
    turmas = db.relationship('Turma', back_populates='professor', lazy='dynamic')
    evolucoes_registradas = db.relationship('EvolucaoAcademica', back_populates='professor', lazy='dynamic')

    def to_dict(self, include_relations=False):
        data = super().to_dict()
        if include_relations:
            data['total_turmas'] = self.turmas.count()
        return data

    def __repr__(self):
        return f'<Professor {self.registro_docente} - {self.nome}>'
