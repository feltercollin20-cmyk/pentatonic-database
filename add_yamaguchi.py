#!/usr/bin/env python3
"""
Add Yamaguchi Set labels to the dataset by reading from the Yamaguchi Pentatonic Sets Excel file.
"""

import json
import openpyxl


def read_yamaguchi_mapping():
    """Read the Yamaguchi Excel file and build a pitch class to label mapping."""
    mapping = {}
    current_label = None
    
    wb = openpyxl.load_workbook('/Users/collin_felter/Desktop/Yamaguchi Pentatonic Sets.xlsx')
    ws = wb.active
    
    for row_idx in range(1, 331):
        row = [cell.value for cell in ws[row_idx]]
        label = row[0]
        variant = row[1]
        
        # Extract pitch classes from columns 2 onwards
        try:
            pcs_list = [int(x) for x in row[2:] if x is not None and isinstance(x, (int, float))]
            pcs = tuple(sorted(pcs_list))
        except:
            pcs = None
        
        if label:
            current_label = label
        if variant and current_label and pcs:
            yama_label = f"{current_label}({variant})"
            mapping[pcs] = yama_label
    
    return mapping


def add_yamaguchi_labels(input_path='data/sets.json'):
    """Add Yamaguchi labels to the dataset."""
    
    # Read Yamaguchi mapping
    print("Reading Yamaguchi mapping...")
    yamaguchi_map = read_yamaguchi_mapping()
    print(f"Loaded {len(yamaguchi_map)} Yamaguchi labels")
    
    # Read dataset
    with open(input_path, 'r') as f:
        data = json.load(f)
    
    # Add Yamaguchi labels
    matched = 0
    unmatched = []
    
    for i, entry in enumerate(data):
        pcs = tuple(entry.get('pcs_transposed_to_0', []))
        if pcs in yamaguchi_map:
            entry['yamaguchi_set'] = yamaguchi_map[pcs]
            matched += 1
        else:
            entry['yamaguchi_set'] = None
            unmatched.append((i, pcs))
    
    # Write updated dataset
    with open(input_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Matched {matched}/{len(data)} sets with Yamaguchi labels")
    if unmatched:
        print(f"Unmatched: {len(unmatched)} sets")
        for idx, pcs in unmatched[:5]:
            print(f"  Set {idx}: {pcs}")
    
    print(f"Updated {input_path}")


if __name__ == '__main__':
    add_yamaguchi_labels()
