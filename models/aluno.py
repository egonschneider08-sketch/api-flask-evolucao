from datetime import date
from .base import db, BaseModel

class Aluno(BaseModel):
    """
    Modelo representativo do Aluno no sistema educacional.
    """
    __tablename__ = 'alunos'

    nome = db.Column(db.String(150), nullable=False)
    matricula = db.Column(db.String(30), unique=True, nullable=False, index=True)
    cpf = db.Column(db.String(14), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(20), nullable=True)
    data_nascimento = db.Column(db.Date, nullable=True)
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    # Relacionamentos
    # Associação N:N com Turma (via tabela associativa turma_alunos)
    turmas = db.relationship('Turma', secondary='turma_alunos', back_populates='alunos', lazy='dynamic')

    # Relacionamento 1:N com registros de evolução acadêmica
    evolucoes = db.relationship(
        'EvolucaoAcademica',
        back_populates='aluno',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )

    def to_dict(self, include_relations=False):
        data = super().to_dict()
        if self.data_nascimento and isinstance(self.data_nascimento, date):
            data['data_nascimento'] = self.data_nascimento.isoformat()
        
        if include_relations:
            data['turmas'] = [t.to_dict() for t in self.turmas]
            data['total_evolucoes'] = self.evolucoes.count()
        return data

    def __repr__(self):
        return f'<Aluno {self.matricula} - {self.nome}>'
