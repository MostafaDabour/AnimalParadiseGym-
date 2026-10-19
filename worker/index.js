// Animal Paradise Gyms: static site + parent consent waiver API.
// Static pages are served straight from ./dist. Only /api/* runs this code (see run_worker_first in wrangler.jsonc).
import { AGREEMENT_HTML, AGREEMENT_SHA256 } from "./agreement.js";

const REQUIRED = ["parent_first", "parent_last", "parent_phone", "parent_email", "minor_first", "minor_last",
  "minor_dob", "minor_phone", "minor_email", "address1", "city", "state", "postal", "sms_ok", "email_ok"];
const MAX_BODY = 600_000; // bytes, signature PNG included

const json = (obj, status = 200) => new Response(JSON.stringify(obj), {
  status, headers: { "content-type": "application/json", "cache-control": "no-store" } });
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const clean = (s, n = 200) => String(s ?? "").replace(/[\u0000-\u001f]/g, " ").trim().slice(0, n);

function validPng(dataUrl) {
  const m = /^data:image\/png;base64,([A-Za-z0-9+/=]+)$/.exec(dataUrl || "");
  if (!m) return null;
  const bin = atob(m[1]);
  if (bin.length < 200 || bin.slice(1, 4) !== "PNG") return null;
  const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
  return bytes;
}

