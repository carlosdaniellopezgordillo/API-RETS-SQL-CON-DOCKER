import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
# Base de datos PostgreSQL (postgresql://usuario:clave@host:puerto/basededatos)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
# Vincula la app con db
db.init_app(app)

# Routes
@app.route('/posts', methods=['GET'])
def obtener_todos_los_posts():
    sql = text("SELECT id, usuario, contenido FROM post")
    resultado = db.session.execute(sql)
    posts = [{'id': row.id, 'usuario': row.usuario, 'contenido': row.contenido} for row in resultado]
    return jsonify(posts)

@app.route('/posts/<usuario>', methods=['GET'])
def obtener_posts_por_usuario(usuario):
    sql = text("SELECT id, usuario, contenido FROM post WHERE usuario = :usuario")
    resultado = db.session.execute(sql, {'usuario': usuario})
    posts = [{'id': row.id, 'usuario': row.usuario, 'contenido': row.contenido} for row in resultado]
    return jsonify(posts)

@app.route('/posts', methods=['POST'])
def crear_post():
    datos = request.json
    sql = text("INSERT INTO post (usuario, contenido) VALUES (:usuario, :contenido)  RETURNING id")
    resultado = db.session.execute(sql, {'usuario': datos['usuario'], 'contenido': datos['contenido']})
    db.session.commit()

    # Obtener el último ID insertado
    nuevo_id = resultado.fetchone().id

    return jsonify({'id': nuevo_id, 'usuario': datos['usuario'], 'contenido': datos['contenido']}), 201

@app.route('/posts/<int:post_id>', methods=['PATCH'])
def actualizar_post(post_id):
    datos = request.json
    sql = text("UPDATE post SET contenido = :contenido WHERE id = :id")
    resultado = db.session.execute(sql, {'contenido': datos['contenido'], 'id': post_id})
    db.session.commit()

    if resultado.rowcount == 0:
        return jsonify({'error': 'Post no encontrado'}), 404

    sql = text("SELECT id, usuario, contenido FROM post WHERE id = :id")
    post_actualizado = db.session.execute(sql, {'id': post_id}).fetchone()
    return jsonify({'id': post_actualizado.id, 'usuario': post_actualizado.usuario, 'contenido': post_actualizado.contenido})

@app.route('/posts/<int:post_id>', methods=['DELETE'])
def eliminar_post(post_id):
    # Obtener el post antes de eliminarlo
    sql = text("SELECT id, usuario, contenido FROM post WHERE id = :id")
    post = db.session.execute(sql, {'id': post_id}).fetchone()

    if not post:
        return jsonify({'error': 'Post no encontrado'}), 404

    # Eliminar el post
    db.session.execute(text("DELETE FROM post WHERE id = :id"), {'id': post_id})
    db.session.commit()

    return jsonify({'id': post.id, 'usuario': post.usuario, 'contenido': post.contenido})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
