from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine("sqlite:///SQLite_recomendado.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Medico(Base):
    __tablename__ = "medicos"

    id         = Column(Integer, primary_key=True)
    nome        = Column(String(100), primary_key=False)
    especialidade = Column(String(100))
    data = Column(Integer)

    pacientes = relationship("Paciente", back_populates="medico", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Paciente(id={self.pacientes}, nome='{self.nome}', cpf={self.especialidade}, data {self.data})>"
    
class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    idade = Column(Integer,nullable=False)
    cpf = Column(Integer)

    medico_id = Column(Integer, ForeignKey("medicos.id"), nullable=False)

    medico = relationship("Medico", back_populates="pacientes")

    def __repr__(self):
        return f"<paciente(nome='{self.nome}', medico_id={self.medico_id}, cpf= {self.cpf})>"

Base.metadata.create_all(engine)

print("\n" + "="*50)
print("CREATE — Inserindo médicos, pacientes e atendimentos")
print("="*50)

with Session() as session:
    try:
        dra_silva = Medico(nome="Dra. Ana Silva",    especialidade="Cardiologia")
        dr_costa  = Medico(nome="Dr. Bruno Costa",   especialidade="Ortopedia")

        joao  = Paciente(nome="João Souza",  cpf="111.111.111-11")
        maria = Paciente(nome="Maria Lima",  cpf="222.222.222-22")
        pedro = Paciente(nome="Pedro Alves", cpf="333.333.333-33")

        session.add_all([dra_silva, dr_costa, joao, maria, pedro])
        session.flush()

        session.add_all([
            Paciente(medico=dra_silva, paciente=joao,  data="2025-01-10", diagnostico="Hipertensão leve"),
            Paciente(medico=dra_silva, paciente=maria, data="2025-01-12", diagnostico="Checkup normal"),
            Paciente(medico=dr_costa,  paciente=joao,  data="2025-01-15", diagnostico="Fratura no tornozelo"),
            Paciente(medico=dr_costa,  paciente=pedro, data="2025-01-20", diagnostico="Dor lombar"),
        ])

    
        session.commit()
        print("Dados inseridos com sucesso!")

    except Exception as erro:
        session.rollback()
        print(f"Erro: {erro}")

# print("\n" + "="*50)
# print("READ — Consultando e navegando")
# print("="*50)

# with Session() as session:
#     try:
#         # Histórico de um paciente: navega paciente → atendimentos → médico
#         print("Histórico do João:")
#         joao = session.query(Paciente).filter_by(nome="João Souza").first()
#         for atend in joao.atendimentos:
#             print(f"  {atend.data} | Dr(a): {atend.medico.nome} | {atend.diagnostico}")

#         # Agenda de um médico: navega médico → atendimentos → paciente
#         print("\nAtendimentos da Dra. Ana Silva:")
#         dra = session.query(Medico).filter_by(nome="Dra. Ana Silva").first()
#         for atend in dra.atendimentos:
#             print(f"  {atend.data} | Paciente: {atend.paciente.nome} | {atend.diagnostico}")

#         # Listando todos os atendimentos diretamente
#         print("\nTodos os atendimentos:")
#         for atend in session.query(Atendimento).all():
#             print(f"  {atend.data} | {atend.medico.nome} → {atend.paciente.nome} | {atend.diagnostico}")

#     except Exception as erro:
#         session.rollback()
#         print(f"Erro: {erro}")

