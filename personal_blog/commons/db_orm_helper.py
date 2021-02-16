from sqlalchemy import MetaData


def init_db():
    from personal_blog import db
    db_session = db.session
    db_model = db.Model
    db_metadata = MetaData(bind=db.engine)
    return (db_session, db_model, db_metadata)


def list_model(result):
    list_model = []
    dict_model = {}
    for k, v in result:
        if not k.startswith('_sa_instance_state'):
            dict_model[k] = v
    list_model.append(dict_model)
    return list_model


def join_list_model(result):
    join_list_model = []
    for obj1, obj2 in result:
        dict_model = {}
        for k1, v1 in obj1.__dict__.items():
            if not k1.startswith('_sa_instance_state'):
                if not k1 in dict_model:
                    dict_model[k1] = v1
        for k2, v2 in obj2.__dict__.items():
            if not k2.startswith('_sa_instance_state'):
                if not k2 in dict_model:
                    dict_model[k2] = v2
        join_list_model.append(dict_model)
    return join_list_model
