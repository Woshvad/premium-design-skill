#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_check.py - render a page in headless Chrome/Edge at fixed viewports and measure what a static scan can't.

Part of the premium-design skill (SKILL.md workflow step 6). slop_check.py reads source code; this script loads
the page in a real browser and measures the rendered result. A clean slop_check is the floor, not evidence of
quality: in testing, pages that scanned clean still had 3-line H1s, 8px SVG labels, horizontal overflow at 320px
and 92-character lines. The reverse also holds: in a blind test, pages that passed both checkers lost to pages that
failed them on display scale, product imagery and brand presence, so read the screenshots, not only the exit code.
Python 3.8+, standard library only (it speaks the Chrome DevTools Protocol itself).

Usage
    python3 render_check.py PAGE [--surface marketing|product|dashboard|native|docs] [--out DIR]
                            [--sizes 320x640,390x844,1440x900] [--no-shots] [--json] [--chrome PATH]
    (use "python" on Windows.) PAGE is a local .html file or an http(s) URL (a dev server). Exit 0 = no FAIL,
    1 = at least one FAIL, 2 = could not run (no browser found, page did not load).

What it does
    Opens a throwaway browser profile in a short temp folder (never your own profile), emulates each viewport
    at its exact layout width (no 500px window minimum, no file:// iframe tricks, no shrink-to-fit, so overflow
    shows as overflow), reloads the page at that size, waits for fonts
    and about 1.2s of settling (entrance motion), then measures. The default sizes are 320x640, 375x667,
    390x844, 768x1024, 1024x768 and 1440x900. Screenshots of the first viewport at 320, 390 and 1440 are saved
    plain and as a greyscale 10px blur (the squint/blur test) to --out (default: a new temp folder; the path is
    printed). Open them with your image viewer or Read tool. Every pass runs with prefers-color-scheme: light
    (headless Chrome would otherwise follow the OS theme); one extra load at the widest size runs dark, and when
    the page has a dark theme a -dark screenshot is saved and its section grounds are compared with light.

FAIL (exit 1) - each is a rule in SKILL.md
    overflow      document wider than the viewport at any size (checklist: no horizontal scroll 320-1440).
    h1-lines      hero H1 above 2 lines at 1280px+ or above 3 lines below that (a 4-line H1 is a size error [2]).
    h1-font       the H1's first font family is a web font that did not load (the page shows a fallback).
    small-text    rendered HTML text under 12px (11px with --surface native, the iOS floor), or SVG <text>
                  whose rendered size (font-size x drawing scale) is under that at any size (SVG units shrink
                  with the drawing).
    measure       paragraphs averaging over 90 characters per line (research range 45-90, target about 65).
    cls           cumulative layout shift during load at or above 0.1.
    viewport      no width=device-width viewport meta (phones would show a zoomed-out desktop layout).
    anchors       an in-page link (href="#x") whose id is missing or shared by several elements (an SVG <symbol>
                  with the same id as a section swallows the nav link).
    rotated-text  a block holding 200+ characters of text rotated by 0.2deg or more: a tilted menu, card or sheet
                  renders soft at 1x and reads as a gimmick (synthesis of the [5] rotated-text tell).
CHECK (reported, no exit code) - look at the screenshot and decide
    h1-breaks     the H1's line-by-line text at each size, flagged when a sentence ends mid-line.
    first-view    (marketing) the largest visual's share of the first viewport at each size; flagged under 25%
                  of the viewport height at 320x640, 375x667 and 390x844 (synthesis threshold) or when the H1
                  starts below the fold.
    display-ratio largest text size / body size at 1440 (marketing wants one display size at least 3x body).
    muted-share   share of running-text words set in a lower-contrast (muted) colour than the ink on the same
                  ground; flagged above 50% (synthesis: leads, story paragraphs and instructions stay full ink).
    text-edges    two different left text edges inside one column band of one section at 1440 (one shared
                  text edge per section). Skipped for native, where inset grouped lists indent by convention.
    repeat-facts  the same number+unit (26 cm, 2.6 kg, 14 days) appearing twice in one section, SVG labels
                  included (removal pass: no fact twice per section).
    inverted      share of page height on a ground inverted against the body (dark band on a light page).
    section-scale (marketing) median H2 under 2x body at 1440: section heads read as labels beside their leads.
    dead-column   at 1024px+, a top-aligned column whose content ends 160px+ (and a quarter of the row) above its
                  neighbour's, with no box of its own: a hole in the page ground (synthesis threshold). Label
                  rails under a quarter of the row width and vertically centred columns are skipped.
    orphans       a heading or lead (1.15x body or more, 4+ words) whose last line is one word or under a fifth
                  of its longest line; fix with text-wrap: balance (headings) or pretty (leads), or rewrite.
    dark-grounds  (pages with a dark theme) a band that is its own ground in light (3:1+ against the page) but
                  under 1.3:1 in dark, or a dark theme where no section keeps its own ground.
    heading-font  an H1-H3 whose first family is a system-stack name (-apple-system, system-ui): it renders as
                  whatever comes next in the stack on non-Apple machines.
    fonts         every web font face and its load status.
