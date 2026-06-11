import json
import csv
from datetime import datetime


def export_csv():
    """Export sets to CSV format."""
    with open('data/sets.json') as f:
        data = json.load(f)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_path = 'exports/pentachords_voicings.csv'
    csv_path_timestamped = f'exports/pentachords_voicings_{timestamp}.csv'
    for path in (csv_path, csv_path_timestamped):
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            # Header
            writer.writerow([
                'SetIndex',
                'SetNames',
                'PCs->0',
                'PrimeForm',
                'Forte',
                'IntervalStructure',
                'PentatonicReference',
                'BassNote',
                'BassName',
                'Inversion',
                'ChordTones',
                'ChordSymbol',
            ])
            # Data rows: one row per voicing
            for i, item in enumerate(data, 1):
                setnames = ', '.join(item.get('names_transposed_to_C', []))
                pcs0 = ', '.join(str(p) for p in item.get('pcs_transposed_to_0', []))
                prime = ', '.join(str(p) for p in item.get('prime_form', []))
                forte = item.get('forte', '—')
                interval_struct = item.get('interval_structure', '')
                pentatonic_refs = ', '.join(item.get('pentatonic_reference', []))
                voicings = item.get('voicings') or []
                if voicings:
                    for v in voicings:
                        writer.writerow([
                            i,
                            setnames,
                            pcs0,
                            prime,
                            forte,
                            interval_struct,
                            pentatonic_refs,
                            v.get('bass_note'),
                            v.get('bass_name'),
                            v.get('inversion', '?'),
                            ', '.join(v.get('chord_tones', [])),
                            v.get('chord_symbol', ''),
                        ])
                else:
                    writer.writerow([i, setnames, pcs0, prime, forte, interval_struct, pentatonic_refs, '', '', '', '', ''])
    print(f'Exported CSV: {csv_path}')
    print(f'Exported CSV: {csv_path_timestamped}')


def export_html():
    """Export sets to HTML format for printing."""
    with open('data/sets.json') as f:
        data = json.load(f)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    html_path = 'exports/pentachords_voicings.html'
    html_path_timestamped = f'exports/pentachords_voicings_{timestamp}.html'
    pretty_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    parts = []
    parts.append('<!DOCTYPE html>')
    parts.append('<html lang="en">')
    parts.append('<head>')
    parts.append('<meta charset="utf-8">')
    parts.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
    parts.append('<title>Pentachords Archive (12-TET)</title>')
    parts.append('<style>body{font-family:Segoe UI, Tahoma, Geneva, Verdana, sans-serif;margin:1rem;background:white;color:#333}th{background:#4a90e2;color:#fff;padding:.5rem;border:1px solid #333}td{padding:.4rem;border:1px solid #ddd}</style>')
    parts.append('</head>')
    parts.append('<body>')
    parts.append(f'<h1>Pentachords in 12-TET: Complete Archive</h1>')
    parts.append(f'<div class="metadata"><p><strong>Total Sets:</strong> {len(data)} pentachords (5-note combinations)</p><p><strong>Generated:</strong> {pretty_timestamp}</p><p><strong>Root Note:</strong> C</p></div>')
    parts.append('<table><thead><tr><th>#</th><th>Set</th><th>PCs</th><th>Prime</th><th>Forte</th><th>Intervals</th><th>Pentatonic</th><th>Bass</th><th>Inversion</th><th>Chord Tones</th><th>Symbol</th></tr></thead><tbody>')

    rownum = 0
    for i, item in enumerate(data, 1):
        names = ', '.join(item.get('names_transposed_to_C', []))
        pcs = ', '.join(str(p) for p in item.get('pcs_transposed_to_0', []))
        prime = ', '.join(str(p) for p in item.get('prime_form', []))
        forte = item.get('forte', '—')
        interval_struct = item.get('interval_structure', '')
        pentatonic_refs = ', '.join(item.get('pentatonic_reference', []))
        voicings = item.get('voicings') or []
        if voicings:
            for v in voicings:
                rownum += 1
                parts.append('<tr>')
                parts.append(f'<td>{rownum}</td>')
                parts.append(f'<td>{names}</td>')
                parts.append(f'<td>{pcs}</td>')
                parts.append(f'<td>{prime}</td>')
                parts.append(f'<td><strong>{forte}</strong></td>')
                parts.append(f'<td>{interval_struct}</td>')
                parts.append(f'<td>{pentatonic_refs}</td>')
                parts.append(f'<td>{v.get("bass_name")}</td>')
                parts.append(f'<td>{v.get("inversion", "?")}</td>')
                parts.append(f'<td>{", ".join(v.get("chord_tones", []))}</td>')
                parts.append(f'<td>{v.get("chord_symbol","")}</td>')
                parts.append('</tr>')
        else:
            rownum += 1
            parts.append('<tr>')
            parts.append(f'<td>{rownum}</td>')
            parts.append(f'<td>{names}</td>')
            parts.append(f'<td>{pcs}</td>')
            parts.append(f'<td>{prime}</td>')
            parts.append(f'<td><strong>{forte}</strong></td>')
            parts.append(f'<td>{interval_struct}</td>')
            parts.append(f'<td>{pentatonic_refs}</td>')
            parts.append('<td></td><td></td><td></td><td></td>')
            parts.append('</tr>')

    parts.append('</tbody></table></body></html>')
    html = '\n'.join(parts)
    with open(html_path, 'w') as f:
        f.write(html)
    with open(html_path_timestamped, 'w') as f:
        f.write(html)
    print(f'Exported HTML: {html_path}')
    print(f'Exported HTML: {html_path_timestamped}')


if __name__ == '__main__':
    import os
    os.makedirs('exports', exist_ok=True)
    export_csv()
    export_html()
    print('All exports complete.')
