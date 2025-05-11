from sqlalchemy.orm import Session
from models import MessageModel, MessageTagModel, TagsModel
from domain.message_domain import DomainMessage

def save_new_message(db: Session, domain_msg) -> tuple:
    db_msg = MessageModel(
        from_user=domain_msg.from_user,
        to_user=domain_msg.to_user,
        content=domain_msg.content,
    )
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    tags_id = [tag.id for tag in db.query(TagsModel).filter(TagsModel.name.in_(domain_msg.tags)).all()]

    tag_objs = update_message_tags(db,db_msg.id, tags_id)

    return DomainMessage(db_msg, tag_objs)

def update_message_tags(db: Session, msg_id:int, tags: list[int]):
     
    tag_objs = []
    for tag_id in tags:
        db_tag = MessageTagModel(message_id=msg_id, tag=tag_id)
        db.add(db_tag)
        tag_objs.append(db_tag)
    db.commit()

    return tag_objs

def get_tags_list(db: Session):
    tags_objs = db.query(TagsModel).all()
    possible_tags = [tag.name for tag in tags_objs]
    return possible_tags