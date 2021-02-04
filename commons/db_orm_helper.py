from sqlalchemy import MetaData


def init_db():
    from app import db
    db_session = db.session
    db_model = db.Model
    db_metadata = MetaData(bind=db.engine)
    return (db_session, db_model, db_metadata)
