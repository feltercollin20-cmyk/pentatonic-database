import json
from pentatonic import (
    generate_all_pentatonic_sets,
    transpose_to_c,
    transpose_to_zero,
    prime_form,
)

# Forte numbers for all 38 pentachord prime forms (5-note sets)
PENTACHORD_FORTE = {
    (0, 1, 2, 3, 4): '5-1',
    (0, 1, 2, 3, 5): '5-2',
    (0, 1, 2, 3, 6): '5-4',
    (0, 1, 2, 3, 7): '5-5',
    (0, 1, 2, 4, 5): '5-3',
    (0, 1, 2, 4, 6): '5-9',
    (0, 1, 2, 4, 7): '5-Z12',
    (0, 1, 2, 4, 8): '5-13',
    (0, 1, 2, 5, 6): '5-6',
    (0, 1, 2, 5, 7): '5-14',
    (0, 1, 2, 5, 8): '5-Z18',
    (0, 1, 2, 6, 7): '5-7',
    (0, 1, 2, 6, 8): '5-15',
    (0, 1, 3, 4, 6): '5-10',
    (0, 1, 3, 4, 7): '5-16',
    (0, 1, 3, 4, 8): '5-Z37',
    (0, 1, 3, 5, 6): '5-Z36',
    (0, 1, 3, 5, 7): '5-24',
    (0, 1, 3, 5, 8): '5-27',
    (0, 1, 3, 6, 7): '5-19',
    (0, 1, 3, 6, 8): '5-29',
    (0, 1, 3, 6, 9): '5-31',
    (0, 1, 3, 7, 8): '5-20',
    (0, 1, 4, 5, 7): '5-Z38',
    (0, 1, 4, 5, 8): '5-21',
    (0, 1, 4, 6, 8): '5-30',
    (0, 1, 4, 6, 9): '5-32',
    (0, 1, 4, 7, 8): '5-22',
    (0, 2, 3, 4, 6): '5-8',
    (0, 2, 3, 4, 7): '5-11',
    (0, 2, 3, 5, 7): '5-23',
    (0, 2, 3, 5, 8): '5-25',
    (0, 2, 3, 6, 8): '5-28',
    (0, 2, 4, 5, 8): '5-26',
    (0, 2, 4, 6, 8): '5-33',
    (0, 2, 4, 6, 9): '5-34',
    (0, 2, 4, 7, 9): '5-35',
    (0, 3, 4, 5, 8): '5-Z17',
}


def get_forte(pcs):
    """Get Forte number for a pitch class set."""
    pf = tuple(prime_form(pcs))
    return PENTACHORD_FORTE.get(pf, '5-?')


def build_dataset():
    sets = generate_all_pentatonic_sets(root=0)
    out = []
    for s in sets:
        pf = prime_form(s)
        data = {
            'pcs': s,
            'names_transposed_to_C': transpose_to_c(s),
            'pcs_transposed_to_0': transpose_to_zero(s),
            'prime_form': list(pf),
            'forte': get_forte(s),
        }
        out.append(data)

    with open('data/sets.json', 'w') as f:
        json.dump(out, f, indent=2)



if __name__ == '__main__':
    import os
    os.makedirs('data', exist_ok=True)
    build_dataset()
    print('Wrote data/sets.json')
