const data=window.AEGIS_DATA;
const q=document.querySelector('#q');
const domain=document.querySelector('#domain');
const cards=document.querySelector('#cards');
const status=document.querySelector('#result-status');
for (const d of [...new Set(data.injects.map(x=>x.domain))]) {
  const option=document.createElement('option'); option.value=d; option.textContent=d; domain.appendChild(option);
}
document.querySelector('#stats').textContent=`${data.summary.inject_count} injects · ${data.summary.csv_count} CSV datasets · ${data.summary.knowledge_count} knowledge documents`;
function tag(text){const s=document.createElement('span');s.className='tag';s.textContent=text;return s;}
function render(){
  const t=q.value.toLowerCase(); const d=domain.value;
  const rows=data.injects.filter(x=>(!d||x.domain===d)&&(!t||JSON.stringify(x).toLowerCase().includes(t)));
  cards.replaceChildren();
  for(const x of rows){
    const a=document.createElement('article');a.className='card';
    a.append(tag(x.id),tag(x.domain));
    const h=document.createElement('h3');h.textContent=x.title;a.appendChild(h);
    const p=document.createElement('p');p.textContent=x.description;a.appendChild(p);
    const e=document.createElement('div');e.className='evidence';e.textContent=x.evidence.join(' · ');a.appendChild(e);
    cards.appendChild(a);
  }
  if(!rows.length){const n=document.createElement('div');n.className='card';n.textContent='No matching evidence.';cards.appendChild(n);}
  status.textContent=`${rows.length} inject${rows.length===1?'':'s'} displayed`;
}
q.addEventListener('input',render);domain.addEventListener('change',render);render();
