import time

from flask import Blueprint, render_template, request, abort

from personal_blog.commons.base64_helper import Base64Helper
from personal_blog.models.blog_model import BlogModel

post_blog_blueprint = Blueprint('post_blog_blueprint', __name__)


@post_blog_blueprint.route('/post-blog')
def post_blog_page():
    blog_model = BlogModel()
    publish_blogs = blog_model.search_all_blog()
    draft_blogs = blog_model.search_all_draft_blog()
    return render_template('post_blog.html', publish_blogs=publish_blogs, draft_blogs=draft_blogs)


@post_blog_blueprint.route('/post-blog/post', methods=['POST'])
def post_blog():
    blog_model = BlogModel()
    id = request.form.get('id')
    article = request.form.get('article')
    type = request.form.get('type')
    content = request.form.get('content')
    thumb = request.form.get('thumb')
    if thumb.startswith("data:image/"):
        obj = Base64Helper(path='./default.png', choice=2, picture=thumb)
        thumb = obj.run()
    draft = request.form.get('draft')
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')

    if draft == '1':
        blog_model.update_blog(id, article, type, content, thumb, draft, current_time)
        return 'Success: Draft successfully'
    else:
        current_blog = blog_model.search_blog_by_id(id)
        if current_blog.draft == 1:
            current_blog.update_blog_draft(id, draft)
        else:
            blog_model.post_blog(article, type, content, thumb, 0, 0, 0, 0, draft, current_time)
        return 'Success: Publish successfully'


@post_blog_blueprint.route('/post-blog/draft', methods=['POST'])
def draft_blog():
    blog_model = BlogModel()
    id = request.form.get('id')
    draft_blog = blog_model.search_blog_by_id(id)
    if not draft_blog:
        abort(404)
    return {'id': draft_blog.id, 'article': draft_blog.article, 'type': draft_blog.type, 'content': draft_blog.content, 'thumb': draft_blog.thumb}
