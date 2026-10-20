from .base import db, BaseModel
from .aluno import Aluno
from .professor import Professor
from .turma import Turma, turma_alunos
from .evolucao_academica import EvolucaoAcademica

__all__ = [
    'db',
    'BaseModel',
    'Aluno',
    'Professor',
    'Turma',
    'turma_alunos',
    'EvolucaoAcademica'
]
