# -*- coding: utf-8 -*-
"""
자동차세 신호등 정적 사이트 빌더

사용법:  python3 _build.py
결과:    ./docs/ 아래에 사이트 전체가 생성됩니다.

밑줄(_)로 시작하는 파일은 원고·데이터·빌더입니다. 지우지 마세요.
"""
import json
import os
import re
import shutil
from datetime import date

import _config as C
import _rates as R
import _cars as CARS
import _posts as P

OUT = "docs"
TODAY = date.today().isoformat()
ROOT = C.SITE_URL.rstrip("/")

# ─────────────────────────────────────────────────────────────
# 공통 템플릿
# ─────────────────────────────────────────────────────────────
CSS = """
:root{
  --bg:#f3f8f7; --card:#ffffff; --ink:#1d2b2a; --muted:#5d7472;
  --line:#dbe9e7; --brand:#2f9e8f; --brand-soft:#e4f4f1; --brand-deep:#1f7a6e;
  --go:#3aa76d; --warn:#e8a33d; --stop:#e05c5c;
  --radius:18px; --shadow:0 2px 14px rgba(31,122,110,.07);
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Pretendard","Noto Sans KR",sans-serif;
  line-height:1.75;font-size:16px;word-break:keep-all}
a{color:var(--brand-deep);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:820px;margin:0 auto;padding:0 16px}
header.site{background:var(--card);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:20}
header.site .wrap{display:flex;align-items:center;gap:14px;height:60px}
.logo{font-weight:800;font-size:18px;color:var(--ink);display:flex;align-items:center;gap:7px}
.logo .dots{display:inline-flex;gap:3px}
.logo .dots i{width:8px;height:8px;border-radius:50%;display:block}
.logo .dots i:nth-child(1){background:var(--go)}
.logo .dots i:nth-child(2){background:var(--warn)}
.logo .dots i:nth-child(3){background:var(--stop)}
nav.site{margin-left:auto;display:flex;gap:16px;font-size:14px}
nav.site a{color:var(--muted);font-weight:600}
main{padding:28px 0 56px}
h1{font-size:27px;line-height:1.35;margin:0 0 10px;letter-spacing:-.4px}
h2{font-size:20px;margin:34px 0 12px;letter-spacing:-.3px}
h3{font-size:17px;margin:24px 0 8px}
p{margin:0 0 14px}
.lead{color:var(--muted);font-size:16px;margin-bottom:22px}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
  padding:20px;box-shadow:var(--shadow);margin-bottom:16px}
.grid{display:grid;gap:12px}
@media(min-width:640px){.grid.two{grid-template-columns:1fr 1fr}}
.grid.specs{grid-template-columns:1fr 1fr;gap:10px 12px}
.grid.specs label{font-size:12px}
.grid.specs input,.grid.specs select{padding:10px;font-size:15px}
table{width:100%;border-collapse:collapse;margin:14px 0;font-size:15px;display:block;overflow-x:auto}
th,td{border-bottom:1px solid var(--line);padding:9px 10px;text-align:left;white-space:nowrap}
th{background:var(--brand-soft);font-weight:700;color:var(--brand-deep)}
td:first-child,th:first-child{white-space:normal}
.src{font-size:13px;color:var(--muted);margin-top:-6px}
.tip{background:var(--brand-soft);border-left:3px solid var(--brand);border-radius:0 10px 10px 0;
  padding:12px 14px;margin:16px 0;font-size:15px}
.cta{background:#fffaf0;border:1px solid #f2e2c4;border-radius:12px;padding:12px 14px;font-size:15px}
.btn{display:inline-block;background:var(--brand);color:#fff;border:0;border-radius:12px;
  padding:12px 20px;font-weight:700;font-size:15px;cursor:pointer;font-family:inherit}
.btn:hover{background:var(--brand-deep);text-decoration:none;color:#fff}
.btn.ghost{background:var(--card);color:var(--brand-deep);border:1px solid var(--line)}
footer.site{border-top:1px solid var(--line);background:var(--card);padding:26px 0;
  font-size:13px;color:var(--muted)}
footer.site a{color:var(--muted)}
footer.site .links{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:10px}
.badge{display:inline-block;background:var(--brand-soft);color:var(--brand-deep);
  border-radius:999px;padding:2px 10px;font-size:12px;font-weight:700;margin-right:5px}
ul,ol{padding-left:20px;margin:0 0 14px}
li{margin-bottom:5px}
.postlist{list-style:none;padding:0}
.postlist li{margin-bottom:12px}
.postlist a{font-weight:700;font-size:17px}
.postlist p{margin:2px 0 0;color:var(--muted);font-size:14px}
.disclaimer{font-size:13px;color:var(--muted);border-top:1px dashed var(--line);
  padding-top:14px;margin-top:26px}

/* 계산기 */
.tabs{display:flex;gap:6px;margin-bottom:16px}
.tabs button{flex:1;padding:11px;border:1px solid var(--line);background:var(--card);
  border-radius:12px;font-weight:700;font-size:15px;cursor:pointer;color:var(--muted);font-family:inherit}
.tabs button.on{background:var(--brand);color:#fff;border-color:var(--brand)}
label{display:block;font-size:13px;font-weight:700;color:var(--muted);margin-bottom:5px}
input,select{width:100%;padding:11px 12px;border:1px solid var(--line);border-radius:12px;
  font-size:16px;font-family:inherit;background:#fff;color:var(--ink)}
input:focus,select:focus{outline:2px solid var(--brand-soft);border-color:var(--brand)}
.field{margin-bottom:14px}
.results{position:relative}
.ac{position:absolute;left:0;right:0;top:100%;background:#fff;border:1px solid var(--line);
  border-radius:12px;box-shadow:var(--shadow);max-height:300px;overflow-y:auto;z-index:10;display:none}
.ac div{padding:10px 12px;cursor:pointer;font-size:15px;border-bottom:1px solid var(--line)}
.ac div:last-child{border-bottom:0}
.ac div:hover,.ac div.sel{background:var(--brand-soft)}
.ac small{color:var(--muted);margin-left:6px}
.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:8px}
.chips button{border:1px solid var(--line);background:#fff;border-radius:999px;padding:6px 13px;
  font-size:13px;cursor:pointer;font-family:inherit;color:var(--muted)}
.chips button.on{background:var(--brand);color:#fff;border-color:var(--brand)}
.out{background:var(--brand-soft);border-radius:14px;padding:16px;margin-top:6px}
.out .row{display:flex;justify-content:space-between;padding:6px 0;font-size:15px;
  border-bottom:1px dashed rgba(47,158,143,.25)}
.out .row:last-child{border-bottom:0}
.out .row.total{font-size:19px;font-weight:800;color:var(--brand-deep);
  border-top:2px solid var(--brand);border-bottom:0;margin-top:8px;padding-top:12px}
.out .row .neg{color:var(--go)}
.out h3{margin:0 0 8px;font-size:15px;color:var(--brand-deep)}
.mini{font-size:13px;color:var(--muted);margin-top:8px}
#allitems table{font-size:14px}
#allitems th,#allitems td{padding:7px 8px}
"""

ADS = ""
if C.ADSENSE_CLIENT:
    ADS = ('<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client='
           + C.ADSENSE_CLIENT + '" crossorigin="anonymous"></script>')


def page(title, desc, body, canonical, extra_head="", extra_js=""):
    full_title = title if title == C.SITE_NAME else f"{title} | {C.SITE_NAME}"
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{C.SITE_NAME}">
<meta name="robots" content="index,follow">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='8' fill='%232f9e8f'/><circle cx='16' cy='9' r='3.4' fill='%233aa76d'/><circle cx='16' cy='16' r='3.4' fill='%23e8a33d'/><circle cx='16' cy='23' r='3.4' fill='%23e05c5c'/></svg>">
<style>{CSS}</style>
{ADS}
{extra_head}
</head>
<body>
<header class="site"><div class="wrap">
  <a class="logo" href="{ROOT}/"><span class="dots"><i></i><i></i><i></i></span>{C.SITE_NAME}</a>
  <nav class="site">
    <a href="{ROOT}/tool.html">계산기</a>
    <a href="{ROOT}/guide.html">가이드</a>
    <a href="{ROOT}/about.html">소개</a>
  </nav>
