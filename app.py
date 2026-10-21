import os
import sys
import uuid

# Garante que a pasta raiz esteja no path de importacao
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from dotenv import load_dotenv

from db import db
from book import Book

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configuração do banco de dados PostgreSQL via .env ou padrão
    database_url = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/books_db')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicialização das extensões
    db.init_app(app)
    Migrate(app, db)

    # Criação das tabelas automaticamente ao iniciar
    with app.app_context():
        db.create_all()

    # Rotas da API
    @app.route('/')
    def index():
        return jsonify({
            'status': 'online',
            'message': 'API Flask Books conectada ao PostgreSQL'
        }), 200

    @app.route('/books', methods=['GET'])
    def get_books():
        books = Book.query.all()
        return jsonify([b.as_dict() for b in books]), 200

    @app.route('/books/<string:book_id>', methods=['GET'])
    def get_book(book_id):
        try:
            parsed_uuid = uuid.UUID(book_id)
        except ValueError:
            return jsonify({'error': 'ID inválido. Deve ser um UUID válido.'}), 400

        book = Book.query.get(parsed_uuid)
        if not book:
            return jsonify({'error': 'Livro não encontrado'}), 404

        return jsonify(book.as_dict()), 200

    @app.route('/books', methods=['POST'])
    def create_book():
        data = request.get_json() or {}
        if not data.get('title') or not data.get('author') or not data.get('description'):
            return jsonify({'error': 'Os campos title, author e description são obrigatórios'}), 400

        novo_livro = Book(
            title=data['title'],
            author=data['author'],
            description=data['description'],
            is_finished=data.get('is_finished', False)
        )
        db.session.add(novo_livro)
        db.session.commit()
        return jsonify(novo_livro.as_dict()), 201

    @app.route('/books/<string:book_id>', methods=['PUT'])
    def update_book(book_id):
        try:
            parsed_uuid = uuid.UUID(book_id)
        except ValueError:
            return jsonify({'error': 'ID inválido. Deve ser um UUID válido.'}), 400

        book = Book.query.get(parsed_uuid)
        if not book:
            return jsonify({'error': 'Livro não encontrado'}), 404

        data = request.get_json() or {}
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.description = data.get('description', book.description)
        if 'is_finished' in data:
            book.is_finished = data['is_finished']

        db.session.commit()
        return jsonify(book.as_dict()), 200

    @app.route('/books/<string:book_id>', methods=['DELETE'])
    def delete_book(book_id):
        try:
            parsed_uuid = uuid.UUID(book_id)
        except ValueError:
            return jsonify({'error': 'ID inválido. Deve ser um UUID válido.'}), 400

        book = Book.query.get(parsed_uuid)
        if not book:
            return jsonify({'error': 'Livro não encontrado'}), 404

        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Livro removido com sucesso'}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
