function join(arr) { return (arr || []).join(', '); }

const DATA_VERSION = '202607031230';
let sets = window.initialSets || [];
let page = 1;
let sortState = { key: 'index', direction: 'asc' };
let appliedSearchQuery = '';
let selectedModeGroup = 'all';

const DEGREE_TO_PITCH_CLASS = {
  '1': 0,
  'b2': 1,
  'b9': 1,
  '2': 2,
  '9': 2,
  '#2': 3,
  '#9': 3,
  'b3': 3,
  '3': 4,
  'b4': 4,
  '4': 5,
  '#4': 6,
  '#11': 6,
  'b5': 6,
  '5': 7,
  '#5': 8,
  'b6': 8,
  'b13': 8,
  '6': 9,
  '13': 9,
  'bb7': 9,
  'b7': 10,
  '7': 11,
  'maj7': 11,
  'addmaj7': 11
};

const COLLECTION_FAMILIES = [
  {
    family: 'Major Modes',
    modes: [
      { name: 'Major', degrees: ['1', '2', '3', '4', '5', '6', '7'] },
      { name: 'Dorian', degrees: ['1', '2', 'b3', '4', '5', '6', 'b7'] },
      { name: 'Phrygian', degrees: ['1', 'b2', 'b3', '4', '5', 'b6', 'b7'] },
      { name: 'Lydian', degrees: ['1', '2', '3', '#4', '5', '6', '7'] },
      { name: 'Mixolydian', degrees: ['1', '2', '3', '4', '5', '6', 'b7'] },
      { name: 'Aeolian', degrees: ['1', '2', 'b3', '4', '5', 'b6', 'b7'] },
      { name: 'Locrian', degrees: ['1', 'b2', 'b3', '4', 'b5', 'b6', 'b7'] }
    ]
  },
  {
    family: 'Melodic Minor Modes',
    modes: [
      { name: 'Melodic Minor', degrees: ['1', '2', 'b3', '4', '5', '6', '7'] },
      { name: 'Dorian b2', degrees: ['1', 'b2', 'b3', '4', '5', '6', 'b7'] },
      { name: 'Lydian Augmented', degrees: ['1', '2', '3', '#4', '5', '6', '7'] },
      { name: 'Lydian Dominant', degrees: ['1', '2', '3', '#4', '5', '6', 'b7'] },
      { name: 'Mixolydian b6', degrees: ['1', '2', '3', '4', '5', 'b6', 'b7'] },
      { name: 'Aeolian b5', degrees: ['1', '2', 'b3', '4', 'b5', 'b6', 'b7'] },
      { name: 'Altered Dominant', degrees: ['1', 'b2', 'b3', '3', 'b5', 'b6', 'b7'] }
    ]
  },
  {
    family: 'Harmonic Minor Modes',
    modes: [
      { name: 'Harmonic Minor', degrees: ['1', '2', 'b3', '4', '5', 'b6', '7'] },
      { name: 'Locrian Maj6', degrees: ['1', 'b2', 'b3', '4', 'b5', '6', 'b7'] },
      { name: 'Ionian Augmented', degrees: ['1', '2', '3', '4', '#5', '6', '7'] },
      { name: 'Dorian #11', degrees: ['1', '2', 'b3', '#4', '5', '6', 'b7'] },
      { name: 'Phrygian Dominant', degrees: ['1', 'b2', '3', '4', '5', 'b6', 'b7'] },
      { name: 'Lydian #2', degrees: ['1', '#2', '3', '#4', '5', '6', '7'] },
      { name: 'Super Locrian bb7', degrees: ['1', 'b2', 'b3', '3', 'b5', 'b6', 'bb7'] }
    ]
  },
  {
    family: 'Harmonic Major Modes',
    modes: [
      { name: 'Harmonic Major', degrees: ['1', '2', '3', '4', '5', 'b6', '7'] },
      { name: 'Dorian b5', degrees: ['1', '2', 'b3', '4', 'b5', '6', 'b7'] },
      { name: 'Phrygian b4', degrees: ['1', 'b2', 'b3', 'b4', '5', 'b6', 'b7'] },
      { name: 'Lydian Minor', degrees: ['1', '2', 'b3', '#4', '5', '6', '7'] },
      { name: 'Mixolydian b2', degrees: ['1', 'b2', '3', '4', '5', '6', 'b7'] },
      { name: 'Lydian Augmented #2', degrees: ['1', '#2', '3', '#4', '#5', '6', '7'] },
      { name: 'Locrian bb7', degrees: ['1', 'b2', 'b3', '4', 'b5', 'b6', 'bb7'] }
    ]
  }
];

