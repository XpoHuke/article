from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id

class Rooms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Rooms %r>' % self.id



@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/room', methods=['POST', 'GET'])
def room():
    if request.method == "POST":
        title = request.form['title']


        roo = Rooms(title=title)
        try:
            db.session.add(roo)
            db.session.commit()
            return redirect('/groom')
        except:
            return "ERROR 404"
    else:
        return render_template('/room.html')

@app.route('/groom')
def groom():
    aroo = Rooms.query.order_by(Rooms.date.desc()).all()
    return render_template('groom.html', aroo=aroo)

@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles)

@app.route('/posts/<int:id>')
def postsdet(id):
    article = Article.query.get(id)
    return render_template('postsdet.html', article=article)

@app.route('/posts/<int:id>/del')
def postsdel(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении произошла ошибка"

@app.route('/posts/<int:id>/upd', methods=['POST', 'GET'])
def postsupd(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При редактировании произошла ошибка"
    else:
        return render_template('/postsupd.html', article=article)

@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(
            title=title,
            intro=intro,
            text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "Произошла ошибка"
    else:
        return render_template('/create-article.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

