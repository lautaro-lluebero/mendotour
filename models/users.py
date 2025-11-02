from models.db import db
from werkzeug.security import generate_password_hash, check_password_hash

class Users(db.Model):
    __tablename__ = "users"

    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),  unique=True, nullable=False)
    email    = db.Column(db.String(120), unique=True, nullable=False)
    # Guarda el HASH (subí a 255 por las variantes de werkzeug)
    password = db.Column(db.String(255), nullable=False)
    rol      = db.Column(db.String(20),  nullable=False, default="cliente")

    def __init__(self, username, email, password, rol="cliente"):
        self.username = username
        self.email    = email
        self.set_password(password)     #SIEMPRE hash
        self.rol      = rol

    # ===== Helpers de password =====
    def set_password(self, raw: str) -> None:
        """Hashea y guarda la contraseña."""
        self.password = generate_password_hash(raw)

    def check_password(self, raw: str) -> bool:
        """Verifica contra el hash guardado."""
        return check_password_hash(self.password, raw)

    def is_hashed(self) -> bool:
        """Detecta si lo almacenado parece un hash de werkzeug."""
        return isinstance(self.password, str) and self.password.startswith("pbkdf2:")

    # ===== Serialización segura (NO exponemos el hash) =====
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "rol": self.rol,
        }
