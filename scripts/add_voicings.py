#!/usr/bin/env python3
import json
import os
import sys
# Ensure project root is on sys.path so we can import project modules when running from scripts/
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from chord_tones import compute_all_voicings
from pentatonic_reference import get_interval_structure, get_pentatonic_reference


def parse_degree_token(token):
    """Convert a degree token like 'b3', '#11', '13' into a semitone 0-11."""
    token = token.replace(' ', '')
    if not token:
        return None
    # count modifiers
    modifier = 0
    # normalize common prefixes like 'add' and 'maj'
    if token.startswith('add'):
        token = token[3:]
    if token.startswith('maj'):
        token = token[3:]
    while token.startswith('b') or token.startswith('#'):
        if token[0] == 'b':
            modifier -= 1
        else:
            modifier += 1
        token = token[1:]

    try:
        deg = int(token)
    except ValueError:
        return None

    # equivalence mapping: 9->2, 11->4, 13->6 (subtract 7 when >=9)
    if deg >= 9:
        deg = deg - 7

    base_map = {
        1: 0,
        2: 2,
        3: 4,
        4: 5,
        5: 7,
        6: 9,
        7: 11,
    }

    base = base_map.get(deg)
    if base is None:
        return None

    return (base + modifier) % 12


def build_collections():
    """Return dict of collection name -> set of pitch classes (0-11)"""
    collections_def = {
        'Major': ['1','2','3','4','5','6','7'],
        'Dorian': ['1','9','b3','4','5','13','b7'],
        'Phrygian': ['1','b9','b3','4','5','b13','b7'],
        'Lydian': ['1','2','3','#11','5','13','7'],
        'Mixolydian': ['1','9','3','4','5','13','b7'],
        'Aeolian': ['1','9','b3','4','5','13','b7'],
        'Locrian': ['1','b9','b3','4','b5','b13','b7'],
    }
    result = {}
    for name, tokens in collections_def.items():
        pcs = set()
        for t in tokens:
            v = parse_degree_token(t)
            if v is not None:
                pcs.add(v)
        result[name] = pcs
    return result


def add_voicings(input_path='data/sets.json', backup=True):
    if not os.path.exists(input_path):
        raise FileNotFoundError(input_path)

    with open(input_path, 'r') as f:
        data = json.load(f)

    if backup:
        bak = input_path + '.bak'
        with open(bak, 'w') as f:
            json.dump(data, f, indent=2)
        print('Backup written to', bak)

    for i, entry in enumerate(data):
        pcs = entry.get('pcs') or entry.get('pcs_transposed_to_0') or entry.get('pcs_transposed_to_0')
        # Ensure pcs is list of ints
        if not pcs:
            print('Skipping entry', i, 'no pcs')
            continue
        
        # Add interval structure
        interval_struct = get_interval_structure(pcs)
        entry['interval_structure'] = interval_struct
        
        # Add pentatonic reference
        prime_form = entry.get('prime_form', [])
        pcs_transposed_to_0 = entry.get('pcs_transposed_to_0')
        pentatonic_refs = get_pentatonic_reference(prime_form, pcs_transposed_to_0)
        entry['pentatonic_reference'] = pentatonic_refs
        
        voicings = compute_all_voicings(pcs)
        collections = build_collections()
        supers = set()
        for v in voicings:
            tones = v.get('chord_tones', [])
            parsed = set()
            for t in tones:
                p = parse_degree_token(t)
                if p is not None:
                    parsed.add(p)
            matched = []
            if parsed:
                for cname, cpcs in collections.items():
                    if parsed.issubset(cpcs):
                        matched.append(cname)
                        supers.add(cname)
            v['superset_collections'] = matched

        entry['voicings'] = voicings
        entry['superset_collections'] = sorted(list(supers))

    with open(input_path, 'w') as f:
        json.dump(data, f, indent=2)

    print('Updated', input_path, 'with voicings')


if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    add_voicings()
