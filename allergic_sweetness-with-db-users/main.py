from flask import Flask, request, render_template, redirect, url_for, flash
import data
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap5
from forms import ArticleForm, RegisterForm, LoginForm, CommentForm
from flask_gravatar import Gravatar
from quotes import quotes
from datetime import date
import random
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user
from sqlalchemy.orm import relationship


app = Flask(__name__)
ckeditor = CKEditor(app=app)
app.config["SECRET_KEY"] = "sdfhkjlsdfhkjdsal"
Bootstrap5(app=app)

gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None
            )

login_manager = LoginManager()
login_manager.init_app(app=app)
# creating login manager from LoginManger() in order to make flask application and flask_login work together.
# LoginManager() has the prebuilt code to do this.

def admin_only(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        admin_user = db.session.get(User, 1)
        if admin_user != current_user:
            pick_quote = random.choice(quotes)
            return render_template("404.html", logged_in=current_user.is_authenticated, quote=pick_quote), 404
        # When the current user is not admin and trying to access the rights of the admin, then this statements of code will run.
        else:
            return function(*args, **kwargs)
    return decorated_function

def login_only(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        users = db.session.execute(db.select(User)).scalars().all()
        if current_user not in users:
            pick_quote = random.choice(quotes)
            return render_template("404.html", logged_in=current_user.is_authenticated, quote=pick_quote), 404
        # When the current user is not logged in and trying to access the rights of the login user, then this statements of code will run.
        else:
            return function(*args, **kwargs)
    return decorated_function
    
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)
# Here, we are loading user with the help of user_id
# It will be triggered when the user try to login, so the user will be loaded as per the user_id stored in the session.

awareness_needs = ["Prevention and Early Detection", "Promoting Healthy Lifestyles", "Reducing Stigma"]
awareness_images = ["static/images/Diabetes-check-up.jpg", "static/images/health-diabetes.jpg", "static/images/diabetes-stigma.jpg"]

question_images = ['static/images/faq-1.jpg', 'static/images/faq-2.jpg', 'static/images/faq-3.jpg', 'static/images/faq-4.jpeg']
response_data = data.faq_list

# Creating Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///articles-diabetes.db"
db = SQLAlchemy()
db.init_app(app=app)

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    articles = relationship("Article", back_populates="author")
    # Will return list of all the articles written by a particular user
    article_comments = relationship("Comment", back_populates="commentator")
    # List of all the comments made by the specific user.
    favorite_articles = relationship("Favorite", back_populates="user")
    # List of all the favorite object(articles) liked by the user.

class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="articles")
    # Will return the author(user object)that created the article.
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    user_comments = relationship("Comment", back_populates="parent_article")
    # List of the comment objects on a specific article.
    user_favorites = relationship("Favorite", back_populates="article_liked")
    # List of the favorite object(user) who liked it.


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    commentator_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    commentator = relationship("User", back_populates="article_comments")
    # Identification of the commentator.
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id"))
    parent_article = relationship("Article", back_populates="user_comments")
    # The article object on which, I have commented.

class Favorite(db.Model):
    __tablename__ = "favorites"
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id"))
    article_liked = relationship("Article", back_populates="user_favorites")
    # Identification of the article that is liked.
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="favorite_articles")
    # Identification of the user who liked that article.

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html", needs=awareness_needs, images=awareness_images, logged_in=current_user.is_authenticated)

@app.route("/faq")
def info():
    return render_template("faq.html", questions=response_data, logged_in=current_user.is_authenticated)

@app.route("/question/<int:question_id>")
def receive_info(question_id):
    question_title = response_data[question_id-1]['question']
    question_subheading = response_data[question_id-1]['subheading']
    question_answer = response_data[question_id-1]['answer']
    question_image = response_data[question_id-1]['image']
    return render_template("answer.html", title=question_title, subheading=question_subheading, answer=question_answer, image=question_image, logged_in=current_user.is_authenticated)

@app.route("/articles")
def show_articles():
    results = db.session.execute(db.select(Article))
    posts = results.scalars().all()
    favorite_article_ids = []
    if current_user.is_authenticated:
        favorite_articles = current_user.favorite_articles
        favorite_article_ids = [favorite.article_id for favorite in favorite_articles]
    return render_template("articles.html", articles=posts, logged_in=current_user.is_authenticated, favorite_article_ids=favorite_article_ids)

@app.route("/support")
def precautions():
    return render_template("support.html", logged_in=current_user.is_authenticated)

@app.route("/article/<int:article_id>", methods=["GET", "POST"])
def show_article(article_id):
    comment_form = CommentForm()
    is_owner = False
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for('login'))
            
        comment = Comment(text=comment_form.comment.data, commentator_id=current_user.id, article_id=article_id)
        db.session.add(comment)
        db.session.commit()

    article_view = db.session.get(Article, article_id)
    author = db.session.get(User, article_view.author_id)
    print(article_view.author_id)
    if author == current_user:
        is_owner = True
    if article_view:
        return render_template("article.html", 
                               article=article_view, 
                               logged_in=current_user.is_authenticated, 
                               form=comment_form, 
                               comments=article_view.user_comments,
                               article_author_id = str(article_view.author_id),
                               is_owner=is_owner
                            )
    else:
        return redirect(url_for('not_found'))

