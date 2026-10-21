import json, re, sys
rates = json.load(open(sys.argv[1])); html = sys.argv[2]
s = open(html, encoding='utf-8').read()
hib = rates.pop('HIB')['hib']
J = lambda o: json.dumps(o, separators=(',', ':'))
plans = ''.join(f'    {p}: {J(rates.get(p, {}))[:-1] + ("," if rates.get(p) else "")}"hib":HIB_RATES}},\n' for p in ('SFWA10', 'SFWA15', 'SFWA20'))
block = f'  var HIB_RATES = {J(hib)};\n  var RATES = {{\n{plans}    ASSURE: {J(rates["ASSURE"])}\n  }};\n'
s, n = re.subn(r'  var HIB_RATES = .*?\n  \};\n', lambda m: block, s, count=1, flags=re.S)
assert n == 1
open(html, 'w', encoding='utf-8').write(s)
print('injected')
