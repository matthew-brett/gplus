""" Parse Google+ posts
"""

from os.path import join as pjoin, split as psplit, abspath, dirname
from glob import glob

from datetime import datetime as dt

from bs4 import BeautifulSoup


class GPPost:
    parser = 'html.parser'
    date_fmt = r'%Y-%m-%dT%H:%M:%S%z'

    def __init__(self, fname):
        with open(fname, 'rt') as fobj:
            self.content = fobj.read()
        self.soup = BeautifulSoup(self.content, self.parser)
        bodies = self.soup.find_all('body')
        assert len(bodies) == 1
        body_parts = list(bodies[0].children)
        assert len(body_parts) > 1
        torso = list(body_parts[0].children)
        self.header, self.parts = torso[0], torso[1:]

    @property
    def date_created(self):
        date_created = self.header.find_all(
            name='span',
            attrs={'itemprop': 'dateCreated'})
        assert len(date_created) == 1
        return dt.strptime(date_created[0].text, self.date_fmt)

    @property
    def title(self):
        t_str = self.soup.title.string
        t_soup = BeautifulSoup(t_str, self.parser)
        for element in t_soup:
            e_str = element.string
            if e_str is None:
                continue
            e_str = e_str.strip()
            if e_str[0].isalnum():
                return e_str
        return t_soup.text


def collect_posts(path, my_name):
    posts = []
    for fname in glob(pjoin(path, '*.html')):
        if my_name + ' hung out with ' in fname:
            continue
        if my_name + ' was in a video ' in fname:
            continue
        posts.append(GPPost(fname))
    return posts
