import time

from flask import Blueprint, request, session

from personal_blog.models.collection_model import CollectionModel

collection_blueprint = Blueprint('collection_blueprint', __name__)


@collection_blueprint.route('/collection', methods=['POST'])
def insert_collection():
    if session.get('login') == 'true':
        try:
            collection_model = CollectionModel()
            article_id = request.form.get('article_id')
            create_time = time.strftime('%Y-%m-%d %H:%M:%S')
            collection_model.insert_collection(article_id, create_time)
            return 'Success: Collection successful'
        except:
            return 'Fail: Collection failed'
    return 'Fail: You are not login'


@collection_blueprint.route('/collection/<int:article_id>', methods=['DELETE'])
def cancel_collection(article_id):
    try:
        collection_model = CollectionModel()
        update_time = time.strftime('%Y-%m-%d %H:%M:%S')
        collection_model.cancel_collection(article_id, update_time)
        return 'Success: Cancel successful'
    except:
        return 'Fail: Cancel failed'
