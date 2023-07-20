from flask import (
    Blueprint,
    render_template,
    request,
    g,
    jsonify,
    redirect,
    url_for,
    flash,
    current_app
)
from dec import login_required
from .forms import PostForm, CommentForm
from models import PostModel, CommentModel, UserModel, CollectionModel
from exts import db
from sqlalchemy import or_
import base64

bp = Blueprint("item", __name__, url_prefix="/")


# index surface, search for specific posts
@bp.route("/")
def index():
    posts = PostModel.query.order_by(db.text("create_time")).all()
    current_app.logger.info("Visit 'Main' page successful.")
    return render_template("index.html", posts=posts)


# explore surface, get all the posts from the model and order them
@bp.route("/explore")
def explore():
    animals_posts = PostModel.query.filter_by(category="Animals").all()
    architecture_posts = PostModel.query.filter_by(category="Architecture").all()
    nature_posts = PostModel.query.filter_by(category="Nature").all()
    humanity_posts = PostModel.query.filter_by(category="Humanity").all()
    posts = PostModel.query.order_by(PostModel.create_time.desc()).all()
    current_app.logger.info("Visit 'Explore' page successful.")
    return render_template("explore.html", posts=posts, animals_posts=animals_posts,
                           architecture_posts=architecture_posts, nature_posts=nature_posts,
                           humanity_posts=humanity_posts)


@bp.route("/about")
def about():
    posts = PostModel.query.all()
    users = UserModel.query.all()
    current_app.logger.info("Visit 'About' page successful.")
    return render_template("about.html", posts=posts, users=users)


@bp.route("/mypost")
def my_post():
    if g.user:
        posts = PostModel.query.order_by(PostModel.create_time.desc()).all()
        current_app.logger.info("Visit 'My Post' page successful.")
        return render_template("my_post.html", posts=posts)
    else:
        current_app.logger.warning("Warning: No login info, can not visit 'My Post' page!")
        return redirect(url_for("user.login"))


# post blog, must log in
# get the input and store
@bp.route("/post/public", methods=['GET', 'POST'])
@login_required
def public_post():
    if g.user:
        # whether the user have logged, if not, jump to login page
        if request.method == 'GET':
            current_app.logger.warning("Wrong methods 'GET'!")
            return render_template("post.html")
        else:
            form = PostForm(request.form)
            # # test for empty input
            # if not form.title.data or not form.category.data or not form.place.data or not form.time.data \
            #         or not form.popular.data or not form.description.data:
            #     result = {
            #         "errcode": -2,
            #         "errmsg": "Empty block exist"
            #     }
            #     return jsonify(result)
            # # test for the length of the title
            # if len(form.title.data) < 2:
            #     result = {
            #         "errcode": -3,
            #         "errmsg": "Title must be longer than 2 characters"
            #     }
            #     return jsonify(result)
            # elif len(form.title.data) > 30:
            #     result = {
            #         "errcode": -4,
            #         "errmsg": "Title must be shorter than 30 characters"
            #     }
            #     return jsonify(result)
            if form.validate():
                title = form.title.data
                category = form.category.data
                img = request.files.get("file")
                pic = base64.b64encode(img.read())
                place = form.place.data
                time = form.time.data
                popular = form.popular.data
                description = form.description.data
                # store the data and update to the database
                post = PostModel(title=title, pic=pic, category=category, place=place, time=time, popular=popular,
                                 description=description, author=g.user)
                db.session.add(post)
                db.session.commit()
                imagedata = base64.b64decode(post.pic)

                file = open("./static/post_img/post_{}.png".format(post.id), "wb")
                file.write(imagedata)
                current_app.logger.info("Public post successful.")
                return redirect(url_for('item.post_detail', post_id=post.id))
            else:
                current_app.logger.error("Error: Post failed! Something Wrong!")
                return render_template("post.html", form=form)
    else:
        current_app.logger.warning("Warning: No login info, can not visit 'Post' page!")
        return redirect(url_for("user.login"))


# choose the specific post according to the id
@bp.route("/post/detail/<int:post_id>")
def post_detail(post_id):
    animals_posts = PostModel.query.filter_by(category="Animals").all()
    architecture_posts = PostModel.query.filter_by(category="Architecture").all()
    nature_posts = PostModel.query.filter_by(category="Nature").all()
    humanity_posts = PostModel.query.filter_by(category="Humanity").all()
    spread_posts = PostModel.query.order_by(PostModel.create_time.desc()).all()
    post = PostModel.query.get(post_id)
    current_app.logger.info("Visit post %d detail successful." % post_id)
    return render_template("details.html", post=post, spread_posts=spread_posts, animals_posts=animals_posts,
                           architecture_posts=architecture_posts, nature_posts=nature_posts,
                           humanity_posts=humanity_posts)


