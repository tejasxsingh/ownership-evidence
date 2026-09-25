export function normalize(s){return String(s).toLowerCase().match(/[a-z0-9]+/g)?.join(' ')||'';}
export function base(s){return normalize(s).split(' ').filter(t=>!['limited','ltd','inc','incorporated','corporation','corp','llc','plc','company','co'].includes(t)).join(' ');}
function distance(a,b){let p=Array.from({length:b.length+1},(_,i)=>i);for(let i=0;i<a.length;i++){let r=[i+1];for(let j=0;j<b.length;j++)r.push(Math.min(r[j]+1,p[j+1]+1,p[j]+(a[i]!==b[j])));p=r;}return p[b.length];}
function jaccard(a,b){return [...a].filter(x=>b.has(x)).length/Math.max(1,new Set([...a,...b]).size);}
export function features(a,b){a=base(a);b=base(b);let ca=a.replaceAll(' ',''),cb=b.replaceAll(' ','');const grams=s=>new Set(Array.from({length:Math.max(0,s.length-1)},(_,i)=>s.slice(i,i+2)));const nums=s=>new Set(s.match(/\d+/g)||[]);let na=nums(a),nb=nums(b);return [1-distance(ca,cb)/Math.max(1,ca.length,cb.length),jaccard(grams(ca),grams(cb)),jaccard(new Set(a.split(' ')),new Set(b.split(' '))),Number(ca===cb),Number(a.split(' ')[0]===b.split(' ')[0]),Number([...na].some(x=>!nb.has(x))||[...nb].some(x=>!na.has(x)))];}
export function score(a,b,model){let z=model.bias+features(a,b).reduce((s,v,i)=>s+v*model.weights[i],0);return 1/(1+Math.exp(-z));}
export function matchEntities(query,names,model){if(!query.trim())return [];return [...new Set(names)].map(name=>({name,score:score(query,name,model)})).sort((a,b)=>b.score-a.score).slice(0,4);}
export function extractText(text,parent,docId){
 const relations=[],warnings=[];const lines=text.split(/\r?\n/);let offset=0;
 for(const [lineIndex,line] of lines.entries()){const clean=line.trim();const m=clean.match(/^(.{2,180}?)\s+(?:owns|holds)\s+(\d+(?:\.\d+)?)%\s+(?:of\s+)?(.{2,180}?)\.?$/i);
  if(m){const pct=Number(m[2]);let owner=m[1].trim(),child=m[3].trim();if(pct>100||pct<=0)warnings.push('Ignored invalid ownership percentage: '+m[2]+'%.');else if(normalize(owner)===normalize(child))warnings.push('Ignored self-ownership statement.');else relations.push({owner,child,percent:pct,kind:'explicit_ownership',jurisdiction:'Not stated',docId,quote:clean,offset,line:lineIndex+1,status:'pending'});}
  else if(/subsidiar/i.test(text)&&clean.includes('|')){const cells=clean.split('|').map(x=>x.trim()).filter(Boolean);if(cells.length===2&&!/name|jurisdiction|incorporat/i.test(cells[0])&&cells[0].length<180)relations.push({owner:parent,child:cells[0],percent:null,kind:'disclosed_subsidiary',jurisdiction:cells[1],docId,quote:clean,offset,line:lineIndex+1,status:'pending'});}
  offset+=line.length+1;
 }
 return {relations,warnings};
}
export function conflicts(relations){const groups=new Map();for(const r of relations.filter(r=>r.status!=='rejected'&&r.percent!==null)){const k=normalize(r.owner)+'|'+normalize(r.child);if(!groups.has(k))groups.set(k,[]);groups.get(k).push(r);}return [...groups.values()].filter(rs=>new Set(rs.map(r=>r.percent)).size>1);}
export function ownershipPaths(relations,root,target){
 const active=relations.filter(r=>r.kind==='explicit_ownership'&&r.status!=='rejected');const blocked=new Set(conflicts(active).flat().map(r=>r.id));const paths=[];
 function walk(node,path,pct,seen){if(path.length>8)return;if(normalize(node)===normalize(target)&&path.length){paths.push({path,percent:pct});return;}for(const r of active){if(normalize(r.owner)!==normalize(node)||blocked.has(r.id)||seen.has(normalize(r.child)))continue;walk(r.child,[...path,r],pct*r.percent/100,new Set([...seen,normalize(r.child)]));}}
 walk(root,[],100,new Set([normalize(root)]));return paths;
}
export function escapeHtml(x){return String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
