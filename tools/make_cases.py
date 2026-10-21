import re, glob, json, sys
Q=0.275; money=lambda x: float(x.replace(',',''))
cases=[]
for f in sorted(glob.glob(sys.argv[1]+'/*.txt')):
    t=open(f,encoding='utf-8',errors='ignore').read(); who=re.sub(r'^[0-9a-f]+-','',f.split('/')[-1])[:-4]
    m=re.search(r'Age Last Birthday\s*:\s*(\d+)\s*\((\w)',t)
    if not m: continue
    sec=t[t.find('Proposal Information'):]; sec=sec[:sec.find('Class:')+300]
    pm=re.search(r'(SUN Fit and Well Advantage (\d+)|Sun LifeAssure)\s*-\s*(Non-Smoker|Smoker)',sec)
    c=dict(who=who,age=int(m.group(1)),gender=m.group(2),smoker='NS' if pm.group(3)=='Non-Smoker' else 'S',plan=pm.group(2) or 'ASSURE',exp={})
    for l in sec.split('\n'):
        ps=re.findall(r'Ps\s+([\d,]+\.\d\d)(/ day)?',l)
        if not ps or ('Total' in l and 'Premium' in l and 'Disability' not in l) or 'Quarterly' in l or 'Semi' in l: continue
        lab=re.sub(r'Ps.*','',l).strip(); v=[money(p[0]) for p in ps]
        if len(v)==2 and (not lab or 'Guaranteed Premium' in lab or 'Fit and Well' in lab or 'LifeAssure' in lab): c['fa']=v[0]; c['exp']['base']=v[1]
        elif 'Dismemberment' in lab: c['exp']['addd']=v[1]
        elif 'Accidental Death Benefit' in lab: c['adbFa']=v[0]; c['exp']['adb']=v[1]
        elif 'Hospital Income' in lab: c['hibDay']=v[0]; c['exp']['hib']=v[1]
        elif 'Total Disability' in lab: c['exp']['tdb']=v[-1]
    if c['plan']=='ASSURE':
        blocks=[]
        for l in t[t.find('Premium Schedule'):].split('\n')[:30]:
            mm=re.match(r'\s*(\d+)\s*(?:-\s*\d+)?\s{2,}',l); nums=re.findall(r'[\d,]+\.\d\d',l)
            if mm and nums: blocks.append(round(money(nums[-1])/Q))
        c['blocks']=blocks
    cases.append(c)
print(json.dumps(cases))
