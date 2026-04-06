from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine("sqlite://SQLite_recomendado.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Medico(Base):
    __tablename__ = "medicos"

    id         = Column(Integer, primary_key=True)
    nome        = Column(String(100), primary_key=False)
    especialidade = Column(Integer(100))

    consultas = relationship("consultas", back_populates="medico", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Paciente(id={self.id}, nome='{self.nome}')>"
    
class Consulta(Base):
    __tablename__ = "consultas"

    id = Column(Integer, primary_key=True)
    data = Column(Integer, primary_key=True)
    diagnostico = Column(Integer,String(100))

    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)

    paciente = relationship("Paciente", back_populates="consultas")

    def __repr__(self):
        return f"<consulta(data='{self.data}', medico_id={self.medico_id}, paciente_id={self.paciente_id})>"




