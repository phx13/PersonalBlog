import time

from flask import Blueprint, render_template, request

from personal_blog.commons.base64_helper import Base64Helper
from personal_blog.models.blog_model import BlogModel

post_blog_blueprint = Blueprint('post_blog_blueprint', __name__)


@post_blog_blueprint.route('/post-blog')
def post_blog_page():
    blog_model = BlogModel()
    publish_blogs = blog_model.search_all_blog()
    draft_blogs = blog_model.search_all_draft_blog()
    return render_template('post_blog.html', publish_blogs=publish_blogs, draft_blogs=draft_blogs)


@post_blog_blueprint.route('/post-blog/blog', methods=['POST'])
def post_blog():
    try:
        blog_model = BlogModel()
        id = request.form.get('id')
        article = request.form.get('article')
        type = request.form.get('type')
        content = request.form.get('content')
        thumb = request.form.get('thumb')
        draft = request.form.get('draft')
        update = request.form.get('update')
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        thumb_time = time.strftime("_%Y_%m_%d_%H_%M_%S")

        current_blog = blog_model.search_blog_by_id(id)
        if thumb.startswith("data:image/"):
            if current_blog:
                image_path = current_blog.thumb
            else:
                image_path = '/images/' + article + '_' + thumb_time + '.jpg'
            obj = Base64Helper(path='./default.png', choice=2, picture=thumb)
            thumb = obj.run(image_path)

        if current_blog:
            blog_model.update_blog(id, article, type, content, thumb, draft, current_time)
        else:
            blog_model.post_blog(article, type, content, thumb, 0, 0, 0, 0, draft, current_time)

        if draft == '1':
            return 'Success (Server) : Draft successfully'
        elif update == '1':
            return 'Success (Server) : Update successfully'
        else:
            return 'Success (Server) : Publish successfully'
    except:
        return 'Fail (Server) : Operation failed'


@post_blog_blueprint.route('/post-blog/load', methods=['POST'])
def load_blog():
    try:
        blog_model = BlogModel()
        id = request.form.get('id')
        current_blog = blog_model.search_blog_by_id(id)
        if current_blog:
            return {'id': current_blog.id, 'article': current_blog.article, 'type': current_blog.type, 'content': current_blog.content, 'thumb': current_blog.thumb,
                    'draft': current_blog.draft}
    except:
        return 'Fail (Server) : Load failed'


@post_blog_blueprint.route('/post-blog/blog/<int:id>', methods=['DELETE'])
def delete_blog(id):
    try:
        blog_model = BlogModel()
        blog_model.delete_blog(id)
        return 'Success (Server) : Delete successfully'
    except:
        return 'Fail (Server) : Delete failed'
