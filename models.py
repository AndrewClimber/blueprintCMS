from app import db
from datetime import datetime
import re



def slugify(s):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', s).lower() # все что не буква или цифра заменим на -


# таблица связи для организации многие ко многим
# у таблиц Post и Tag
post_tags = db.Table('post_tags',
                      db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                      db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                     )



class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique = True) # чпу
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default = datetime.now())

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.generate_slug()

    tags = db.relationship('Tag', secondary = post_tags, backref = db.backref('posts', lazy = 'dynamic'))


    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return '<Post id: {}, title: {}>'.format(self.id, self.title)

# в консоли питона надо сгенерить таблицы по нашей модели.
# >> import models
# >> from app import db
# >> db.create_all() # генерирует таблицы по модели
# теперь создадим пост
# >> from models import Post
# >> p = Post(title = 'First post', body = 'First post body')
# >> db.session.add(p)
# >> db.session.commit()

# Прочитаем все посты
# from models import Post
# from app import db
# post = Post.query.all()
# post
# p2 = Post.query.filter(Post.title.contains('second')).all()
#
# p3 = Post.query.filter(Post.title == 'First post').all()
# p4 = Post.query.filter(Post.title == 'First post').first()


# python manage.py db init
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    slug = db.Column(db.String(100))

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self):
        return '<Post id: {}, name: {}>'.format(self.id, self.name)

# python manage.py db migrate
# python manage.py db upgrade


# from app import db
# from models import Tag
# tag = Tag(name = 'python')
# tag1 = Tag(name = 'golang')
# tag2 = Tag(name = 'php')
# db.session.add_all([tag, tag1, tag2])
# db.session.commit()


# from app import db
# from models import Post, Tag
# t = Tag.query.all()
# p1 = Post.query
# p1.count()
# p1 = p1.first()
# p1.tags
# p1.tags.append(t[0])
# p1.tags.append(t[1])
# db.session.add(p1)
# db.session.commit()
