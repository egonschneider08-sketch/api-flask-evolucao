from flask import Flask, jsonify
from models import db

def create_app():
    app = Flask(__name__)
    
    # Configuração básica com banco de dados SQLite local
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///evolucao.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa o ORM com a aplicação
    db.init_app(app)

    with app.app_context():
        # Cria as tabelas caso ainda não existam
        db.create_all()

    @app.route('/')
    def index():
        return jsonify({
            'message': 'API de Acompanhamento e Evolução Acadêmica (FIESC/SENAI)',
            'status': 'online'
        })

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
