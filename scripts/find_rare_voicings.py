#!/usr/bin/env python3
import json
from collections import defaultdict

with open('data/sets.json') as f:
    data = json.load(f)

categories = defaultdict(list)

for si, s in enumerate(data, 1):
    for v in s.get('voicings', []):
        sym = v.get('chord_symbol', '')
        tones = v.get('chord_tones', [])
        # bb7 literal
        if 'bb7' in sym or 'bb7' in tones:
            categories['bb7'].append((si, s['pcs'], s['names_transposed_to_C'], v))
        # degree symbol
        if '\u00B0' in sym or '°' in sym:
            categories['degree'].append((si, s['pcs'], s['names_transposed_to_C'], v))
        # sus and degree together
        if 'sus' in sym and ('\u00B0' in sym or '°' in sym):
            categories['sus_and_degree'].append((si, s['pcs'], s['names_transposed_to_C'], v))
        # long voicing (>=6 tones)
        if len(tones) >= 6:
            categories['long'].append((si, s['pcs'], s['names_transposed_to_C'], v))
        # conflict: both #5 and b13
        if '#5' in tones and 'b13' in tones:
            categories['conflict_b13_hash5'].append((si, s['pcs'], s['names_transposed_to_C'], v))
        # bb7 and 13 together as literal tone names (same pitch class)
        if 'bb7' in tones and '13' in tones:
            categories['bb7_and_13'].append((si, s['pcs'], s['names_transposed_to_C'], v))
        # 4 still present
        if '4' in tones:
            categories['has4'].append((si, s['pcs'], s['names_transposed_to_C'], v))

def print_examples(cat, limit=6):
    items = categories.get(cat, [])[:limit]
    if not items:
        return
    print(f'-- {cat} (total {len(categories.get(cat,[]))})')
    for si, pcs, names, v in items:
        print(f'Set#{si} pcs={pcs} names={names}')
        print(f'  bass {v.get("bass_note")} {v.get("bass_name")}')
        print(f'  tones: {v.get("chord_tones")}')
        print(f'  symbol: {v.get("chord_symbol")}')
    print()

for c in ['bb7','degree','sus_and_degree','long','conflict_b13_hash5','bb7_and_13','has4']:
    print_examples(c)

print('Done')