@bp.route("/comment/public", methods=["POST"])
@login_required
def public_comment():
    if g.user:
        form = CommentForm(request.form)
        # # test for empty input
        # if not form.content.data:
        #     result = {
        #         "errcode": -2,
        #         "errmsg": "Empty block exist"
        #     }
        #     return jsonify(result)
        if form.validate():
            content = form.content.data
            post_id = form.post_id.data
            comment = CommentModel(content=content, post_id=post_id, author_id=g.user.id)
            db.session.add(comment)
            db.session.commit()
            current_app.logger.info("Public comment successful.")
            return redirect(url_for("item.post_detail", post_id=post_id))
        else:
            print(form.errors)
            current_app.logger.error("Error: Comment failed! Something Wrong!")
            return redirect(url_for("item.post_detail", post_id=request.form.get("post_id")))
    else:
        current_app.logger.warning("Warning: No login info, can not public comment!")
        return redirect(url_for("user.login"))


# search method use for search the key word
@bp.route("/post/search")
def search():
    # /search?q=element you are searching for
    s = request.args.get("search")
    posts = PostModel.query.filter(or_(PostModel.title.contains(s),
                                       PostModel.description.contains(s),
                                       PostModel.category.contains(s))).order_by(PostModel.create_time.desc())
    current_app.logger.info("Search successful.")
    return render_template("explore.html", posts=posts)


# get the category as a variable and direct the web to different page
@bp.route("/category/<string:post_category>")
def category(post_category):
    animals_posts = PostModel.query.filter_by(category="Animals").all()
    architecture_posts = PostModel.query.filter_by(category="Architecture").all()
    nature_posts = PostModel.query.filter_by(category="Nature").all()
    humanity_posts = PostModel.query.filter_by(category="Humanity").all()
    posts = PostModel.query.order_by(db.text("category")).order_by(PostModel.create_time.desc()).all()
    current_app.logger.info("Visit category %s successful." % post_category)
    return render_template("category.html", posts=posts, post_category=post_category, animals_posts=animals_posts,
                           architecture_posts=architecture_posts, nature_posts=nature_posts,
                           humanity_posts=humanity_posts)


# delete the chosen post according to the id
# update the change in the database
@bp.route("/post/delete/<int:post_id>")
def delete_post(post_id):
    post = PostModel.query.get(post_id)
    if not post:
        current_app.logger.warning("Warning: No such post!")
        flash("Nothing related found to deleted!")
    else:
        try:
            db.session.delete(post)
            db.session.commit()
            current_app.logger.info("Delete post %d successful." % post_id)
        except Exception as e:
            db.session.rollback()
    return redirect("/mypost")


@bp.route("/like/<int:post_id>", methods=["GET", "POST"])
def like(post_id):
    if g.user:
        post_model = PostModel.query.filter_by(id=post_id).first()
        recent_collection = CollectionModel.query.filter_by(post_id=post_id, author_id=g.user.id).first()
        if post_model and not recent_collection:
            collection_model = CollectionModel(post_id=post_id, author_id=g.user.id)
            db.session.add(collection_model)
            db.session.commit()
            current_app.logger.info("Like post %d successful." % post_id)
            return redirect(url_for("item.collections"))
        else:
            current_app.logger.error("Error: Like failed, something wrong!")
            return redirect(url_for("item.explore"))
    else:
        current_app.logger.warning("Warning: No login info, can not add the post to favourite!")
        return redirect(url_for("user.login"))


@bp.route("/my_collection")
def collections():
    if g.user:
        posts = CollectionModel.query.filter_by(author_id=g.user.id).all()
        current_app.logger.info("Visit 'My Collection' page successful.")
        return render_template("my_collection.html", posts=posts)
    else:
        current_app.logger.warning("Warning: No login info, can not visit 'My Collection' page!")
        return redirect(url_for("user.login"))


@bp.route("/post/remove/<int:collection_id>")
def remove_collection(collection_id):
    collection = CollectionModel.query.get(collection_id)
    if not collection:
        current_app.logger.warning("Warning: No such post!")
        flash("Nothing related found to deleted!")
    else:
        try:
            db.session.delete(collection)
            db.session.commit()
            current_app.logger.info("Remove post %d successful." % collection_id)
        except Exception as e:
            db.session.rollback()
    return redirect("/my_collection")


@bp.route("/<int:post_id>/delete/comment/<int:comment_id>")
def delete_comment(post_id, comment_id):
    comment = CommentModel.query.get(comment_id)
    if not comment:
        current_app.logger.warning("Warning: No such comment!")
        flash("Nothing related found to deleted!")
    else:
        try:
            db.session.delete(comment)
            db.session.commit()
            current_app.logger.info("Remove post %d successful." % comment_id)
        except Exception as e:
            db.session.rollback()

    return redirect('/post/detail/%d' % post_id)