const SPECIAL_COLLECTIONS = [
  { name: 'Augmented Scale', degrees: ['1', 'b3', '3', '5', 'b6', '7'] },
  { name: 'Augmented Scale Half-Third', degrees: ['1', 'b2', '3', '4', '#5', '6'] }
];

const HEXATONIC_PARENT_LABELS = [
  { name: 'HEX 0,1 Pentatonic Subset', pcs: [0, 1, 4, 5, 8, 9] },
  { name: 'HEX 3,4 Pentatonic Subset', pcs: [0, 3, 4, 7, 8, 11] }
];

const MODE_GROUP_OPTIONS = [
  { value: 'all', label: 'All Groups', labels: [] },
  { value: 'major', label: 'Major Modes', labels: ['Major Modes'] },
  { value: 'melodic-minor', label: 'Melodic Minor Modes', labels: ['Melodic Minor Modes'] },
  { value: 'harmonic-minor', label: 'Harmonic Minor Modes', labels: ['Harmonic Minor Modes'] },
  { value: 'harmonic-major', label: 'Harmonic Major Modes', labels: ['Harmonic Major Modes'] },
  { value: 'diminished', label: 'Diminished Scale', labels: ['Diminished Scale'] },
  { value: 'augmented', label: 'Augmented Scale', labels: ['Augmented Scale'] },
  { value: 'octatonic', label: 'Octatonic Pentatonic Subsets', labels: ['OCT 0,1 Pentatonic Subset', 'OCT 2,3 Pentatonic Subset'] },
  { value: 'hexatonic', label: 'Hexatonic Pentatonic Subsets', labels: ['HEX 0,1 Pentatonic Subset', 'HEX 3,4 Pentatonic Subset'] }
];

const COLLECTION_SEARCH_ALIASES = {
  'Half-Whole Diminished': ['Diminished Scale'],
  'Whole-Half Diminished': ['Diminished Scale']
};

function fieldContains(field, q) {
  return field && field.toString().toLowerCase().includes(q);
}

function getPitchClassForDegree(tone) {
  if (Object.prototype.hasOwnProperty.call(DEGREE_TO_PITCH_CLASS, tone)) {
    return DEGREE_TO_PITCH_CLASS[tone];
  }
  return null;
}

function getPitchClassSet(degrees) {
  const pitchClasses = new Set();
  (degrees || []).forEach(degree => {
    const pitchClass = getPitchClassForDegree(degree);
    if (pitchClass !== null) pitchClasses.add(pitchClass);
  });
  return pitchClasses;
}

function isSubsetOfScale(chordTones, scaleDegrees) {
  if (!chordTones || chordTones.length === 0) return false;
  const normalizedChordTones = getPitchClassSet(chordTones);
  const scalePitchClasses = getPitchClassSet(scaleDegrees);
  if (normalizedChordTones.size === 0) return false;

  for (const pitchClass of normalizedChordTones) {
    if (!scalePitchClasses.has(pitchClass)) return false;
  }
  return true;
}

function getModalCollectionLabels(chordTones) {
  const labels = [];
  COLLECTION_FAMILIES.forEach(family => {
    family.modes.forEach(mode => {
      if (isSubsetOfScale(chordTones, mode.degrees)) labels.push(mode.name);
    });
  });
  SPECIAL_COLLECTIONS.forEach(collection => {
    if (isSubsetOfScale(chordTones, collection.degrees)) labels.push(collection.name);
  });
  return labels;
}

