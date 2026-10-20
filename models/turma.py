from datetime import datetime
from .base import db, BaseModel

# Tabela associativa para a relação N:N entre Turmas e Alunos
turma_alunos = db.Table(
    'turma_alunos',
    db.Column('turma_id', db.Integer, db.ForeignKey('turmas.id', ondelete='CASCADE'), primary_key=True),
    db.Column('aluno_id', db.Integer, db.ForeignKey('alunos.id', ondelete='CASCADE'), primary_key=True),
    db.Column('data_matricula', db.DateTime, default=datetime.utcnow, nullable=False),
    db.Column('status_matricula', db.String(20), default='ATIVO', nullable=False)  # ATIVO, CONCLUIDO, TRANCADO, CANCELADO
)

class Turma(BaseModel):
    """
    Modelo representativo da Turma / Componente Curricular.
    """
    __tablename__ = 'turmas'

    codigo = db.Column(db.String(30), unique=True, nullable=False, index=True)
    nome = db.Column(db.String(120), nullable=False)
    curso = db.Column(db.String(120), nullable=False)  # Ex: Técnico em Desenvolvimento de Sistemas
    ano_letivo = db.Column(db.Integer, nullable=False)
    semestre = db.Column(db.Integer, default=1, nullable=False)
    turno = db.Column(db.String(20), nullable=False)  # MATUTINO, VESPERTINO, NOTURNO, INTEGRAL
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    # Chave estrangeira para o docente responsável
    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'), nullable=True)

    # Relacionamentos
    professor = db.relationship('Professor', back_populates='turmas')
    alunos = db.relationship('Aluno', secondary=turma_alunos, back_populates='turmas', lazy='dynamic')
    evolucoes = db.relationship('EvolucaoAcademica', back_populates='turma', cascade='all, delete-orphan', lazy='dynamic')

    def to_dict(self, include_relations=False):
        data = super().to_dict()
        if include_relations:
            data['professor'] = self.professor.to_dict() if self.professor else None
            data['total_alunos'] = self.alunos.count()
        return data

    def __repr__(self):
        return f'<Turma {self.codigo} - {self.nome}>'
