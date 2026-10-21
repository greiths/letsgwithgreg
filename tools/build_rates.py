"""Build premium rate tables from Sun Life proposal text files (pdftotext -layout)."""
import re, glob, json, sys
Q = 0.275
BAND_1M = 0.40          # LifeAssure: rate is 0.40/1000 lower when FA >= 1,000,000
rates = {}             # plan -> comp -> key -> age -> rate
src = {}
conflicts = []
def put(plan, comp, key, age, v, who):
    v = round(v, 4)
    d = rates.setdefault(plan, {}).setdefault(comp, {}).setdefault(key, {})
    if age in d and abs(d[age] - v) > 0.006:
        conflicts.append(f"{plan} {comp} {key} age {age}: {d[age]} ({src[(plan,comp,key,age)]}) vs {v} ({who})")
        return
    d[age] = v; src[(plan, comp, key, age)] = who
def money(x): return float(x.replace(',', ''))

for f in sorted(glob.glob(sys.argv[1] + '/*.txt')):
    t = open(f, encoding='utf-8', errors='ignore').read()
    who = re.sub(r'^[0-9a-f]+-', '', f.split('/')[-1])[:-4]
    m = re.search(r'Age Last Birthday\s*:\s*(\d+)\s*\((\w)', t)
    if not m: continue
    age, g = int(m.group(1)), m.group(2)
    sec = t[t.find('Proposal Information'):]; sec = sec[:sec.find('Class:') + 300]
    pm = re.search(r'(SUN Fit and Well Advantage (\d+)|Sun LifeAssure)\s*-\s*(Non-Smoker|Smoker)', sec)
    plan = 'SFWA' + pm.group(2) if pm.group(2) else 'ASSURE'
    key = g + '-' + ('NS' if pm.group(3) == 'Non-Smoker' else 'S')
    cls = key[2:]
    fa = None
    for l in sec.split('\n'):
        ps = re.findall(r'Ps\s+([\d,]+\.\d\d)(/ day)?', l)
        if not ps or 'Total' in l and 'Premium' in l and 'Disability' not in l or 'Quarterly' in l or 'Semi' in l: continue
        lab = re.sub(r'Ps.*', '', l).strip()
        vals = [money(p[0]) for p in ps]
        if len(vals) == 2 and (not lab or 'Guaranteed Premium' in lab or 'Fit and Well' in lab or 'LifeAssure' in lab):
            fa = vals[0]
            if plan != 'ASSURE': put(plan, 'base', key, age, vals[1] / fa * 1000, who)
            continue
        if 'Dismemberment' in lab and plan != 'ASSURE': put(plan, 'addd', key, age, vals[1] / vals[0] * 1000, who)
        elif 'Hospital Income' in lab: put('HIB', 'hib', key, age, vals[1] / vals[0], who)
        elif 'Total Disability' in lab and plan != 'ASSURE': put(plan, 'tdb', key, age, vals[-1] / fa * 1000, who)
    if plan == 'ASSURE':
        s = t[t.find('Premium Schedule'):]
        lines = s.split('\n')[:30]
        cols = {}
        for l in lines[:8]:
            for name, lab in (('base', 'Basic Premium'), ('tdb', 'Total Disability'), ('adb', 'Accidental'), ('tot', 'Total Premium')):
                i = l.find(lab)
                if i >= 0: cols[name] = i + len(lab) / 2
        for l in lines:
            mm = re.match(r'\s*(\d+)\s*(?:-\s*\d+)?\s{2,}', l)
            nums = [(x.end(), money(x.group())) for x in re.finditer(r'[\d,]+\.\d\d', l)]
            if not mm or not nums: continue
            a = age + int(mm.group(1)) - 1
            for end, v in nums:
                # numbers are right-aligned under their header; match on nearest header centre
                c = min(cols, key=lambda k: abs(cols[k] - (end - 4)))
                if c == 'tot': continue
                r = round(v / Q) / fa * 1000
                if c == 'base':
                    put('ASSURE', 'base', key, a, r + (BAND_1M if fa >= 1000000 else 0), who)
                else:
                    rfa = fa
                    if c == 'adb':
                        mm2 = re.search(r'Accidental Death Benefit\s+Ps\s+([\d,]+\.\d\d)', sec); rfa = money(mm2.group(1))
                    for gg in 'FM': put('ASSURE', c, gg + '-' + cls, a, round(v / Q) / rfa * 1000, who)
print(json.dumps({p: {c: {k: dict(sorted(v.items())) for k, v in cs.items()} for c, cs in d.items()} for p, d in rates.items()}))
for c in conflicts: print('CONFLICT', c, file=sys.stderr)
