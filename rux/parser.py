# coding=utf8

"""
    rux.parser
    ~~~~~~~~~~

    Parser from post source to html.
"""

from datetime import datetime
import os
import re

from . import charset, src_ext
from .exceptions import *

import houdini
import misaka
from misaka import HtmlRenderer, SmartyPants
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound


class ColorRender(HtmlRenderer, SmartyPants):
    """misaka render with color codes feature"""

    def _code_no_lexer(self, text):
        # encode to utf8 string
        text = text.encode(charset).strip()
        return(
            """
            <div class="highlight">
              <pre><code>%s</code></pre>
            </div>
            """ % houdini.escape_html(text)
        )

    def block_code(self, text, lang):
        """text: unicode text to render"""

        if not lang:
            return self._code_no_lexer(text)

        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except ClassNotFound:  # lexer not found, use plain text
            return self._code_no_lexer(text)

        formatter = HtmlFormatter()

        return highlight(text, lexer, formatter)


class Parser(object):
    """Usage::

        parser = Parser()
        parser.parse(str)   # return dict
        parser.markdown.render(markdown_str)  # render markdown to html

    """

    # title's matching pattern
    title_p = re.compile(r'(?P<title>[^\n]+)\n\s*={3,}\s*\n*')

    def __init__(self):
        """Initialize the parser, set markdown render handler as
        an attribute `markdown` of the parser"""
        render = ColorRender()  # initialize the color render
        extensions = (
            misaka.EXT_FENCED_CODE |
            misaka.EXT_NO_INTRA_EMPHASIS |
            misaka.EXT_AUTOLINK
        )

        self.markdown = misaka.Markdown(render, extensions=extensions)

    def parse(self, source):
        """Parse unicode post source, return dict"""

        title, markdown = self.split(source)

        # render to html
        html = self.markdown.render(markdown)
        summary = self.markdown.render(markdown[:200])

        return {
            'title': title,
            'markdown': markdown,
            'html': html,
            'summary': summary,
        }

    def split(self, source):
        """split title and body from source, return tuple(title, body)"""
        generator = self.title_p.finditer(source)

        try:  # try to get the first matched result
            first_matched = generator.next()
        except StopIteration:
            # no title found
            raise PostTitleNotFound

        # get position and title
        title = first_matched.group('title')
        end_position = first_matched.end()

        # get body
        body = source[end_position:]

        return title, body

    def parse_markdown(self, markdown):
        """Parse markdown to html"""
        return self.markdown.render(body)

    def parse_file(self, file_path):
        """parse post from file"""
        name = os.path.basename(file_path)[:-len(src_ext)]

        try:
            dt = datetime.strptime(name, "%Y-%m-%d-%H-%M")
        except ValueError:
            raise PostNameInvalid

        data = self.parse(open(file_path).read().decode(charset))

        data["datetime"] = dt
        data["name"] = name

        return data


parser = Parser()  # build a runtime parser
