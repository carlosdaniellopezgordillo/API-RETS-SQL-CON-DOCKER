from app import db

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), nullable=False)
    contenido = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "usuario": self.usuario,
            "contenido": self.contenido
        }
