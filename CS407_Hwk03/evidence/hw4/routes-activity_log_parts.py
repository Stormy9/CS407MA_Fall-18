# THIS IS JUST FOR REFERENCE PURPOSES
#______________________________________________________________________
from app.models import User, Post, Category, Comment, ActivityLog

#______________________________________________________________________

# part of activity logging...update ActivityLog.log_event()   (1)
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        ActivityLog.log_event(user, f"Login {user}")    # removed .id
        return redirect(url_for("index"))
    elif form.is_submitted():
        return redirect(url_for("login"))
    else:
        return render_template(
            "login.html", greeting_name=greeting_name(), title="Login", form=form
        )

#______________________________________________________________________

# part of activity logging...update ActivityLog.log_event()   (2)
@app.route("/logout")
def logout():
    ActivityLog.log_event(current_user, f"Logout {current_user}")   
    logout_user()							# ^^^ removed .id
    return redirect(url_for("index"))

#______________________________________________________________________

# part of activity logging...update ActivityLog.log_event()   (3)
@app.route("/create_post", methods=["GET", "POST"])
def create_post():
    if not current_user.is_authenticated:
        return redirect(url_for("register"))

    category_id = request.args.get("category_id", None, type=int)
    form = PostForm()
    categories = Category.query.order_by("title")
    form.category_id.choices = [
        (c.id, c.title) for c in categories
    ]
    form.category_id.data = (category_id
                             if category_id
                             else categories.first().id)

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            body=form.body.data,
            link=form.link.data,
            url=form.url.data,
            category_id=form.category_id.data,
            author=current_user,
        )
        db.session.add(post)
        db.session.commit()
        ActivityLog.log_event(current_user, f"Create: {post}")
        flash("Your post is now live!")		      # ^^^ removed .id
        return redirect(url_for("index"))
    return render_template(
        "create_post.html",
        greeting_name=greeting_name(),
        title="Create Post",
        form=form,
    )

#______________________________________________________________________

# part of activity logging...update ActivityLog.log_event()   (4)
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        ActivityLog.log_event(user, "Register")    # removed .id
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template(
        "register.html", greeting_name=greeting_name(), title="Register", form=form
    )

#______________________________________________________________________

# this looks like it handles comments... this doesn't go in activity log?
@app.route("/post/<id>", methods=["GET", "POST"])
def post(id):
    post = Post.query.filter_by(id=id).first_or_404()
    form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            return redirect(url_for("login"))
        post.add_comment(form.body.data, current_user)
        flash("Your comment is now live!")
        return redirect(url_for("post", id=id))
    return render_template(
        "post.html",
        greeting_name=greeting_name(),
        title=post.title,
        post=post,
        comments=post.comments,
        form=form,
    )

#______________________________________________________________________

# part of activity logging...update ActivityLog.log_event()   (5)
@app.route("/up_vote/<id>")
def up_vote(id):
    next = request.args.get("next")
    if current_user.is_authenticated:
        post = Post.query.filter_by(id=id).first_or_404()
        post.up_vote(current_user)
        ActivityLog.log_event(current_user, f"Up Vote: {post}") 
        return redirect(next or url_for("index"))	  # ^^^ removed .id
    else:
        return redirect(url_for("login"))

#______________________________________________________________________

# part of activity logging...update ActivityLog.log_event()   (6)
@app.route("/down_vote/<id>")
def down_vote(id):
    next = request.args.get("next")
    if current_user.is_authenticated:
        post = Post.query.filter_by(id=id).first_or_404()
        post.down_vote(current_user)
        ActivityLog.log_event(current_user, f"Down Vote: {post}")
        return redirect(next or url_for("index"))	  # ^^^ removed .id
    else:
        return redirect(url_for("login"))

#______________________________________________________________________

# part of activity logging...update ActivityLog.log_event()   (7)
@app.route("/up_vote_comment/<id>")
def up_vote_comment(id):
    next = request.args.get("next")
    if current_user.is_authenticated:
        comment = Comment.query.filter_by(id=id).first_or_404()
        comment.up_vote(current_user)
        ActivityLog.log_event(current_user, f"Up Vote: {comment}")
        return redirect(next or url_for("index"))	  # ^^^ removed .id
    else:
        return redirect(url_for("login"))

#______________________________________________________________________

# part of activity logging...update ActivityLog.log_event()   (8)
@app.route("/down_vote_comment/<id>")
def down_vote_comment(id):
    next = request.args.get("next")
    if current_user.is_authenticated:
        comment = Comment.query.filter_by(id=id).first_or_404()
        comment.down_vote(current_user)
        ActivityLog.log_event(current_user, f"Down Vote: {comment}")
        return redirect(next or url_for("index"))	  # ^^^ removed .id
    else:
        return redirect(url_for("login"))
