from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(180), nullable=False)
    salt = db.Column(db.String(120), nullable=False)
    avatar = db.Column(db.String(120), default="https://i.pravatar.cc/300")
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.now(), onupdate=db.func.now(), nullable=False)
    todos = db.relationship("Todos", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "avatar": self.avatar,
            # "todos": self.todos
        }


class Todos(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    label = db.Column(db.String(255), nullable=False)
    is_done =db.Column(db.Boolean(), default=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.now(), onupdate=db.func.now(), nullable=False)
    user = db.relationship("User", back_populates="todos")