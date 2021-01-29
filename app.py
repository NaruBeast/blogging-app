from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50), nullable=False, default="Unknown")
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category = db.Column(db.String(25), nullable=False, default="Uncategorized")

    def __repr__(self):
        return f'Blog Post: {self.id}'


# all_posts = [
#     {
#         'title': 'Post 1',
#         'content': 'Content for post 1',
#         'id': 1,
#         'author': 'Lol'
#     },
#     {
#         'title': 'Post 2',
#         'content': 'Content for post 2',
#         'id': 2
#     }
# ]

@app.route('/')
def index():
    return redirect('/posts')
    # return render_template('index.html')

@app.route('/home/users/<string:name>/posts/<int:id>')
def hello(name, id):
    return f"Hi, {name}. Your post id is {id}"

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        temp_post_title = request.form['title']
        temp_post_content = request.form['content']
        # temp_post_author = request.form['author']
        # category = request.form['category']
        if request.form['category'].strip() != '':
            category = request.form['category']
        else:
            category = "Uncategorized"

        if request.form['author'].strip() != '':
            temp_post_author = request.form['author']
        else:
            temp_post_author = "Unknown"
        new_post = BlogPost(title=temp_post_title, content=temp_post_content, author=temp_post_author, category=category)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
        return render_template('posts.html', posts=all_posts)

@app.route('/posts/delete/<int:post_id>')
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if request.method == 'POST':
        post = BlogPost.query.get_or_404(post_id)
        # post.id = request.form['id']
        post.content = request.form['content']
        post.title = request.form['title']

        if request.form['category'].strip() != '':
            post.category = request.form['category']
        else:
            post.category = "Uncategorized"

        if request.form['author'].strip() != '':
            post.author = request.form['author']
        else:
            post.author = "Unknown"
        
        # post.date_posted = request.form['date_posted']
        db.session.commit()
        return redirect('/posts')
    else:
        post = BlogPost.query.get_or_404(post_id)
        return render_template('edit-post.html', post=post)

@app.route('/posts/<int:post_id>')
def display_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template('view-post.html', post=post)

@app.route('/new-post')
def create_post():
    return render_template('new-post.html')

@app.route('/onlyget', methods=['GET'])
def get_req():
    return "You can only get this webpage"

if __name__ == "__main__":
    app.run(debug=True)
