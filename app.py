from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, BlogPost, ContactMessage, Product, ToDo
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

# ---------------- HOME (Portfolio) ----------------
@app.route('/')
def home():
    return render_template('home.html')

# ---------------- BLOG ----------------
@app.route('/blog')
def blog():
    posts = BlogPost.query.order_by(BlogPost.date.desc()).all()
    return render_template('blog.html', posts=posts)

@app.route('/blog/<int:id>')
def blog_post(id):
    post = BlogPost.query.get_or_404(id)
    return render_template('blog_post.html', post=post)

@app.route('/blog/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        db.session.add(BlogPost(title=title, content=content))
        db.session.commit()
        return redirect(url_for('blog'))
    return render_template('new_post.html')

# ---------------- STORE ----------------
@app.route('/store')
def store():
    products = Product.query.all()
    return render_template('store.html', products=products)

@app.route('/cart', methods=['POST', 'GET'])
def cart():
    if 'cart' not in session:
        session['cart'] = []
    if request.method == 'POST':
        product_id = request.form['product_id']
        session['cart'].append(product_id)
    items = Product.query.filter(Product.id.in_(session['cart'])).all()
    return render_template('cart.html', items=items)

@app.route('/checkout')
def checkout():
    session.pop('cart', None)
    return render_template('checkout.html')

# ---------------- CONTACT FORM ----------------
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        msg = ContactMessage(
            name=request.form['name'],
            email=request.form['email'],
            message=request.form['message']
        )
        db.session.add(msg)
        db.session.commit()
        flash('Message sent!')
        return redirect(url_for('contact'))
    return render_template('contact.html')

# ---------------- CRM ----------------
@app.route('/crm')
def crm():
    messages = ContactMessage.query.all()
    return render_template('crm.html', messages=messages)

# ---------------- TO-DO ----------------
@app.route('/todo', methods=['GET', 'POST'])
def todo():
    if request.method == 'POST':
        db.session.add(ToDo(task=request.form['task']))
        db.session.commit()
    todos = ToDo.query.all()
    return render_template('todo.html', todos=todos)

@app.route('/todo/done/<int:id>')
def mark_done(id):
    todo = ToDo.query.get(id)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for('todo'))

if __name__ == '__main__':
    app.run(debug=True)
