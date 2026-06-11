import re
import json
import requests

WIKI_URL = 'https://en.wikipedia.org/wiki/List_of_set_classes'
API_URL = 'https://en.wikipedia.org/w/api.php'


def parse_wiki_for_5card(html_text):
    # Find table rows for set classes; look for entries starting with '5-'
    # Pattern: | 5-1 | [0,1,2,3,4]
    pattern = re.compile(r"\|\s*(5[-A-Z0-9]+)\s*\|\s*\[([^\]]+)\]")
    mapping = {}
    for m in pattern.finditer(html_text):
        forte = m.group(1).strip()
        prime_text = m.group(2).strip()
        # prime_text may contain T or E for 10/11; replace
        prime_text = prime_text.replace('T', '10').replace('E', '11')
        parts = [p.strip() for p in prime_text.split(',') if p.strip()!='']
        try:
            prime = tuple(int(p) for p in parts)
        except ValueError:
            continue
        mapping[prime] = forte
    return mapping


def update_data():
    # Try getting page raw wikitext via MediaWiki API for easier parsing
    params = {
        'action': 'parse',
        'page': 'List_of_set_classes',
        'prop': 'wikitext',
        'format': 'json'
    }
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; PentatonicBot/1.0)'}
    r = requests.get(API_URL, params=params, timeout=15, headers=headers)
    r.raise_for_status()
    data = r.json()
    wikitext = data.get('parse', {}).get('wikitext', {}).get('*', '')
    if not wikitext:
        # fallback to fetching HTML
        r2 = requests.get(WIKI_URL, timeout=15, headers=headers)
        r2.raise_for_status()
        text = r2.text
    else:
        text = wikitext
    mapping = parse_wiki_for_5card(text)

    with open('data/sets.json','r') as f:
        data = json.load(f)

    updated = 0
    for item in data:
        pf = tuple(item.get('prime_form', []))
        if not pf:
            continue
        if pf in mapping:
            item['forte'] = mapping[pf]
            updated += 1

    with open('data/sets.json','w') as f:
        json.dump(data, f, indent=2)

    print(f'Updated {updated} sets with Forte labels')


if __name__ == '__main__':
    update_data()