@app.route("/edit-article/<int:article_id>", methods=["GET", "POST"])
@login_only
def edit_article(article_id):
    article_edit = db.session.get(Article, article_id)
    if article_edit.author_id != current_user.id:
        pick_quote = random.choice(quotes)
        return render_template("404.html", logged_in=current_user.is_authenticated, quote=pick_quote), 404
    
    article_form = ArticleForm(title=article_edit.title, 
                               subtitle=article_edit.subtitle, 
                               img_url=article_edit.img_url,
                               body=article_edit.body
                            )
    if request.method == "POST":
        if article_form.validate_on_submit():
            article_edit.title = article_form.title.data
            article_edit.subtitle= article_form.subtitle.data
            article_edit.img_url = article_form.img_url.data
            article_edit.body = article_form.body.data

            db.session.commit()
            return redirect(url_for('show_article', article_id=article_id))
        
    return render_template('new_post.html', form=article_form, logged_in=current_user.is_authenticated, is_edit = True)

@app.route("/register", methods=["GET", "POST"])
def register_user():
    register_form = RegisterForm()
    if request.method == "POST":
        if register_form.validate_on_submit():
            user = db.session.execute(db.select(User).where(User.email==register_form.email.data)).scalar()
            if not user:
                new_user = User(email=register_form.email.data,
                                password=generate_password_hash(password=register_form.password.data, method="pbkdf2:sha256", salt_length=8),
                                name=register_form.name.data,
                            )
                db.session.add(new_user)
                db.session.commit()
                login_user(user=new_user)
                return redirect(url_for('show_articles'))
            
            else:
                flash("You've already signed up with this email. Kindly login!")
                return redirect(url_for('login'))
    
    return render_template('register.html', form=register_form, logged_in=current_user.is_authenticated)

@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if request.method == "POST":
        if login_form.validate_on_submit():
            login_email = login_form.email.data
            login_password = login_form.password.data
            user = db.session.execute(db.select(User).where(User.email==login_email)).scalar()

            if not user:
                flash("The email is not registered, please try again.")
            elif not check_password_hash(pwhash=user.password, password=login_password):
                flash("Password incorrect, please try again.")
            else:
                login_user(user=user)
                return redirect(url_for('show_articles'))
    
    return render_template("login.html", form=login_form, logged_in=current_user.is_authenticated)

@app.route("/logout")
@login_only
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/new-article", methods=["GET", "POST"])
def add_new_article():
    article_form = ArticleForm()

    if not current_user.is_authenticated:
                flash("You need to login or register to create new Article.")
                return redirect(url_for('login'))
    
    if request.method == "POST":
        if article_form.validate_on_submit():
            
            article = Article(title=article_form.title.data,
                            subtitle=article_form.subtitle.data,
                            img_url=article_form.img_url.data,
                            body=article_form.body.data,
                            date=date.today().strftime("%B %d, %Y"),
                            author_id=current_user.id,
                        )
            db.session.add(article)
            db.session.commit()
            return redirect(url_for('home'))
    
    return render_template("new_post.html", form=article_form, logged_in=current_user.is_authenticated, is_edit = False)

@app.route("/favorites")
@login_only
def your_favorites():
    favorite_article_id = request.args.get("article_id")
    favorite_user_articles = current_user.favorite_articles
    print(favorite_user_articles)
    # titles = [favorite.article_liked.title for favorite in favorite_user_articles]
    # print(titles)
    if favorite_article_id:
        for favorite in favorite_user_articles:
            print(type(favorite.article_id))
            if favorite.article_id == int(favorite_article_id):
                favorite_obj = db.session.get(Favorite, favorite.id)
                db.session.delete(favorite_obj)
                db.session.commit()
                return redirect(url_for('show_articles'))
        # Due to lazy load on obtaining author name.
        favorite_article = Favorite(article_id=request.args.get("article_id"), user_id=current_user.id)
        db.session.add(favorite_article) 
            # Setting the user who liked the article.
        db.session.commit()
        
        return redirect(url_for("show_articles"))
    # user_now = db.session.get(User, current_user.id)
    # favorite_articles = user_now.favorite_articles
    return render_template("favorites.html", logged_in=current_user.is_authenticated, favorite_articles=favorite_user_articles)

@app.route("/user-detail/<user_id>")
@login_only
def user_details(user_id):
    user_obj = db.session.get(User, user_id)
    user_name = user_obj.name
    user_written_articles = user_obj.articles
    return render_template("user-details.html", logged_in=current_user.is_authenticated, user_name=user_name, user_articles=user_written_articles)

@app.route("/delete-article/<int:article_id>")
@admin_only
def delete_article(article_id):
    article_delete = db.session.get(Article, article_id)
    if article_delete:
        db.session.delete(article_delete)
        db.session.commit()
        return redirect(url_for('show_show_articles'))
    else:
        return redirect(url_for('not_found'))
    
@app.errorhandler(404)
def not_found(e):
    pick_quote = random.choice(quotes)
    return render_template("404.html", logged_in=current_user.is_authenticated, quote=pick_quote), 404

if __name__ == "__main__":
    app.run(debug=True)