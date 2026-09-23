from pathlib import Path

APP = Path('/app/static/app.js') if Path('/app/static/app.js').exists() else Path('static/app.js')
CSS = Path('/app/static/styles.css') if Path('/app/static/styles.css').exists() else Path('static/styles.css')

s = APP.read_text()

old_nav = """const nav=[['command','Command Centre'],['decision','Decision Centre'],['accounts','ICP & Accounts'],['relationships','Buying Committee'],['conversations','Conversations'],['meetings','Meetings'],['signals','Content Intelligence'],['evidence','Evidence Library'],['content','Content Engine'],['approvals','Approvals'],['schedule','Schedule'],['engagement','Engagement Queue'],['intent','Intent & Identity'],['pipeline','Demand & Pipeline'],['attribution','Revenue Attribution'],['performance','Performance'],['experiments','Experiments & Learning'],['activity','Activity & Automation'],['playbooks','Playbooks']];
function shell(content){const ws=state.me?.workspace;const user=state.me?.user;return `<div class=\"app-shell\">\n<aside class=\"sidebar\"><div class=\"brand\" data-route=\"command\">EPILO<small>AUTHORITY & DEMAND OS · v0.6</small></div><div class=\"nav\"><h5>Operate</h5>${nav.map(([r,l])=>`<a data-route=\"${r}\" class=\"${state.route===r?'active':''}\"><span class=\"dot\"></span>${l}</a>`).join('')}<h5>System</h5><a data-route=\"integrations\" class=\"${state.route==='integrations'?'active':''}\"><span class=\"dot\"></span>Integrations</a><a data-route=\"settings\" class=\"${state.route==='settings'?'active':''}\"><span class=\"dot\"></span>Settings</a></div><div class=\"sidefoot\"><b>${esc(ws?.name||'EPILO MEDIA')}</b><br>${esc(user?.email||'')}<br>Role: ${esc(ws?.role||'')}<br><button class=\"btn small\" style=\"margin-top:10px;width:100%\" data-action=\"logout\">Sign out</button></div></aside>\n<div><div class=\"mobile-top\"><div class=\"brand\">EPILO</div><button id=\"mobileMenu\" class=\"iconbtn\">☰</button></div><main class=\"main\">${content}</main></div></div>`}
"""

new_nav = """const navGroups=[
  {id:'today',label:'Today',icon:'◉',landing:'command',items:[['command','Overview'],['decision','Decisions']]},
  {id:'accounts',label:'Accounts',icon:'◎',landing:'accounts',items:[['accounts','Accounts'],['relationships','Buying Committee'],['conversations','Conversations'],['meetings','Meetings'],['evidence','Evidence'],['intent','Intent']]},
  {id:'content',label:'Content',icon:'◇',landing:'signals',items:[['signals','Intelligence'],['content','Production'],['approvals','Approvals'],['schedule','Schedule']]},
  {id:'revenue',label:'Revenue',icon:'↗',landing:'engagement',items:[['engagement','Engagement'],['pipeline','Pipeline'],['attribution','Attribution']]},
  {id:'learn',label:'Learn',icon:'△',landing:'performance',items:[['performance','Performance'],['experiments','Experiments']]},
  {id:'system',label:'System',icon:'⚙',landing:'activity',items:[['activity','Automation'],['playbooks','Playbooks'],['integrations','Integrations'],['settings','Settings']]}
];
const nav=navGroups.flatMap(g=>g.items);
const activeNavGroup=()=>navGroups.find(g=>g.items.some(([r])=>r===state.route))||navGroups[0];
function navMarkup(){const active=activeNavGroup();return navGroups.map(g=>{const open=g.id===active.id;return `<div class=\"nav-group ${open?'open':''}\"><button class=\"nav-group-head ${open?'active':''}\" data-group-route=\"${g.landing}\"><span class=\"nav-icon\">${g.icon}</span><span>${g.label}</span><span class=\"nav-chevron\">${open?'⌄':'›'}</span></button>${open?`<div class=\"nav-children\">${g.items.map(([r,l])=>`<a data-route=\"${r}\" class=\"${state.route===r?'active':''}\">${l}</a>`).join('')}</div>`:''}</div>`}).join('')}
function shell(content){const ws=state.me?.workspace;const user=state.me?.user;return `<div class=\"app-shell\">\n<aside class=\"sidebar\"><div class=\"brand\" data-route=\"command\">EPILO<small>AUTHORITY & DEMAND OS · v0.6</small></div><div class=\"nav\">${navMarkup()}</div><div class=\"sidefoot\"><b>${esc(ws?.name||'EPILO MEDIA')}</b><br>${esc(user?.email||'')}<br>Role: ${esc(ws?.role||'')}<br><button class=\"btn small\" style=\"margin-top:10px;width:100%\" data-action=\"logout\">Sign out</button></div></aside>\n<div><div class=\"mobile-top\"><div class=\"brand\">EPILO</div><button id=\"mobileMenu\" class=\"iconbtn\">☰</button></div><main class=\"main\">${content}</main></div></div>`}
"""