function getCollectionFamilyLabels(collections) {
  const labels = new Set();

  COLLECTION_FAMILIES.forEach(family => {
    if (family.modes.some(mode => collections.includes(mode.name))) {
      labels.add(family.family);
    }
  });

  if (collections.includes('Augmented Scale') || collections.includes('Augmented Scale Half-Third')) {
    labels.add('Augmented Scale');
  }

  collections.forEach(collection => {
    (COLLECTION_SEARCH_ALIASES[collection] || []).forEach(alias => labels.add(alias));
  });

  return [...labels];
}

function getModeGroupOption(groupValue) {
  return MODE_GROUP_OPTIONS.find(option => option.value === groupValue) || MODE_GROUP_OPTIONS[0];
}

function getSetSearchCollections(set) {
  const labels = new Set();
  (set.pentatonic_reference || []).forEach(ref => labels.add(ref));
  getHexatonicParentLabels(set).forEach(label => labels.add(label));
  (set.voicings || []).forEach(voicing => {
    getVoicingSearchCollections(voicing).forEach(label => labels.add(label));
  });
  return [...labels];
}

function matchesModeGroup(set, groupValue) {
  const option = getModeGroupOption(groupValue);
  if (!option.labels.length) return true;
  const labels = getSetSearchCollections(set);
  return option.labels.some(label => labels.includes(label));
}

function getVoicingCollections(v) {
  const baseCollections = v.superset_collections || [];
  const derivedCollections = getModalCollectionLabels(v.chord_tones);
  return [...new Set([...baseCollections, ...derivedCollections])];
}

function getVoicingSearchCollections(v) {
  const collections = getVoicingCollections(v);
  const familyLabels = getCollectionFamilyLabels(collections);
  return [...new Set([...collections, ...familyLabels])];
}

function getDisplayedChordSymbol(v) {
  const symbol = v.chord_symbol || '';
  const chordTones = v.chord_tones || [];
  const hasNaturalNine = chordTones.includes('9');
  const hasAlteredNine = chordTones.includes('b9') || chordTones.includes('#9');

  if (!symbol || !hasNaturalNine || !hasAlteredNine) return symbol;

  const toneOrder = ['b9', '9', '#9'];
  const nineTones = toneOrder.filter(tone => chordTones.includes(tone));
  const symbolMatch = symbol.match(/^(.*?)(?:\((.*)\))?$/);
  if (!symbolMatch) return symbol;

  const baseSymbol = symbolMatch[1];
  const extensionText = symbolMatch[2] || '';
  const extensions = extensionText
    ? extensionText.split(',').map(part => part.trim()).filter(Boolean)
    : [];

  const otherExtensions = extensions.filter(extension => !toneOrder.includes(extension));
  const mergedExtensions = [...nineTones, ...otherExtensions];

  if (mergedExtensions.length === 0) return baseSymbol;
  return `${baseSymbol}(${mergedExtensions.join(', ')})`;
}

function getHexatonicParentLabels(set) {
  const pcs = new Set(set.pcs_transposed_to_0 || set.pcs || []);
  if (pcs.size === 0) return [];
  return HEXATONIC_PARENT_LABELS.filter(collection => {
    for (const pc of pcs) {
      if (!collection.pcs.includes(pc)) return false;
    }
    return true;
  }).map(collection => collection.name);
}

function getPentatonicReferenceLabels(set) {
  const refs = (set.pentatonic_reference || []).filter(ref => !(ref.includes('Major Pentatonic') && ref.includes('alteration')));
  return [...new Set([...refs, ...getHexatonicParentLabels(set)])];
}

function voicingMatches(v, q) {
  if (fieldContains(v.bass_name, q)) return true;
  if (fieldContains(v.inversion, q)) return true;
  if (fieldContains(join(v.chord_tones), q)) return true;
  if (fieldContains(v.chord_symbol, q)) return true;
  if (fieldContains(join(getVoicingSearchCollections(v)), q)) return true;
  return false;
}

