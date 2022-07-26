from flask import Flask, Blueprint, render_template, abort, request

from bp_posts.dao.comment_dao import CommentDAO
from bp_posts.dao.post import Post
from config import DATA_PATH_POSTS, DATA_PATH_COMMENTS
from bp_posts.dao.post_dao import PostDAO

bp_posts = Blueprint("bp_posts", __name__, template_folder="templates")
post_dao = PostDAO(DATA_PATH_POSTS)
comments_dao = CommentDAO(DATA_PATH_COMMENTS)


@bp_posts.route("/")
def page_post_index():
    all_posts = post_dao.get_all()
    return render_template("posts_index.html", posts=all_posts)


@bp_posts.route("/posts/<int:pk>")
def page_post_single(pk: int):
    post: Post | None = post_dao.get_by_pk(pk)
    comments = comments_dao.get_comments_by_post_pk(pk)

    if post is None:
        abort(404)

    return render_template("posts_single.html",
                           post=post,
                           comments=comments,
                           comments_len=len(comments)
                           )


@bp_posts.route("/users/<user_name>")
def page_post_by_user(user_name: str):

    posts = post_dao.get_by_poster(user_name)

    if not posts:
        abort(404, "Такого пользователя не существует")
    return render_template("posts_user-feed.html",
                           posts=posts,
                           user_name=user_name
                           )


@bp_posts.route("/search/")
def page_post_search():

    query = request.args.get("s", "")

    if query == "":
        posts = []
    else:
        posts = post_dao.search_in_content(query)
    return render_template("posts_search.html",
                           posts=posts,
                           query=query,
                           posts_len=len(posts)
                           )





