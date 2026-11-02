import os, html
NAME="Adnan Rana"; EMAIL="adnan3624@gmail.com"; PHONE="+923069098215"; PHONE_D="+92 306 9098215"; LI="https://www.linkedin.com/in/adnan3624/"; GH="https://github.com/adnan3624"
SITE="https://adnan3624.github.io"
H1="Ad platforms, GA4, and sales data rarely agree. I reconcile them and show what is actually driving revenue and where budget should move."
def head(title,desc,p,path):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website"><meta property="og:url" content="{SITE}/{path}">
<link rel="canonical" href="{SITE}/{path}"><link rel="icon" href="{p}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}assets/css/style.css"></head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="nav"><div class="wrap nav-in"><a class="brand" href="{p}index.html">{NAME}</a>
<button class="burger" aria-label="Toggle menu" aria-expanded="false" aria-controls="menu"><i data-lucide="menu"></i></button>
<nav id="menu"><a href="{p}index.html#home">Home</a><a href="{p}index.html#expertise">Expertise</a><a href="{p}index.html#projects">Projects</a><a href="{p}index.html#about">About</a><a href="{p}index.html#contact">Contact</a>
<a class="btn small" href="{p}assets/documents/CV.pdf" download>Download CV</a></nav></div></header><main id="main">'''
def foot(p):
    return f'''</main><footer><div class="wrap foot"><span>&copy; 2026 {NAME}. Marketing Data Analyst.</span><span><a href="{LI}">LinkedIn</a> &nbsp; <a href="{GH}">GitHub</a> &nbsp; <a href="mailto:{EMAIL}">Email</a> &nbsp; <a href="tel:{PHONE}">{PHONE_D}</a></span></div></footer>
