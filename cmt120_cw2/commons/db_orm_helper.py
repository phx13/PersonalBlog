from sqlalchemy import MetaData


def init_db():
    from cmt120_cw2 import db
    db_session = db.session
    db_model = db.Model
    db_metadata = MetaData(bind=db.engine)
    return (db_session, db_model, db_metadata)
