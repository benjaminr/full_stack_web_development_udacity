from flask import current_app
from google.cloud import datastore

builtin_list = list


def init_app(app):
    pass


def get_client():
    return datastore.Client(current_app.config['PROJECT_ID'])


def from_datastore(entity):
    """Translates Datastore results into the format expected by the
    application.

    Datastore typically returns:
        [Entity{key: (kind, id), prop: val, ...}]

    This returns:
        {id: id, prop: val, ...}
    """
    if not entity:
        return None
    if isinstance(entity, builtin_list):
        entity = entity.pop()

    entity['id'] = entity.key.id
    return entity


def list(limit=10, cursor=None):
    ds = get_client()

    query = ds.query(kind='Blog-Post', order=['title'])
    query_iterator = query.fetch(limit=limit, start_cursor=cursor)
    page = next(query_iterator.pages)

    entities = builtin_list(map(from_datastore, page))
    next_cursor = (
        query_iterator.next_page_token.decode('utf-8')
        if query_iterator.next_page_token else None)

    return entities, next_cursor


# [START list_by_user]
def list_by_user(user_id, limit=10, cursor=None):
    ds = get_client()
    query = ds.query(
            kind='Blog-Post',
            filters=[
                ('createdById', '=', user_id)
            ]
    )

    query_iterator = query.fetch(limit=limit, start_cursor=cursor)
    page = next(query_iterator.pages)

    entities = builtin_list(map(from_datastore, page))
    next_cursor = (
        query_iterator.next_page_token.decode('utf-8')
        if query_iterator.next_page_token else None)

    return entities, next_cursor


# [END list_by_user]


def read(id):
    ds = get_client()
    key = ds.key('Blog-Post', int(id))
    results = ds.get(key)
    return from_datastore(results)


def read_comment(id):
    ds = get_client()
    key = ds.key('Comment', int(id))
    results = ds.get(key)
    return from_datastore(results)


def update(data, id=None):
    ds = get_client()
    if id:
        key = ds.key('Blog-Post', int(id))
    else:
        key = ds.key('Blog-Post')

    entity = datastore.Entity(
            key=key,
            exclude_from_indexes=['body'], )

    entity.update(data)
    ds.put(entity)
    return from_datastore(entity)


def comment(data, id=None):
    ds = get_client()
    if id:
        key = ds.key('Comment', int(id))
    else:
        key = ds.key('Comment')

    entity = datastore.Entity(
            key=key,
            exclude_from_indexes=['body'])

    entity.update(data)
    ds.put(entity)
    return from_datastore(entity)


def like(id, data):
    ds = get_client()
    key = ds.key('Blog-Post', int(id))
    blog_post = ds.get(key)

    if "liked_by" in blog_post.keys():
        if data["liked_by"] in blog_post["liked_by"]:
            return
        blog_post["liked_by"].append(data["liked_by"])
    else:
        blog_post["liked_by"] = []
        blog_post["liked_by"].append(data["liked_by"])

    ds.put(blog_post)
    return from_datastore(blog_post)


create = update



def delete(id):
    ds = get_client()
    key = ds.key('Blog-Post', int(id))
    ds.delete(key)

def delete_comment(id):
    ds = get_client()
    key = ds.key('Comment', int(id))
    ds.delete(key)
