import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String

# Criação da base declarativa
Base = declarative_base()

# Diretório e arquivo do banco de dados
db_directory = "token"
db_file = "token.db"
db_path = os.path.join(db_directory, db_file)

# Certifique-se de que o diretório exista
os.makedirs(db_directory, exist_ok=True)

# Configuração do motor de banco de dados
engine = sqlalchemy.create_engine(f"sqlite:///{db_path}", echo=False)

# Criação de sessão
Session = sessionmaker(bind=engine)

# Criar as tabelas do banco de dados
def create_base():
    Base.metadata.create_all(bind=engine)

# Iniciando a sessão
db = Session()

# Definição da classe Token
class Token(Base):
    __tablename__ = "token"
    id = Column(Integer, primary_key=True)
    content = Column(String(200))


def save_token(t):
    remove_token()
    token=Token(content=t)
    db.add(token)
    db.commit()

def remove_token():
    token=db.query(Token).all()
    for t in token:
        db.delete(t)
    db.commit()

def get_token():
    t = db.query(Token).first()
    if t:
        return t.content
    else:
        return None
def check_isLoged():
    t= db.query(Token).first()
    if t != None:
        return True
    else:
        False