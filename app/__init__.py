from app import models
from flask import Flask, request
from app.models import BlogPost
from sqlalchemy import desc


def create_app():
    app = Flask(__name__, static_folder='web')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    models.db.init_app(app)

    @app.route('/blog/posts')
    def get_blog_posts():
        items = []
        for post in BlogPost.query.order_by(desc(BlogPost.created_at)).all():
            items.append({
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at
            })
        return {'items': items}

    @app.route('/blog/posts', methods=["POST"])
    def add_blog_posts():
        print(request.json)
        post = BlogPost(title=request.json['title'], content=request.json['content'])
        models.db.session.add(post)
        models.db.session.commit()
        return request.json

    @app.route('/init')
    def version():
        models.db.drop_all()
        models.db.create_all()
        return 'ok'

    return app