</div></header>
<main><div class="wrap">
{body}
</div></main>
<footer class="site"><div class="wrap">
  <div class="links">
    <a href="{ROOT}/about.html">사이트 소개</a>
    <a href="{ROOT}/privacy.html">개인정보처리방침</a>
    <a href="{ROOT}/terms.html">이용약관</a>
    <a href="{ROOT}/contact.html">문의</a>
  </div>
  <div>© {date.today().year} {C.OPERATOR}. 이 사이트의 계산 결과는 참고용이며 법적 효력이 없습니다.
  실제 세액은 관할 지방자치단체와 위택스에서 확인하세요.</div>
</div></footer>
{extra_js}
</body>
</html>"""


def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full) or OUT, exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


# ─────────────────────────────────────────────────────────────
# 계산 로직 (파이썬 쪽 — 정적 페이지의 미리 계산된 값에 사용)
# ─────────────────────────────────────────────────────────────
def car_tax(cc, fuel, ages=(2, 2), commercial=False, kind="승용"):
    """연간 자동차세(교육세 포함) 계산.

    지방세법 제127조 제3항의 산식을 그대로 따릅니다.
        각 기분세액 = A/2 − (A/2 × 5/100) × (n − 2)
    기분(반기)마다 따로 계산하고 각각 10원 미만을 절사한 뒤 합산합니다.

    ages : (1기분 차령, 2기분 차령). R.car_age() 로 구합니다.
    반환 : (본세 합계, 교육세 합계, 총액, 경감률, 기분별 내역)

    승합·화물자동차는 배기량이 아니라 인승·적재량 기준 정액이며
    지방교육세도 붙지 않습니다. 연료(전기 포함)와도 무관합니다.
    """
    use = "영업용" if commercial else "비영업용"

    def flat(b):
        h = b // 2
        halves = [(h, 0), (b - h, 0)]
        return b, 0, b, 0.0, halves

    if kind == "승합":
        return flat(R.CAR_TAX_BUS_DEFAULT[use])
    if kind == "화물":
        return flat(R.CAR_TAX_TRUCK_DEFAULT[use])
    if fuel in ("전기", "수소") or cc == 0:
        b = R.CAR_TAX_FLAT_EV[use]
        h = b // 2
        halves = [(h, int(h * R.EDU_TAX_RATE) if not commercial else 0),
                  (b - h, int((b - h) * R.EDU_TAX_RATE) if not commercial else 0)]
        edu = sum(e for _, e in halves)
        return b, edu, b + edu, 0.0, halves

    rate = next(r for lim, r in R.CAR_TAX_CC[use] if cc <= lim)
    A = cc * rate                      # 연세액 (경감 전)
    halves, disc = [], 0.0
    for n in ages:
        d = R.age_discount(n) if not commercial else 0.0
        disc = max(disc, d)
        h = int(A / 2 * (1 - d) / 10) * 10          # 10원 미만 절사
        e = int(h * R.EDU_TAX_RATE / 10) * 10 if not commercial else 0
        halves.append((h, e))
    base = sum(h for h, _ in halves)
    edu = sum(e for _, e in halves)
    return base, edu, base + edu, disc, halves


def acq_tax(price_won, kind, fuel, commercial=False):
    """취득세 계산. price_won 은 VAT 포함 금액. 반환: (과세표준, 세액, 감면액, 감면명)"""
    basis = int(price_won / 1.1)
    use = "영업용" if commercial else "비영업용"
    key = "경차" if (kind == "경차" and fuel not in ("전기", "수소")) else \
          ("승용" if kind in ("승용", "경차") else kind)
    rate = R.ACQ_RATES.get(key, R.ACQ_RATES["승용"])[use]
    tax = int(basis * rate / 10) * 10  # 10원 미만 절사

    # 감면 — 중복감면 배제(지방세특례제한법 제180조): 가장 유리한 하나만
    cands = []
    if kind == "경차" and fuel not in ("전기", "수소"):
        cands.append(("경차", min(tax, R.EXEMPTIONS["경차"]["limit"])))
    if fuel in ("전기", "수소"):
        cands.append(("전기·수소차", min(tax, R.EXEMPTIONS["전기차"]["limit"])))
    if fuel == "하이브리드":
        cands.append(("하이브리드", min(tax, R.EXEMPTIONS["하이브리드"]["limit"])))
    if cands:
        name, amt = max(cands, key=lambda x: x[1])
    else:
        name, amt = "", 0
    return basis, tax, amt, name


def won(n):
    return f"{int(n):,}원"


# ─────────────────────────────────────────────────────────────
# 계산기용 JSON 데이터
# ─────────────────────────────────────────────────────────────
def build_data_json():
    models = []
    for maker, name, aliases, kind, origin, trims in CARS.CARS:
        models.append({
            "mk": maker, "nm": name, "al": aliases, "kd": kind, "og": origin,
            "sl": CARS.slug(maker, name),
            "tr": [{"n": t[0], "cc": t[1], "p": t[2] * 10000, "f": t[3]} for t in trims],
        })
    return {
        "models": models,
        "ccRate": R.CAR_TAX_CC,
        "evFlat": R.CAR_TAX_FLAT_EV,
        "busFlat": R.CAR_TAX_BUS_DEFAULT,
        "truckFlat": R.CAR_TAX_TRUCK_DEFAULT,
        "edu": R.EDU_TAX_RATE,
        "ageStep": R.AGE_STEP,
        "ageBase": R.AGE_BASE,
        "ageMax": R.AGE_MAX,
        "acq": {k: v for k, v in R.ACQ_RATES.items()},
        "exempt": {k: v["limit"] for k, v in R.EXEMPTIONS.items()},
        "bond": R.BOND_RATES,
        "bondDiscount": R.BOND_DISCOUNT,
        "bondUnit": R.BOND_ROUND_UNIT,
        "bondEvLimit": R.BOND_EV_LIMIT,
        "bondHevLimit": R.BOND_HEV_LIMIT,
        "prepay": R.PREPAY_RATE,
        "prepayWindows": [[w[0], w[1], R.prepay_days(w[2], date.today().year), w[3]]
                          for w in R.PREPAY_WINDOWS],
        "yearDays": R.days_in_year(date.today().year),
        "residual": R.RESIDUAL_PUBLISHED,
        "decay": R.RESIDUAL_DECAY,
        "fees": R.REG_FEES,
        "year": date.today().year,
    }


CALC_JS = r"""
const D = window.__DATA__;
const CHO = ["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"];
function initials(s){let o="";for(const ch of s){const c=ch.charCodeAt(0);
  if(c>=0xAC00&&c<=0xD7A3){o+=CHO[Math.floor((c-0xAC00)/588)];}else{o+=ch;}}return o.toLowerCase();}
function norm(s){return (s||"").toLowerCase().replace(/\s|-/g,"");}
function won(n){return Math.round(n).toLocaleString("ko-KR")+"원";}

/* ── 검색 ── */
const IDX = D.models.map(m=>({m, keys:[norm(m.mk+m.nm), norm(m.nm), ...m.al.map(norm),
  initials(m.nm.replace(/\s/g,"")), initials(m.mk+m.nm)]}));
function search(q){
  q = norm(q); if(!q) return [];
  const starts=[], has=[];
  for(const it of IDX){
    if(it.keys.some(k=>k.startsWith(q))) starts.push(it.m);
    else if(it.keys.some(k=>k.includes(q))) has.push(it.m);
  }
  return starts.concat(has).slice(0,40);
}