function matchesFilter(s, q) {
  if (!q) return true;
  q = q.toLowerCase();
  if (fieldContains(join(s.names_transposed_to_C), q)) return true;
  if (fieldContains(join(s.pcs_transposed_to_0), q)) return true;
  if (fieldContains(join(s.prime_form), q)) return true;
  if (fieldContains((s.prime_form || []).join(''), q)) return true;
  if (fieldContains(s.forte, q)) return true;
  if (fieldContains(s.yamaguchi_set, q)) return true;
  if (fieldContains(s.interval_structure, q)) return true;
  if (fieldContains(intervalVectorString(s), q)) return true;
  if (fieldContains(join(s.pentatonic_reference), q)) return true;
  if ((s.voicings || []).some(v => voicingMatches(v, q))) return true;
  return false;
}

function getAlterationCount(set) {
  const refs = set.pentatonic_reference || [];
  for (const ref of refs) {
    const match = ref.match(/(\d+)\s+alteration/);
    if (match) return Number(match[1]);
  }
  return 0;
}

function getIntervalVector(set) {
  const pcs = set.pcs_transposed_to_0 || set.pcs || set.prime_form || [];
  const counts = [0, 0, 0, 0, 0, 0];
  for (let i = 0; i < pcs.length; i++) {
    for (let j = i + 1; j < pcs.length; j++) {
      let diff = Math.abs(pcs[j] - pcs[i]);
      diff = Math.min(diff, 12 - diff);
      if (diff >= 1 && diff <= 6) counts[diff - 1] += 1;
    }
  }
  return counts;
}

function intervalVectorString(set) {
  return `<${getIntervalVector(set).join('')}>`;
}

function sortSets(arr, sortState) {
  if (sortState.key === 'index') return arr;
  const sorted = arr.slice();
  sorted.sort((a, b) => {
    const key = sortState.key;
    let aValue = '';
    let bValue = '';

    switch (key) {
      case 'names_transposed_to_C':
        aValue = join(a.names_transposed_to_C);
        bValue = join(b.names_transposed_to_C);
        break;
      case 'pcs_transposed_to_0':
        aValue = join(a.pcs_transposed_to_0);
        bValue = join(b.pcs_transposed_to_0);
        break;
      case 'prime_form':
        aValue = join(a.prime_form);
        bValue = join(b.prime_form);
        break;
      case 'forte':
        aValue = a.forte || '';
        bValue = b.forte || '';
        break;
      case 'yamaguchi_set':
        aValue = a.yamaguchi_set || '';
        bValue = b.yamaguchi_set || '';
        break;
      case 'interval_structure':
        aValue = a.interval_structure || '';
        bValue = b.interval_structure || '';
        break;
      case 'interval_vector':
        aValue = intervalVectorString(a);
        bValue = intervalVectorString(b);
        break;
      case 'pentatonic_reference':
        aValue = join(a.pentatonic_reference);
        bValue = join(b.pentatonic_reference);
        break;
      case 'alteration_count':
        return sortState.direction === 'asc'
          ? getAlterationCount(a) - getAlterationCount(b)
          : getAlterationCount(b) - getAlterationCount(a);
      default:
        aValue = '';
        bValue = '';
    }

    if (aValue < bValue) return sortState.direction === 'asc' ? -1 : 1;
    if (aValue > bValue) return sortState.direction === 'asc' ? 1 : -1;
    return 0;
  });
  return sorted;
}

function getFilteredVoicings(voicings, query) {
  if (!voicings || voicings.length === 0) return [];
  if (!query) return voicings;

  const normalizedQuery = query.trim().toLowerCase();
  if (!normalizedQuery) return voicings;
  return voicings.filter(v => voicingMatches(v, normalizedQuery));
}

