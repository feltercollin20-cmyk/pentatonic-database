"""
Chord tone naming and voicing logic for pentatonic sets over bass notes.
"""

PITCH_NAMES = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

# Inversion labels: interval in semitones from each bass note UP to C
INVERSION_LABELS = {
    0: 'R',      # C to C = root position
    1: 'm2',     # B to C = minor 2nd
    2: 'M2',     # Bb to C = major 2nd
    3: 'm3',     # A to C = minor 3rd
    4: 'M3',     # Ab to C = major 3rd
    5: 'P4',     # G to C = perfect 4th
    6: 'TT',     # F# to C = tritone
    7: 'P5',     # F to C = perfect 5th
    8: 'm6',     # E to C = minor 6th
    9: 'M6',     # Eb to C = major 6th
    10: 'b7',    # D to C = minor 7th
    11: 'maj7',  # C# to C = major 7th
}


def get_inversion_label(bass_note):
    """
    Get the inversion label for a bass note.
    The interval is calculated from bass_note UP to C (pitch class 0).
    """
    interval = (0 - bass_note) % 12
    return INVERSION_LABELS.get(interval, '?')


def get_chord_tones(pcs, bass_note):
    """
    Given a pentatonic set (pitch classes 0-11) and a bass note,
    compute the chord tones and chord symbol.
    
    Args:
        pcs: list of pitch classes [0-11]
        bass_note: bass pitch class [0-11]
    
    Returns:
        {
            'bass_name': str,
            'chord_tones': [list of tone names],
            'chord_symbol': str
        }
    """
    intervals = [((p - bass_note) % 12) for p in pcs]
    unique_intervals = set(intervals)

    has_major_3rd = 4 in unique_intervals
    has_minor_3rd = 3 in unique_intervals
    has_perfect_5th = 7 in unique_intervals
    has_fourth = 5 in unique_intervals
    has_augmented_fifth = 8 in unique_intervals
    has_b7 = 10 in unique_intervals
    has_maj7 = 11 in unique_intervals

    # Keep both thirds present so we can label the minor third as #9
    # whenever the major third is also in the set.
    seventh_type = None
    add_maj7 = False
    if has_b7 and has_maj7:
        seventh_type = 'b7'
        add_maj7 = True
    elif has_b7:
        seventh_type = 'b7'
    elif has_maj7:
        seventh_type = 'maj7'

    tone_names = []
    for interval in intervals:
        if interval == 0:
            tone_names.append('1')
            continue

        tone_name = name_interval(
            interval,
            has_major_3rd,
            has_minor_3rd,
            has_fourth,
            has_perfect_5th,
            has_augmented_fifth,
            has_b7,
            has_maj7,
        )
        if tone_name:
            tone_names.append(tone_name)

    if has_minor_3rd and '#5' in tone_names:
        tone_names = ['b13' if t == '#5' else t for t in tone_names]

    if add_maj7 and 'maj7' in tone_names:
        tone_names = ['addmaj7' if t == 'maj7' else t for t in tone_names]

    seen = set()
    unique_tones = []
    for t in tone_names:
        if t not in seen:
            unique_tones.append(t)
            seen.add(t)
    tone_names = unique_tones

    bass_name = PITCH_NAMES[bass_note]
    chord_symbol = build_chord_symbol(
        bass_name,
        tone_names,
        seventh_type,
        has_major_3rd,
        has_minor_3rd,
        has_perfect_5th,
        has_fourth,
        has_augmented_fifth,
    )
    inversion = get_inversion_label(bass_note)

    return {
        'bass_name': bass_name,
        'inversion': inversion,
        'chord_tones': tone_names,
        'chord_symbol': chord_symbol,
    }


def name_interval(interval, has_major_3rd, has_minor_3rd, has_fourth, has_perfect_5th, has_augmented_fifth, has_b7, has_maj7):
    """Name a single interval based on chord context."""

    if interval == 1:
        return 'b9'
    elif interval == 2:
        return '9'
    elif interval == 3:
        if has_major_3rd:
            return '#9'
        return 'b3'
    elif interval == 4:
        return '3'
    elif interval == 5:
        return '4'
    elif interval == 6:
        if has_perfect_5th or has_major_3rd or has_augmented_fifth:
            return '#11'
        return 'b5'
    elif interval == 7:
        return '5'
    elif interval == 8:
        if has_minor_3rd or has_perfect_5th:
            return 'b13'
        return '#5'
    elif interval == 9:
        if has_b7 or has_maj7 or (not has_major_3rd and has_perfect_5th):
            return '13'
        return '6'
    elif interval == 10:
        return 'b7'
    elif interval == 11:
        return 'maj7'

    return None


