const { chromium } = require('playwright'); const fs=require('fs');
(async () => {
  const cases=JSON.parse(fs.readFileSync(process.argv[2])); const b=await chromium.launch(); const p=await b.newPage();
  const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.goto('file://'+process.argv[3]); let pass=0, fail=0;
  for (const c of cases){
    const isA=c.plan==='ASSURE';
    const st={age:c.age,gender:c.gender,smoker:c.smoker,aManual:false,bManual:false};
    if(isA) Object.assign(st,{bCov:c.fa,bAdb:'adb' in c.exp,bTdb:'tdb' in c.exp}); else Object.assign(st,{plan:c.plan,aCov:c.fa,addd:'addd' in c.exp,tdb:'tdb' in c.exp,aHib:c.hibDay||0});
    const r=await p.evaluate(s=>{policySim.set(s); return policySim.compute();},st);
    let got, exp, ok;
    if(isA){ got=r.B.sched.map(x=>x.p.total); exp=c.blocks; if(c.adbFa && c.adbFa!==c.fa){ got=got.slice(0,0); exp=[]; } }
    else { const k=r.A.brk||{}; got={base:k.base,tdb:k.tdb,hib:k.hib,addd:k.addd}; exp={base:c.exp.base,tdb:c.exp.tdb||0,hib:c.exp.hib||0,addd:c.exp.addd||0}; }
    ok=JSON.stringify(got)===JSON.stringify(exp);
    const est = isA ? (r.B.first&&r.B.first.est) : (r.A.brk&&r.A.brk.est);
    ok?pass++:fail++;
    if(!ok||est) console.log((ok?'ok  ':'FAIL'), c.who, isA?'':'SFWA'+c.plan, c.age+c.gender+'-'+c.smoker, est?'(est)':'', ok?'':JSON.stringify(got)+' vs '+JSON.stringify(exp));
  }
  console.log(`passed ${pass}/${pass+fail}`, errs); await b.close();
})();
