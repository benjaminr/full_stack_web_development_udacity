from blog import get_model, oauth2
from flask import Blueprint, redirect, render_template, request, \
    session, url_for

crud = Blueprint('crud', __name__)


@crud.route("/")
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    blog_posts, next_page_token = get_model().list(cursor=token)

    return render_template(
            "list_blog_posts.html",
            blog_posts=blog_posts,
            next_page_token=next_page_token)


# [START list_mine]
@crud.route("/my-posts")
@oauth2.required
def list_mine():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    blog_posts, next_page_token = get_model().list_by_user(
            user_id=session['profile']['id'],
            cursor=token)

    return render_template(
            "list_blog_posts.html",
            blog_posts=blog_posts,
            next_page_token=next_page_token)


# [END list_mine]


@crud.route('/<id>')
def view(id):
    blog_post = get_model().read(id)
    return render_template("view.html", blog_post=blog_post)


# [START add]
@crud.route('/add-post', methods=['GET', 'POST'])
@oauth2.required
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        # If the user is logged in, associate their profile with the new blog
        #  post.
        if 'profile' in session:
            data['createdBy'] = session['profile']['displayName']
            data['createdById'] = session['profile']['id']
            data['liked_by'] = [session['profile']['id']]

        blog_post = get_model().create(data)

        return redirect(url_for('.view', id=blog_post['id']))

    return render_template("blog_post_form.html", action="Add", blog_post={})


# [END add]

@crud.route('/<id>/edit', methods=['GET', 'POST'])
@oauth2.required
def edit(id):
    blog_post = get_model().read(id)

    # only authors can edit

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        data["liked_by"] = []
        blog_post = get_model().update(data, id)

        return redirect(url_for('.view', id=blog_post['id']))
    if session['profile']['id'] == blog_post['createdById']:
        return render_template("blog_post_form.html", action="Edit",
                           blog_post=blog_post)


@crud.route('/<id>/like', methods=['GET', 'POST'])
@oauth2.required
def like(id):
    blog_post = get_model().read(id)

    if request.method == 'POST':
        data = {}

        if ('profile' in session) and (session['profile']['id'] != blog_post[
                'createdById']):
            data['liked_by'] = session['profile']['id']
            get_model().like(id, data)

    return redirect(url_for('.list'))


@crud.route('/<id>/delete')
@oauth2.required
def delete(id):
    get_model().delete(id)
    return redirect(url_for('.list'))
