from app import app, db
from models import Post

with app.app_context():
    db.create_all()

    if not Post.query.first():
        posts_iniciales = [
            Post(usuario='ana', contenido='Hola, este es mi primer post'),
            Post(usuario='carlos', contenido='Buenos días a todos'),
            Post(usuario='ana', contenido='Estoy aprendiendo Flask'),
            Post(usuario='maria', contenido='Hoy fue un gran día'),
            Post(usuario='luis', contenido='¿Alguien recomienda libros de Python?'),
            Post(usuario='julia', contenido='Feliz lunes a todos'),
            Post(usuario='carlos', contenido='Me encanta programar en Flask'),
            Post(usuario='maria', contenido='Estoy probando esta API REST'),
            Post(usuario='ana', contenido='¿Quién quiere colaborar en un proyecto?'),
            Post(usuario='luis', contenido='Estoy creando un bot en Telegram'),
        ]

        db.session.bulk_save_objects(posts_iniciales)
        db.session.commit()
        print("Datos iniciales insertados")
    else:
        print("Ya existen datos, no se insertó nada.")