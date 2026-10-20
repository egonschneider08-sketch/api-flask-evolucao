from flask import Flask, request, jsonify
from flask_migrate import Migrate
from db import db
from models.book import Book

def create_app():
    app = Flask(__name__)

    # Configuração do banco de dados (SQLite)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicialização das extensões
    db.init_app(app)
    Migrate(app, db)

    # Rotas da API
    @app.route('/')
    def index():
        return jsonify({
            'status': 'online',
            'message': 'API Flask Books'
        }), 200

    @app.route('/books', methods=['GET'])
    def get_books():
        books = Book.query.all()
        return jsonify([b.to_dict() for b in books]), 200

    @app.route('/books/<int:book_id>', methods=['GET'])
    def get_book(book_id):
        book = Book.query.get_or_404(book_id)
        return jsonify(book.to_dict()), 200

    @app.route('/books', methods=['POST'])
    def create_book():
        data = request.get_json() or {}
        if not data.get('title') or not data.get('author'):
            return jsonify({'error': 'Os campos title e author são obrigatórios'}), 400

        novo_livro = Book(
            title=data['title'],
            author=data['author'],
            year=data.get('year')
        )
        db.session.add(novo_livro)
        db.session.commit()
        return jsonify(novo_livro.to_dict()), 201

    @app.route('/books/<int:book_id>', methods=['PUT'])
    def update_book(book_id):
        book = Book.query.get_or_404(book_id)
        data = request.get_json() or {}

        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.year = data.get('year', book.year)

        db.session.commit()
        return jsonify(book.to_dict()), 200

    @app.route('/books/<int:book_id>', methods=['DELETE'])
    def delete_book(book_id):
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Livro removido com sucesso'}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