/* ── 세금 계산 ── */
function residual(age, origin){
  const t = D.residual[origin] || D.residual["국산"];
  if(t[age]!==undefined) return t[age];
  const last = Math.max(...Object.keys(t).map(Number));
  const r = t[last] * Math.pow(D.decay[origin]||0.8475, Math.min(age,20)-last);
  return Math.max(Math.round(r*10000)/10000, 0.05);
}
/* 차령 n : 최초등록일 기준. 1~6월 등록은 (과세연도-등록연도)+1, 7~12월은 1기분만 -1 */
function carAges(regYear, regMonth, taxYear){
  const d = taxYear - regYear;
  return regMonth <= 6 ? [d+1, d+1] : [d, d+1];
}
function ageDiscount(n){
  const steps = Math.min(Math.max(n - D.ageBase, 0), D.ageMax - D.ageBase);
  return Math.round(steps * D.ageStep * 100) / 100;
}
/* 각 기분세액 = A/2 − (A/2 × 5/100)(n−2), 기분마다 10원 미만 절사 */
function carTax(cc, fuel, ages, commercial, kind){
  const use = commercial ? "영업용" : "비영업용";
  const flat = b => {
    const h = Math.floor(b/2);
    return {base:b, edu:0, total:b, disc:0, halves:[[h,0],[b-h,0]]};
  };
  if(kind==="승합") return Object.assign(flat(D.busFlat[use]), {flatKind:"승합"});
  if(kind==="화물") return Object.assign(flat(D.truckFlat[use]), {flatKind:"화물"});
  if(fuel==="전기"||fuel==="수소"||!cc){
    const b = D.evFlat[use], h = Math.floor(b/2);
    const hv = [[h, commercial?0:Math.floor(h*D.edu)], [b-h, commercial?0:Math.floor((b-h)*D.edu)]];
    const edu = hv[0][1]+hv[1][1];
    return {base:b, edu, total:b+edu, disc:0, halves:hv, flatKind:"전기"};
  }
  const row = D.ccRate[use].find(r=>cc<=r[0]);
  const A = cc*row[1];
  let halves=[], disc=0;
  for(const n of ages){
    const d = commercial ? 0 : ageDiscount(n);
    if(d>disc) disc = d;
    const h = Math.floor(A/2*(1-d)/10)*10;
    const e = commercial ? 0 : Math.floor(h*D.edu/10)*10;
    halves.push([h,e]);
  }
  const base = halves[0][0]+halves[1][0], edu = halves[0][1]+halves[1][1];
  return {base, edu, total:base+edu, disc, halves};
}
function acqTax(price, kind, fuel, commercial, extra){
  const basis = Math.floor(price/1.1);
  const use = commercial ? "영업용" : "비영업용";
  const isLight = kind==="경차" && fuel!=="전기" && fuel!=="수소";
  const key = isLight ? "경차" : (kind==="경차" ? "승용" : (D.acq[kind] ? kind : "승용"));
  const rate = D.acq[key][use];
  const tax = Math.floor(basis*rate/10)*10;
  const cands = [];
  if(isLight) cands.push(["경차 면제", Math.min(tax, D.exempt["경차"])]);
  if(fuel==="전기"||fuel==="수소") cands.push(["전기·수소차 감면", Math.min(tax, D.exempt["전기차"])]);
  if(fuel==="하이브리드") cands.push(["하이브리드 감면", Math.min(tax, D.exempt["하이브리드"])]);
  if(extra==="다자녀"){
    const full = (kind==="승합"||kind==="화물") ? tax : Math.min(tax, D.exempt["다자녀"]);
    cands.push(["다자녀 감면", full]);
  }
  if(extra==="장애인") cands.push(["장애인·국가유공자 면제", tax]);
  let name="", amt=0;
  for(const c of cands){ if(c[1]>amt){ name=c[0]; amt=c[1]; } }
  return {basis, rate, tax, cut:amt, cutName:name, net:tax-amt};
}
function bondCost(basis, cc, fuel, region, commercial, kind){
  if(commercial) return {buy:0, loss:0, note:"영업용 채권 기준은 지자체마다 달라 계산에서 제외했습니다"};
  if(fuel==="전기"||fuel==="수소")
    return {buy:0, loss:0, note:"전기·수소차는 채권 매입이 250만원 한도로 면제됩니다 (2026.12.31까지)"};
  if(kind==="경차") return {buy:0, loss:0, note:"경차는 전 지역에서 채권 매입이 면제됩니다"};
  if(kind==="승합"||kind==="화물")
    return {buy:0, loss:0, note:"승합·화물자동차 채권 기준은 지자체마다 달라 계산에서 제외했습니다"};
  if(cc && cc < 1600)
    return {buy:0, loss:0, note:"1,600cc 미만은 2023년 3월부터 전국에서 면제입니다"};
  const table = D.bond[region]; if(!table) return {buy:0, loss:0, note:""};
  const row = table.find(r=>cc<=r[0]) || table[table.length-1];
  const rate = row[1];
  let buy = Math.ceil(basis*rate/D.bondUnit)*D.bondUnit;
  let note = "";
  if(fuel==="하이브리드"){
    const cut = Math.min(buy, D.bondHevLimit);
    if(cut>0){ buy -= cut; note = "하이브리드 채권 면제 "+won(cut)+" 적용"; }
  }
  return {buy, loss: Math.round(buy*D.bondDiscount), rate, note};
}

/* ── 상태 ── */
const S = {mode:"new", model:null, trim:null, cc:1598, price:20000000,
  fuel:"가솔린", kind:"승용", origin:"국산", regYear:D.year, regMonth:1,
  region:"서울", commercial:false, extra:""};

/* ── UI ── */
const $ = s=>document.querySelector(s);
function el(id){return document.getElementById(id);}