function renderVoicingsTable(voicings, query) {
  const filteredVoicings = getFilteredVoicings(voicings, query);
  if (!voicings || voicings.length === 0) return '<div class="no-voicings">No voicings computed</div>';
  if (filteredVoicings.length === 0) return '<div class="no-voicings">No matching superimpositions</div>';
  let rows = filteredVoicings.map(v => {
    const bassName = v.bass_name || v.bass_note;
    const scaleDegree = v.inversion || '—';
    const collections = getVoicingCollections(v).join(', ');
    return `<tr><td>${bassName}</td><td>${scaleDegree}</td><td>${join(v.chord_tones)}</td><td>${getDisplayedChordSymbol(v)}</td><td>${collections || '—'}</td></tr>`;
  }).join('\n');
  return `<table class="voicings-table"><thead><tr><th>Bass</th><th>Scale Degree</th><th>Tones</th><th>Symbol</th><th>Collections</th></tr></thead><tbody>${rows}</tbody></table>`;
}

function renderSortIndicators() {
  document.querySelectorAll('#sets-table th.sortable').forEach(th => {
    th.classList.remove('sorted-asc', 'sorted-desc');
    if (th.dataset.sortKey === sortState.key) {
      th.classList.add(sortState.direction === 'asc' ? 'sorted-asc' : 'sorted-desc');
    }
  });
}

function render() {
  const normalizedQuery = appliedSearchQuery.trim().toLowerCase();
  const perPageValue = document.getElementById('per-page').value;

  let filtered = sets.filter(s => matchesModeGroup(s, selectedModeGroup) && matchesFilter(s, normalizedQuery));
  filtered = sortSets(filtered, sortState);

  const total = filtered.length;
  const perPage = perPageValue === 'all' ? (total || 1) : parseInt(perPageValue, 10);
  const pages = Math.max(1, Math.ceil(total / perPage));
  if (page > pages) page = pages;
  const start = (page - 1) * perPage;
  const pageItems = filtered.slice(start, start + perPage);

  const tbody = document.getElementById('table-body');
  tbody.innerHTML = '';
  if (pageItems.length === 0) {
    const tr = document.createElement('tr');
    const td = document.createElement('td');
    td.setAttribute('colspan', '10');
    td.className = 'no-results';
    td.textContent = 'No results found. Try a different search or clear the filter.';
    tr.appendChild(td);
    tbody.appendChild(tr);
  }
  pageItems.forEach((s, idx) => {
    const tr = document.createElement('tr');

    const tdIndex = document.createElement('td'); tdIndex.textContent = start + idx + 1; tr.appendChild(tdIndex);
    const tdNames = document.createElement('td'); tdNames.textContent = join(s.names_transposed_to_C); tr.appendChild(tdNames);
    const tdPcs = document.createElement('td'); tdPcs.textContent = join(s.pcs_transposed_to_0); tr.appendChild(tdPcs);
    const tdPrime = document.createElement('td'); tdPrime.textContent = `(${(s.prime_form || []).join('')})`; tr.appendChild(tdPrime);
    const tdForte = document.createElement('td'); tdForte.textContent = s.forte || '—'; tr.appendChild(tdForte);
    const tdYamaguchi = document.createElement('td'); tdYamaguchi.textContent = s.yamaguchi_set || '—'; tr.appendChild(tdYamaguchi);
    const tdIntervals = document.createElement('td'); tdIntervals.textContent = s.interval_structure || '—'; tr.appendChild(tdIntervals);
    const tdIntervalVector = document.createElement('td'); tdIntervalVector.textContent = intervalVectorString(s); tr.appendChild(tdIntervalVector);
    
    // Extract alteration count and other pentatonic references
    const refs = getPentatonicReferenceLabels(s);
    const alterationCount = getAlterationCount(s);
    const tdPentatonic = document.createElement('td');
    tdPentatonic.textContent = refs.join(', ') || '—';
    tr.appendChild(tdPentatonic);
    
    const tdAlteration = document.createElement('td');
    tdAlteration.textContent = alterationCount || '—';
    tr.appendChild(tdAlteration);

    const tdVoicing = document.createElement('td');
    if (s.voicings && s.voicings.length > 0) {
      const btn = document.createElement('button'); btn.textContent = 'Show'; btn.className = 'voicing-toggle';
      const panel = document.createElement('div'); panel.className = 'voicings-panel'; panel.style.display = 'none';
      const hasSearchQuery = normalizedQuery.length > 0;
      panel.innerHTML = renderVoicingsTable(s.voicings, normalizedQuery);
      panel.style.display = hasSearchQuery ? 'block' : 'none';
      btn.textContent = hasSearchQuery ? 'Hide' : 'Show';
      btn.addEventListener('click', (e) => { e.stopPropagation(); if (panel.style.display === 'none') { panel.style.display = 'block'; btn.textContent = 'Hide'; } else { panel.style.display = 'none'; btn.textContent = 'Show'; } });
      tdVoicing.appendChild(btn);
      tdVoicing.appendChild(panel);
    } else {
      tdVoicing.textContent = '—';
      tdVoicing.className = 'no-voicings-cell';
    }
    tr.appendChild(tdVoicing);

    tbody.appendChild(tr);
  });

  document.getElementById('page-info').textContent = `Page ${page} / ${pages} — ${total} matches`;
  renderSortIndicators();
}

