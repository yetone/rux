# coding=utf8

"""
    rux.models
    ~~~~~~~~~~

    rux's models: blog, author, post, page
"""

from . import src_ext, out_ext, src_dir, out_dir
from .utils import join


class Blog(object):
    """The blog
    attributes
      name          unicode     blog's name
      description   unicode     blog's description
      theme         str         blog's theme"""

    def __init__(self, name="", description="", theme=""):
        self.name = name
        self.description = description
        self.theme = theme


blog = Blog()


class Author(object):
    """The blog's owner, only one
    attributes
      name      unicode     author's name
      email     unicode     author's email
    """

    def __init__(self, name="", email=""):
        self.name = name
        self.email = email


author = Author()


class Post(object):
    """The blog's post object.
    attributes
      name      unicode     post's filename without extension
      title     unicode     post's title
      datetime  datetime    post's created time
      markdown  unicode     post's body source, it's in markdown
      html      unicode     post's html, parsed from markdown
      summary   unicode     post's summary"""

    src_dir = src_dir
    out_dir = join(out_dir, "post")
    template = "post.html"

    def __init__(self, name="", title="", datetime=None, markdown="",
                 html="", summary=""):
        self.name = name
        self.title = title
        self.datetime = datetime
        self.markdown = markdown
        self.html = html
        self.summary = summary

    @property
    def src(self):
        return join(Post.src_dir, self.name + src_ext)

    @property
    def out(self):
        return join(Post.out_dir, self.name + out_ext)


class Page(object):
    """The 1st, 2nd, 3rd page..
    attributes
      number    int         the page's order
      posts     list        lists of post objects
      first     bool        is the first page?
      last      bool        is the last page?"""

    template = "page.html"
    out_dir = join(out_dir, "page")

    def __init__(self, number=1, posts=None, first=False, last=False):
        self.number = number
        self.first = first
        self.last = last

        if posts is None:
            self.posts = []
        else:
            self.posts = posts

    @property
    def out(self):
        if self.first:
            return join(out_dir, "index" + out_ext)
        else:
            return join(Page.out_dir, str(self.number) + out_ext)