Limits: hover, click, keyboard and scroll-driven states are not exercised; do those by hand. Thresholds marked
synthesis are calibration for a review, not research values.
"""

from __future__ import print_function

import argparse
import base64
import json
import os
import re
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import time

try:
    from urllib.request import urlopen
    from urllib.parse import urlparse
except ImportError:  # pragma: no cover
    from urllib2 import urlopen  # type: ignore
    from urlparse import urlparse  # type: ignore

DEFAULT_SIZES = '320x640,375x667,390x844,768x1024,1024x768,1440x900'
SHOT_WIDTHS = (320, 390, 1440)

CHROME_CANDIDATES = [
    os.environ.get('CHROME_PATH', ''),
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
    os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe'),
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
]
CHROME_NAMES = ['google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser', 'chrome', 'msedge',
                'microsoft-edge']


def find_chrome(explicit=None):
    if explicit:
        return explicit if os.path.isfile(explicit) else None
    for p in CHROME_CANDIDATES:
        if p and os.path.isfile(p):
            return p
    for n in CHROME_NAMES:
        p = shutil.which(n)
        if p:
            return p
    return None


# --------------------------------------------------------------------------------------
# Minimal WebSocket + DevTools client (standard library only)
# --------------------------------------------------------------------------------------

class WebSocket(object):
    def __init__(self, url, timeout=30):
        m = re.match(r'ws://([^/:]+):(\d+)(/.*)$', url)
        if not m:
            raise IOError('bad websocket url %s' % url)
        host, port, path = m.group(1), int(m.group(2)), m.group(3)
        self.sock = socket.create_connection((host, port), timeout=timeout)
        key = base64.b64encode(os.urandom(16)).decode()
        req = ('GET %s HTTP/1.1\r\nHost: %s:%d\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n'
               'Sec-WebSocket-Key: %s\r\nSec-WebSocket-Version: 13\r\n\r\n' % (path, host, port, key))
        self.sock.sendall(req.encode('ascii'))
        buf = b''
        while b'\r\n\r\n' not in buf:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise IOError('websocket handshake failed')
            buf += chunk
        head, rest = buf.split(b'\r\n\r\n', 1)
        if b' 101' not in head.split(b'\r\n')[0]:
            raise IOError('websocket handshake refused: %s' % head[:200].decode('latin-1'))
        self.buf = bytearray(rest)

    def settimeout(self, t):
        self.sock.settimeout(t)

    def _frame(self, opcode, data):
        hdr = bytearray([0x80 | opcode])
        n = len(data)
        if n < 126:
            hdr.append(0x80 | n)
        elif n < 65536:
            hdr.append(0x80 | 126)
            hdr += struct.pack('>H', n)
        else:
            hdr.append(0x80 | 127)
            hdr += struct.pack('>Q', n)
        mask = os.urandom(4)
        hdr += mask
        body = bytearray(data)
        for i in range(n):
            body[i] ^= mask[i & 3]
        self.sock.sendall(bytes(hdr) + bytes(body))

    def send(self, text):
        self._frame(0x1, text.encode('utf-8'))

    def _read(self, n):
        while len(self.buf) < n:
            chunk = self.sock.recv(max(65536, n - len(self.buf)))
            if not chunk:
                raise IOError('browser closed the connection')
            self.buf += chunk
        out = bytes(self.buf[:n])
        del self.buf[:n]
        return out

    def recv(self):
        parts = []
        while True:
            b1, b2 = bytearray(self._read(2))
            fin, op = b1 & 0x80, b1 & 0x0F
            n = b2 & 0x7F
            if n == 126:
                n = struct.unpack('>H', self._read(2))[0]
            elif n == 127:
                n = struct.unpack('>Q', self._read(8))[0]
            mask = self._read(4) if b2 & 0x80 else None
            payload = self._read(n)
            if mask:
                payload = bytes(bytearray(b ^ mask[i & 3] for i, b in enumerate(bytearray(payload))))
            if op == 0x9:
                self._frame(0xA, payload)
                continue
            if op == 0x8:
                raise IOError('browser closed the connection')
            if op == 0xA:
                continue
            parts.append(payload)
            if fin:
                return b''.join(parts).decode('utf-8', 'replace')

    def close(self):
        try:
            self.sock.close()
        except Exception:
            pass


class DevTools(object):
    def __init__(self, ws):
        self.ws = ws
        self.n = 0
        self.events = []

    def call(self, method, params=None, timeout=60):
        self.n += 1
        mid = self.n
        self.ws.settimeout(timeout)
        self.ws.send(json.dumps({'id': mid, 'method': method, 'params': params or {}}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get('id') == mid:
                if 'error' in msg:
                    raise RuntimeError('%s: %s' % (method, msg['error'].get('message')))
                return msg.get('result', {})
            if 'method' in msg:
                self.events.append(msg)

    def wait_for(self, name, timeout):
        end = time.time() + timeout
        for i, e in enumerate(self.events):
            if e.get('method') == name:
                del self.events[:i + 1]
                return True
        while time.time() < end:
            self.ws.settimeout(max(0.05, end - time.time()))
            try:
                msg = json.loads(self.ws.recv())
            except socket.timeout:
                return False
            if msg.get('method') == name:
                return True
            if 'method' in msg:
                self.events.append(msg)
        return False

    def eval(self, expr, timeout=60):
        r = self.call('Runtime.evaluate', {'expression': expr, 'awaitPromise': True, 'returnByValue': True},
                      timeout=timeout)
        if r.get('exceptionDetails'):
            d = r['exceptionDetails']
            raise RuntimeError('page script error: %s' % (d.get('exception', {}).get('description') or d.get('text')))
        return r.get('result', {}).get('value')


class Browser(object):
    def __init__(self, chrome):
        self.profile = tempfile.mkdtemp(prefix='rc-')
        args = [chrome, '--headless=new', '--remote-debugging-port=0', '--user-data-dir=' + self.profile,
                '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--disable-sync',
                '--disable-component-update', '--disable-default-apps', '--mute-audio', '--hide-scrollbars',
                '--disable-features=Translate,MediaRouter', '--force-color-profile=srgb', 'about:blank']
        self.proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        port_file = os.path.join(self.profile, 'DevToolsActivePort')
        port = None
        for _ in range(300):
            if os.path.isfile(port_file):
                try:
                    with open(port_file) as f:
                        port = int(f.readline().strip())
                    break
                except (ValueError, OSError):
                    pass
            if self.proc.poll() is not None:
                break
            time.sleep(0.05)
        if not port:
            self.close()
            raise RuntimeError('the browser did not start (no DevTools port)')
        targets = []
        for _ in range(60):
            try:
                targets = json.loads(urlopen('http://127.0.0.1:%d/json/list' % port, timeout=5).read().decode())
            except Exception:
                targets = []
            if any(t.get('type') == 'page' for t in targets):
                break
            time.sleep(0.1)
        page = [t for t in targets if t.get('type') == 'page']
        if not page:
            self.close()
            raise RuntimeError('no page target in the browser')
        self.ws = WebSocket(page[0]['webSocketDebuggerUrl'])
        self.dt = DevTools(self.ws)
        self.dt.call('Page.enable')
        self.dt.call('Runtime.enable')

    def close(self):
        try:
            self.ws.close()
        except Exception:
            pass
        try:
            self.proc.terminate()
            self.proc.wait(timeout=10)
        except Exception:
            try:
                self.proc.kill()
            except Exception:
                pass
        for _ in range(20):
            shutil.rmtree(self.profile, ignore_errors=True)
            if not os.path.exists(self.profile):
                break
            time.sleep(0.2)


# --------------------------------------------------------------------------------------
# In-page measurement
# --------------------------------------------------------------------------------------

MEASURE_JS = r"""
(async () => {
  await (document.fonts ? document.fonts.ready : Promise.resolve());
  await new Promise(r => setTimeout(r, 1200));
  const W = innerWidth, H = innerHeight, de = document.documentElement, body = document.body || de;
  const MIN_PX = __MIN_PX__, NATIVE = __NATIVE__;
  const out = {w: W, h: H};
  const desc = el => {
    if (!el || !el.tagName) return '?';
    let s = el.tagName.toLowerCase();
    if (el.id) s += '#' + el.id;
    const cl = (el.getAttribute('class') || '').trim().split(/\s+/).filter(Boolean).slice(0, 2);
    if (cl.length) s += '.' + cl.join('.');
    return s;
  };
  const shown = el => {
    for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
      const cs = getComputedStyle(n);
      if (cs.display === 'none' || cs.visibility === 'hidden' || cs.visibility === 'collapse' || parseFloat(cs.opacity) === 0) return false;
    }
    const r = el.getBoundingClientRect();
    return r.width > 1 && r.height > 1;
  };
  const srOnly = el => { const r = el.getBoundingClientRect(); return r.width <= 2 || r.height <= 2; };
  // Computed colours may come back as oklch()/color(); resolve every one to sRGB through a 1px canvas.
  const cv = document.createElement('canvas'); cv.width = cv.height = 1;
  const cx = cv.getContext('2d', {willReadFrequently: true});
  const colourCache = {};
  const rgb = s => {
    if (!s) return null;
    if (s in colourCache) return colourCache[s];
    let res = null;
    const m = s.match(/^rgba?\(([^)]+)\)$/);
    if (m) {
      const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(parseFloat);
      res = [p[0], p[1], p[2], p.length > 3 ? p[3] : 1];
    } else {
      try {
        cx.clearRect(0, 0, 1, 1); cx.fillStyle = '#000'; cx.fillStyle = s; cx.fillRect(0, 0, 1, 1);
        const d = cx.getImageData(0, 0, 1, 1).data;
        res = [d[0], d[1], d[2], d[3] / 255];
      } catch (e) { res = null; }
    }
    colourCache[s] = res;
    return res;
  };
  const lum = c => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]); };
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  const bgOf = el => {
    for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
      const c = rgb(getComputedStyle(n).backgroundColor);
      if (c && c[3] > 0.5) return c;
    }
    const c = rgb(getComputedStyle(de).backgroundColor);
    return c && c[3] > 0.5 ? c : [255, 255, 255, 1];
  };
  const lineRects = el => {
    const rg = document.createRange(); rg.selectNodeContents(el);
    const rs = [...rg.getClientRects()].filter(r => r.width > 1 && r.height > 1);
    const lines = [];
    for (const r of rs) {
      const cy = r.top + r.height / 2;
      if (!lines.some(l => Math.abs(l - cy) < Math.max(4, r.height * 0.45))) lines.push(cy);
    }
    return lines.length;
  };
  const lineTexts = el => {
    const groups = [];
    const tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    const rg = document.createRange();
    let node;
    while ((node = tw.nextNode())) {
      const t = node.textContent;
      for (let i = 0; i < t.length; i++) {
        rg.setStart(node, i); rg.setEnd(node, i + 1);
        const r = rg.getBoundingClientRect();
        if (r.height < 1) { if (groups.length) groups[groups.length - 1].s += t[i]; continue; }
        const cy = r.top + r.height / 2;
        let g = groups.find(g => Math.abs(g.cy - cy) < Math.max(4, r.height * 0.45));
        if (!g) { g = {cy, s: ''}; groups.push(g); }
        g.s += t[i];
      }
    }
    groups.sort((a, b) => a.cy - b.cy);
    return groups.map(g => g.s.replace(/\s+/g, ' ').trim()).filter(Boolean);
  };

  // overflow
  out.scrollWidth = Math.max(de.scrollWidth, body.scrollWidth);
  out.overflow = out.scrollWidth > W + 1;
  if (out.overflow) {
    const offs = [];
    for (const el of body.querySelectorAll('*')) {
      const r = el.getBoundingClientRect();
      if (r.right <= W + 1 || r.width < 1 || r.height < 1) continue;
      let clipped = false;
      for (let p = el.parentElement; p && p !== body; p = p.parentElement) {
        const o = getComputedStyle(p).overflowX;
        if (o !== 'visible') { clipped = true; break; }
      }
      if (clipped || getComputedStyle(el).position === 'fixed') continue;
      const par = el.parentElement;
      if (par && par !== body && par.getBoundingClientRect().right > W + 1) continue;
      offs.push({el: desc(el), right: Math.round(r.right)});
    }
    out.overflowBy = offs.sort((a, b) => b.right - a.right).slice(0, 4);
  }

  // H1
  const bodyFs = (() => {
    const counts = {};
    for (const p of document.querySelectorAll('p')) {
      if (!shown(p) || (p.innerText || '').trim().split(/\s+/).length < 12) continue;
      const fs = Math.round(parseFloat(getComputedStyle(p).fontSize));
      counts[fs] = (counts[fs] || 0) + 1;
    }
    const k = Object.keys(counts).sort((a, b) => counts[b] - counts[a])[0];
    return k ? +k : parseFloat(getComputedStyle(body).fontSize);
  })();
  out.bodyFs = bodyFs;
  const fontState = fam => {
    const f = fam.replace(/^["']|["']$/g, '').trim();
    const lf = f.toLowerCase();
    if (/^(-apple-system|blinkmacsystemfont|system-ui|ui-sans-serif|ui-serif|ui-rounded|sans-serif|serif|monospace|ui-monospace)$/.test(lf))
      return {family: f, state: 'system stack (renders as the next available family on this machine)'};
    const faces = document.fonts ? [...document.fonts].filter(x => x.family.replace(/^["']|["']$/g, '').toLowerCase() === lf) : [];
    if (!faces.length) return {family: f, state: 'local/installed name (not a web font; renders only where installed)'};
    return {family: f, state: faces.some(x => x.status === 'loaded') ? 'loaded' : 'NOT LOADED (fallback shown)'};
  };
  out.h1 = [...document.querySelectorAll('h1')].filter(shown).map(h => {
    const cs = getComputedStyle(h), r = h.getBoundingClientRect();
    return {text: (h.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 120), lines: lineRects(h), lineText: lineTexts(h),
            fs: parseFloat(cs.fontSize), top: Math.round(r.top + scrollY), bottom: Math.round(r.bottom + scrollY),
            font: fontState(cs.fontFamily.split(',')[0])};
  });
  out.headingFonts = [];
  for (const tag of ['h2', 'h3']) {
    const el = [...document.querySelectorAll(tag)].find(shown);
    if (el) out.headingFonts.push({el: desc(el), font: fontState(getComputedStyle(el).fontFamily.split(',')[0])});
  }
  let maxFs = 0;
  for (const el of body.querySelectorAll('h1,h2,h3,p,span,div,a,strong,b,dt,dd,li,figcaption,blockquote')) {
    if (![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 1)) continue;
    if (!shown(el)) continue;
    maxFs = Math.max(maxFs, parseFloat(getComputedStyle(el).fontSize));
  }
  out.maxFs = maxFs;

  // small HTML text
  const small = [];
  const tw = document.createTreeWalker(body, NodeFilter.SHOW_TEXT);
  let tn;
  const seen = new Set();
  while ((tn = tw.nextNode())) {
    const el = tn.parentElement;
    if (!el || seen.has(el) || tn.textContent.trim().length < 2) continue;
    seen.add(el);
    if (el.closest('svg,script,style,noscript,template')) continue;
    if (!shown(el) || srOnly(el)) continue;
    const fs = parseFloat(getComputedStyle(el).fontSize);
    if (fs < MIN_PX - 0.05) small.push({el: desc(el), px: Math.round(fs * 10) / 10, text: tn.textContent.trim().slice(0, 30)});
  }
  out.smallText = small.slice(0, 6); out.smallTextCount = small.length;

  // SVG text rendered size
  const svgSmall = [];
  let svgMin = null;
  for (const t of document.querySelectorAll('svg text')) {
    if (!shown(t) || !(t.textContent || '').trim()) continue;
    const m = t.getScreenCTM && t.getScreenCTM();
    if (!m) continue;
    const px = parseFloat(getComputedStyle(t).fontSize) * Math.hypot(m.a, m.b);
    if (svgMin === null || px < svgMin) svgMin = px;
    if (px < MIN_PX - 0.05) svgSmall.push({text: t.textContent.trim().slice(0, 30), px: Math.round(px * 10) / 10});
  }
  out.svgSmall = svgSmall.slice(0, 6); out.svgSmallCount = svgSmall.length;
  out.svgMin = svgMin === null ? null : Math.round(svgMin * 10) / 10;

  // measure
  const long = [];
  for (const p of document.querySelectorAll('p,li,dd,blockquote,figcaption')) {
    if (!shown(p) || p.closest('nav,button,table')) continue;
    const text = (p.innerText || '').replace(/\s+/g, ' ').trim();
    if (text.length < 160) continue;
    if (lineRects(p) < 3) continue;
    const lt = lineTexts(p).slice(0, -1);  // full lines only: the last line is usually short
    const cpl = lt.reduce((a, x) => a + x.length, 0) / Math.max(1, lt.length);
    if (cpl > 80) long.push({el: desc(p), cpl: Math.round(cpl), text: text.slice(0, 40)});
  }
  out.longLines = long.sort((a, b) => b.cpl - a.cpl).slice(0, 5);

  // muted share of running text
  let words = 0, muted = 0;
  const blocks = [];
  for (const p of document.querySelectorAll('p,li,dd,figcaption,blockquote,td')) {
    if (!shown(p) || p.closest('nav,footer,button,label,header nav,[role=navigation]')) continue;
    if (p.querySelector('p,li,dd')) continue;
    const text = (p.innerText || '').trim();
    const n = text ? text.split(/\s+/).length : 0;
    if (n < 4) continue;
    const c = rgb(getComputedStyle(p).color), bg = bgOf(p);
    if (!c) continue;
    blocks.push({n, cr: ratio(c, bg), bg: bg.slice(0, 3).map(Math.round).join(',')});
  }
  const inkByBg = {};
  for (const el of document.querySelectorAll('h1,h2,h3,h4,p,li,dd,dt,strong,td,th')) {
    if (!shown(el)) continue;
    const c = rgb(getComputedStyle(el).color), bg = bgOf(el);
    if (!c) continue;
    const k = bg.slice(0, 3).map(Math.round).join(',');
    inkByBg[k] = Math.max(inkByBg[k] || 0, ratio(c, bg));
  }
  for (const b of blocks) { words += b.n; if (b.cr < 0.78 * (inkByBg[b.bg] || b.cr)) muted += b.n; }
  out.mutedShare = words ? Math.round(100 * muted / words) : null;
  out.runningWords = words;

  // sections
  const sectionEls = [...document.querySelectorAll('header,section,footer,article,aside,[role=region]')]
    .filter(s => shown(s) && !s.parentElement.closest('section,article,aside,[role=region]') && !s.closest('nav'));
  const sections = sectionEls.length ? sectionEls : [...(document.querySelector('main') || body).children].filter(shown);
  // text edges within one column band (widest viewport only)
  out.edgeIssues = [];
  if (W >= 1024 && !NATIVE) {
    for (const s of sections) {
      const items = [];
      for (const el of s.querySelectorAll('h1,h2,h3,h4,p,ul,ol,dl,blockquote,table')) {
        if (!shown(el) || el.closest('nav,button,figure,svg,li,dd,td,th,label,form,dialog')) continue;
        if (el.parentElement && el.parentElement.closest('ul,ol,dl,blockquote,table') ) continue;
        const cs = getComputedStyle(el);
        if (cs.textAlign === 'center' || cs.position === 'absolute' || cs.position === 'fixed') continue;
        const r = el.getBoundingClientRect();
        if (r.width < 160 || r.height < 8) continue;
        let left = r.left + parseFloat(cs.paddingLeft || 0);
        if (/^(UL|OL)$/.test(el.tagName) && cs.listStyleType !== 'none') continue;
        items.push({el, left, right: r.right, tag: desc(el)});
      }
      for (let i = 0; i < items.length; i++) for (let j = i + 1; j < items.length; j++) {
        const a = items[i], b = items[j];
        const ov = Math.min(a.right, b.right) - Math.max(a.left, b.left);
        const narrow = Math.min(a.right - a.left, b.right - b.left);
        const d = Math.abs(a.left - b.left);
        if (ov > 0.5 * narrow && d > 8 && d < 200 && !a.el.contains(b.el) && !b.el.contains(a.el)) {
          out.edgeIssues.push({section: desc(s), a: a.tag, b: b.tag, dx: Math.round(d)});
          i = items.length; break;
        }
      }
    }
    out.edgeIssues = out.edgeIssues.slice(0, 5);
  }
  // repeated number+unit facts per section
  out.repeatFacts = [];
  const unitRe = /(\d+(?:[.,]\d+)?)\s?(mm|cm|km|kg|g|°C|°F|ml|cl|l|in|ft|lb|oz|MB|GB|TB|ms|min|hours?|days?|weeks?|months?|years?)(?![\w°])/gi;
  for (const s of sections) {
    let txt = (s.innerText || '');
    for (const t of s.querySelectorAll('svg text')) if (shown(t)) txt += '\n' + t.textContent;
    const counts = {};
    let m;
    while ((m = unitRe.exec(txt))) { const k = (m[1].replace(',', '.') + ' ' + m[2].toLowerCase()); counts[k] = (counts[k] || 0) + 1; }
    const dup = Object.keys(counts).filter(k => counts[k] > 1);
    if (dup.length) out.repeatFacts.push({section: desc(s), facts: dup.slice(0, 6).map(k => k + ' x' + counts[k])});
  }
  // inverted ground share
  const docH = Math.max(de.scrollHeight, body.scrollHeight);
  const bodyBg = bgOf(body);
  let inv = 0;
  for (const s of sections) {
    const bg = bgOf(s);
    if (ratio(bg, bodyBg) >= 4.5) inv += s.getBoundingClientRect().height;
  }
  out.invertedShare = docH ? Math.round(100 * inv / docH) : 0;
  out.docH = docH;
  out.bodyBg = bodyBg.slice(0, 3).map(Math.round);
  out.grounds = sections.map(s => ({el: desc(s), bg: bgOf(s).slice(0, 3).map(Math.round)}));

  // in-page links whose target is missing or shared by several elements (the link scrolls nowhere)
  const idCount = {};
  for (const el of document.querySelectorAll('[id]')) idCount[el.id] = (idCount[el.id] || 0) + 1;
  const badAnchors = {};
  for (const a of document.querySelectorAll('a[href^="#"]')) {
    let h = a.getAttribute('href').slice(1);
    try { h = decodeURIComponent(h); } catch (e) {}
    if (!h || h === 'top' || badAnchors[h]) continue;
    const n = idCount[h] || 0;
    if (!n) badAnchors[h] = 'no element has id="' + h + '"';
    else if (n > 1) badAnchors[h] = n + ' elements share id="' + h + '"; the link goes to the first, ' + desc(document.getElementById(h));
  }
  out.badAnchors = Object.keys(badAnchors).slice(0, 6).map(k => ({href: '#' + k, why: badAnchors[k]}));

  // rotated reading surfaces: a tilted block of running text renders soft and reads as a gimmick
  const angleOf = cs => {
    let deg = 0;
    if (cs.transform && cs.transform !== 'none') {
      try { const m = new DOMMatrixReadOnly(cs.transform); deg += Math.atan2(m.b, m.a) * 180 / Math.PI; } catch (e) {}
    }
    if (cs.rotate && cs.rotate !== 'none') {
      const t = cs.rotate.trim().split(/\s+/), v = t[t.length - 1];
      const zAxis = t.length === 1 || /^z$/i.test(t[0]) || (t.length === 4 && !parseFloat(t[0]) && !parseFloat(t[1]));
      if (zAxis) {
        const num = parseFloat(v);
        deg += /grad$/.test(v) ? num * 0.9 : /rad$/.test(v) ? num * 180 / Math.PI : /turn$/.test(v) ? num * 360 : num;
      }
    }
    return ((deg + 180) % 360 + 360) % 360 - 180;
  };
  const rotNodes = [];
  for (const el of body.querySelectorAll('*')) {
    if (el.closest('svg')) continue;
    const cs = getComputedStyle(el);
    if ((!cs.transform || cs.transform === 'none') && (!cs.rotate || cs.rotate === 'none')) continue;
    const d = angleOf(cs);
    if (Math.abs(d) < 0.2 || rotNodes.some(r => r.node.contains(el)) || !shown(el)) continue;
    const chars = (el.innerText || '').replace(/\s+/g, ' ').trim().length;
    if (chars >= 200) rotNodes.push({node: el, el: desc(el), deg: Math.round(d * 10) / 10, chars});
  }
  out.rotatedText = rotNodes.slice(0, 4).map(r => ({el: r.el, deg: r.deg, chars: r.chars}));

  // one-word (or very short) last lines on headings and leads
  out.orphans = [];
  for (const el of document.querySelectorAll('h1,h2,h3,p,blockquote')) {
    if (!shown(el) || el.closest('nav,button,footer,figure,svg,table,label,pre,code,dialog')) continue;
    const txt = (el.innerText || '').replace(/\s+/g, ' ').trim();
    if (txt.length < 20 || txt.length > 400 || txt.split(' ').length < 4) continue;
    if (!/^H/.test(el.tagName) && parseFloat(getComputedStyle(el).fontSize) < bodyFs * 1.15) continue;
    const lt = lineTexts(el);
    if (lt.length < 2) continue;
    const last = lt[lt.length - 1], longest = Math.max(...lt.map(x => x.length));
    if (last.split(' ').length === 1 || last.length < 0.2 * longest)
      out.orphans.push({el: desc(el), last: last.slice(0, 30), lines: lt.length});
  }
  out.orphans = out.orphans.slice(0, 8);

  // section heading sizes (marketing wants section heads well clear of body and lead text)
  out.h2Fs = [...document.querySelectorAll('h2')]
    .filter(h => shown(h) && !srOnly(h) && !h.closest('nav,footer,dialog,[role=dialog],figure'))
    .map(h => parseFloat(getComputedStyle(h).fontSize)).sort((a, b) => a - b);

  // dead columns: side-by-side columns whose content ends far apart leave a hole in the page ground
  out.deadColumns = [];
  if (W >= 1024) {
    const boxed = el => {
      const cs = getComputedStyle(el), c = rgb(cs.backgroundColor);
      return (c && c[3] > 0.1) || cs.backgroundImage !== 'none' || cs.boxShadow !== 'none' ||
        parseFloat(cs.borderTopWidth) + parseFloat(cs.borderLeftWidth) + parseFloat(cs.borderRightWidth) > 0;
    };
    // [top, bottom] of the visible content (text, media, boxed blocks) inside an element
    const contentSpan = el => {
      let b = -1, tp = Infinity;
      const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT), rg = document.createRange();
      let t;
      while ((t = walker.nextNode())) {
        if (!t.textContent.trim() || !t.parentElement || !shown(t.parentElement)) continue;
        rg.selectNodeContents(t);
        const r = rg.getBoundingClientRect();
        if (r.height > 0) { b = Math.max(b, r.bottom); tp = Math.min(tp, r.top); }
      }
      const blocks = [...el.querySelectorAll('img,svg,video,canvas,picture,iframe,input,select,textarea,button')]
        .filter(m => !(m.parentElement && m.parentElement.closest('svg')))
        .concat([...el.querySelectorAll('div,article,aside,figure,ul,ol,dl,table,form,pre')].filter(boxed));
      for (const m of blocks) {
        if (!shown(m)) continue;
        const r = m.getBoundingClientRect();
        b = Math.max(b, r.bottom); tp = Math.min(tp, r.top);
      }
      return [tp, b];
    };
    const seenRows = new Set();
    for (const c of body.querySelectorAll('*')) {
      if (c.closest('nav,header,footer,svg,dialog,table')) continue;
      const cs = getComputedStyle(c);
      const isRow = (cs.display.includes('flex') && cs.flexDirection.startsWith('row')) || cs.display.includes('grid');
      if (!isRow || !shown(c)) continue;
      const kids = [...c.children].filter(k => {
        if (!shown(k)) return false;
        const p = getComputedStyle(k).position;
        return p !== 'absolute' && p !== 'fixed' && k.getBoundingClientRect().width >= 160;
      });
      if (kids.length < 2) continue;
      // group grid items into visual columns (items stacked in one track belong together)
      const cols = [];
      for (const k of kids) {
        const r = k.getBoundingClientRect();
        let col = cols.find(cl => Math.min(cl.right, r.right) - Math.max(cl.left, r.left) > 0.5 * Math.min(cl.right - cl.left, r.width));
        if (!col) { col = {left: r.left, right: r.right, top: r.top, kids: []}; cols.push(col); }
        col.top = Math.min(col.top, r.top);
        col.kids.push(k);
      }
      if (cols.length < 2) continue;
      for (const cl of cols) {
        const spans = cl.kids.map(contentSpan);
        cl.cb = Math.max(...spans.map(x => x[1]));
        cl.ct = Math.min(...spans.map(x => x[0]));
        cl.boxed = cl.kids.every(boxed);
        cl.sticky = cl.kids.some(k => getComputedStyle(k).position === 'sticky' ||
          [...k.children].some(ch => getComputedStyle(ch).position === 'sticky'));
      }
      const live = cols.filter(cl => cl.cb > 0);
      if (live.length < 2) continue;
      const top = Math.min(...live.map(cl => cl.top)), maxCb = Math.max(...live.map(cl => cl.cb));
      const span = maxCb - top;
      if (span < 400) continue;
      for (const cl of live) {
        const gap = maxCb - cl.cb;
        if (gap < 160 || gap < 0.25 * span || cl.boxed || cl.top > top + 0.5 * span) continue;
        if (cl.ct - top > 0.5 * gap) continue;  // content centred or bottom-set in its track: space on both sides
        if (cl.right - cl.left < 0.25 * c.getBoundingClientRect().width) continue;  // a label rail, not a column
        const sec = cl.kids[0].closest('section,article,header,footer,aside,main') || c;
        const key = desc(sec) + Math.round(top);
        if (seenRows.has(key)) continue;
        seenRows.add(key);
        out.deadColumns.push({section: desc(sec), col: cl.kids.map(desc).slice(0, 2).join(' + '), gap: Math.round(gap),
                              span: Math.round(span), sticky: cl.sticky});
      }
    }
    out.deadColumns = out.deadColumns.sort((a, b) => b.gap - a.gap).slice(0, 5);
  }

  // first-viewport visual
  let best = null;
  const cands = [...document.querySelectorAll('img,video,canvas,svg,picture,figure,[role=img]')];
  for (const el of body.querySelectorAll('*')) {
    const bi = getComputedStyle(el).backgroundImage;
    if (bi && bi.includes('url(')) cands.push(el);
  }
  for (const el of cands) {
    if (el.tagName.toLowerCase() === 'svg' && el.parentElement && el.parentElement.closest('svg')) continue;
    if (el.closest('button,a,label,nav') && el.getBoundingClientRect().height < 120) continue;
    if (!shown(el)) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 80 || r.height < 80) continue;
    const vis = Math.max(0, Math.min(r.bottom, H) - Math.max(r.top, 0));
    const visW = Math.max(0, Math.min(r.right, W) - Math.max(r.left, 0));
    if (!vis || !visW) continue;
    const area = vis * visW;
    if (!best || area > best.area) best = {area, el: desc(el), pct: Math.round(100 * vis / H)};
  }
  out.firstVisual = best ? {el: best.el, pct: best.pct} : null;

  // layout shift during load
  out.cls = await new Promise(res => {
    let s = 0;
    try {
      const po = new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) s += e.value; });
      po.observe({type: 'layout-shift', buffered: true});
      setTimeout(() => { po.disconnect(); res(Math.round(s * 1000) / 1000); }, 60);
    } catch (e) { res(null); }
  });
  const faceState = {};
  for (const f of (document.fonts ? [...document.fonts] : [])) {
    const k = f.family.replace(/^["']|["']$/g, '') + ' ' + f.weight + (f.style === 'normal' ? '' : ' ' + f.style);
    faceState[k] = faceState[k] === 'loaded' || f.status === 'loaded' ? 'loaded' : f.status;
  }
  out.fonts = Object.keys(faceState).slice(0, 12).map(k => k + ' ' + faceState[k]);
  out.title = document.title;
  const vp = document.querySelector('meta[name=viewport]');
  out.viewportMeta = vp ? vp.getAttribute('content') : null;
  return out;
})()
"""

BLUR_ON = r"""(() => { const s = document.createElement('style'); s.id = '__rc_blur';
  s.textContent = 'html{filter:grayscale(1) blur(10px)!important}'; document.head.appendChild(s); return true; })()"""
BLUR_OFF = r"""(() => { const s = document.getElementById('__rc_blur'); if (s) s.remove(); return true; })()"""


# --------------------------------------------------------------------------------------
# Run
# --------------------------------------------------------------------------------------

def long_path(p):
    """Absolute path; on Windows add the extended-length prefix near MAX_PATH (deep project or temp folders)."""
    p = os.path.abspath(p)
    prefix = '\\\\?\\'
    if os.name == 'nt' and not p.startswith(prefix) and len(p) >= 200:
        return prefix + p.replace('/', '\\')
    return p


def to_url(page):
    if re.match(r'^(https?|file):', page, re.I):
        return page
    p = os.path.abspath(page)
    if not os.path.isfile(p):
        raise SystemExit('render_check: no such file: %s' % page)
    from pathlib import Path
    return Path(p).as_uri()


def parse_sizes(s):
    out = []
    for tok in s.split(','):
        m = re.match(r'^\s*(\d+)x(\d+)\s*$', tok)
        if not m:
            raise SystemExit('render_check: bad size %r (use WxH, e.g. 390x844)' % tok)
        out.append((int(m.group(1)), int(m.group(2))))
    return out


def measure(dt, url, w, h, surface, scheme='light'):
    dt.call('Emulation.setDeviceMetricsOverride', {'width': w, 'height': h, 'deviceScaleFactor': 1,
                                                    'mobile': False, 'screenWidth': w, 'screenHeight': h})
    # Pin the colour scheme: headless Chrome otherwise follows the OS theme, so results would change with it.
    dt.call('Emulation.setEmulatedMedia', {'features': [{'name': 'prefers-color-scheme', 'value': scheme}]})
    dt.events = []
    dt.call('Page.navigate', {'url': url})
    dt.wait_for('Page.loadEventFired', 45)
    js = MEASURE_JS.replace('__MIN_PX__', '11' if surface == 'native' else '12').replace(
        '__NATIVE__', 'true' if surface == 'native' else 'false')
    return dt.eval(js, timeout=90)


def shoot(dt, path, blur=False):
    if blur:
        dt.eval(BLUR_ON)
        time.sleep(0.15)
    data = dt.call('Page.captureScreenshot', {'format': 'png'}).get('data')
    if blur:
        dt.eval(BLUR_OFF)
    if data:
        with open(long_path(path), 'wb') as f:
            f.write(base64.b64decode(data))
        return path
    return None


FULL_PAGE_WIDTHS = (390, 1440)
FULL_PAGE_MAX = 16000

# Scroll through the page so scroll-triggered reveals fire, then return to the top.
SCROLL_THROUGH = '''(async () => {
  const H = Math.min(document.documentElement.scrollHeight, %d), step = Math.max(200, innerHeight * 0.7);
  for (let y = 0; y < H; y += step) { scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); }
  scrollTo(0, H); await new Promise(r => setTimeout(r, 300));
  scrollTo(0, 0); await new Promise(r => setTimeout(r, 400));
  // Fixed/sticky chrome would be painted at every slice offset; pin it to its place at the top instead.
  for (const el of document.querySelectorAll('body *')) {
    const p = getComputedStyle(el).position;
    if (p === 'fixed') el.style.setProperty('position', 'absolute', 'important');
    else if (p === 'sticky') el.style.setProperty('position', 'relative', 'important');
  }
  await new Promise(r => setTimeout(r, 150));
  return Math.min(document.documentElement.scrollHeight, %d);
})()''' % (FULL_PAGE_MAX, FULL_PAGE_MAX)


def shoot_full(dt, stem_path, w):
    """Whole page at the current width, as JPEG slices about 1.25 x the width (at least 1500px) tall, readable when viewed,
    named <stem>-01.jpg, -02.jpg ... Capped at FULL_PAGE_MAX px of page height."""
    height = dt.eval(SCROLL_THROUGH, timeout=120) or 0
    paths, step = [], max(int(w * 1.25), 1500)
    for n, y in enumerate(range(0, height, step), 1):
        clip = {'x': 0, 'y': y, 'width': w, 'height': min(step, height - y), 'scale': 1}
        data = dt.call('Page.captureScreenshot', {'format': 'jpeg', 'quality': 75, 'captureBeyondViewport': True,
                                                  'clip': clip}, timeout=120).get('data')
        if data:
            path = '%s-%02d.jpg' % (stem_path, n)
            with open(long_path(path), 'wb') as f:
                f.write(base64.b64decode(data))
            paths.append(path)
    return paths


def analyse(results, surface):
    fails, checks = [], []
    floor = 11 if surface == 'native' else 12

    def add(lst, kind, size, msg):
        lst.append({'kind': kind, 'size': size, 'message': msg})
    widest = max(results, key=lambda r: r['w']) if results else None
    widest_r = widest
    rotated, orphans = {}, {}
    for r in results:
        size = '%dx%d' % (r['w'], r['h'])
        for t in r.get('rotatedText') or []:
            rotated.setdefault(t['el'], (t, []))[1].append(str(r['w']))
        for o in r.get('orphans') or []:
            orphans.setdefault(o['el'] + o['last'], (o, []))[1].append(str(r['w']))
        if r.get('overflow'):
            who = ', '.join('%s (right edge %dpx)' % (o['el'], o['right']) for o in r.get('overflowBy') or [])
            add(fails, 'overflow', size, 'page is %dpx wide in a %dpx viewport%s' % (r['scrollWidth'], r['w'],
                                                                                    ': ' + who if who else ''))
        h1s = r.get('h1') or []
        if len(h1s) > 1:
            add(checks, 'h1-count', size, '%d visible H1 elements (one per page)' % len(h1s))
        if h1s:
            h = h1s[0]
            limit = 2 if r['w'] >= 1280 else 3
            if surface in ('marketing', 'docs') and h['lines'] > limit:
                add(fails, 'h1-lines', size, 'H1 runs %d lines at %dpx font-size (limit %d at this width): %s'
                    % (h['lines'], round(h['fs']), limit, ' / '.join(h['lineText'])))
            lt = h.get('lineText') or []
            if len(lt) > 1 and any(re.search(r'[.!?]\s+\S', x) for x in lt):
                add(checks, 'h1-breaks', size, 'a sentence ends mid-line in the H1: %s' % ' / '.join(lt))
            if 'NOT LOADED' in h['font']['state']:
                add(fails, 'h1-font', size, 'H1 face "%s" did not load; a fallback is showing' % h['font']['family'])
        if r is widest_r:
            for hf in ([{'el': 'h1', 'font': h1s[0]['font']}] if h1s else []) + (r.get('headingFonts') or []):
                if hf['font']['state'].startswith('system stack') and surface in ('marketing', 'native'):
                    add(checks, 'heading-font', size, '%s is set in "%s": off Apple devices it renders in the next '
                        'family of the stack, so a shared mock or brand page shows a default face' %
                        (hf['el'], hf['font']['family']))
        if r.get('smallTextCount'):
            ex = ', '.join('%s %spx "%s"' % (s['el'], s['px'], s['text']) for s in r['smallText'][:3])
            add(fails, 'small-text', size, '%d text element(s) under %dpx: %s' % (r['smallTextCount'], floor, ex))
        if r.get('svgSmallCount'):
            ex = ', '.join('"%s" %spx' % (s['text'], s['px']) for s in r['svgSmall'][:3])
            add(fails, 'small-text', size, '%d SVG label(s) render under %dpx (font-size x drawing scale): %s. Use '
                'HTML labels over the drawing, or a label set per breakpoint' % (r['svgSmallCount'], floor, ex))
        for ll in (r.get('longLines') or [])[:2]:
            if ll['cpl'] > 90:
                add(fails, 'measure', size, '%s averages %d characters per line ("%s...")' % (ll['el'], ll['cpl'],
                                                                                            ll['text']))
        if r.get('cls') is not None and r['cls'] >= 0.1:
            add(fails, 'cls', size, 'layout shift during load %.3f (target under 0.1)' % r['cls'])
        if surface == 'marketing' and r['w'] < 768:
            fv = r.get('firstVisual')
            if h1s and h1s[0]['top'] >= r['h']:
                add(checks, 'first-view', size, 'the H1 starts below the fold (y=%d)' % h1s[0]['top'])
            if fv is None:
                add(checks, 'first-view', size, 'no image, video, canvas or drawing in the first viewport')
            elif fv['pct'] < 25:
                add(checks, 'first-view', size, 'largest visual (%s) fills %d%% of the first viewport height' %
                    (fv['el'], fv['pct']))
    if widest:
        r = widest
        size = '%dx%d' % (r['w'], r['h'])
        vp = r.get('viewportMeta')
        if not vp or 'width=device-width' not in vp.replace(' ', ''):
            add(fails, 'viewport', 'all', 'no <meta name="viewport" content="width=device-width, initial-scale=1">: '
                'phones render the page at desktop width, zoomed out')
        if surface == 'marketing' and r.get('bodyFs') and r['w'] >= 1024:  # the 3x jump is a desktop measure
            ratio = r['maxFs'] / r['bodyFs']
            if ratio < 3:
                add(checks, 'display-ratio', size, 'largest text %.0fpx is %.1fx body (%.0fpx); marketing pages want '
                    'one display size at least 3x body' % (r['maxFs'], ratio, r['bodyFs']))
        if r.get('mutedShare') is not None and r['runningWords'] >= 80 and r['mutedShare'] > 50:
            add(checks, 'muted-share', size, '%d%% of %d running-text words are in a muted colour; leads, story '
                'paragraphs and instructions stay at full ink' % (r['mutedShare'], r['runningWords']))
        for e in r.get('edgeIssues') or []:
            add(checks, 'text-edges', size, 'in %s, %s and %s share a column band but start %dpx apart' %
                (e['section'], e['a'], e['b'], e['dx']))
        for f in r.get('repeatFacts') or []:
            add(checks, 'repeat-facts', size, 'in %s the same fact appears more than once: %s' %
                (f['section'], ', '.join(f['facts'])))
        if r.get('invertedShare', 0) > 25:
            add(checks, 'inverted', size, '%d%% of the page height sits on an inverted ground' % r['invertedShare'])
        for a in r.get('badAnchors') or []:
            add(fails, 'anchors', 'all', 'in-page link %s scrolls nowhere: %s' % (a['href'], a['why']))
        if surface == 'marketing' and r.get('bodyFs') and r.get('h2Fs') and r['w'] >= 1024:
            med = r['h2Fs'][len(r['h2Fs']) // 2]
            if med / r['bodyFs'] < 2:
                add(checks, 'section-scale', size, 'section headings (median H2 %.0fpx) are %.1fx body (%.0fpx): they '
                    'read as labels beside the leads; marketing section heads run about 2.5-3.5x body' %
                    (med, med / r['bodyFs'], r['bodyFs']))
        for d in r.get('deadColumns') or []:
            add(checks, 'dead-column', size, 'in %s, %s ends %dpx above its neighbour (row %dpx tall)%s: stack it, '
                'move the heading above the row, or give the column content that fills the row' %
                (d['section'], d['col'], d['gap'], d['span'], ', sticky' if d['sticky'] else ''))
    for el, (t, sizes) in rotated.items():
        add(fails, 'rotated-text', ','.join(sizes), '%s rotates %d characters of reading text by %.1fdeg; text on a '
            'tilt renders soft and reads as a gimmick (tilt images or a short label, never a reading surface)' %
            (el, t['chars'], t['deg']))
    for key, (o, sizes) in list(orphans.items())[:6]:
        add(checks, 'orphans', ','.join(sizes), '%s ends on a short last line "%s" (%d lines): text-wrap: balance '
            'on headings, pretty on leads, or rewrite' % (o['el'], o['last'], o['lines']))
    return fails, checks


def _lum(c):
    def f(v):
        v = v / 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2])


def _ratio(a, b):
    x, y = _lum(a), _lum(b)
    return (max(x, y) + 0.05) / (min(x, y) + 0.05)


def dark_checks(light, dark):
    """Compare section grounds of the light and dark passes at the widest size. None when no dark theme exists."""
    lg, dg = light.get('grounds') or [], dark.get('grounds') or []
    if light.get('bodyBg') == dark.get('bodyBg') and [g['bg'] for g in lg] == [g['bg'] for g in dg]:
        return None
    checks = []
    size = '%dx%d' % (dark['w'], dark['h'])
    if len(lg) == len(dg):
        for a, b in zip(lg, dg):
            rl, rd = _ratio(a['bg'], light['bodyBg']), _ratio(b['bg'], dark['bodyBg'])
            if rl >= 3 and rd < 1.3:
                checks.append({'kind': 'dark-grounds', 'size': size, 'message': '%s is its own ground in light (%.1f:1 '
                               'against the page) but only %.2f:1 in dark, so the band merges into the canvas: give it a '
                               'lighter tier, the brand hue or a rule in the dark theme' % (a['el'], rl, rd)})
    lsteps = sum(1 for g in lg if _ratio(g['bg'], light['bodyBg']) >= 1.1)
    dsteps = sum(1 for g in dg if _ratio(g['bg'], dark['bodyBg']) >= 1.1)
    if lsteps >= 2 and dsteps == 0:
        checks.append({'kind': 'dark-grounds', 'size': size, 'message': '%d sections sit on their own ground in light, '
                       'none in dark: the dark theme is one flat slab' % lsteps})
    return checks


def main(argv=None):
    ap = argparse.ArgumentParser(description='Render a page in headless Chrome/Edge and measure it (premium-design '
                                             'skill, step 6). Exit 1 on any FAIL, 2 when it cannot run.')
    ap.add_argument('page', help='local .html file or http(s) URL')
    ap.add_argument('--surface', default='marketing', choices=['marketing', 'product', 'dashboard', 'native', 'docs'],
                    help='surface pinned in the brief; H1 and first-viewport checks apply to marketing (and docs)')
    ap.add_argument('--sizes', default=DEFAULT_SIZES, help='comma-separated WxH viewports (default %s)' % DEFAULT_SIZES)
    ap.add_argument('--out', help='folder for screenshots (default: a new temp folder)')
    ap.add_argument('--no-shots', action='store_true', help='skip screenshots')
    ap.add_argument('--full', action='store_true',
                    help='also save whole-page JPEGs at 390 and 1440 wide (scrolls first so reveal animations fire)')
    ap.add_argument('--json', action='store_true', help='machine-readable output')
    ap.add_argument('--chrome', help='path to a Chrome, Chromium or Edge binary (or set CHROME_PATH)')
    a = ap.parse_args(argv)
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
    except Exception:
        pass
    url = to_url(a.page)
    sizes = parse_sizes(a.sizes)
    chrome = find_chrome(a.chrome)
    if not chrome:
        print('render_check: no Chrome, Chromium or Edge found; pass --chrome PATH or set CHROME_PATH. Without a '
              'browser, do the step 6 checks by hand.', file=sys.stderr)
        return 2
    out_dir = None
    if not a.no_shots:
        out_dir = a.out or tempfile.mkdtemp(prefix='render-')
        out_dir = os.path.abspath(out_dir)
        os.makedirs(long_path(out_dir), exist_ok=True)
    stem = re.sub(r'[^\w-]+', '-', os.path.splitext(os.path.basename(urlparse(url).path) or 'page')[0])[:24] or 'page'
    results, shots = [], []
    try:
        br = Browser(chrome)
    except Exception as e:
        print('render_check: %s' % e, file=sys.stderr)
        return 2
    try:
        for (w, h) in sizes:
            r = measure(br.dt, url, w, h, a.surface)
            if not r:
                raise RuntimeError('the page returned no measurements at %dx%d' % (w, h))
            results.append(r)
            if out_dir and w in SHOT_WIDTHS:
                shots.append(shoot(br.dt, os.path.join(out_dir, '%s-%d.png' % (stem, w))))
                shots.append(shoot(br.dt, os.path.join(out_dir, '%s-%d-blur.png' % (stem, w)), blur=True))
            if out_dir and a.full and w in FULL_PAGE_WIDTHS:
                shots.extend(shoot_full(br.dt, os.path.join(out_dir, '%s-%d-full' % (stem, w)), w))
        # one more load at the widest size with a dark colour scheme, to check a theme that follows the OS
        wl = max(results, key=lambda r: r['w'])
        dark = measure(br.dt, url, wl['w'], wl['h'], a.surface, scheme='dark')
        dark_found = dark_checks(wl, dark) if dark else None
        if dark_found is not None and out_dir:
            shots.append(shoot(br.dt, os.path.join(out_dir, '%s-%d-dark.png' % (stem, wl['w']))))
    except Exception as e:
        print('render_check: %s' % e, file=sys.stderr)
        br.close()
        return 2
    br.close()
    fails, checks = analyse(results, a.surface)
    checks += dark_found or []
    code = 1 if fails else 0
    if a.json:
        print(json.dumps({'url': url, 'surface': a.surface, 'exit': code, 'fail': fails, 'check': checks,
                          'darkTheme': dark_found is not None,
                          'screenshots': [s for s in shots if s], 'measurements': results}, indent=2))
        return code
    print('render_check: %s (surface: %s, %s)' % (url, a.surface, os.path.basename(chrome)))
    for r in results:
        h = (r.get('h1') or [None])[0]
        h1 = ('H1 %dpx, %d line(s), %s' % (round(h['fs']), h['lines'], h['font']['state'])) if h else 'no H1'
        fv = r.get('firstVisual')
        print('  %4dx%-4d width %-5s %s; first-view visual %s; min SVG label %s' % (
            r['w'], r['h'], 'OK' if not r.get('overflow') else '%dpx' % r['scrollWidth'], h1,
            ('%d%% (%s)' % (fv['pct'], fv['el'])) if fv else 'none',
            ('%spx' % r['svgMin']) if r.get('svgMin') is not None else '-'))
    wd = max(results, key=lambda r: r['w'])
    print('  at %dpx: body %spx, largest text %spx, muted running text %s%%, inverted ground %s%% of %dpx' % (
        wd['w'], wd.get('bodyFs'), round(wd.get('maxFs') or 0), wd.get('mutedShare'), wd.get('invertedShare'),
        wd.get('docH') or 0))
    if wd.get('fonts'):
        print('  fonts: %s' % '; '.join(wd['fonts']))
    print('  dark theme: %s' % ('none (no prefers-color-scheme: dark styles change the grounds)' if dark_found is None
                                else 'measured at %dpx (section grounds compared with light)' % wd['w']))
    for f in fails:
        print('FAIL  %-12s %-9s %s' % (f['kind'], f['size'], f['message']))
    for c in checks:
        print('CHECK %-12s %-9s %s' % (c['kind'], c['size'], c['message']))
    if shots:
        print('screenshots (plain and greyscale 10px blur): %s' % os.path.dirname(shots[0]))
        for s in shots:
            if s:
                print('  %s' % s)
    print('render_check: %d FAIL, %d CHECK.%s Hover, click, keyboard and scroll states still need a hand pass.' % (
        len(fails), len(checks), ' Exit 1.' if fails else ''))
    return code


if __name__ == '__main__':
    sys.exit(main())
