from infraestructure.db.config import Base, engine
from infraestructure.db import models

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas correctamente.")