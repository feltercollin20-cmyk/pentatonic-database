"""
Pentatonic reference identification and interval structure calculation.
"""

# Interval semitone to name mapping
INTERVAL_NAMES = {
    1: 'm2',
    2: 'M2',
    3: 'm3',
    4: 'M3',
    5: 'P4',
    6: 'TT',
    7: 'P5',
    8: 'm6',
    9: 'M6',
    10: 'm7',
    11: 'M7',
}

# Standard pentatonic prime forms
MAJOR_PENTATONIC_PRIME = [0, 2, 4, 7, 9]
MINOR_PENTATONIC_PRIME = [0, 3, 5, 7, 10]

def get_interval_structure(pcs):
    """
    Calculate the interval structure for a pitch class set.
    Returns a string like "M2-M2-m3-M2-m3"
    """
    if not pcs or len(pcs) < 2:
        return ""
    
    sorted_pcs = sorted(set(pcs))
    if len(sorted_pcs) < 2:
        return ""
    
    intervals = []
    for i in range(len(sorted_pcs)):
        current = sorted_pcs[i]
        next_pc = sorted_pcs[(i + 1) % len(sorted_pcs)]
        if i == len(sorted_pcs) - 1:
            # Wrap around from last to first (within octave)
            interval = (next_pc + 12 - current) % 12
        else:
            interval = (next_pc - current) % 12
        
        if interval in INTERVAL_NAMES:
            intervals.append(INTERVAL_NAMES[interval])
    
    return '-'.join(intervals)


def get_all_rotations(pcs):
    """Get all rotations (modes) of a pitch class set."""
    sorted_pcs = sorted(set(pcs))
    rotations = []
    for i in range(len(sorted_pcs)):
        rotation = sorted_pcs[i:] + sorted_pcs[:i]
        # Normalize to start at 0
        normalized = [(p - rotation[0]) % 12 for p in rotation]
        rotations.append(tuple(sorted(normalized)))
    return rotations


def normalize_pcs(pcs):
    """Normalize pitch class set to start at 0."""
    if not pcs:
        return []
    sorted_pcs = sorted(set(pcs))
    min_pc = min(sorted_pcs)
    return sorted([(p - min_pc) % 12 for p in sorted_pcs])