def build_chord_symbol(bass_name, tone_names, seventh_type, has_major_3rd, has_minor_3rd, has_perfect_5th, has_fourth, has_augmented_fifth):
    """Build a readable chord symbol from bass and tone names."""
    symbol = bass_name

    has_3rd = '3' in tone_names
    has_b3 = 'b3' in tone_names
    has_5th = '5' in tone_names
    has_aug_5th = '#5' in tone_names
    has_b5 = 'b5' in tone_names
    has_4 = '4' in tone_names
    has_13 = '13' in tone_names
    has_9 = '9' in tone_names
    has_6 = '6' in tone_names
    has_11 = '11' in tone_names
    has_sharp11 = '#11' in tone_names
    has_b13 = 'b13' in tone_names
    has_addmaj7 = 'addmaj7' in tone_names

    suspended = False
    if has_4:
        if has_3rd or has_b3:
            tone_names = ['11' if t == '4' else t for t in tone_names]
        else:
            suspended = True

    is_dim = has_b3 and has_b5
    is_half_dim = has_b3 and has_b5 and seventh_type == 'b7'
    is_minor = has_b3 and not is_dim
    is_augmented = has_aug_5th and not has_b3

    if is_dim:
        if seventh_type == 'b7':
            symbol += '°7'
            seventh_type = None
        elif seventh_type == 'maj7' or has_addmaj7:
            symbol += 'dim maj7'
            seventh_type = None
        else:
            symbol += '°'
    elif is_minor:
        if seventh_type == 'maj7':
            symbol += 'mmaj7'
            seventh_type = None
        else:
            symbol += 'm'
    elif has_3rd and has_aug_5th:
        symbol += '+'
    elif has_3rd and has_b5:
        symbol += '(b5)'
    elif is_augmented:
        symbol += '+'
    elif suspended:
        symbol += 'sus'
        if has_b5:
            symbol += ' diminished'

    if seventh_type == 'maj7':
        symbol += 'maj7'
    elif seventh_type == 'b7':
        if not has_3rd and not has_b3:
            if suspended:
                symbol += '7'
            else:
                symbol = bass_name + '7'
        else:
            symbol += '7'

    extensions = []
    if 'b9' in tone_names:
        extensions.append('b9')
    if '9' in tone_names and 'b9' not in tone_names:
        extensions.append('9')
    if '#9' in tone_names:
        extensions.append('#9')
    if '11' in tone_names:
        extensions.append('11')
    if '#11' in tone_names:
        extensions.append('#11')
    if '13' in tone_names:
        extensions.append('13')
    if 'b13' in tone_names:
        extensions.append('b13')
    if '6' in tone_names and not seventh_type and '13' not in tone_names:
        extensions.append('6')
    if has_addmaj7:
        extensions.append('addmaj7')

    if '6' in extensions and '9' in extensions and not seventh_type:
        extensions = [e for e in extensions if e not in ['6', '9']]
        extensions.insert(0, '6/9')

    if len(extensions) > 1:
        if all(e in ['9', '11', '13', 'addmaj7'] for e in extensions):
            highest = None
            for ext in ['13', '11', '9']:
                if ext in extensions:
                    highest = ext
                    break
            extensions = [highest] + [e for e in extensions if e == 'addmaj7'] if highest else [e for e in extensions if e == 'addmaj7']

    if extensions:
        symbol += '(' + ', '.join(extensions) + ')'
    elif symbol == bass_name and suspended:
        symbol = bass_name + 'sus'

    return symbol


def compute_all_voicings(pcs):
    """
    For a given pentachord, compute voicings over all 12 bass notes.
    
    Returns:
        list of {bass_note, bass_name, chord_tones, chord_symbol}
    """
    voicings = []
    for bass in range(12):
        voicing = get_chord_tones(pcs, bass)
        voicing['bass_note'] = bass
        voicings.append(voicing)
    return voicings
