# All 12-TET Pentatonics: Altered and Superimposed

A comprehensive, interactive database and analysis tool for all 5-note pitch-class sets (pentachords) in 12-tone equal temperament, with Forte labeling, Yamaguchi Set classification, interval vectors, voicing superimpositions, and searchable/sortable features.

**Created for Collin Felter's Dissertation:** *Jazz Pentatonicism: A Study of History, Abstraction, and Pragmaticism* (Ph.D., History and Theory of Music, University of California, Irvine)

## Features

- **Complete Database**: All 330 unique pentachord pitch-class sets
- **Forte Labeling**: Official Forte numbers with Yamaguchi Set variants
- **Interval Vectors**: Computed from pitch-class sets in `<p,m2,M2,m3,M3,P4>` format
- **Voicing Superimpositions**: Chord tones, symbols, and superset collections for each bass inversion
- **Advanced Search**: Filter across all columns, pitch classes, chord symbols, and voicing details
- **Sortable Columns**: Click headers to sort by any field (ascending/descending)
- **Pagination**: Choose 25, 50, 100 items per page, or continuous scroll
- **Explode All**: Expand all superimposition panels at once

## Local Development

### Prerequisites
- Python 3.10 or higher
- pip

### Installation & Running Locally

```bash
# Clone the repository
git clone https://github.com/<your-username>/pentatonic-database.git
cd pentatonic-database

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate dataset (if needed)
python generate_sets.py

# Start Flask server
python app.py
```

Open **http://127.0.0.1:5000/** in your browser.

## Hosting on Squarespace via GitHub Pages

### Step 1: Publish to GitHub

1. **Create a new repository** on GitHub:
   - Go to [github.com/new](https://github.com/new)
   - Name it `pentatonic-database` (or your preferred name)
   - Description: "Interactive 12-TET pentachord database"
   - Choose **Public** (required for free GitHub Pages)
   - Do NOT initialize with README (we already have one)
   - Click **Create repository**

2. **Initialize Git locally** (in the project folder):
   ```bash
   cd '/Users/collin_felter/Desktop/pentatonic python'
   git init
   git add .
   git commit -m "Initial commit: pentatonic database with UI"
   git branch -M main
   git remote add origin https://github.com/<your-username>/pentatonic-database.git
   git push -u origin main
   ```
   Replace `<your-username>` with your GitHub username.

### Step 2: Build Static HTML Version

The app requires Flask to run dynamically. To host on Squarespace, convert to static HTML:

1. **Export the database as static HTML:**
   ```bash
   python export_spreadsheet.py
   ```
   This creates files in the `exports/` folder.

2. **Create a static version:**
   - The `exports/pentachords_voicings.html` is a standalone HTML file
   - You can also use `templates/index.html` + `static/main.js` + `static/main.css` together

### Step 3: Embed on Squarespace

#### Option A: Embed HTML File (Recommended for Full Interactivity)

1. In Squarespace, go to **Pages** → Select the page where you want the table
2. Add a **Code Block** (under Custom)
3. Paste an `<iframe>` pointing to your GitHub-hosted file:
   ```html
   <iframe 
     src="https://cdn.jsdelivr.net/gh/<your-username>/pentatonic-database@main/exports/pentachords_voicings.html"
     style="width:100%; height:2000px; border:none;">
   </iframe>
   ```
   Replace `<your-username>` with your GitHub username.

4. Adjust the `height` value as needed (2000px is a starting point).

#### Option B: Host via GitHub Pages + Iframe

1. **Enable GitHub Pages:**
   - Go to your repository **Settings** → **Pages**
   - Under "Source", select **main** branch and **/root** folder
   - Click **Save**
   - GitHub will publish at `https://<your-username>.github.io/pentatonic-database`

2. **Update Squarespace iframe:**
   ```html
   <iframe 
     src="https://<your-username>.github.io/pentatonic-database/exports/pentachords_voicings.html"
     style="width:100%; height:2000px; border:none;">
   </iframe>
   ```

3. (Optional) If you want interactive Flask features, you'd need to host the Flask app on a server like Heroku, Railway, or Render (not supported by Squarespace's free tier).

#### Option C: Embed via jsDelivr (Simplest)

jsDelivr serves files directly from GitHub with no additional setup:

```html
<iframe 
  src="https://cdn.jsdelivr.net/gh/<your-username>/pentatonic-database@main/exports/pentachords_voicings.html"
  style="width:100%; height:2000px; border:none;"
  title="12-TET Pentachord Database">
</iframe>
```

This works immediately after your first commit to GitHub.

### Step 4: Test & Refine

1. Copy the iframe code into a Squarespace Code Block
2. Test the search, sort, and pagination features
3. Adjust iframe height if content is cut off
4. If embedding fails, check browser console for CORS issues (most CDNs allow cross-origin embedding)

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

Each pentachord in `data/sets.json` includes:

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
- **Data**: JSON (330 pentachords with voicing metadata)
- **Classification**: Forte numbers, Yamaguchi Sets, interval vectors

## License

This project is created for academic research and public educational use.

## Contact

For questions or contributions, please reach out through GitHub Issues or create a Pull Request.

---

*Dissertation Advisor: [Your Advisor Name], UC Irvine*
