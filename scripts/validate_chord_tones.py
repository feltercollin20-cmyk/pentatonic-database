import json

ERRORS = []

with open('data/sets.json', 'r') as f:
    data = json.load(f)

for i, entry in enumerate(data):
    pcs = entry.get('pcs_transposed_to_0') or entry.get('pcs') or []
    for v in entry.get('voicings', []):
        tones = v.get('chord_tones', [])
        sym = v.get('chord_symbol', '')
        bass = v.get('bass_name')

        if '3' in tones and 'b3' in tones:
            ERRORS.append((i, pcs, bass, tones, sym, '3 and b3 both present'))

        if 'b3' in tones and 'b5' in tones:
            if 'dim maj7' in sym:
                if 'maj7' not in tones and '13' not in tones:
                    ERRORS.append((i, pcs, bass, tones, sym, 'dim maj7 symbol without maj7/13'))
            elif 'ø7' in sym or '°7' in sym:
                ERRORS.append((i, pcs, bass, tones, sym, 'diminished triad labeled half-dim or dim7'))

        if 'b5' in tones and '4' in tones and 'sus' in sym and 'dim' not in sym:
            ERRORS.append((i, pcs, bass, tones, sym, 'sus chord missing dim'))

        if 'b5' in tones and 'sus' not in sym and 'dim' not in sym:
            ERRORS.append((i, pcs, bass, tones, sym, 'b5 present without sus/dim indicator'))


print('validation errors:', len(ERRORS))
if ERRORS:
    print('examples:')
    for err in ERRORS[:20]:
        print(err)
    raise SystemExit(1)