function renderAC(list){
  const box = el("ac");
  if(!list.length){ box.style.display="none"; return; }
  box.innerHTML = list.map((m,i)=>
    `<div data-i="${i}"><b>${m.mk} ${m.nm}</b><small>${m.kd} · ${m.tr.length}개 트림</small></div>`).join("");
  box.style.display="block";
  box.querySelectorAll("div").forEach(d=>{
    d.onclick=()=>{ pickModel(list[+d.dataset.i]); box.style.display="none"; };
  });
}
function pickModel(m){
  S.model=m; S.kind=m.kd; S.origin=m.og;
  el("q").value = m.mk+" "+m.nm;
  const sel = el("trim");
  sel.innerHTML = m.tr.map((t,i)=>
    `<option value="${i}">${t.n} — ${t.cc?t.cc.toLocaleString()+"cc":"전기"} · ${(t.p/10000).toLocaleString()}만원</option>`).join("");
  sel.parentElement.style.display="block";
  pickTrim(0);
}
function pickTrim(i){
  const t = S.model.tr[i]; S.trim=t; S.cc=t.cc; S.price=t.p; S.fuel=t.f;
  el("cc").value = t.cc; el("price").value = Math.round(t.p/10000);
  el("fuel").value = t.f;
  calc();
}
function calc(){
  S.cc = +el("cc").value||0;
  S.price = (+el("price").value||0)*10000;
  S.fuel = el("fuel").value;
  S.regYear = +el("regYear").value||D.year;
  S.regMonth = +el("regMonth").value||1;
  S.region = el("region").value;
  S.commercial = el("use").value==="영업용";
  const ages = carAges(S.regYear, S.regMonth, D.year);
  const age = Math.max(0, D.year - S.regYear);

  // 중고차: 시가표준액 추정
  let taxPrice = S.price, basisNote="";
  if(S.mode==="used"){
    const std = Math.floor(S.price/1.1*residual(age, S.origin))*1.1;
    const deal = (+el("deal").value||0)*10000;
    taxPrice = Math.max(std, deal);
    basisNote = deal>std
      ? `실거래가(${won(deal)})가 시가표준액(${won(std)})보다 높아 실거래가 기준`
      : `시가표준액 ${won(std)} 기준 (잔가율 ${residual(age,S.origin)}, 경과 ${age}년)`;
  }

  const a = acqTax(taxPrice, S.kind, S.fuel, S.commercial, S.extra);
  const b = bondCost(a.basis, S.cc, S.fuel, S.region, S.commercial, S.kind);
  const fees = Object.values(D.fees).reduce((x,y)=>x+y,0);
  const c = carTax(S.cc, S.fuel, ages, S.commercial, S.kind);

  // 연납
  const pre = D.prepayWindows.map(w=>{
    const cut = Math.floor(c.total * w[2]/D.yearDays * D.prepay / 10)*10;
    return {label:w[0], days:w[2], period:w[3], pay:c.total-cut, cut};
  });

  let html = `<div class="out">
    <h3>취득 단계</h3>
    <div class="row"><span>과세표준 (부가세 제외)</span><b>${won(a.basis)}</b></div>
    <div class="row"><span>취득세 ${(a.rate*100).toFixed(0)}%</span><b>${won(a.tax)}</b></div>`;
  if(a.cut>0) html += `<div class="row"><span>${a.cutName}</span><b class="neg">−${won(a.cut)}</b></div>`;
  if(b.buy>0){
    html += `<div class="row"><span>공채 매입 (${S.region}${b.rate?" "+(b.rate*100).toFixed(0)+"%":""})</span><b>${won(b.buy)}</b></div>`;
    html += `<div class="row"><span>└ 즉시매도 시 실부담</span><b>${won(b.loss)}</b></div>`;
  }
  html += `<div class="row"><span>번호판·증지 등 부대비용</span><b>${won(fees)}</b></div>`;
  html += `<div class="row total"><span>등록 시 실부담 합계</span><span>${won(a.net + b.loss + fees)}</span></div>`;
  if(b.buy>0) html += `<div class="mini">공채를 만기까지 보유하면 원금을 돌려받습니다. 즉시매도 기준으로 계산했습니다.</div>`;
  if(b.note) html += `<div class="mini">${b.note}</div>`;
  if(basisNote) html += `<div class="mini">${basisNote}</div>`;
  if(S.extra==="장애인" && S.cc > 2000 && S.kind==="승용")
    html += `<div class="mini" style="color:var(--stop)">장애인·국가유공자 면제는 배기량 2,000cc 이하 승용차가 원칙입니다.
      2,000cc를 넘는 차는 승차정원 7~10인승이어야 대상이 됩니다. 요건을 확인하세요.</div>`;
  if(S.extra==="다자녀" && S.kind==="승용")
    html += `<div class="mini">6인승 이하 승용차는 140만원 한도, 7~10인승은 한도 없이 전액 면제입니다.
      위 계산은 6인승 이하 기준입니다.</div>`;
  if(a.cut>0) html += `<div class="mini">감면은 중복 적용되지 않고 가장 유리한 하나만 적용됩니다 (지방세특례제한법 제180조).</div>`;
  html += `</div>`;

  const h1 = c.halves[0][0]+c.halves[0][1], h2 = c.halves[1][0]+c.halves[1][1];
  const ageTxt = c.flatKind ? "" :
    (ages[0]===ages[1] ? ` (차령 ${ages[0]}년${c.disc?`, ${(c.disc*100).toFixed(0)}% 경감`:""})`
                       : ` (차령 1기분 ${ages[0]}년 · 2기분 ${ages[1]}년)`);
  html += `<div class="out" style="margin-top:14px">
    <h3>보유 단계 — 연간 자동차세</h3>
    <div class="row"><span>자동차세${ageTxt}</span><b>${won(c.base)}</b></div>`;
  if(!S.commercial && !c.flatKind) html += `<div class="row"><span>지방교육세 30%</span><b>${won(c.edu)}</b></div>`;
  html += `<div class="row total"><span>연간 납부액</span><span>${won(c.total)}</span></div>
    <div class="mini">6월(1기분) ${won(h1)} + 12월(2기분) ${won(h2)}</div>`;
  if(!c.flatKind) html += `<div class="mini">기분마다 <b>A/2 − (A/2 × 5/100)(n−2)</b> 로 계산하고 각각 10원 미만을 절사합니다 (지방세법 제127조 제3항).</div>`;
  if(c.flatKind==="승합") html += `<div class="mini">승합자동차(11~15인승)는 배기량과 무관하게 정액으로 과세하고 지방교육세가 붙지 않습니다. 차령 경감도 없습니다.</div>`;
  if(c.flatKind==="화물") html += `<div class="mini">화물자동차는 적재량 기준 정액입니다. 위 금액은 1,000kg 이하 기준이며 지방교육세가 붙지 않습니다.</div>`;
  if(c.flatKind==="전기") html += `<div class="mini">전기·수소차는 정액 과세라 차령이 지나도 줄어들지 않습니다.</div>`;
  html += `</div>`;

  html += `<div class="out" style="margin-top:14px">
    <h3>연납 할인 (공제율 ${(D.prepay*100).toFixed(0)}%)</h3>`;
  pre.forEach(p=>{
    html += `<div class="row"><span>${p.label} 연납 <small style="color:var(--muted)">${p.period} · ${p.days}일분</small></span>
      <b>${won(p.pay)} <span class="neg">(−${won(p.cut)})</span></b></div>`;
  });
  html += `<div class="mini">공제액 = 연세액 × (납부기한 다음날부터 12/31까지 일수 ÷ ${D.yearDays}) × ${(D.prepay*100).toFixed(0)}%.
    1월 연납도 334일분이라 실질 할인은 약 2.74%입니다.</div>
    <div class="mini">3·6·9월 연납액은 이미 도래한 기분의 납부 여부에 따라 지자체 산출과 다를 수 있습니다.</div></div>`;

  el("result").innerHTML = html;
}

/* ── 이벤트 ── */
function boot(){
  el("q").addEventListener("input", e=>renderAC(search(e.target.value)));
  el("q").addEventListener("focus", e=>{ if(e.target.value) renderAC(search(e.target.value)); });
  document.addEventListener("click", e=>{ if(!e.target.closest(".results")) el("ac").style.display="none"; });
  el("trim").addEventListener("change", e=>pickTrim(+e.target.value));
  ["cc","price","fuel","regYear","regMonth","region","use","deal"].forEach(id=>{
    const n = el(id); if(n) n.addEventListener("input", calc), n.addEventListener("change", calc);
  });
  document.querySelectorAll(".tabs button").forEach(b=>{
    b.onclick=()=>{
      document.querySelectorAll(".tabs button").forEach(x=>x.classList.remove("on"));
      b.classList.add("on"); S.mode=b.dataset.mode;
      el("usedbox").style.display = S.mode==="used" ? "block" : "none";
      calc();
    };
  });
  document.querySelectorAll("#extras button").forEach(b=>{
    b.onclick=()=>{
      const on = b.classList.contains("on");
      document.querySelectorAll("#extras button").forEach(x=>x.classList.remove("on"));
      if(!on){ b.classList.add("on"); S.extra=b.dataset.v; } else { S.extra=""; }
      calc();
    };
  });
  // ?q= 딥링크
  const p = new URLSearchParams(location.search);
  if(p.get("q")){ const r = search(p.get("q")); if(r.length) pickModel(r[0]); }
  else if(p.get("m")){ const m = D.models.find(x=>x.sl===p.get("m")); if(m) pickModel(m); }
  else calc();
}
document.addEventListener("DOMContentLoaded", boot);
"""


# ─────────────────────────────────────────────────────────────
# 페이지 생성
# ─────────────────────────────────────────────────────────────
def build_index():
    top = []
    for maker, name, aliases, kind, origin, trims in CARS.CARS[:24]:
        sl = CARS.slug(maker, name)
        top.append(f'<a class="btn ghost" style="padding:7px 13px;font-size:14px;margin:0 5px 7px 0" '
                   f'href="{ROOT}/car/{sl}.html">{name}</a>')

    body = f"""
<h1>차종만 고르면 세금이 바로 나옵니다</h1>
<p class="lead">{C.SITE_DESC}</p>

<div class="card" style="text-align:center;background:linear-gradient(180deg,#e4f4f1,#fff)">
  <p style="margin-bottom:14px"><strong>신차 취득세 · 중고차 취득세 · 연간 자동차세 · 연납 할인</strong>을 한 화면에서 확인하세요.</p>
  <a class="btn" href="{ROOT}/tool.html">계산기 열기</a>
</div>

<h2>이 계산기가 다른 점</h2>
<div class="grid two">
  <div class="card">
    <span class="badge">과세표준</span>
    <p style="margin:8px 0 0">차값을 그대로 곱하지 않고 <strong>부가가치세를 뺀 공급가액</strong>으로 계산합니다.
    3,000만원 차의 취득세는 210만원이 아니라 190만 9,090원입니다.</p>
  </div>
  <div class="card">
    <span class="badge">중복감면 배제</span>
    <p style="margin:8px 0 0">경차·전기차·다자녀 감면을 <strong>더하지 않고</strong> 가장 유리한 하나만 적용합니다.
    지방세특례제한법 제180조 그대로입니다.</p>
  </div>
  <div class="card">
    <span class="badge">공채</span>
    <p style="margin:8px 0 0">2023년 3월부터 <strong>1,600cc 미만은 전국 면제</strong>입니다.
    지역별 매입률과 즉시매도 실부담까지 계산합니다.</p>
  </div>
  <div class="card">
    <span class="badge">연납</span>
    <p style="margin:8px 0 0">2026년 공제율은 3%이고, 남은 일수에만 적용돼 실질 할인은 <strong>약 2.74%</strong>입니다.
    1·3·6·9월 신청분을 모두 보여 줍니다.</p>
  </div>
