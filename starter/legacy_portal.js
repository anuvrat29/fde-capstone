// Deliberately unsafe brownfield browser code.
export function renderClaim(note, role) {
  // Defects: XSS, role supplied by client, no tenant/purpose check, no provenance.
  document.querySelector('#result').innerHTML = `<h3>${role}</h3><div>${note}</div>`;
}
export async function approveClaim(claimId) {
  // Defect: creates a side effect from an advisory UI without confirmation or idempotency.
  return fetch('/api/claims/'+claimId+'/approve',{method:'POST'});
}
