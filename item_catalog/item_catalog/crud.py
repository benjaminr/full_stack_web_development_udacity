from collections import defaultdict

from item_catalog import get_model, oauth2
from flask import Blueprint, redirect, render_template, request, \
    session, url_for

crud = Blueprint('crud', __name__)


@crud.route("/")
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    items, next_page_token = get_model().list(cursor=token)

    return render_template(
            "list_items.html",
            items=items,
            next_page_token=next_page_token)


# [START list_mine]
@crud.route("/my-items")
@oauth2.required
def list_mine():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    items, next_page_token = get_model().list_by_user(
            user_id=session['profile']['id'],
            cursor=token)

    return render_template(
            "list_items.html",
            items=items,
            next_page_token=next_page_token)


# [END list_mine]


@crud.route('/<id>')
def view(id):
    item = get_model().read(id)
    comments = []
    if "comments" in item.keys():
        for comment_id in item["comments"]:
            comment = get_model().read_comment(comment_id)
            comments.append(comment)
    return render_template("view.html", item=item, comments=comments)


# [START add]
@crud.route('/add-item', methods=['GET', 'POST'])
@oauth2.required
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        # If the user is logged in, associate their profile with the new blog
        #  post.
        if 'profile' in session:
            data['createdBy'] = session['profile']['displayName']
            data['createdById'] = session['profile']['id']
            data['liked_by'] = []
            data['comments'] = []

        item = get_model().create(data)

        return redirect(url_for('.view', id=item['id']))

    return render_template("item_form.html", action="Add", item={})


# [END add]

@crud.route('/<id>/edit', methods=['GET', 'POST'])
@oauth2.required
def edit(id):
    item = get_model().read(id)

    if session['profile']['id'] == item['createdById']:

        # only authors can edit

        if request.method == 'POST':
            data = request.form.to_dict(flat=True)
            item['title'] = data['title']
            item['body'] = data['body']
            item = get_model().update(item, id)
            return redirect(url_for('.view', id=item['id']))

        return render_template("item_form.html", action="Edit",
                                   item=item)

    return redirect(url_for('.view', id=item['id']))


@crud.route('/<id>/comment', methods=['GET', 'POST'])
@oauth2.required
def comment(id):
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        # If the user is logged in, associate their profile with the new comment
        if 'profile' in session:
            data['createdBy'] = session['profile']['displayName']
            data['createdById'] = session['profile']['id']
            comment = get_model().comment(data)

            # associate the comment with the blog post by ID
            item = get_model().read(id)
            if "comments" in item.keys():
                item["comments"].append(comment['id'])
            else:
                item["comments"] = []
                item["comments"].append(comment['id'])
            get_model().update(item, id)

    return redirect(url_for('.view', id=item['id']))


@crud.route('/<id>/comment/<c_id>/edit', methods=['GET', 'POST'])
@oauth2.required
def edit_comment(id, c_id):
    item = get_model().read(id)
    comment = get_model().read_comment(c_id)

    if session['profile']['id'] == comment['createdById']:

        # only authors can edit

        if request.method == 'POST':
            data = request.form.to_dict(flat=True)
            comment["body"] = data["body"]
            comment = get_model().comment(comment, c_id)
            return redirect(url_for('.view', id=item['id']))

        return render_template("comment_post_form.html", action="Edit",
                                   comment=comment)

    return redirect(url_for('.view', id=item['id']))

@crud.route('/<id>/comment/<c_id>/delete')
@oauth2.required
def delete_comment(id, c_id):
    item = get_model().read(id)
    comment = get_model().read_comment(c_id)
    if session['profile']['id'] == comment['createdById']:
        item["comments"].remove(comment['id'])
        get_model().update(item, id)
        get_model().delete_comment(c_id)
    return redirect(url_for('.view', id=item['id']))


@crud.route('/<id>/like', methods=['GET', 'POST'])
@oauth2.required
def like(id):
    item = get_model().read(id)

    if request.method == 'POST':
        data = defaultdict()

        if ('profile' in session) and (session['profile']['id'] != item[
            'createdById']) and (session['profile']['id'] not in item[
            "liked_by"]):
            data['liked_by'] = session['profile']['id']
            get_model().like(id, data)

    return redirect(url_for('.list'))


@crud.route('/<id>/delete')
@oauth2.required
def delete(id):
    item = get_model().read(id)
    if session['profile']['id'] == item['createdById']:
        get_model().delete(id)
    return redirect(url_for('.list'))