</div>

<h2>많이 찾는 차종</h2>
<p>{''.join(top)}</p>
<p><a href="{ROOT}/tool.html#allitems">전체 {len(CARS.CARS)}개 차종 보기 →</a></p>

<h2>알아 두면 좋은 글</h2>
<ul class="postlist">
{''.join(f'<li><a href="{ROOT}/guide/{p["slug"]}.html">{p["title"]}</a><p>{p["desc"]}</p></li>' for p in P.POSTS[:6])}
</ul>
<p><a href="{ROOT}/guide.html">가이드 전체 보기 →</a></p>

<div class="disclaimer">
이 사이트의 계산 결과는 공개된 법령과 지자체 안내를 바탕으로 한 <strong>참고용 추정치</strong>입니다.
실제 부과되는 세액은 차량 형식별 시가표준액, 지자체 조례, 개별 감면 요건에 따라 달라질 수 있습니다.
정확한 금액은 <a href="https://www.wetax.go.kr" target="_blank" rel="noopener">위택스</a> 또는
관할 차량등록사업소에서 확인하세요.
</div>
"""
    write("index.html", page(C.SITE_NAME, C.SITE_DESC, body, ROOT + "/"))


def calc_form(embed=False):
    """계산기 입력 폼 HTML — tool.html 과 embed.html 이 공유합니다."""
    regions = "".join(f'<option value="{r}">{r}</option>' for r in R.BOND_RATES)
    years = "".join(f'<option value="{y}">{y}년</option>'
                    for y in range(date.today().year, date.today().year - 25, -1))
    months = "".join(f'<option value="{m}">{m}월</option>' for m in range(1, 13))
    return f"""
<div class="card">
  <div class="tabs">
    <button class="on" data-mode="new">신차</button>
    <button data-mode="used">중고차</button>
  </div>

  <div class="field results">
    <label for="q">차종 검색 <span style="font-weight:400">— 초성도 됩니다 (ㄱㄹㅈ → 그랜저)</span></label>
    <input id="q" type="text" placeholder="아반떼, ㅅㄹㅌ, model3, EV6 …" autocomplete="off">
    <div class="ac" id="ac"></div>
  </div>

  <div class="field" style="display:none">
    <label for="trim">트림</label>
    <select id="trim"></select>
  </div>

  <div class="grid specs">
    <div class="field"><label for="cc">배기량 (cc) — 전기차는 0</label>
      <input id="cc" type="number" value="1598" min="0" step="1"></div>
    <div class="field"><label for="price">차량가격 (만원, 부가세 포함)</label>
      <input id="price" type="number" value="2100" min="0" step="10"></div>
    <div class="field"><label for="fuel">연료</label>
      <select id="fuel">
        <option>가솔린</option><option>디젤</option><option>LPG</option>
        <option>하이브리드</option><option>전기</option><option>수소</option>
      </select></div>
    <div class="field"><label for="regYear">최초등록 연도</label>
      <select id="regYear">{years}</select></div>
    <div class="field"><label for="regMonth">최초등록 월</label>
      <select id="regMonth">{months}</select></div>
    <div class="field"><label for="region">등록 지역 (공채)</label>
      <select id="region">{regions}</select></div>
    <div class="field"><label for="use">용도</label>
      <select id="use"><option>비영업용</option><option>영업용</option></select></div>
  </div>

  <div id="usedbox" style="display:none">
    <div class="field"><label for="deal">실제 거래가 (만원)</label>
      <input id="deal" type="number" value="0" min="0" step="10"
        placeholder="0을 넣으면 시가표준액으로 계산합니다">
      <div class="mini">중고차는 실거래가와 시가표준액 중 <strong>높은 쪽</strong>이 과세표준입니다.</div>
    </div>
  </div>

  <div class="mini" style="margin:-4px 0 14px">
    차령은 자동차등록증의 <b>최초등록일</b> 기준입니다. 제작연도(연식)와 다를 수 있습니다.
  </div>

  <div class="field" style="margin-bottom:6px">
    <label>추가 감면 (하나만 적용됩니다)</label>
    <div class="chips" id="extras">
      <button data-v="다자녀">18세 미만 자녀 3명 이상</button>
      <button data-v="장애인">장애인 · 국가유공자</button>
    </div>
  </div>
</div>

<div id="result"></div>
"""


def build_embed():
    """블로그 iframe 삽입용 경량 페이지 (헤더·푸터·전체표 없음)."""
    data = build_data_json()
    extra_css = """
body{background:transparent;padding:0}
.wrap{max-width:100%;padding:0 4px}
main{padding:0}
.card{margin-bottom:12px;padding:16px}
.embed-foot{font-size:12px;color:var(--muted);text-align:center;padding:10px 4px 16px}
.embed-foot a{font-weight:700}
"""
    resize_js = """
<script>
function postH(){
  try{ parent.postMessage({cartaxHeight: document.documentElement.scrollHeight}, "*"); }catch(e){}
}
new MutationObserver(postH).observe(document.body, {subtree:true, childList:true, characterData:true});
window.addEventListener("load", postH);
setInterval(postH, 800);
</script>"""
    body = f"""
{calc_form(embed=True)}
<div class="embed-foot">
  계산 결과는 참고용입니다 ·
  <a href="{ROOT}/tool.html" target="_blank" rel="noopener">{C.SITE_NAME}에서 자세히 보기 →</a>
</div>
"""
    js = ('<script>window.__DATA__=' + json.dumps(data, ensure_ascii=False) + ';</script>\n'
          '<script>' + CALC_JS + '</script>' + resize_js)
    html = page("자동차세 계산기", C.SITE_DESC, body, ROOT + "/embed.html",
                extra_head=f"<style>{extra_css}</style>"
                           '<meta name="robots" content="noindex,follow">',
                extra_js=js)
    # 임베드 페이지에서는 사이트 헤더·푸터를 제거
    html = re.sub(r'<header class="site">.*?</header>', "", html, flags=re.S)
    html = re.sub(r'<footer class="site">.*?</footer>', "", html, flags=re.S)
    write("embed.html", html)


def build_tool():
    data = build_data_json()
    regions = "".join(f'<option value="{r}">{r}</option>' for r in R.BOND_RATES)
    years = "".join(f'<option value="{y}">{y}년식</option>' for y in range(date.today().year, date.today().year - 25, -1))

    rows = []
    for maker, name, aliases, kind, origin, trims in CARS.CARS:
        sl = CARS.slug(maker, name)
        for t in trims:
            tname, cc, price, fuel = t
            _, _, total, _, _ = car_tax(cc, fuel, (2, 2), False, kind)
            basis, tax, cut, cutname = acq_tax(price * 10000, kind, fuel, False)
            rows.append(
                f'<tr><td><a href="{ROOT}/car/{sl}.html">{maker} {name}</a></td>'
                f'<td>{tname}</td><td>{cc:,}cc</td>'
                f'<td>{won(tax - cut)}</td><td>{won(total)}</td></tr>'
                if cc else
                f'<tr><td><a href="{ROOT}/car/{sl}.html">{maker} {name}</a></td>'
                f'<td>{tname}</td><td>전기</td>'
                f'<td>{won(tax - cut)}</td><td>{won(total)}</td></tr>')

    body = f"""
<h1>자동차 취득세 · 자동차세 계산기</h1>
<p class="lead">차종을 검색하거나 배기량과 가격을 직접 넣으면 등록 시 실부담과 연간 자동차세가 바로 나옵니다.</p>

{calc_form()}