document.addEventListener('DOMContentLoaded', ()=>{
  if (!sets || sets.length===0) {
    if (typeof initialSets !== 'undefined' && initialSets.length > 0) {
      sets = initialSets;
      render();
    } else {
      fetch(`data/sets.json?v=${DATA_VERSION}`).then(r=>r.json()).then(data=>{ sets = data; render(); });
    }
  }
  const searchInput = document.getElementById('search');
  const searchButton = document.getElementById('search-submit');
  const modeGroupSelect = document.getElementById('mode-group');

  const applySearch = () => {
    appliedSearchQuery = searchInput ? searchInput.value.trim() : '';
    page = 1;
    render();
  };

  if (searchInput) {
    searchInput.addEventListener('keydown', event => {
      if (event.key === 'Enter') {
        event.preventDefault();
        applySearch();
      }
    });
  }

  if (searchButton) {
    searchButton.addEventListener('click', applySearch);
  }

  const clearBtn = document.getElementById('clear-search');
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      if (searchInput) {
        searchInput.value = '';
      }
      appliedSearchQuery = '';
      selectedModeGroup = 'all';
      if (modeGroupSelect) modeGroupSelect.value = 'all';
      page = 1;
      render();
    });
  }
  const revertBtn = document.getElementById('revert-order');
  if (revertBtn) {
    revertBtn.addEventListener('click', ()=>{ sortState = { key: 'index', direction: 'asc' }; page = 1; render(); });
  }
  const explodeBtn = document.getElementById('explode-all');
  if (explodeBtn) {
    explodeBtn.addEventListener('click', ()=>{
      document.querySelectorAll('.voicing-toggle').forEach(btn=>{
        const panel = btn.nextElementSibling;
        if (panel && panel.classList.contains('voicings-panel')) {
          panel.style.display = 'block';
          btn.textContent = 'Hide';
        }
      });
    });
  }
  if (modeGroupSelect) {
    modeGroupSelect.addEventListener('change', () => {
      selectedModeGroup = modeGroupSelect.value;
      page = 1;
      render();
    });
  }
  document.getElementById('per-page').addEventListener('change', ()=>{ page = 1; render(); });
  document.querySelectorAll('#sets-table th.sortable').forEach(th => {
    th.addEventListener('click', () => {
      const key = th.dataset.sortKey;
      if (!key) return;
      if (sortState.key === key) {
        sortState.direction = sortState.direction === 'asc' ? 'desc' : 'asc';
      } else {
        sortState.key = key;
        sortState.direction = 'asc';
      }
      page = 1;
      render();
    });
  });
  document.getElementById('prev').addEventListener('click', ()=>{ if(page>1){ page--; render(); }});
  document.getElementById('next').addEventListener('click', ()=>{ page++; render(); });
  render();
});
