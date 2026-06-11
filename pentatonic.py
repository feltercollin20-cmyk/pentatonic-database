from itertools import combinations
from typing import List, Tuple

NOTE_NAME_CANDIDATES = {
    0: ['C'],
    1: ['Db', 'C#'],
    2: ['D'],
    3: ['Eb', 'D#'],
    4: ['E'],
    5: ['F'],
    6: ['Gb', 'F#'],
    7: ['G'],
    8: ['Ab', 'G#'],
    9: ['A'],
    10: ['Bb', 'A#'],
    11: ['B'],
}


def note_letter(name: str) -> str:
    return name[0]


def pcs_to_names(pcs: List[int]) -> List[str]:
    pcs = sorted(set(p % 12 for p in pcs))
    return choose_note_names(pcs)


def choose_note_names(pcs: List[int]) -> List[str]:
    if not pcs:
        return []

    candidates_list = [NOTE_NAME_CANDIDATES[pc] for pc in pcs]
    best_assignment = None

    def penalty(name: str) -> int:
        if len(name) == 1:
            return 0
        return 1 if '#' not in name else 2

    def search(index: int, current: List[str], used_letters: set, score: int) -> None:
        nonlocal best_assignment
        if best_assignment is not None and score > best_assignment[0]:
            return
        if index == len(candidates_list):
            candidate = (score, current.copy())
            if best_assignment is None or candidate < best_assignment:
                best_assignment = candidate
            return

        for name in candidates_list[index]:
            letter = note_letter(name)
            duplicate_penalty = 100 if letter in used_letters else 0
            next_score = score + duplicate_penalty + penalty(name)
            if best_assignment is not None and next_score > best_assignment[0]:
                continue
            current.append(name)
            search(index + 1, current, used_letters | {letter}, next_score)
            current.pop()

    search(0, [], set(), 0)
    return best_assignment[1] if best_assignment else []


def normal_order(pcs: List[int]) -> List[int]:
    pcs = sorted(set(p % 12 for p in pcs))
    n = len(pcs)
    best = None
    best_span = None
    for i in range(n):
        order = [((pcs[(i + j) % n] - pcs[i]) % 12) for j in range(n)]
        span = order[-1]
        if best is None or span < best_span or (span == best_span and order < best):
            best = order
            best_span = span
    return best


def invert(pcs: List[int]) -> List[int]:
    return sorted({(-p) % 12 for p in pcs})


def prime_form(pcs: List[int]) -> Tuple[int, ...]:
    pcs = sorted(set(p % 12 for p in pcs))
    if not pcs:
        return tuple()
    n = len(pcs)
    # normal order for original
    orig_norm = normal_order(pcs)
    # normal order for inversion
    inv = invert(pcs)
    inv_norm = normal_order(inv)

    # choose lexicographically smaller between orig_norm and inv_norm
    # both are lists starting at 0
    chosen = orig_norm if orig_norm < inv_norm else inv_norm
    return tuple(chosen)


def transpose_to_c(pcs: List[int]) -> List[str]:
    # assuming we want notation transposed so that 0 is C
    pcs = sorted(set(p % 12 for p in pcs))
    return pcs_to_names(pcs)


def transpose_to_zero(pcs: List[int]) -> List[int]:
    pcs = sorted(set(p % 12 for p in pcs))
    min_pc = pcs[0]
    return [((p - min_pc) % 12) for p in pcs]


def generate_all_pentatonic_sets(root: int = 0) -> List[List[int]]:
    pcs = list(range(12))
    others = [p for p in pcs if p != root]
    sets = []
    for combo in combinations(others, 4):
        s = sorted([root] + list(combo))
        sets.append(s)
    return sets
