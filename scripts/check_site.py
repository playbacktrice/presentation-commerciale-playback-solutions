#!/usr/bin/env python3
"""Validate the five V2 pages, relative URLs, references and photo contracts."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import re
import subprocess
import tempfile
import shutil

ROOT = Path(__file__).resolve().parents[1]
PAGES = {'index.html','creative-lab.html','performing-systems.html','reliable-systems.html','contact.html'}


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path=path; self.ids=set(); self.links=[]; self.h1=0; self.main=0; self.current=[]; self.text=[]
        self.stack=[]; self.contact_links=[]; self.outside_contact=[]; self.collection=[]
        self.feed(path.read_text(encoding='utf-8'))
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'data-project-slugs' in attrs:self.collection.append(attrs['data-project-slugs'].split())
        if tag not in {'meta','link','img','br','hr','input','source','wbr'}:
            self.stack.append((tag,attrs.get('class','').split()))
        in_contact=any('contact-band' in classes for _,classes in self.stack)
        if attrs.get('href','').startswith(('tel:','mailto:')):
            assert in_contact, f'{self.path}: contact link outside contact section'
            self.contact_links.append(attrs['href'])
        if not in_contact:self.outside_contact.extend(value for value in attrs.values() if value is not None)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'{self.path}: duplicate ID'
            self.ids.add(attrs['id'])
        if tag=='h1': self.h1+=1
        if tag=='main': self.main+=1
        if attrs.get('aria-current')=='page': self.current.append(attrs['href'])
        if tag=='img': assert 'alt' in attrs
        for key in ('href','src'):
            if key in attrs: self.links.append(attrs[key])
    def handle_data(self,data):
        self.text.append(data)
        if not any('contact-band' in classes for _,classes in self.stack):self.outside_contact.append(data)
    def handle_endtag(self,tag):
        for index in range(len(self.stack)-1,-1,-1):
            if self.stack[index][0]==tag:
                self.stack=self.stack[:index];break


def main():
    docs={p.name:Document(p) for p in ROOT.glob('*.html')}
    assert set(docs)==PAGES, f'Unexpected pages: {set(docs)^PAGES}'
    checked=0
    for name,doc in docs.items():
        assert doc.h1==doc.main==1
        assert doc.current==[name]
        assert doc.contact_links==['tel:+33602256978','mailto:anthony@playback-solutions.com']
        outside=' '.join(doc.outside_contact)
        assert not re.search(r'(?:\+33[\s().-]*|0)6(?:[\s().-]*\d){8}',outside)
        assert 'anthony@playback-solutions.com' not in outside
        raw_page=doc.path.read_text()
        for forbidden in ['lang="en"','audiovisuel','A creative lab.','Reliable systems for demanding','Care. Precision.','Hardware','software','show-control']:
            assert forbidden not in (' '.join(doc.text) if forbidden in {'software','Hardware'} else raw_page),(name,forbidden)
        for raw in doc.links:
            u=urlsplit(raw)
            if u.scheme in {'tel','mailto'}:continue
            assert not u.scheme and not u.netloc and not u.path.startswith('/'),raw
            target=(ROOT/unquote(u.path)).resolve() if u.path else doc.path.resolve()
            assert target.is_relative_to(ROOT) and target.is_file(),(name,raw)
            if u.fragment: assert unquote(u.fragment) in docs[target.name].ids
            assert 'visual-' not in raw and '/preview/' not in raw
            checked+=1
    assert len(json.loads((ROOT/'data/projects.json').read_text()))==40
    media=json.loads((ROOT/'data/media.json').read_text())
    assert len(media)==15
    source=''.join(p.read_text() for p in ROOT.glob('*.html'))
    for key in media: assert f'data-media="{key}"' in source
    assert 'Catalogue' not in source
    for name in ['Justice','Polo &amp; Pan','Mylène Farmer','Eddy de Pretto','Kungs','Damso','Jeux olympiques de Paris 2024']:
        assert name in (ROOT/'index.html').read_text()
    projects=json.loads((ROOT/'data/projects.json').read_text())
    approved=[item for item in projects if item.get('publication_approved') is True]
    integrated=[slug for group in docs['index.html'].collection for slug in group]
    assert len(approved)==39 and len(docs['index.html'].collection)==34
    assert sorted(integrated)==sorted(item['slug'] for item in approved)
    assert len(integrated)==len(set(integrated))
    assert {item['name'] for item in approved if item['slug'].startswith('mc-solaar-')}=={'MC Solaar'}
    assert [item['edition'] for item in approved if item['name']=='MC Solaar']==['2022','2023']
    assert [item['edition'] for item in approved if item['name']=='Mylène Farmer']==['2019','Nevermore','Mylène le retour']
    assert any(item['name']=='Claire Laffut' and item['edition']=='2021' for item in approved)
    assert not set(integrated).intersection(item['slug'] for item in projects if item.get('publication_approved') is not True)
    assert (ROOT/'index.html').read_text().count('<li>')==6
    # Validate the future photo path using an isolated fixture, never a site image.
    with tempfile.TemporaryDirectory(prefix='playback-v2-test-') as folder:
        fixture=Path(folder)
        for name in ['scripts','data','assets']:
            shutil.copytree(ROOT/name,fixture/name)
        photo=fixture/'assets/photos/fixture.png';photo.parent.mkdir(exist_ok=True)
        shutil.copy2(ROOT/'assets/logo_playback_BLACK_HORIZONTAL.png',photo)
        data=json.loads(json.dumps(media))
        data['home-justice'].update(src='assets/photos/fixture.png',alt='Image technique de test',credit='Fixture de test uniquement',approved=True)
        (fixture/'data/media.json').write_text(json.dumps(data))
        fixture_projects=json.loads(json.dumps(projects))
        next(project for project in fixture_projects if project['slug']=='damso').update(image='assets/photos/fixture.png',image_alt='Image technique de test',image_credit='Fixture de test uniquement')
        (fixture/'data/projects.json').write_text(json.dumps(fixture_projects))
        subprocess.run(['python3',str(fixture/'scripts/build.py')],check=True,capture_output=True)
        output=(fixture/'index.html').read_text()
        assert 'src="assets/photos/fixture.png"' in output and 'Fixture de test uniquement' in output
        assert 'data-media="project-damso"' in output
        data['home-justice']['approved']=False
        (fixture/'data/media.json').write_text(json.dumps(data))
        result=subprocess.run(['python3',str(fixture/'scripts/build.py')],capture_output=True)
        assert result.returncode!=0 and b'validated photo' in result.stderr
    print(f'PASS: 5 pages; {checked} internal links/assets/anchors; 15 photo entries; 7 featured references; all 39 approved entries in 34 groups; contacts restricted to contact sections; all 40 source references retained; validated-photo fixture accepted and unapproved fixture rejected.')


if __name__=='__main__':main()