<script src="https://cdn.jsdelivr.net/npm/lucide@0.469.0/dist/umd/lucide.min.js"></script><script src="{p}assets/js/main.js"></script></body></html>'''

# ---------- case studies ----------
SYN="All data on this page is synthetic and illustrative. It demonstrates the method; it is not client data and the figures are not results."
cases=[
dict(f="cross-channel-measurement",t="Cross-Channel Marketing Performance Measurement",d="Reconciling Google Ads, Meta, GA4 and Shopify order data in BigQuery to compare ROAS and MER by channel.",
 ctx="A DTC store runs Google and Meta ads. Each platform, GA4 and Shopify reports a different revenue figure, so budget conversations start with an argument about whose number is right.",
 prob="Platform ROAS is inflated by overlapping attribution, GA4 undercounts consented traffic, and nobody has a single revenue figure tied to spend.",
 src=["Google Ads and Meta Ads daily campaign exports (spend, clicks, platform-reported conversions and value)","GA4 BigQuery export (events_*)","Shopify orders (order id, net revenue, discounts, refunds, UTM landing data)"],
 arch="Raw tables land in BigQuery, are standardised in a staging layer (one grain: date x channel x campaign), then joined in a mart that holds spend, platform revenue, GA4 revenue and Shopify revenue side by side.",
 impl="Daily Python loads write raw tables. SQL views map UTM and click-id values to a single channel taxonomy. Orders are the source of truth for revenue; GA4 and platforms are compared against it.",
 sql="""-- channel mart (illustrative)
SELECT d.date, d.channel,
  SUM(s.spend)                         AS spend,
  SUM(s.platform_revenue)              AS platform_revenue,
  SUM(g.ga4_revenue)                   AS ga4_revenue,
  SUM(o.net_revenue)                   AS order_revenue,
  SAFE_DIVIDE(SUM(s.platform_revenue), SUM(s.spend)) AS platform_roas,
  SAFE_DIVIDE(SUM(o.net_revenue), SUM(s.spend))      AS blended_roas
FROM dim_date_channel d
LEFT JOIN stg_spend s USING (date, channel)
LEFT JOIN stg_ga4   g USING (date, channel)
LEFT JOIN stg_orders o USING (date, channel)
GROUP BY 1,2;""",
 out=["Daily and weekly channel table with spend, three revenue views and variance","ROAS by platform versus order-based ROAS","MER (total net revenue / total ad spend) trend"],
 find=["In this synthetic example, platform-reported revenue sums to more than total orders, which is the classic double-counting signature.","Variance between GA4 and orders is largest on days with consent or checkout changes, so it is flagged for tracking review before it is read as performance."],
 rec=["Judge budget moves on MER and order-based ROAS, using platform ROAS only for in-platform optimisation.","Investigate channels where platform and order revenue diverge by a stable ratio before shifting spend."],
 lim="Order-to-channel mapping relies on UTMs and click ids, so untagged orders sit in an unattributed bucket. Revenue reconciliation shows where numbers disagree, not which channel caused the sale."),
dict(f="amazon-ads-analytics",t="Amazon Advertising Analytics",d="Campaign, keyword, search term and ASIN-level analysis of Amazon Ads with ACoS, ROAS and negative keyword discovery.",
 ctx="A marketplace seller spends on Sponsored Products and Sponsored Brands and needs to know which campaigns, search terms and ASINs earn their spend.",
 prob="Amazon reports sales attributed to ads, but there is no customer-level journey as in a DTC store, and ad-attributed sales overlap with organic sales.",
 src=["Advertising API or console exports: campaign, targeting and search term reports","Business Reports by ASIN (sessions, units, total sales)","Product cost and fee data for margin"],
 arch="Reports are loaded daily into BigQuery, keyed by campaign, ad group, targeting, search term and ASIN. Reconciliation is done at campaign, ASIN and channel level, never by customer.",
 impl="SQL classifies search terms by spend and orders, flags terms with clicks above a threshold and no orders, and joins ad sales to total ASIN sales to estimate ad dependence (TACoS).",
 sql="""-- negative keyword candidates (illustrative)
SELECT campaign, search_term,
  SUM(clicks) AS clicks, SUM(spend) AS spend, SUM(orders) AS orders
FROM stg_search_terms
WHERE report_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 60 DAY)
GROUP BY 1,2
HAVING SUM(clicks) >= 20 AND SUM(orders) = 0
ORDER BY spend DESC;""",
 out=["Search term waste table","ACoS and ROAS by campaign and match type","ASIN view: ad sales, total sales, TACoS, contribution margin"],
 find=["In the synthetic data, a small share of search terms holds most zero-order spend, making negative keyword cleanup the fastest lever.","High ACoS on an ASIN can be acceptable if margin and organic lift support it, so ACoS is read alongside TACoS and margin."],
 rec=["Add exact negatives for repeat zero-order terms and review weekly.","Set ACoS targets per ASIN from margin, not one account-wide number."],
 lim="Marketplace reporting does not expose customer-level data, and attribution windows differ from DTC platforms. Amazon figures should not be compared to GA4 or Meta numbers as if they were measured the same way."),
dict(f="ga4-funnel-analysis",t="GA4 and E-commerce Funnel Analysis",d="Session and funnel analysis from the GA4 BigQuery export to find conversion leakage and reconcile revenue.",
 ctx="An online store sees traffic rise while conversion rate falls, and the GA4 interface does not explain where users drop.",
 prob="The GA4 UI samples and thresholds data, sessions are hard to rebuild, and purchase revenue does not match the order system.",
 src=["GA4 BigQuery export (events_*)","Order system extract for revenue comparison"],
 arch="Raw events are flattened into a session table (user_pseudo_id + ga_session_id), then into a funnel table with one row per session and a flag for each step.",
 impl="Event parameters are unnested in SQL. Steps follow GA4 e-commerce events: view_item, add_to_cart, begin_checkout, purchase. Results are cut by device, channel and landing page.",
 sql="""-- session funnel (illustrative)
WITH s AS (
 SELECT user_pseudo_id,
  (SELECT value.int_value FROM UNNEST(event_params) WHERE key='ga_session_id') AS sid,
  event_name
 FROM `project.analytics_XXXX.events_*`
 WHERE _TABLE_SUFFIX BETWEEN '20260101' AND '20260131')
SELECT COUNTIF(event_name='view_item') AS viewed,
  COUNT(DISTINCT IF(event_name='add_to_cart', CONCAT(user_pseudo_id,sid), NULL)) AS carted,
  COUNT(DISTINCT IF(event_name='purchase', CONCAT(user_pseudo_id,sid), NULL)) AS purchased
FROM s;""",
 out=["Step-to-step conversion and drop-off by segment","GA4 purchase revenue versus orders by day"],
 find=["In this synthetic example, the largest drop is between cart and checkout on mobile.","Duplicate purchase events inflate GA4 revenue unless deduplicated by transaction_id."],
 rec=["Fix event duplication first, then prioritise the largest segment drop-off for testing.","Track a daily GA4-to-orders ratio as a health check."],
 lim="GA4 export excludes users who decline consent unless Consent Mode modelling is used, and modelled data is not in the export. Funnel steps depend on correct event implementation."),
dict(f="attribution-analysis",t="Marketing Attribution and Incrementality",d="Comparing first-touch, last-touch, linear and position-based attribution, and how incrementality testing differs.",
 ctx="A team wants to know how much each channel contributes to conversions, and whether paid channels create sales or only claim them.",
 prob="Different attribution rules give different channel credit. None of them proves a channel caused a sale.",
 src=["Session-level touchpoints with channel and timestamp (GA4 export)","Conversions from the order system"],
 arch="Touchpoints are joined to conversions within a lookback window to create one path per conversion, then credit is assigned by each model.",
 impl="SQL assigns credit: first touch 100% to the first channel, last touch 100% to the last, linear equal split, position-based 40/20/40 style splits. Results are compared side by side.",
 sql="""-- linear credit (illustrative)
SELECT channel, SUM(1.0/path_len) AS linear_credit
FROM conversion_paths, UNNEST(touch_channels) AS channel
GROUP BY channel;""",
 out=["Channel credit table under four models","Rank-change view showing which channels depend on the model chosen"],
 find=["In the synthetic data, upper-funnel channels gain credit under first-touch and linear, while branded search gains under last-touch."],
 rec=["Use attribution to describe the journey, not to prove value.","Use geo or holdout experiments with a pre-set sample size, confidence interval and decision threshold to measure incrementality for the largest budget lines."],
 lim="Modelled attribution is correlational. Incrementality requires a control group (geo holdout, conversion lift or randomised test) and measures the causal effect. These are separate methods and should not be reported as the same thing."),
dict(f="reporting-automation",t="Automated Marketing Reporting Infrastructure",d="Python and SQL pipelines into BigQuery with validation checks, feeding Power BI and Looker Studio.",
 ctx="Weekly reporting is assembled manually from platform exports and spreadsheets, which is slow and error-prone.",
 prob="Manual steps create version errors, delay decisions and make it hard to trust or audit figures.",
 src=["Advertising platform exports or APIs","GA4 BigQuery export","Order data"],
 arch="Python ingestion writes raw tables to BigQuery, SQL (or dbt) builds staging and mart layers, validation tests run, and BI tools read only the mart layer.",
 impl="A scheduled job (GitHub Actions or Cloud Scheduler) runs ingestion, then transformations, then checks for row counts, null keys, duplicate ids and spend-versus-source totals. Failures send an alert.",
 sql="""-- validation check (illustrative)
SELECT 'duplicate_orders' AS check, COUNT(*) AS failures
FROM (SELECT order_id FROM stg_orders GROUP BY 1 HAVING COUNT(*)>1);""",
 out=["Power BI and Looker Studio dashboards on a single mart","Daily data-quality log"],
 find=["Validation catches schema changes and duplicate loads before they reach dashboards."],
 rec=["Version SQL in Git, document metric definitions, and keep one definition of each KPI."],
 lim="Time saved depends on how manual the starting process was. This page describes the method; reported results are on the homepage and need verification before use in applications."),
]
os.makedirs("projects",exist_ok=True)
def li(x): return "<ul>"+"".join(f"<li>{html.escape(i)}</li>" for i in x)+"</ul>"
for c in cases:
    p="../"
    body=head(c['t']+" | "+NAME,c['d'],p,"projects/"+c['f']+".html")
    body+=f'''<section class="wrap case"><a class="back" href="../index.html#projects">Back to projects</a><h1>{c['t']}</h1><p class="lede">{c['d']}</p>
