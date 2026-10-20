from datetime import datetime
from .base import db, BaseModel

class EvolucaoAcademica(BaseModel):
    """
    Modelo de Evolução Acadêmica do estudante (registro de acompanhamento de competências,
    desempenho técnico, atitudinal e feedbacks pedagógicos).
    """
    __tablename__ = 'evolucoes_academicas'

    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id', ondelete='CASCADE'), nullable=False, index=True)
    turma_id = db.Column(db.Integer, db.ForeignKey('turmas.id', ondelete='CASCADE'), nullable=False, index=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id', ondelete='SET NULL'), nullable=True)

    data_registro = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    tipo_registro = db.Column(
        db.String(50),
        default='DESEMPENHO',
        nullable=False
    )  # DESEMPENHO, ATITUDINAL, FREQUENCIA, FEEDBACK_INDIVIDUAL, PLANO_RECUPERACAO

    nota = db.Column(db.Float, nullable=True)  # Nota da avaliação (0.0 a 10.0)
    percentual_frequencia = db.Column(db.Float, nullable=True)  # Frequência acumulada em %
    competencias_atingidas = db.Column(db.Text, nullable=True)  # Competências curriculares/técnicas desenvolvidas
    pontos_atencao = db.Column(db.Text, nullable=True)  # Dificuldades detectadas
    plano_acao = db.Column(db.Text, nullable=True)  # Orientações pedagógicas e plano de melhoria
    observacoes = db.Column(db.Text, nullable=True)

    # Relacionamentos
    aluno = db.relationship('Aluno', back_populates='evolucoes')
    turma = db.relationship('Turma', back_populates='evolucoes')
    professor = db.relationship('Professor', back_populates='evolucoes_registradas')

    def to_dict(self, include_details=False):
        data = super().to_dict()
        if self.data_registro:
            data['data_registro'] = self.data_registro.isoformat()
        
        if include_details:
            data['aluno_nome'] = self.aluno.nome if self.aluno else None
            data['turma_nome'] = self.turma.nome if self.turma else None
            data['professor_nome'] = self.professor.nome if self.professor else None
        return data

    def __repr__(self):
        return f'<EvolucaoAcademica id={self.id} aluno_id={self.aluno_id} tipo={self.tipo_registro}>'