<div class="card" style="margin-top:18px">
  <h3 style="margin-top:0">계산 기준</h3>
  <ul style="font-size:14px;color:var(--muted);margin:0">
    <li>취득세 과세표준 = 차량가격 ÷ 1.1 (부가가치세 제외 공급가액)</li>
    <li>승용 7% / 경차 4% / 승합·화물 5% / 영업용 4% — 자동차 취득세에는 지방교육세가 붙지 않습니다</li>
    <li>자동차세는 기분(반기)마다 <b>A/2 − (A/2 × 5/100)(n−2)</b> 로 계산하고 각각 10원 미만 절사 — A는 연세액, n은 차령</li>
    <li>차령 n 은 <b>최초등록일</b> 기준: 1~6월 등록은 (과세연도−등록연도)+1, 7~12월 등록은 1기분만 1년 적게</li>
    <li>지방교육세는 기분별 자동차세의 30% (비영업용 승용차만)</li>
    <li>전기·수소차는 정액 10만원 + 교육세 = 연 13만원, 차령 경감 없음</li>
    <li>감면은 중복 적용되지 않고 가장 유리한 하나만 적용됩니다 (지방세특례제한법 제180조)</li>
    <li>공채는 1,600cc 미만 전국 면제, 즉시매도 손실률 {int(R.BOND_DISCOUNT*100)}% 기준</li>
    <li>연납 공제액 = 연세액 × (납부기한 다음날~12/31 일수 ÷ 365) × {int(R.PREPAY_RATE*100)}%</li>
  </ul>
</div>

<h2 id="allitems">전체 차종 세금표 ({len(CARS.CARS)}개 모델 · {sum(len(c[5]) for c in CARS.CARS)}개 트림)</h2>
<p class="lead" style="font-size:15px">신차 기준, 비영업용, 감면 적용 후 금액입니다. 차종을 누르면 상세 페이지로 갑니다.</p>
<table>
<thead><tr><th>차종</th><th>트림</th><th>배기량</th><th>취득세</th><th>연 자동차세</th></tr></thead>
<tbody>
{''.join(rows)}
</tbody>
</table>

<div class="disclaimer">
계산 결과는 참고용입니다. 실제 세액은 차량 형식별 시가표준액과 지자체 조례에 따라 달라질 수 있으며,
정확한 금액은 <a href="https://www.wetax.go.kr" target="_blank" rel="noopener">위택스</a>에서 확인하세요.
</div>
"""
    js = ('<script>window.__DATA__=' + json.dumps(data, ensure_ascii=False) + ';</script>\n'
          '<script>' + CALC_JS + '</script>')
    write("tool.html", page("자동차 취득세·자동차세 계산기",
                            "차종만 고르면 신차·중고차 취득세와 연간 자동차세, 공채 매입비, 연납 할인까지 한 번에 계산합니다.",
                            body, ROOT + "/tool.html", extra_js=js))


def build_car_pages():
    for maker, name, aliases, kind, origin, trims in CARS.CARS:
        sl = CARS.slug(maker, name)
        rows, rows_age = [], []
        for tname, cc, price, fuel in trims:
            basis, tax, cut, cutname = acq_tax(price * 10000, kind, fuel, False)
            base, edu, total, _, _ = car_tax(cc, fuel, (2, 2), False, kind)
            ccs = f"{cc:,}cc" if cc else "전기"
            rows.append(f"<tr><td>{tname}</td><td>{ccs}</td><td>{price:,}만원</td>"
                        f"<td>{won(tax)}</td><td>{'−'+won(cut) if cut else '-'}</td>"
                        f"<td><b>{won(tax-cut)}</b></td></tr>")
            rows_age.append((tname, cc, fuel, total))

        age_rows = []
        for tname, cc, fuel, _ in rows_age:
            cells = []
            for a in (2, 3, 5, 8, 12):
                _, _, t, _, _ = car_tax(cc, fuel, (a, a), False, kind)
                cells.append(f"<td>{won(t)}</td>")
            age_rows.append(f"<tr><td>{tname}</td>{''.join(cells)}</tr>")

        all_ev = all(t[3] in ("전기", "수소") for t in trims)
        if kind == "승합":
            age_section = """
<h2>연식별 자동차세</h2>
<p>승합자동차(11~15인승)는 배기량과 무관하게 <strong>연 65,000원 정액</strong>으로 과세합니다.
지방교육세도 붙지 않고 차령 경감도 없습니다. 신차든 15년 된 차든 같은 금액입니다.</p>
<p>같은 차의 9인승 모델이 승용자동차로 분류돼 연 90만원대를 내는 것과 비교하면
<a href="{ROOT}/guide/seat-count-tax.html">좌석 수 하나가 만드는 차이</a>가 큽니다.</p>
""".replace("{ROOT}", ROOT)
        elif kind == "화물":
            age_section = """
<h2>연식별 자동차세</h2>
<p>화물자동차는 배기량이 아니라 <strong>적재량 기준 정액</strong>입니다. 1톤 이하는 연 28,500원이고,
지방교육세도 붙지 않으며 차령 경감도 없습니다.</p>
<p>같은 배기량 승용차와 비교하면 20배 이상 저렴합니다.
자세한 내용은 <a href="{ROOT}/guide/truck-tax.html">1톤 트럭 세금</a>에서 다룹니다.</p>
""".replace("{ROOT}", ROOT)
        elif all_ev:
            age_section = """
<h2>연식별 자동차세</h2>
<p>전기·수소차는 배기량이 아니라 정액으로 과세하기 때문에 <strong>차령 경감이 적용되지 않습니다.</strong>
신차든 10년 된 차든 연 130,000원으로 같습니다.</p>
<p>반대로 내연기관차는 차령 12년이 되면 세금이 절반까지 떨어집니다. 오래 탈수록 두 차종의 자동차세 격차는 줄어듭니다.</p>
"""
        else:
            age_section = f"""
<h2>차령별 자동차세</h2>
<p>차령 3년째부터 매년 5%포인트씩, 12년 이상이면 50%까지 줄어듭니다.
차령은 <strong>최초등록일</strong> 기준이라 연식과 1년 차이가 날 수 있습니다.</p>
<table>
<thead><tr><th>트림</th><th>차령 2년↓</th><th>3년</th><th>5년</th><th>8년</th><th>12년↑</th></tr></thead>
<tbody>{''.join(age_rows)}</tbody>
</table>"""

        cc_main = trims[0][1]
        fuel_main = trims[0][3]
        price_main = trims[0][2]
        _, _, total_main, _, _ = car_tax(cc_main, fuel_main, (2, 2), False, kind)
        _, tax_main, cut_main, _ = acq_tax(price_main * 10000, kind, fuel_main, False)

        note = ""
        if fuel_main in ("전기", "수소"):
            note = ('<div class="tip">전기·수소차는 배기량이 없어 자동차세를 <strong>정액 10만원</strong>으로 매기고, '
                    '지방교육세를 더해 연 13만원입니다. 차령이 지나도 줄어들지 않습니다. '
                    '취득세는 140만원 한도로 감면됩니다.</div>')
        elif kind == "경차":
            note = ('<div class="tip">경차는 취득세가 <strong>75만원 한도로 면제</strong>되고, '
                    '고속도로 통행료·공영주차장 요금 50% 할인과 유류세 환급(연 30만원 한도)까지 받습니다.</div>')
        elif cc_main and cc_main < 1600:
            note = ('<div class="tip">1,600cc 미만이라 <strong>공채 매입이 면제</strong>되고, '
                    '자동차세도 cc당 140원 구간이라 2,000cc급보다 크게 저렴합니다.</div>')
        elif cc_main and cc_main >= 2000:
            note = ('<div class="tip">2,000cc를 넘어 공채 매입률이 가장 높은 구간입니다. '
                    f'서울에서 등록하면 부가세를 뺀 차값의 20%에 해당하는 채권을 사야 합니다.</div>')

        body = f"""
<h1>{maker} {name} 취득세 · 자동차세</h1>
<p class="lead">{maker} {name}의 신차 취득세와 연간 자동차세를 트림별로 정리했습니다.
{date.today().year}년 기준, 비영업용 승용 기준입니다.</p>

