#!/usr/bin/env python3
"""
Feed generator script for Hirosaki View.
Reads all observation files from observations/*.md (excluding index.md)
and builds RSS 2.0 (feed.xml) and Atom 1.0 (feed.atom) feeds containing
full observation text, front matter metadata, public HTML page links,
and Raw Markdown links (Source of Truth).
"""

import os
import glob
import re
import html
from datetime import datetime

BASE_URL = "https://yamamotoaomoriski-creator.github.io/hirosaki-view"
RAW_BASE_URL = "https://raw.githubusercontent.com/yamamotoaomoriski-creator/hirosaki-view/main"

def parse_md_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    parts = content.split('---', 2)
    front_matter = {}
    body = content

    if len(parts) >= 3:
        fm_text = parts[1]
        body = parts[2].strip()
        for line in fm_text.strip().splitlines():
            if ':' in line:
                key, val = line.split(':', 1)
                front_matter[key.strip()] = val.strip().strip('"').strip("'")

    filename = os.path.basename(filepath)
    slug = filename.replace('.md', '')

    date_str = front_matter.get('date', '')
    if not date_str:
        match = re.match(r'^(\d{4}-\d{2}-\d{2})', slug) or re.match(r'^(\d{4})(\d{2})(\d{2})', slug)
        if match:
            if len(match.groups()) == 1 and '-' in match.group(1):
                date_str = match.group(1)
            elif len(match.groups()) == 3:
                date_str = f"{match.group(1)}-{match.group(2)}-{match.group(3)}"

    title = front_matter.get('title', slug)

    return {
        'filename': filename,
        'slug': slug,
        'filepath': filepath,
        'front_matter': front_matter,
        'title': title,
        'date_str': date_str,
        'body': body
    }

def build_rss_feed(items):
    sorted_items = sorted(items, key=lambda x: x['date_str'], reverse=True)

    rss_items_xml = []
    for item in sorted_items:
        html_url = f"{BASE_URL}/observations/{item['slug']}.html"
        raw_url = f"{RAW_BASE_URL}/observations/{item['filename']}"

        try:
            dt = datetime.strptime(item['date_str'], '%Y-%m-%d')
            pub_date = dt.strftime('%a, %d %b %Y 00:00:00 +0900')
        except Exception:
            pub_date = item['date_str']

        fm = item['front_matter']
        meta_lines = [
            f"観測ID: {fm.get('id', '')}",
            f"観測日時: {fm.get('date', item['date_str'])}",
            f"場所: {fm.get('location', '')}",
            f"シリーズ: {fm.get('series', '')}",
            f"観測種別: {fm.get('type', '')}",
            f"観測者: {fm.get('observer', '')}",
            f"Web公開ページ: {html_url}",
            f"Source of Truth (Raw MD): {raw_url}"
        ]
        meta_block = "\n".join([line for line in meta_lines if line.split(': ')[1]])

        full_text = f"=== Front Matter Metadata ===\n{meta_block}\n\n=== Observation Content ===\n{item['body']}"
        escaped_title = html.escape(item['title'])
        escaped_body = html.escape(full_text)

        item_xml = f"""    <item>
      <title>{escaped_title}</title>
      <link>{html_url}</link>
      <guid isPermaLink="true">{html_url}</guid>
      <pubDate>{pub_date}</pubDate>
      <description>{escaped_body}</description>
      <source url="{raw_url}">Source Markdown (Source of Truth)</source>
    </item>"""
        rss_items_xml.append(item_xml)

    items_str = "\n".join(rss_items_xml)
    last_build = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0900')

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Hirosaki View — 一次都市観測アーカイブ RSS Feed</title>
    <link>{BASE_URL}/</link>
    <atom:link href="{BASE_URL}/feed.xml" rel="self" type="application/rss+xml" />
    <description>青森県弘前市の物理的現実（都市景観・建築・イベント仮設・工事）を現地で直接観測した一次情報ログのRSSフィード。</description>
    <language>ja</language>
    <lastBuildDate>{last_build}</lastBuildDate>
{items_str}
  </channel>
</rss>
"""

def build_atom_feed(items):
    sorted_items = sorted(items, key=lambda x: x['date_str'], reverse=True)

    atom_entries_xml = []
    for item in sorted_items:
        html_url = f"{BASE_URL}/observations/{item['slug']}.html"
        raw_url = f"{RAW_BASE_URL}/observations/{item['filename']}"

        try:
            dt = datetime.strptime(item['date_str'], '%Y-%m-%d')
            updated_date = dt.strftime('%Y-%m-%dT00:00:00+09:00')
        except Exception:
            updated_date = f"{item['date_str']}T00:00:00+09:00"

        fm = item['front_matter']
        meta_lines = [
            f"観測ID: {fm.get('id', '')}",
            f"観測日時: {fm.get('date', item['date_str'])}",
            f"場所: {fm.get('location', '')}",
            f"シリーズ: {fm.get('series', '')}",
            f"観測種別: {fm.get('type', '')}",
            f"観測者: {fm.get('observer', '')}",
            f"Web公開ページ: {html_url}",
            f"Source of Truth (Raw MD): {raw_url}"
        ]
        meta_block = "\n".join([line for line in meta_lines if line.split(': ')[1]])

        full_text = f"=== Front Matter Metadata ===\n{meta_block}\n\n=== Observation Content ===\n{item['body']}"
        escaped_title = html.escape(item['title'])
        escaped_body = html.escape(full_text)

        entry_xml = f"""  <entry>
    <title>{escaped_title}</title>
    <link rel="alternate" type="text/html" href="{html_url}" />
    <link rel="via" type="text/markdown" href="{raw_url}" title="Source Markdown (Source of Truth)" />
    <id>{html_url}</id>
    <updated>{updated_date}</updated>
    <content type="text">{escaped_body}</content>
  </entry>"""
        atom_entries_xml.append(entry_xml)

    entries_str = "\n".join(atom_entries_xml)
    feed_updated = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+09:00')

    return f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Hirosaki View — 一次都市観測アーカイブ Atom Feed</title>
  <subtitle>青森県弘前市の物理的現実（都市景観・建築・イベント仮設・工事）を現地で直接観測した一次情報ログのAtomフィード。</subtitle>
  <link rel="self" href="{BASE_URL}/feed.atom" />
  <link rel="alternate" href="{BASE_URL}/" />
  <id>{BASE_URL}/</id>
  <updated>{feed_updated}</updated>
{entries_str}
</feed>
"""

def generate_feeds():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    obs_dir = os.path.join(repo_root, 'observations')
    obs_files = [f for f in sorted(glob.glob(os.path.join(obs_dir, '*.md'))) if not f.endswith('index.md')]

    items = [parse_md_file(f) for f in obs_files]

    rss_xml = build_rss_feed(items)
    rss_path = os.path.join(repo_root, 'feed.xml')
    with open(rss_path, 'w', encoding='utf-8') as f:
        f.write(rss_xml)

    atom_xml = build_atom_feed(items)
    atom_path = os.path.join(repo_root, 'feed.atom')
    with open(atom_path, 'w', encoding='utf-8') as f:
        f.write(atom_xml)

    print(f"Successfully generated {rss_path} and {atom_path} from {len(items)} observations.")

if __name__ == '__main__':
    generate_feeds()
