function join(arr) { return (arr || []).join(', '); }

let sets = window.initialSets || [];
let page = 1;
let sortState = { key: 'index', direction: 'asc' };

function fieldContains(field, q) {
  return field && field.toString().toLowerCase().includes(q);
}

function voicingMatches(v, q) {
  if (fieldContains(v.bass_name, q)) return true;
  if (fieldContains(v.inversion, q)) return true;
  if (fieldContains(join(v.chord_tones), q)) return true;
  if (fieldContains(v.chord_symbol, q)) return true;
  if (fieldContains(join(v.superset_collections), q)) return true;
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

function renderVoicingsTable(voicings) {
  if (!voicings || voicings.length === 0) return '<div class="no-voicings">No voicings computed</div>';
  let rows = voicings.map(v => {
    const bassName = v.bass_name || v.bass_note;
    const scaleDegree = v.inversion || '—';
    const collections = (v.superset_collections || []).join(', ');
    return `<tr><td>${bassName}</td><td>${scaleDegree}</td><td>${join(v.chord_tones)}</td><td>${v.chord_symbol || ''}</td><td>${collections || '—'}</td></tr>`;
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
  const q = document.getElementById('search').value.trim();
  const perPageValue = document.getElementById('per-page').value;

  let filtered = sets.filter(s => matchesFilter(s, q));
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
    const refs = s.pentatonic_reference || [];
    let alterationCount = '';
    const otherRefs = refs.filter(ref => {
      if (ref.includes('Major Pentatonic') && ref.includes('alteration')) {
        const match = ref.match(/(\d+)\s+alteration/);
        if (match) {
          alterationCount = match[1];
          return false;
        }
      }
      return true;
    });
    
    const tdPentatonic = document.createElement('td');
    tdPentatonic.textContent = otherRefs.join(', ') || '—';
    tr.appendChild(tdPentatonic);
    
    const tdAlteration = document.createElement('td');
    tdAlteration.textContent = alterationCount || '—';
    tr.appendChild(tdAlteration);

    const tdVoicing = document.createElement('td');
    if (s.voicings && s.voicings.length > 0) {
      const btn = document.createElement('button'); btn.textContent = 'Show'; btn.className = 'voicing-toggle';
      const panel = document.createElement('div'); panel.className = 'voicings-panel'; panel.style.display = 'none';
      panel.innerHTML = renderVoicingsTable(s.voicings);
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
      fetch('data/sets.json').then(r=>r.json()).then(data=>{ sets = data; render(); });
    }
  }
  document.getElementById('search').addEventListener('input', ()=>{ page = 1; render(); });
  const clearBtn = document.getElementById('clear-search');
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      const searchInput = document.getElementById('search');
      if (searchInput) {
        searchInput.value = '';
        page = 1;
        render();
      }
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
