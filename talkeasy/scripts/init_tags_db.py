from sqlalchemy.orm import Session
from infraestructure.db.config import SessionLocal
from infraestructure.db.models import TagsModel

TAGS_TO_CREATE = ["importante", "urgente", "personal", "laboral", "informativo"]

def create_predefined_tags():
    db: Session = SessionLocal()
    try:
        for tag_name in TAGS_TO_CREATE:
            # Comprueba si ya existe
            exists = db.query(TagsModel).filter_by(name=tag_name).first()
            if not exists:
                tag = TagsModel(name=tag_name)
                db.add(tag)
        db.commit()
        print("Tags predefinidos insertados correctamente.")
    finally:
        db.close()

if __name__ == "__main__":
    create_predefined_tags()