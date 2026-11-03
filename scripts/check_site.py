#!/usr/bin/env python3
"""Check every generated page, internal destination, anchor and local asset."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.ids, self.links = path, set(), []
        self.h1 = self.main = self.titles = 0
        self.current = []
        self.feed(path.read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'{self.path.name}: duplicate ID'
            self.ids.add(attrs['id'])
        if tag == 'h1': self.h1 += 1
        if tag == 'main': self.main += 1
        if tag == 'title': self.titles += 1
        if attrs.get('aria-current') == 'page': self.current.append(attrs.get('href'))
        if tag == 'img': assert 'alt' in attrs, f'{self.path.name}: image without alt'
        for key in ('href', 'src'):
            if key in attrs: self.links.append(attrs[key])


def main():
    docs = {path.name: Document(path) for path in ROOT.glob('*.html')}
    assert len(docs) == 7, f'Expected seven pages, got {len(docs)}'
    checked = 0
    for name, doc in docs.items():
        assert doc.h1 == doc.main == doc.titles == 1, f'{name}: missing/duplicate landmark or title'
        assert doc.current == [name], f'{name}: incorrect active navigation'
        for raw in doc.links:
            url = urlsplit(raw)
            if url.scheme == 'tel':
                assert raw == 'tel:+33602256978', 'Unknown contact phone number'
                continue
            assert not url.scheme and not url.netloc, f'{name}: unexpected external resource {raw}'
            assert not url.path.startswith('/'), f'{name}: root-relative path breaks project Pages'
            target = ROOT / unquote(url.path) if url.path else doc.path
            assert target.resolve().is_relative_to(ROOT), f'{name}: escaping site root'
            assert target.is_file(), f'{name}: broken link {raw}'
            if url.fragment:
                assert target.suffix == '.html'
                assert unquote(url.fragment) in docs[target.name].ids, f'{name}: missing anchor {raw}'
            checked += 1
    for path in (ROOT/'assets').glob('*.svg'):
        ET.parse(path)
    for project in json.loads((ROOT/'data/projects.json').read_text(encoding='utf-8')):
        assert project['name'] in docs['projets.html'].path.read_text(encoding='utf-8').replace('&amp;', '&')
    assert (ROOT/'.nojekyll').exists()
    print(f'PASS: {len(docs)} pages, {checked} internal links/assets/anchors, 3 SVGs, all project entries.')


if __name__ == '__main__':
    main()