<div class="card" style="background:var(--brand-soft)">
  <div style="display:flex;justify-content:space-between;padding:4px 0">
    <span>취득세 (감면 후)</span><b>{won(tax_main - cut_main)}</b></div>
  <div style="display:flex;justify-content:space-between;padding:4px 0">
    <span>연간 자동차세</span><b>{won(total_main)}</b></div>
  <div style="display:flex;justify-content:space-between;padding:4px 0">
    <span>기준 트림</span><b>{trims[0][0]}</b></div>
</div>
<p><a class="btn" href="{ROOT}/tool.html?m={sl}">이 차로 계산기 열기</a></p>

{note}

<h2>트림별 취득세</h2>
<table>
<thead><tr><th>트림</th><th>배기량</th><th>차량가</th><th>취득세</th><th>감면</th><th>실납부</th></tr></thead>
<tbody>{''.join(rows)}</tbody>
</table>
<p class="src">차량가격은 참고용 신차가(부가세 포함)입니다. 옵션과 할인에 따라 달라집니다.</p>

{age_section}

<h2>세금을 줄이는 방법</h2>
<ul>
<li>18세 미만 자녀가 3명 이상이면 <a href="{ROOT}/guide/multi-child-disabled.html">다자녀 감면</a>을 받을 수 있습니다. 7인승 이상이면 한도 없이 전액 면제입니다.</li>
<li>1월에 <a href="{ROOT}/guide/prepayment-discount.html">자동차세를 연납</a>하면 약 2.74% 할인됩니다.</li>
<li>중고로 살 때는 <a href="{ROOT}/guide/used-car-tax-base.html">시가표준액</a>과 실거래가 중 높은 쪽이 기준이 됩니다.</li>
</ul>

<div class="disclaimer">
계산 결과는 참고용 추정치입니다. 실제 세액은 차량 형식별 시가표준액과 지자체 조례에 따라 달라질 수 있습니다.
정확한 금액은 <a href="https://www.wetax.go.kr" target="_blank" rel="noopener">위택스</a> 또는 관할 차량등록사업소에서 확인하세요.
</div>
"""
        desc = (f"{maker} {name} 취득세 {won(tax_main - cut_main)}, 연간 자동차세 {won(total_main)}. "
                f"트림별·연식별 세액을 한눈에 정리했습니다.")
        write(f"car/{sl}.html", page(f"{maker} {name} 취득세·자동차세", desc, body,
                                     f"{ROOT}/car/{sl}.html"))


def build_guides():
    by_slug = {p["slug"]: p for p in P.POSTS}
    sections = []
    for gname, gdesc, gslugs in P.GROUPS:
        items = "".join(
            f'<li><a href="{ROOT}/guide/{s}.html">{by_slug[s]["title"]}</a>'
            f'<p>{by_slug[s]["desc"]}</p></li>'
            for s in gslugs if s in by_slug)
        sections.append(f'<h2>{gname}</h2>\n<p class="lead" style="margin-bottom:10px;font-size:15px">'
                        f'{gdesc}</p>\n<ul class="postlist">{items}</ul>')
    body = f"""
<h1>자동차 세금 가이드</h1>
<p class="lead">취득세부터 자동차세, 공채, 감면까지 {len(P.POSTS)}편.
법 조문과 지자체 안내를 근거로 정리했습니다.</p>
{"".join(sections)}
"""
    write("guide.html", page("자동차 세금 가이드",
                             "자동차 취득세·자동차세·공채·감면 제도를 법령 기준으로 정리한 가이드 모음입니다.",
                             body, ROOT + "/guide.html"))

    for i, p in enumerate(P.POSTS):
        prev_p = P.POSTS[i - 1] if i > 0 else None
        next_p = P.POSTS[i + 1] if i < len(P.POSTS) - 1 else None
        nav = []
        if prev_p:
            nav.append(f'<a href="{ROOT}/guide/{prev_p["slug"]}.html">← {prev_p["title"]}</a>')
        if next_p:
            nav.append(f'<a href="{ROOT}/guide/{next_p["slug"]}.html">{next_p["title"]} →</a>')
        tags = "".join(f'<span class="badge">{t}</span>' for t in p["tags"])
        by_slug = {q["slug"]: q for q in P.POSTS}
        related = ""
        for gname, _gdesc, gslugs in P.GROUPS:
            if p["slug"] in gslugs:
                sibs = [s for s in gslugs if s != p["slug"] and s in by_slug][:3]
                if sibs:
                    lis = "".join(
                        f'<li><a href="{ROOT}/guide/{s}.html">{by_slug[s]["title"]}</a></li>'
                        for s in sibs)
                    related = (f'<h2>같은 주제의 다른 글</h2>'
                               f'<p class="lead" style="font-size:15px;margin-bottom:8px">{gname}</p>'
                               f'<ul>{lis}</ul>')
                break
        body = f"""
<p style="font-size:13px;color:var(--muted)"><a href="{ROOT}/guide.html">가이드</a> › {p["tags"][0]}</p>
<h1>{p["title"]}</h1>
<p class="lead">{tags} <span style="font-size:13px">{p["date"]} 작성</span></p>
{p["body"].replace("{ROOT}", ROOT)}
<div class="disclaimer">
이 글은 공개된 법령과 지자체 안내를 바탕으로 작성한 참고 자료이며 세무 상담을 대신하지 않습니다.
개별 사안은 관할 지방자치단체 세무과에 문의하세요.
</div>
{related}
<div style="display:flex;justify-content:space-between;gap:12px;margin-top:22px;font-size:14px">{''.join(nav)}</div>
<p style="margin-top:22px"><a class="btn" href="{ROOT}/tool.html">계산기로 확인하기</a></p>
"""
        write(f"guide/{p['slug']}.html",
              page(p["title"], p["desc"], body, f"{ROOT}/guide/{p['slug']}.html"))


def build_static():
    write("about.html", page("사이트 소개", f"{C.SITE_NAME}이 어떤 자료를 근거로 계산하는지 설명합니다.", f"""
<h1>사이트 소개</h1>
<p>{C.SITE_NAME}은 자동차를 사고 보유할 때 내는 세금을 누구나 몇 초 만에 확인할 수 있게 만든 무료 계산기입니다.</p>

<h2>무엇을 계산하나</h2>
<ul>
<li><strong>취득세</strong> — 신차·중고차, 차종별 세율, 경차·전기차·다자녀·장애인 감면</li>
<li><strong>공채</strong> — 지역별 도시철도채권·지역개발채권 매입액과 즉시매도 실부담</li>
<li><strong>자동차세</strong> — 배기량별 세액, 지방교육세, 차령 경감</li>
<li><strong>연납 할인</strong> — 1·3·6·9월 신청 시 실제 납부액</li>
</ul>

<h2>계산 근거</h2>
<ul>
<li>지방세법 제12조(취득세 표준세율), 제127조(자동차세 과세표준과 세율), 제128조(납기와 징수방법)</li>
<li>지방세특례제한법 제66조~제67조(경차·친환경차 감면), 제180조(중복감면 배제)</li>
<li>지방세 시가표준액 조사·산정 기준 [별표 16] 차량 용도별 감가상각률표</li>
<li>각 지방자치단체 차량등록사업소의 취득세·공채 안내</li>
</ul>

<h2>정확도에 대해</h2>
<p>계산 결과는 <strong>참고용 추정치</strong>입니다. 특히 다음 두 가지는 실제와 차이가 날 수 있습니다.</p>
<ul>
<li><strong>중고차 시가표준액</strong> — 실제로는 차량 '형식'별로 고시된 기준가격을 씁니다.
이 사이트는 최초 공급가액에 공표 잔가율을 곱해 추정합니다.</li>
<li><strong>공채 매입률</strong> — 지자체 조례로 정해 수시로 바뀝니다.</li>
</ul>
<p>정확한 금액은 <a href="https://www.wetax.go.kr" target="_blank" rel="noopener">위택스</a>나 관할 차량등록사업소에서 확인하세요.
오류를 발견하시면 <a href="{ROOT}/contact.html">문의</a>로 알려 주시면 바로 고치겠습니다.</p>

<h2>운영자</h2>
<p>{C.OPERATOR}<br>문의: {C.EMAIL}</p>
""", ROOT + "/about.html"))

    write("privacy.html", page("개인정보처리방침", "개인정보처리방침", f"""