<p class="note">{SYN}</p>
<h2>Business context</h2><p>{c['ctx']}</p><h2>Problem statement</h2><p>{c['prob']}</p>
<h2>Data sources</h2>{li(c['src'])}<h2>Data architecture</h2><p>{c['arch']}</p>
<h2>Technical implementation</h2><p>{c['impl']}</p><h2>SQL methodology</h2><pre><code>{html.escape(c['sql'])}</code></pre>
<h2>Analytical outputs</h2>{li(c['out'])}<h2>Key findings</h2>{li(c['find'])}<h2>Business recommendations</h2>{li(c['rec'])}
<h2>Limitations and assumptions</h2><p>{c['lim']}</p></section>'''
    open(f"projects/{c['f']}.html","w").write(body+foot(p))

# ---------- home ----------
def svg():
    def box(x,y,w,h,t,s=""): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" class="bx"/><text x="{x+12}" y="{y+22}" class="t1">{t}</text><text x="{x+12}" y="{y+40}" class="t2">{s}</text>'
    src=box(10,20,150,52,"Advertising platforms","Spend, clicks")+box(10,110,150,52,"Website analytics","GA4 sessions, events")+box(10,200,150,52,"E-commerce orders","Net revenue")
    mid='<rect x="215" y="85" width="130" height="102" rx="6" class="core"/><text x="280" y="125" text-anchor="middle" class="t1w">Unified</text><text x="280" y="143" text-anchor="middle" class="t1w">measurement layer</text><text x="280" y="164" text-anchor="middle" class="t2w">SQL, Python, BigQuery</text>'
    out=box(400,10,150,50,"Channel performance")+box(400,78,150,50,"Revenue analysis")+box(400,146,150,50,"Profitability")+box(400,214,150,50,"Budget allocation")
    lines="".join(f'<path d="M160 {y} C190 {y},190 136,215 136" class="ln"/>' for y in (46,136,226))+"".join(f'<path d="M345 136 C375 136,375 {y},400 {y}" class="ln"/>' for y in (35,103,171,239))
    return f'<svg viewBox="0 0 560 275" role="img" aria-label="Diagram: advertising platforms, website analytics and e-commerce orders feed a unified measurement layer that produces channel performance, revenue analysis, profitability and budget allocation insights.">{lines}{src}{mid}{out}</svg>'
svc=[("chart-column","Marketing Analytics","Channel, campaign and keyword efficiency tied to margin, with budget recommendations.",["CAC, CPA, MER, ROAS, ACoS","Contribution margin analysis","Ad spend leakage","Budget allocation"],"SQL, Python, Excel"),
("git-merge","Measurement and Attribution","Tracking audits and reconciliation of platform, GA4 and order data. Amazon is reconciled at campaign, ASIN and channel level, because marketplace reports do not give customer-level visibility.",["GA4 and GTM audits, Consent Mode","Server-side tagging","Conversion tracking validation","Funnel, cohort and attribution models"],"GA4, GTM, BigQuery"),
("flask-conical","Experimentation and Incrementality","Test design that separates causal lift from modelled attribution.",["A/B and geographic experiments","Conversion lift","Significance and confidence intervals","Sizing and test design"],"Python, SQL"),
("database","Reporting Infrastructure","Pipelines and dashboards that replace manual reporting.",["SQL and Python pipelines, dbt","BigQuery and GA4 export","Validation and automation","Power BI, Looker Studio"],"BigQuery, Power BI, Looker Studio")]
sv="".join(f'<article class="card"><i data-lucide="{i}"></i><h3>{t}</h3><p>{d}</p>{li(b)}<p class="tech">{k}</p></article>' for i,t,d,b,k in svc)
res=[("18%","Reduced wasted advertising spend through negative keyword restructuring and match-type budget optimization."),("25%","Improved advertising profitability through keyword and bid analysis. This refers to advertising profitability, not overall company profit."),("40 hours / month","Saved through automation of manual reporting workflows.")]
rs="".join(f'<div class="res"><strong>{a}</strong><p>{b}</p></div>' for a,b in res)
pj="".join(f'<a class="card pj" href="projects/{c["f"]}.html"><h3>{c["t"]}</h3><p>{c["d"]}</p><span class="more">Read case study</span></a>' for c in cases)
tk=[("Data and programming","SQL, Python, Pandas, NumPy, Git"),("Engineering and warehousing","Google BigQuery, dbt, Python pipelines, GA4 BigQuery export"),("Measurement and tracking","GA4, Google Tag Manager, Consent Mode, server-side tagging"),("Advertising platforms","Amazon Ads, Google Ads, Meta Ads"),("E-commerce","Shopify, Amazon Marketplace"),("Business intelligence","Power BI, Looker Studio, Excel, Google Sheets")]
tkh="".join(f'<div><h3>{a}</h3><p>{b}</p></div>' for a,b in tk)
home=head("Marketing Data Analyst | Marketing Measurement and E-commerce Analytics","Marketing Data Analyst with 5+ years in paid media. GA4 BigQuery analytics, Amazon advertising analytics, marketing attribution and reporting automation.","","index.html")
home+=f'''<section id="home" class="wrap hero"><div><p class="role">Marketing Data Analyst | Marketing Measurement | E-commerce Analytics</p><h1>{H1}</h1>
<p class="lede">With 5+ years in paid media and e-commerce analytics, I connect advertising, website, and order data to build reliable measurement systems and actionable performance reporting.</p>
<div class="cta"><a class="btn" href="#projects">View My Work</a><a class="btn ghost" href="mailto:{EMAIL}?subject=Analytics%20enquiry">Let's Discuss Your Analytics</a></div></div>
<div class="viz">{svg()}</div></section>
<section id="expertise" class="band"><div class="wrap"><h2>What I do</h2><div class="grid4">{sv}</div></div></section>
<section id="results" class="wrap"><h2>Selected results</h2><div class="grid3">{rs}</div><p class="small">Selected results from US e-commerce client work. Figures come from separate engagements and are not one client's combined outcome.</p></section>
<section id="projects" class="band"><div class="wrap"><h2>Selected projects</h2><p class="small">Case studies use synthetic, illustrative data and describe method, not client outcomes.</p><div class="grid3">{pj}</div></div></section>
<section id="about" class="wrap about"><div class="photo" role="img" aria-label="Profile photo placeholder">Photo</div><div><h2>About</h2>
<p>I bring together hands-on paid media experience and technical marketing analytics.</p><p>Having managed Amazon Ads and Google Ads accounts, I understand how advertising platforms generate their reported metrics, where measurement gaps occur, and why platform-reported performance can differ from actual business results.</p>
<p>My work focuses on connecting advertising, website analytics, and sales data through SQL, Python, and BigQuery, helping businesses make more informed decisions about channel performance, profitability, and marketing investment.</p>
<p><a class="btn small" href="assets/documents/CV.pdf" download>Download CV</a> <a class="btn small ghost" href="{LI}">LinkedIn</a> <a class="btn small ghost" href="{GH}">GitHub</a></p></div></section>
<section class="band"><div class="wrap"><h2>Technical toolkit</h2><div class="grid3 tk">{tkh}</div></div></section>
<section id="contact" class="wrap contact"><h2>Better marketing decisions start with reliable measurement.</h2><p class="lede">If you're looking to reconcile marketing performance, improve measurement infrastructure, automate reporting, or understand what's actually driving revenue, let's connect.</p>
<p><a class="btn" href="mailto:{EMAIL}">{EMAIL}</a> <a class="btn ghost" href="tel:{PHONE}">{PHONE_D}</a> <a class="btn ghost" href="{LI}">LinkedIn</a> <a class="btn ghost" href="{GH}">GitHub</a> <a class="btn ghost" href="assets/documents/CV.pdf" download>Download CV</a></p></section>'''
open("index.html","w").write(home+foot(""))

# ---------- assets ----------
os.makedirs("assets/css",exist_ok=True);os.makedirs("assets/js",exist_ok=True);os.makedirs("assets/documents",exist_ok=True);os.makedirs("assets/images",exist_ok=True)
open("assets/css/style.css","w").write(''':root{--bg:#fff;--surf:#f4f6f9;--ink:#0d1b2e;--mut:#556070;--acc:#1e56d6;--line:#dfe4ec}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:72px}
body{margin:0;font-family:Manrope,system-ui,-apple-system,Segoe UI,sans-serif;color:var(--ink);background:var(--bg);line-height:1.65}
.wrap{max-width:1120px;margin:0 auto;padding-left:24px;padding-right:24px}.skip{position:absolute;left:-999px}.skip:focus{left:8px;top:8px;background:#fff;padding:8px;z-index:99}
a{color:var(--acc)}a:focus-visible,button:focus-visible{outline:3px solid var(--acc);outline-offset:2px}
.nav{position:sticky;top:0;background:rgba(255,255,255,.96);border-bottom:1px solid var(--line);z-index:10}
.nav-in{display:flex;align-items:center;justify-content:space-between;height:64px}.brand{font-weight:800;color:var(--ink);text-decoration:none}
nav{display:flex;gap:22px;align-items:center}nav a{color:var(--ink);text-decoration:none;font-weight:500;font-size:.95rem}nav a:hover{color:var(--acc)}
.burger{display:none;background:none;border:0;color:var(--ink);cursor:pointer}
.btn{display:inline-block;background:var(--acc);color:#fff!important;padding:12px 22px;border-radius:6px;font-weight:700;text-decoration:none;margin:4px 6px 4px 0;border:1px solid var(--acc)}
.btn.ghost{background:#fff;color:var(--acc)!important}.btn.small{padding:8px 16px;font-size:.9rem}
h1{font-size:clamp(1.9rem,3.6vw,2.7rem);line-height:1.2;letter-spacing:-.02em;margin:.4em 0}h2{font-size:1.9rem;letter-spacing:-.01em;margin:0 0 24px}h3{margin:.6em 0 .3em}
.hero{display:grid;grid-template-columns:1.1fr 1fr;gap:48px;align-items:center;padding-top:72px;padding-bottom:72px}
.role{color:var(--acc);font-weight:700;font-size:.9rem;margin:0}.lede{color:var(--mut);font-size:1.1rem;max-width:62ch}
.viz{background:var(--surf);border:1px solid var(--line);border-radius:10px;padding:16px}.viz svg{width:100%;height:auto}
.bx{fill:#fff;stroke:#c9d2e0}.core{fill:var(--ink)}.ln{fill:none;stroke:#8aa3d6;stroke-width:1.5}
.t1{font:700 12px Manrope,sans-serif;fill:#0d1b2e}.t2{font:400 11px Manrope,sans-serif;fill:#556070}.t1w{font:700 13px Manrope,sans-serif;fill:#fff}.t2w{font:400 11px Manrope,sans-serif;fill:#c8d4ee}
section{padding:64px 0}.hero{padding-top:72px;padding-bottom:72px}.band{background:var(--surf)}
.grid4{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.card{background:#fff;border:1px solid var(--line);border-radius:8px;padding:24px;box-shadow:0 1px 2px rgba(13,27,46,.05);text-decoration:none;color:var(--ink);display:block}
.card ul,.case ul{padding-left:18px;color:var(--mut)}.card svg{color:var(--acc)}.tech{font-size:.85rem;color:var(--mut);border-top:1px solid var(--line);padding-top:10px}
.pj:hover{border-color:var(--acc)}.more{color:var(--acc);font-weight:700}.pj p{color:var(--mut)}
.res strong{font-size:2.4rem;color:var(--acc);display:block;letter-spacing:-.02em}.res p{color:var(--mut)}.small{color:var(--mut);font-size:.9rem}
.about{display:grid;grid-template-columns:220px 1fr;gap:40px;align-items:start}.photo{aspect-ratio:1;background:var(--surf);border:1px dashed #aab4c5;display:grid;place-items:center;color:var(--mut);border-radius:8px}
.tk p{color:var(--mut);margin:0}.contact{text-align:left}
.case{max-width:780px;padding-top:40px}.case h2{font-size:1.3rem;margin:32px 0 8px}.back{font-weight:600}.note{background:#fff7e0;border:1px solid #ecd58a;padding:10px 14px;border-radius:6px;font-size:.92rem}
pre{background:#0d1b2e;color:#e6ecf7;padding:16px;border-radius:8px;overflow-x:auto;font-size:.85rem}
footer{border-top:1px solid var(--line);padding:24px 0;color:var(--mut);font-size:.9rem}.foot{display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px}
@media(max-width:860px){.hero,.about{grid-template-columns:1fr}.grid4,.grid3{grid-template-columns:1fr}.burger{display:block}
nav{display:none;position:absolute;top:64px;left:0;right:0;background:#fff;flex-direction:column;align-items:flex-start;padding:16px 24px;border-bottom:1px solid var(--line)}nav.open{display:flex}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}''')
open("assets/js/main.js","w").write('''if(window.lucide)lucide.createIcons();
const b=document.querySelector(".burger"),m=document.getElementById("menu");
b.addEventListener("click",()=>{const o=m.classList.toggle("open");b.setAttribute("aria-expanded",o)});
m.querySelectorAll("a").forEach(a=>a.addEventListener("click",()=>{m.classList.remove("open");b.setAttribute("aria-expanded","false")}));''')
open("favicon.svg","w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="6" fill="#0d1b2e"/><path d="M7 22l6-7 5 4 7-10" stroke="#5b8cff" stroke-width="3" fill="none"/></svg>')
open("robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
urls=["index.html"]+["projects/"+c['f']+".html" for c in cases]
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{SITE}/{u}</loc></url>" for u in urls)+"</urlset>")
open("README.md","w").write(f'''# Marketing Data Analyst Portfolio
Static site (HTML, CSS, JS). No build step needed to host.

## Before publishing
1. Search and replace `Your Name`, `you@example.com`, the LinkedIn and GitHub URLs, and `https://adnan3624.github.io` (also in sitemap.xml and robots.txt).
2. Put your CV at `assets/documents/CV.pdf`.
3. Replace the profile photo placeholder in the About section with an image in `assets/images/`.
4. Confirm the three results on the homepage before sharing.

## Deploy on GitHub Pages
1. On github.com click New repository, name it `portfolio` (or `your-username.github.io` for a root URL), set it Public, create it.
2. Upload every file and folder from this project (Add file > Upload files), then commit to `main`.
3. Open Settings > Pages. Under Build and deployment choose Deploy from a branch, branch `main`, folder `/ (root)`, Save.
4. After about a minute the site is live at `https://adnan3624.github.io/`. Open every page and the CV download.
5. To update: edit files on GitHub or push from Git. Pages redeploys on each commit.

`build.py` regenerates all HTML (edit the content at the top, run `python3 build.py`).
''')

open("assets/documents/.gitkeep","w").write("");open("assets/images/.gitkeep","w").write("")

# ---------- illustrative images (synthetic) ----------
W,Hh=800,420; C=["#1e56d6","#7ea0ea","#0d1b2e","#b7c4dc"]
def wrap_svg(title,sub,inner,desc):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Hh}" role="img" aria-label="{desc}"><rect width="{W}" height="{Hh}" fill="#fff"/><text x="30" y="38" font-family="Arial,sans-serif" font-size="18" font-weight="700" fill="#0d1b2e">{title}</text><text x="30" y="58" font-family="Arial,sans-serif" font-size="12" fill="#556070">{sub}</text>{inner}<text x="{W-30}" y="{Hh-14}" text-anchor="end" font-family="Arial,sans-serif" font-size="11" fill="#556070">Synthetic data for illustration</text></svg>'
def T(x,y,s,a="middle",sz=12,col="#556070",w=400): return f'<text x="{x}" y="{y}" text-anchor="{a}" font-family="Arial,sans-serif" font-size="{sz}" fill="{col}" font-weight="{w}">{s}</text>'
def grouped(title,sub,cats,series,vals,ymax,fmt,desc,line=None):
    x0,x1,y0,y1=70,770,90,340; o=""
    for i in range(5):
        y=y1-(y1-y0)*i/4; o+=f'<line x1="{x0}" x2="{x1}" y1="{y}" y2="{y}" stroke="#e3e8f0"/>'+T(x0-8,y+4,fmt.format(ymax*i/4),"end",11)
    gw=(x1-x0)/len(cats); bw=min(34,(gw-30)/len(series))
    for ci,c in enumerate(cats):
        gx=x0+gw*ci+gw/2-bw*len(series)/2
        for si in range(len(series)):
            h=(y1-y0)*vals[si][ci]/ymax; o+=f'<rect x="{gx+si*bw:.1f}" y="{y1-h:.1f}" width="{bw-3:.1f}" height="{h:.1f}" fill="{C[si]}"/>'
        o+=T(x0+gw*ci+gw/2,y1+20,c)
    if line is not None:
        y=y1-(y1-y0)*line[0]/ymax; o+=f'<line x1="{x0}" x2="{x1}" y1="{y}" y2="{y}" stroke="#0d1b2e" stroke-dasharray="6 4"/>'+T(x1,y-6,line[1],"end",11,"#0d1b2e",700)
    if len(series)>1 or series[0]:
        for si,s in enumerate(series):
            if s: o+=f'<rect x="{30+si*165}" y="372" width="12" height="12" fill="{C[si]}"/>'+T(48+si*165,383,s,"start")
    return wrap_svg(title,sub,o,desc)
imgs={}
imgs["cross-channel-measurement"]=grouped("Revenue by source and channel","Platform-reported vs GA4 vs orders, thousands of dollars",["Google Shopping","Google Search","Meta Ads"],["Platform-reported","GA4","Orders"],[[120,90,110],[95,72,70],[82,66,58]],160,"{:.0f}","Bar chart: platform-reported revenue is higher than GA4 revenue, which is higher than order revenue, for each channel.")
imgs["amazon-ads-analytics"]=grouped("ACoS by campaign type","Against a target ACoS of 25 percent",["Auto","Broad","Phrase","Exact","Brand"],[""],[[38,31,26,19,14]],40,"{:.0f}%","Bar chart of ACoS by campaign type with a dashed target line at 25 percent.",line=(25,"Target 25%"))
imgs["attribution-analysis"]=grouped("Channel credit by attribution model","Share of conversions, percent",["Paid social","Paid search","Email","Organic"],["First touch","Last touch","Linear","Position-based"],[[34,18,6,42],[12,38,22,28],[24,27,15,34],[26,28,14,32]],48,"{:.0f}%","Grouped bar chart showing how channel credit changes between first-touch, last-touch, linear and position-based attribution.")
steps=[("Item views",10000),("Add to cart",1800),("Begin checkout",900),("Purchase",420)]; o=""
for i,(n,v) in enumerate(steps):
    w=620*v/10000+80; y=90+i*66; o+=f'<rect x="30" y="{y}" width="{w:.0f}" height="46" fill="{C[0] if i<3 else C[2]}" opacity="{1-i*0.12}"/>'+T(42,y+28,f"{n}","start",14,"#fff",700)+T(30+w+10,y+28,f"{v:,}"+("" if i==0 else f"  ({v/steps[i-1][1]*100:.0f}% of previous step)"),"start",13,"#0d1b2e",600)
imgs["ga4-funnel-analysis"]=wrap_svg("Session funnel","GA4 e-commerce events, one month, sessions",o,"Funnel chart from item views through add to cart and checkout to purchase.")
boxes=["Ad platforms, GA4 export, orders","Python ingestion","BigQuery raw tables","SQL and dbt marts","Validation checks","Power BI and Looker Studio"]; o=""
for i,b in enumerate(boxes):
    x=24+i*125; fill="#0d1b2e" if i==3 else "#fff"; col="#fff" if i==3 else "#0d1b2e"
    o+=f'<rect x="{x}" y="170" width="112" height="80" rx="6" fill="{fill}" stroke="#c9d2e0"/>'
    ws=b.split(); lines=[" ".join(ws[:len(ws)//2+len(ws)%2])," ".join(ws[len(ws)//2+len(ws)%2:])]
    for j,l in enumerate(lines):
        if l: o+=T(x+56,205+j*16,l,"middle",11.5,col,700)
    if i<5: o+=f'<path d="M{x+112} 210 L{x+125} 210" stroke="#1e56d6" stroke-width="2"/>'
imgs["reporting-automation"]=wrap_svg("Reporting pipeline","From source extracts to dashboards, with checks before publishing",o,"Pipeline diagram: sources, Python ingestion, BigQuery raw tables, SQL and dbt marts, validation checks, and dashboards.")
for k,v in imgs.items(): open(f"assets/images/{k}.svg","w").write(v)
# inject images into pages
import re
for c in cases:
    f=f"projects/{c['f']}.html"; s=open(f).read()
    if "<figure" not in s:
        s=s.replace('<h2>Business context</h2>',f'<figure><img src="../assets/images/{c["f"]}.svg" alt="{c["t"]}: illustrative chart using synthetic data" width="800" height="420"><figcaption>Illustrative chart built from synthetic data, not client results.</figcaption></figure><h2>Business context</h2>',1)
        open(f,"w").write(s)
s=open("index.html").read()
for c in cases:
    s=s.replace(f'<a class="card pj" href="projects/{c["f"]}.html"><h3>',f'<a class="card pj" href="projects/{c["f"]}.html"><img class="thumb" src="assets/images/{c["f"]}.svg" alt="" width="800" height="420" loading="lazy"><h3>',1)
s=s.replace('aria-label="Profile photo placeholder">Photo</div>','aria-label="Profile photo placeholder">Photo<img src="assets/images/profile.jpg" alt="Portrait of Adnan Rana" onerror="this.remove()"></div>',1)
open("index.html","w").write(s)
open("assets/css/style.css","a").write('\n.thumb,figure img{width:100%;height:auto;border:1px solid var(--line);border-radius:6px;display:block}.thumb{margin-bottom:14px}figure{margin:24px 0}figcaption{font-size:.85rem;color:var(--mut);margin-top:6px}.photo{position:relative;overflow:hidden}.photo img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}\n')
