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

    pacientes = relationship("Paciente", back_populates="medico", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Paciente(id={self.pacientes}, nome='{self.nome}', cpf={self.especialidade})>"
    
class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    idade = Column(Integer,nullable=False)
    cpf = Column(Integer)

    medico_id = Column(Integer, ForeignKey("medicos.id"), nullable=False)

    medico = relationship("Medico", back_populates="pacientes")

    def __repr__(self):
        return f"<paciente(nome='{self.nome}', idade={self.idade}, cpf= {self.cpf})>"

Base.metadata.create_all(engine)

print("\n" + "="*50)
print("CREATE — Inserindo médicos, pacientes")
print("="*50)

with Session() as session:
    try:
        dra_silva = Medico(nome="Dra. Ana Silva", especialidade="Cardiologia")
        dr_costa  = Medico(nome="Dr. Bruno Costa", especialidade="Ortopedia")

        # FIX: Assigned doctors to patients directly via the 'medico' relationship 
        # to satisfy the nullable=False constraint on medico_id
        joao  = Paciente(nome="João Souza", idade=10, cpf="111.111.111-11", medico=dra_silva)
        maria = Paciente(nome="Maria Lima", idade=19, cpf="222.222.222-22", medico=dr_costa)
        pedro = Paciente(nome="Pedro Alves", idade=25, cpf="333.333.333-33", medico=dra_silva)

        session.add_all([dra_silva, dr_costa, joao, maria, pedro])
        session.commit()
        print("Dados inseridos com sucesso!")

    except Exception as erro:
        session.rollback()
        print(f"Erro: {erro}")


print("\n" + "="*50)
print("READ — Consultando e navegando")
print("="*50)

with Session() as session:
    try:
        # Consultando os dados do médico de um paciente específico
        print("Médico responsável pelo João:")
        joao = session.query(Paciente).filter_by(nome="João Souza").first()
        if joao and joao.medico:
            print(f"  Paciente: {joao.nome} | Médico: {joao.medico.nome} ({joao.medico.especialidade})")

        # Consultando todos os pacientes de um médico específico
        print("\nLista de pacientes da Dra. Ana Silva:")
        dra = session.query(Medico).filter_by(nome="Dra. Ana Silva").first()
        if dra:
            for pac in dra.pacientes:
                print(f"  {pac.nome} - {pac.idade} anos (CPF: {pac.cpf})")

        # Listando todos os pacientes e seus médicos
        print("\nTodos os pacientes na base:")
        for pac in session.query(Paciente).all():
            print(f"  {pac.nome} é atendido por {pac.medico.nome}")

    except Exception as erro:
        print(f"Erro na consulta: {erro}")