if old_nav not in s:
    raise RuntimeError('Expected legacy navigation block not found')
s = s.replace(old_nav, new_nav)

old_setup = """function setupNav(){qsa('[data-route]').forEach(a=>a.onclick=()=>go(a.dataset.route));const m=qs('#mobileMenu');if(m)m.onclick=()=>{const old=qs('.mobile-nav');if(old){old.remove();return}const div=document.createElement('div');div.className='mobile-nav';div.innerHTML=nav.map(([r,l])=>`<a data-mobile-route=\"${r}\">${l}</a>`).join('')+`<a data-mobile-route=\"integrations\">Integrations</a><a data-mobile-route=\"settings\">Settings</a>`;document.body.appendChild(div);qsa('[data-mobile-route]',div).forEach(a=>a.onclick=()=>{div.remove();go(a.dataset.mobileRoute)})}};"""
new_setup = """function setupNav(){qsa('[data-route]').forEach(a=>a.onclick=()=>go(a.dataset.route));qsa('[data-group-route]').forEach(a=>a.onclick=()=>go(a.dataset.groupRoute));const m=qs('#mobileMenu');if(m)m.onclick=()=>{const old=qs('.mobile-nav');if(old){old.remove();return}const div=document.createElement('div');div.className='mobile-nav';div.innerHTML=navGroups.map(g=>`<div class=\"mobile-nav-group\"><div class=\"mobile-nav-title\">${g.label}</div>${g.items.map(([r,l])=>`<a data-mobile-route=\"${r}\" class=\"${state.route===r?'active':''}\">${l}</a>`).join('')}</div>`).join('');document.body.appendChild(div);qsa('[data-mobile-route]',div).forEach(a=>a.onclick=()=>{div.remove();go(a.dataset.mobileRoute)})}};"""
if old_setup not in s:
    raise RuntimeError('Expected legacy setupNav block not found')
s = s.replace(old_setup, new_setup)

for old, new in {
    "top('Command Centre'": "top('Overview'",
    "top('Decision Centre'": "top('Decisions'",
    "top('ICP & Accounts'": "top('Accounts'",
    "top('Content Intelligence'": "top('Intelligence'",
    "top('Content Engine'": "top('Production'",
    "top('Engagement Queue'": "top('Engagement'",
    "top('Demand & Pipeline'": "top('Pipeline'",
    "top('Revenue Attribution'": "top('Attribution'",
    "top('Experiments & Learning'": "top('Experiments'",
    "top('Activity & Automation'": "top('Automation'",
    "top('Intent & Identity'": "top('Intent'",
    "top('Evidence Library'": "top('Evidence'",
}.items():
    s = s.replace(old, new)
APP.write_text(s)

