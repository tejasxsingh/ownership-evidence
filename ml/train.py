"""Train/export a small name-variant ranker; no identity-verification claim."""
from pathlib import Path
import re,json,random,hashlib
import numpy as np
from sklearn.linear_model import LogisticRegression
ROOT=Path(__file__).resolve().parents[1]

def norm(s):
 return ' '.join(re.findall(r'[a-z0-9]+',s.lower()))
def base(s):return ' '.join(t for t in norm(s).split() if t not in {'limited','ltd','inc','incorporated','corporation','corp','llc','plc','company','co'})
def lev(a,b):
 prev=list(range(len(b)+1))
 for i,x in enumerate(a):
  row=[i+1]
  for j,y in enumerate(b):row.append(min(row[-1]+1,prev[j+1]+1,prev[j]+(x!=y)))
  prev=row
 return prev[-1]
def feats(a,b):
 a,b=base(a),base(b);ta,tb=set(a.split()),set(b.split());ca,cb=a.replace(' ',''),b.replace(' ','')
 ga={ca[i:i+2] for i in range(max(0,len(ca)-1))};gb={cb[i:i+2] for i in range(max(0,len(cb)-1))}
 return [1-lev(ca,cb)/max(1,len(ca),len(cb)),len(ga&gb)/max(1,len(ga|gb)),len(ta&tb)/max(1,len(ta|tb)),float(ca==cb),float(a.split()[:1]==b.split()[:1]),float(bool(set(re.findall(r'\d+',a))^set(re.findall(r'\d+',b))))]

def main():
 r=random.Random(81);train=[];val=[]
 stems=['Cedar','Harbor','Willow','Aster','Orion','Lumen','Rivet','Mosaic','Juniper','Sequoia'];sectors=['Payments','Analytics','Research','Trading','Capital','Systems','Ventures']
 for i in range(600):
  stem=stems[i%10]+str(i);sector=sectors[i%7];name=f'{stem} {sector} Limited'
  typo=stem[:2]+stem[3:] if len(stem)>3 else stem
  rows=[(name,name,1),(f'{stem} {sector} Ltd',name,1),(f'{stem.upper()} {sector.upper()} INC.',name,1),(f'{typo} {sector} Ltd',name,1),(f'{stem[:3]} {stem[3:]} {sector}',name,1),(f'{stem} {sectors[(i+1)%7]} Limited',name,0),(f'{stems[(i+3)%10]}{i+7} {sector} Limited',name,0),(f'{stem} {sector} International Limited',name,0)]
  (val if i%5==0 else train).extend(rows)
 x=np.array([feats(a,b) for a,b,y in train]);y=np.array([y for a,b,y in train]);m=LogisticRegression(C=4,max_iter=800).fit(x,y)
 ps=m.predict_proba([feats(a,b) for a,b,y in val])[:,1];ys=np.array([y for a,b,y in val]);options=[]
 for t in np.arange(.5,.991,.01):
  selected=ps>=t
  if selected.sum() and ys[selected].mean()>=.98:options.append((int(selected.sum()),float(t)))
 threshold=max(options)[1] if options else .99
 exported={'features':['edit_similarity','bigram_jaccard','token_jaccard','normalized_exact','first_token_equal','numeric_conflict'],'weights':m.coef_[0].tolist(),'bias':float(m.intercept_[0]),'threshold':threshold,'version':'name-ranker-1'}
 (ROOT/'dist/model.json').write_text(json.dumps(exported,indent=2))
 selected=ps>=threshold
 card={'model':'Logistic regression over six lexical comparison features','training_pairs':len(train),'validation_pairs':len(val),'split':'Disjoint generated base names, 80/20; name patterns repeat across partitions.','threshold':threshold,'validation_precision':float(ys[selected].mean()) if selected.any() else None,'validation_selected':int(selected.sum()),'training_seed':81,'limitations':['Synthetic name-pair labels; validation is not real identity accuracy.','Ranks spelling variants; cannot resolve aliases, establish legal identity or certify ownership.','Scores are not calibrated real-world probabilities.','A high-scoring candidate still requires analyst review and source evidence.','No neural or LLM document extraction; supported extraction patterns are explicit and deterministic.'],'reproduce':'Run ml/train.py using scikit-learn and numpy.'}
 (ROOT/'dist/model-card.json').write_text(json.dumps(card,indent=2));print(card)
if __name__=='__main__':main()
