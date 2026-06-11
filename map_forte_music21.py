import json
from music21.chord import Chord

PITCH_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def pcs_to_names(pcs):
    return [PITCH_NAMES[p % 12] for p in pcs]

def update_with_music21():
    with open('data/sets.json') as f:
        data = json.load(f)

    updated = 0
    for item in data:
        pcs = item.get('pcs', [])
        names = pcs_to_names(pcs)
        c = Chord(names)
        forte = getattr(c, 'forteClass', None)
        if forte:
            item['forte'] = forte
            updated += 1

    with open('data/sets.json','w') as f:
        json.dump(data, f, indent=2)

    print(f'Updated {updated} sets with Forte labels via music21')

if __name__ == '__main__':
    update_with_music21()