c = CSS.read_text()
old_css = """*{box-sizing:border-box}html,body{margin:0;min-height:100%;background:var(--paper);color:var(--ink);font-family:Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,\"Segoe UI\",sans-serif}button,input,textarea,select{font:inherit;color:inherit}.app-shell{display:grid;grid-template-columns:252px minmax(0,1fr);min-height:100vh}.sidebar{background:#1a1a17;color:#f7f3eb;padding:28px 20px;display:flex;flex-direction:column;gap:26px;position:sticky;top:0;height:100vh}.brand{font-family:Georgia,serif;font-size:24px;letter-spacing:.12em;cursor:pointer}.brand small{display:block;font-family:inherit;font-size:9px;letter-spacing:.18em;color:#bdb8ae;margin-top:6px}.nav h5{font-size:9px;letter-spacing:.18em;color:#8f8a80;margin:19px 10px 8px;text-transform:uppercase}.nav a{display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:9px;color:#d9d3ca;text-decoration:none;font-size:12px;margin-bottom:4px;cursor:pointer}.nav a:hover{background:#25241f}.nav a.active{background:#302f2a;color:#fff}.dot{width:7px;height:7px;border-radius:50%;background:#82765e;flex:none}.active .dot{background:#b69a64}.sidefoot{margin-top:auto;border-top:1px solid #37352f;padding-top:15px;font-size:10px;color:#aaa398;line-height:1.65}.mobile-top{display:none}.main{padding:36px 40px 64px;min-width:0}"""
new_css = """*{box-sizing:border-box}html,body{margin:0;min-height:100%;background:var(--paper);color:var(--ink);font-family:Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,\"Segoe UI\",sans-serif}button,input,textarea,select{font:inherit;color:inherit}.app-shell{display:grid;grid-template-columns:220px minmax(0,1fr);min-height:100vh}.sidebar{background:#1a1a17;color:#f7f3eb;padding:24px 14px 18px;display:flex;flex-direction:column;gap:20px;position:sticky;top:0;height:100vh}.brand{font-family:Georgia,serif;font-size:22px;letter-spacing:.12em;cursor:pointer;padding:0 8px}.brand small{display:block;font-family:inherit;font-size:8px;letter-spacing:.15em;color:#8f8a80;margin-top:6px;line-height:1.45}.nav{display:flex;flex-direction:column;gap:3px}.nav-group{border-radius:10px}.nav-group-head{width:100%;border:0;background:transparent;color:#b9b3aa;display:grid;grid-template-columns:18px 1fr 16px;gap:8px;align-items:center;text-align:left;padding:9px 10px;border-radius:9px;font-size:11px;font-weight:650;cursor:pointer}.nav-group-head:hover{background:#24231f;color:#f6f1e8}.nav-group-head.active{color:#fff;background:#23221e}.nav-icon{font-size:11px;color:#91836d;text-align:center}.nav-chevron{font-size:14px;color:#777168;text-align:right}.nav-children{padding:3px 0 5px 28px}.nav-children a{display:flex;align-items:center;min-height:29px;padding:6px 9px;border-radius:7px;color:#9e9890;text-decoration:none;font-size:10.5px;margin:1px 0;cursor:pointer;position:relative}.nav-children a:hover{color:#eee8de;background:#24231f}.nav-children a.active{color:#fff;background:#2c2b26}.nav-children a.active:before{content:\"\";position:absolute;left:-8px;top:9px;width:2px;height:12px;border-radius:2px;background:#b69a64}.sidefoot{margin-top:auto;border-top:1px solid #302f2a;padding:14px 8px 0;font-size:9px;color:#8f8a80;line-height:1.65}.mobile-top{display:none}.main{padding:34px 38px 64px;min-width:0}"""
if old_css not in c:
    raise RuntimeError('Expected legacy navigation CSS block not found')
c = c.replace(old_css, new_css)
c = c.replace(
    ".mobile-nav a{display:block;color:#ddd;text-decoration:none;padding:12px;border-bottom:1px solid #333}",
    ".mobile-nav-group{margin-bottom:18px}.mobile-nav-title{font-size:9px;letter-spacing:.16em;text-transform:uppercase;color:#8f8a80;padding:8px 12px}.mobile-nav a{display:block;color:#cfc9c0;text-decoration:none;padding:10px 12px;border-radius:8px;margin:2px 0;font-size:12px}.mobile-nav a.active{background:#302f2a;color:#fff}"
)
CSS.write_text(c)