def get_pentatonic_reference(prime_form, pcs_transposed_to_zero=None):
    """
    Identify pentatonic reference for a prime form or a root-transposed set.
    Returns a list of reference strings.
    """
    if pcs_transposed_to_zero and len(pcs_transposed_to_zero) == 5:
        normalized_pcs = normalize_pcs(pcs_transposed_to_zero)
    elif prime_form and len(prime_form) == 5:
        normalized_pcs = normalize_pcs(prime_form)
    else:
        return []

    prime_tuple = tuple(normalized_pcs)
    references = []

    families = [
        {
            'prime': tuple(MAJOR_PENTATONIC_PRIME),
            'name': 'Major Pentatonic',
            'mode_name': 'Mode of Major Pentatonic',
            'precedence': 1,
        },
        {
            'prime': tuple(MINOR_PENTATONIC_PRIME),
            'name': 'Minor Pentatonic',
            'mode_name': 'Mode of Minor Pentatonic',
            'precedence': 2,
        },
        {
            'prime': (0, 2, 5, 7, 10),
            'name': "Terefenko's Suspended Dominant",
            'mode_name': 'Mode of Suspended Dominant',
            'precedence': 3,
        },
        {
            'prime': (0, 2, 3, 7, 9),
            'name': "Terefenko's Dorian Pentatonic",
            'mode_name': 'Mode of Dorian Pentatonic',
            'precedence': 3,
        },
        {
            'prime': (0, 3, 7, 9, 11),
            'name': "Terefenko's Melodic Minor Pentatonic",
            'mode_name': 'Mode of Melodic Minor Pentatonic',
            'precedence': 3,
        },
        {
            'prime': (0, 1, 5, 7, 10),
            'name': "Terefenko's Phrygian Pentatonic",
            'mode_name': 'Mode of Phrygian Pentatonic',
            'precedence': 3,
        },
        {
            'prime': (0, 4, 6, 9, 11),
            'name': "Terefenko's Lydian Pentatonic",
            'mode_name': 'Mode of Lydian Pentatonic',
            'precedence': 3,
        },
        {
            'prime': (0, 2, 5, 7, 8),
            'name': "Terefenko's Aeolian Pentatonic",
            'mode_name': 'Mode of Aeolian Pentatonic',
            'precedence': 3,
        },
        {
            'prime': (0, 3, 5, 6, 10),
            'name': "Terefenko's Locrian Pentatonic",
            'mode_name': 'Mode of Locrian Pentatonic',
            'precedence': 3,
        },
        {
            'prime': (0, 4, 6, 8, 9),
            'name': "Terefenko's Lydian Augmented Pentatonic",
            'mode_name': 'Mode of Lydian Augmented Pentatonic',
            'precedence': 3,
        },
        {
            'prime': (0, 2, 3, 6, 10),
            'name': "Terefenko's Locrian M2 Pentatonic",
            'mode_name': 'Mode of Locrian M2 Pentatonic',
            'precedence': 3,
        },
        {
            'prime': (0, 1, 4, 8, 10),
            'name': "Terefenko's Altered Pentatonic",
            'mode_name': 'Mode of Altered Pentatonic',
            'precedence': 3,
        },
        {
            'prime': (0, 2, 4, 7, 10),
            'name': "Khan's Dominant Pentatonic",
            'mode_name': 'Mode of Dominant Pentatonic',
            'precedence': 4,
        },
        {
            'prime': (0, 3, 5, 7, 9),
            'name': "Bergonzi's Minor 6 Pentatonic",
            'mode_name': 'Mode of Minor 6 Pentatonic',
            'precedence': 5,
        },
        {
            'prime': (0, 2, 4, 7, 8),
            'name': "Bergonzi's Major b6 Pentatonic",
            'mode_name': 'Mode of Major b6 Pentatonic',
            'precedence': 5,
        },
        {
            'prime': (0, 3, 5, 6, 10),
            'name': "Bergonzi's Minor 7b5 Pentatonic",
            'mode_name': 'Mode of Minor 7b5 Pentatonic',
            'precedence': 5,
        },
        {
            'prime': (0, 1, 4, 7, 9),
            'name': "Bergonzi's Major b2 Pentatonic",
            'mode_name': 'Mode of Major b2 Pentatonic',
            'precedence': 5,
        },
        {
            'prime': (0, 1, 2, 3, 4),
            'name': 'Chromatic Pentatonic Subset',
            'mode_name': 'Mode of Chromatic Pentatonic',
            'precedence': 6,
        },
        {
            'prime': (0, 2, 4, 6, 8),
            'name': 'Whole Tone Pentatonic Subset',
            'mode_name': 'Mode of Whole Tone Pentatonic',
            'precedence': 6,
        },
    ]

    exact_precedences = []
    for family in families:
        family_prime = tuple(family['prime'])
        family_rotations = get_all_rotations(list(family['prime']))
        if prime_tuple == family_prime:
            references.append(family['name'])
            exact_precedences.append(family['precedence'])
        elif prime_tuple in family_rotations:
            references.append(family['mode_name'])

    if exact_precedences:
        min_exact_precedence = min(exact_precedences)
        filtered = []
        for family in families:
            if family['precedence'] > min_exact_precedence:
                # remove mode labels from lower-priority families when a higher-priority exact family exists
                continue
            filtered.append(family)

        # Rebuild references with precedence filtering to preserve order
        references = []
        for family in filtered:
            family_prime = tuple(family['prime'])
            family_rotations = get_all_rotations(list(family['prime']))
            if prime_tuple == family_prime:
                references.append(family['name'])
            elif prime_tuple in family_rotations:
                references.append(family['mode_name'])

    major_rotations = get_all_rotations(MAJOR_PENTATONIC_PRIME)
    best_shared = 0
    for major_rotation in major_rotations:
        shared = len(set(prime_tuple) & set(major_rotation))
        best_shared = max(best_shared, shared)

    alterations = 5 - best_shared
    references.append(f"Major Pentatonic {alterations} alteration" + ("s" if alterations != 1 else ""))

    # Preserve order while removing duplicates
    deduped = []
    for ref in references:
        if ref not in deduped:
            deduped.append(ref)
    return deduped