function signedCopy(r, sigUrl) {
  const row = (k, v) => `<tr><th>${esc(k)}</th><td>${esc(v)}</td></tr>`;
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>Signed waiver: ${esc(r.minor_first)} ${esc(r.minor_last)}</title>
<style>body{font:15px/1.6 system-ui,sans-serif;color:#1a1814;max-width:820px;margin:32px auto;padding:0 20px}
h1{font-size:22px;margin:0 0 4px}h2.wv-title{font-size:17px}h3{font-size:15px;margin:18px 0 4px}
table{border-collapse:collapse;width:100%;margin:16px 0}th,td{border:1px solid #ddd;padding:7px 10px;text-align:left;vertical-align:top}
th{width:38%;background:#f6f3ec}.box{border:1px solid #ddd;border-radius:8px;padding:6px 18px;margin:18px 0}
.sig{border:1px solid #ccc;border-radius:8px;max-width:420px;width:100%;background:#fff}.meta{color:#666;font-size:13px}
@media print{.noprint{display:none}}</style></head><body>
<p class="noprint"><button onclick="print()">Print or save as PDF</button></p>
<h1>Parent Consent Waiver, signed</h1>
<p class="meta">Animal Paradise Gyms, 3849 S Delsea Dr, Suite E000, Vineland, NJ 08360 · Record ${esc(r.id)}</p>
<table>
${row("Parent or guardian", `${r.parent_first} ${r.parent_last}`)}${row("Parent phone", r.parent_phone)}${row("Parent email", r.parent_email)}
${row("Minor", `${r.minor_first} ${r.minor_last}`)}${row("Minor date of birth", r.minor_dob)}${row("Minor phone", r.minor_phone)}${row("Minor email", r.minor_email)}
${row("Address", [r.address1, r.address2, r.city, r.state, r.postal].filter(Boolean).join(", "))}
${row("Text notifications", r.sms_ok)}${row("Email notifications", r.email_ok)}
${row("Agreed to terms", "Yes")}${row("Signed (UTC)", r.signed_at)}${row("Signed (gym time)", r.signed_local)}
</table>
<p><b>Signature</b></p><img class="sig" src="${sigUrl}" alt="Signature of ${esc(r.parent_first)} ${esc(r.parent_last)}">
<div class="box">${AGREEMENT_HTML}</div>
<p class="meta">Agreement version (SHA-256) ${AGREEMENT_SHA256}<br>IP ${esc(r.ip)} · ${esc(r.country)} · ${esc(r.user_agent)}</p>
</body></html>`;
}

async function submit(request, env) {
  const len = +request.headers.get("content-length") || 0;
  if (len > MAX_BODY) return json({ ok: false, error: "Signature image is too large. Please clear it and sign again." }, 413);
  let b;
  try { b = await request.json(); } catch { return json({ ok: false, error: "Something went wrong. Please try again." }, 400); }
  if (b.website) return json({ ok: true }); // honeypot: pretend success

  const r = {};
  for (const k of [...REQUIRED, "address2"]) r[k] = clean(b[k]);
  const missing = REQUIRED.filter((k) => !r[k]);
  if (missing.length) return json({ ok: false, error: "Please fill in every field.", missing }, 400);
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(r.parent_email)) return json({ ok: false, error: "Please check the parent email address.", missing: ["parent_email"] }, 400);
  if (b.agree !== true) return json({ ok: false, error: "Please tick the box to agree to the terms.", missing: ["agree"] }, 400);
  const png = validPng(b.signature);
  if (!png) return json({ ok: false, error: "Please sign in the signature box.", missing: ["signature"] }, 400);

  const now = new Date();
  r.id = `${now.toISOString().slice(0, 10)}-${crypto.randomUUID()}`;
  r.signed_at = now.toISOString();
  r.signed_local = now.toLocaleString("en-US", { timeZone: "America/New_York", dateStyle: "long", timeStyle: "short" }) + " ET";
  r.ip = request.headers.get("cf-connecting-ip") || "";
  r.country = request.cf?.country || "";
  r.user_agent = clean(request.headers.get("user-agent"), 300);
  r.agreement_sha256 = AGREEMENT_SHA256;

  const origin = new URL(request.url).origin;
  const copyUrl = `${origin}/api/waiver/${r.id}`;
  const base = `waivers/${r.id}`;
  await env.WAIVERS.put(`${base}/signature.png`, png, { httpMetadata: { contentType: "image/png" } });
  await env.WAIVERS.put(`${base}/record.json`, JSON.stringify(r, null, 2), { httpMetadata: { contentType: "application/json" } });
  const sigData = `data:image/png;base64,${b.signature.split(",")[1]}`;
  await env.WAIVERS.put(`${base}/signed-waiver.html`, signedCopy(r, sigData), { httpMetadata: { contentType: "text/html; charset=utf-8" } });

  // hand the contact to GHL; the waiver is already safe in storage even if this fails
  if (env.WAIVER_WEBHOOK) {
    const payload = {
      form: "parent-consent-waiver", source: "website", tags: "waiver-signed",
      first_name: r.parent_first, last_name: r.parent_last, full_name: `${r.parent_first} ${r.parent_last}`,
      email: r.parent_email, phone: r.parent_phone,
      address1: r.address1, address2: r.address2, city: r.city, state: r.state, postal_code: r.postal, country: "US",
      minor_name: `${r.minor_first} ${r.minor_last}`, minor_first_name: r.minor_first, minor_last_name: r.minor_last,
      minor_dob: r.minor_dob, minor_phone: r.minor_phone, minor_email: r.minor_email,
      sms_notifications: r.sms_ok, email_notifications: r.email_ok,
      waiver_signed_at: r.signed_at, waiver_signed_local: r.signed_local, waiver_url: copyUrl, waiver_id: r.id,
    };
    try {
      await fetch(env.WAIVER_WEBHOOK, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(payload) });
    } catch (e) { console.log("webhook failed", r.id, String(e)); }
  }
  return json({ ok: true, id: r.id });
}

async function view(id, env) {
  if (!/^\d{4}-\d{2}-\d{2}-[0-9a-f-]{36}$/.test(id)) return new Response("Not found", { status: 404 });
  const obj = await env.WAIVERS.get(`waivers/${id}/signed-waiver.html`);
  if (!obj) return new Response("Not found", { status: 404 });
  return new Response(obj.body, { headers: { "content-type": "text/html; charset=utf-8", "cache-control": "private, no-store",
    "x-robots-tag": "noindex, nofollow", "referrer-policy": "no-referrer" } });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/waiver" && request.method === "POST") return submit(request, env);
    const m = url.pathname.match(/^\/api\/waiver\/([^/]+)$/);
    if (m && request.method === "GET") return view(m[1], env);
    if (url.pathname.startsWith("/api/")) return json({ ok: false, error: "Not found" }, 404);
    return env.ASSETS.fetch(request);
  },
};