<h1>개인정보처리방침</h1>
<p>{C.SITE_NAME}(이하 "사이트")은 이용자의 개인정보를 소중히 다룹니다.</p>

<h2>1. 수집하는 개인정보</h2>
<p>사이트는 회원가입 절차가 없으며, 이름·연락처 등 <strong>개인을 식별할 수 있는 정보를 직접 수집하지 않습니다.</strong>
계산기에 입력한 차량 정보는 이용자의 브라우저 안에서만 처리되며 서버로 전송되거나 저장되지 않습니다.</p>

<h2>2. 자동으로 수집되는 정보</h2>
<p>서비스 이용 과정에서 다음 정보가 자동으로 생성·수집될 수 있습니다.</p>
<ul>
<li>접속 IP 주소, 브라우저 종류 및 버전, 운영체제</li>
<li>방문 일시, 방문 페이지, 이동 경로</li>
</ul>

<h2>3. 쿠키 및 광고</h2>
<p>사이트는 Google AdSense를 통해 광고를 게재할 수 있습니다.
Google을 포함한 제3자 광고 공급업체는 쿠키를 사용하여 이용자의 이전 방문 기록을 바탕으로 광고를 제공합니다.</p>
<p>이용자는 <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener">Google 광고 설정</a>에서
맞춤 광고를 해제할 수 있으며, <a href="https://www.aboutads.info" target="_blank" rel="noopener">www.aboutads.info</a>에서
제3자 공급업체의 쿠키 사용을 거부할 수 있습니다.</p>
<p>브라우저 설정에서 쿠키 저장을 거부할 수도 있으나, 이 경우 일부 기능이 제한될 수 있습니다.</p>

<h2>4. 개인정보의 제3자 제공</h2>
<p>사이트는 이용자의 개인정보를 제3자에게 제공하지 않습니다.
다만 법령에 근거하여 수사기관 등이 적법한 절차에 따라 요청하는 경우는 예외로 합니다.</p>

<h2>5. 이용자의 권리</h2>
<p>이용자는 언제든지 개인정보 관련 사항에 대해 열람·정정·삭제를 요청할 수 있습니다.
아래 연락처로 문의하시면 지체 없이 조치하겠습니다.</p>

<h2>6. 개인정보 보호책임자</h2>
<p>책임자: {C.OPERATOR}<br>이메일: {C.EMAIL}</p>

<h2>7. 시행일</h2>
<p>본 방침은 {C.POLICY_DATE}부터 시행됩니다. 내용이 변경될 경우 이 페이지를 통해 공지합니다.</p>
""", ROOT + "/privacy.html"))

    write("terms.html", page("이용약관", "이용약관", f"""
<h1>이용약관</h1>

<h2>제1조 (목적)</h2>
<p>본 약관은 {C.SITE_NAME}(이하 "사이트")이 제공하는 서비스의 이용 조건과 절차, 이용자와 운영자의 권리·의무를 정함을 목적으로 합니다.</p>

<h2>제2조 (서비스의 내용)</h2>
<p>사이트는 자동차 취득세·자동차세 등 자동차 관련 세금의 <strong>추정 계산 정보</strong>와 관련 해설을 무료로 제공합니다.</p>

<h2>제3조 (정보의 성격과 면책)</h2>
<ol>
<li>사이트가 제공하는 모든 계산 결과와 설명은 <strong>참고용 정보</strong>이며, 세무 자문·법률 자문에 해당하지 않습니다.</li>
<li>실제 부과되는 세액은 차량 형식별 시가표준액, 지방자치단체 조례, 개별 감면 요건 등에 따라 달라질 수 있습니다.</li>
<li>운영자는 정보의 정확성을 위해 노력하나 완전성을 보장하지 않으며,
이용자가 사이트의 정보를 근거로 내린 판단과 그 결과에 대하여 책임을 지지 않습니다.</li>
<li>세액 관련 최종 확인은 위택스 또는 관할 지방자치단체를 통해 하시기 바랍니다.</li>
</ol>

<h2>제4조 (저작권)</h2>
<p>사이트에 게시된 콘텐츠의 저작권은 운영자에게 있습니다.
이용자는 사전 동의 없이 이를 복제·배포·전송하거나 영리 목적으로 이용할 수 없습니다.
다만 출처를 밝힌 인용은 허용됩니다.</p>

<h2>제5조 (서비스의 변경·중단)</h2>
<p>운영자는 서비스의 내용을 변경하거나 중단할 수 있으며, 이로 인한 손해에 대해 별도의 보상을 하지 않습니다.</p>

<h2>제6조 (약관의 변경)</h2>
<p>본 약관은 필요 시 변경될 수 있으며, 변경된 약관은 이 페이지에 게시한 시점부터 효력이 발생합니다.</p>

<p style="margin-top:24px">시행일: {C.POLICY_DATE}</p>
""", ROOT + "/terms.html"))

    write("contact.html", page("문의", "문의 및 오류 제보", f"""
<h1>문의</h1>
<p>계산 결과의 오류, 빠진 차종, 바뀐 세율 제보를 환영합니다.
알려 주시면 확인 후 빠르게 반영하겠습니다.</p>

<div class="card">
<p style="margin:0"><strong>이메일</strong><br>
<a href="mailto:{C.EMAIL}">{C.EMAIL}</a></p>
</div>

<h2>제보해 주시면 좋은 것</h2>
<ul>
<li>계산 결과가 실제 고지서·영수증과 다른 경우 (차종·연식·지역을 함께 알려 주시면 큰 도움이 됩니다)</li>
<li>목록에 없는 차종</li>
<li>세율·감면 제도 변경</li>
<li>지자체 공채 매입률 변경</li>
</ul>

<h2>답변</h2>
<p>1인이 운영하는 사이트라 답변까지 며칠 걸릴 수 있습니다. 양해 부탁드립니다.</p>
<p>세무 상담은 드리기 어렵습니다. 개별 사안은 관할 지방자치단체 세무과나 세무 전문가에게 문의하세요.</p>

<h2>운영자</h2>
<p>{C.OPERATOR}</p>
""", ROOT + "/contact.html"))

    write("404.html", page("페이지를 찾을 수 없습니다", "요청하신 페이지가 없습니다.", f"""
<h1>페이지를 찾을 수 없습니다</h1>
<p class="lead">주소가 바뀌었거나 삭제된 페이지입니다.</p>
<p><a class="btn" href="{ROOT}/tool.html">계산기로 가기</a>
<a class="btn ghost" href="{ROOT}/">홈으로</a></p>
""", ROOT + "/404.html"))


def build_meta():
    urls = [("/", "1.0", "weekly"), ("/tool.html", "1.0", "weekly"),
            ("/guide.html", "0.8", "weekly"), ("/about.html", "0.5", "monthly"),
            ("/privacy.html", "0.3", "yearly"), ("/terms.html", "0.3", "yearly"),
            ("/contact.html", "0.4", "monthly")]
    urls += [(f"/guide/{p['slug']}.html", "0.8", "monthly") for p in P.POSTS]
    urls += [(f"/car/{CARS.slug(c[0], c[1])}.html", "0.7", "monthly") for c in CARS.CARS]

    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, pr, cf in urls:
        sm.append(f"  <url><loc>{ROOT}{u}</loc><lastmod>{TODAY}</lastmod>"
                  f"<changefreq>{cf}</changefreq><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm))

    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {ROOT}/sitemap.xml\n")
    write("ads.txt", (f"google.com, {C.ADSENSE_CLIENT.replace('ca-pub-','pub-')}, DIRECT, f08c47fec0942fa0\n"
                      if C.ADSENSE_CLIENT else
                      "# 애드센스 승인 후 _config.py 의 ADSENSE_CLIENT 를 채우고 다시 빌드하세요.\n"))
    write(".nojekyll", "")


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT, exist_ok=True)
    build_index()
    build_tool()
    build_embed()
    build_car_pages()
    build_guides()
    build_static()
    build_meta()

    n = sum(len(files) for _, _, files in os.walk(OUT))
    print(f"빌드 완료 → {OUT}/")
    print(f"  차종 페이지 {len(CARS.CARS)}개")
    print(f"  가이드 {len(P.POSTS)}편")
    print(f"  전체 파일 {n}개")


if __name__ == "__main__":
    main()
