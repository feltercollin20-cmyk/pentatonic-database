# All 12-TET Pentatonics: Altered and Superimposed

A comprehensive, interactive database for all 5-note pitch-class sets in 12-tone equal temperament, with set theory labelling, interval vectors, superimpositions, and searchable/sortable features.

**Created for Collin Felter's Dissertation:** *Jazz Pentatonicism: A Study of History, Abstraction, and Pragmaticism* (Ph.D., History and Theory of Music, University of California, Irvine)

## Features

- **Complete Database**: All 330 unique pentatonic pitch-class sets
- **Forte Labeling**: Official Forte numbers with Yamaguchi Set variants
- **Interval Vectors**: Computed from pitch-class sets in `<p,m2,M2,m3,M3,P4>` format
- **Voicing Superimpositions**: Chord tones, symbols, and superset collections for each bass inversion
- **Advanced Search**: Filter across all columns, pitch classes, chord symbols, and voicing details
- **Sortable Columns**: Click headers to sort by any field (ascending/descending)
- **Pagination**: Choose 25, 50, 100 items per page, or continuous scroll
- **Explode All**: Expand all superimposition panels at once

### Prerequisites
- Python 3.10 or higher
- pip

## Project Structure

```
pentatonic-database/
├── app.py                    # Flask application
├── generate_sets.py          # Generate pentachord dataset
├── chord_tones.py            # Chord tone naming & voicing logic
├── pentatonic.py             # Pentatonic set utilities
├── pentatonic_reference.py   # Reference pentatonic mappings
├── data/
│   └── sets.json             # Complete pentachord database (330 sets)
├── templates/
│   └── index.html            # HTML page template
├── static/
│   ├── main.js               # Search, sort, pagination logic
│   └── main.css              # Styling
├── exports/
│   └── pentachords_voicings.html  # Static export for Squarespace
├── scripts/
│   └── add_voicings.py       # Generate voicing superimpositions
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Data Format

Each pentatonic in `data/sets.json` includes:

```json
{
  "pcs": [0, 1, 2, 3, 4],
  "names_transposed_to_C": ["C", "Db", "D", "Eb", "E"],
  "pcs_transposed_to_0": [0, 1, 2, 3, 4],
  "prime_form": [0, 1, 2, 3, 4],
  "forte": "5-1",
  "yamaguchi_set": "5-1(a)",
  "interval_structure": "m2-m2-m2-m2-m6",
  "pentatonic_reference": ["Chromatic Pentatonic Subset"],
  "voicings": [
    {
      "bass_name": "C",
      "inversion": "R",
      "chord_tones": ["1", "b9", "9", "b3", "3"],
      "chord_symbol": "Cm(b9)",
      "superset_collections": []
    }
  ]
}
```

## Technologies

- **Backend**: Python 3, Flask
- **Frontend**: HTML5, vanilla JavaScript, CSS3
- **Data**: JSON (330 pentatonics with voicing metadata)
- **Classification**: Forte numbers, Yamaguchi Sets, interval vectors

## License

This project is created for academic research and public educational use.

## Contact

For questions or contributions, please reach out through collinfelter.com

---


