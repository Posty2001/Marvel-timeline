#!/usr/bin/env python3
"""Genera tools/restyle_icons.css (maschere SVG data-URI per le icone coerenti) e tools/restyle_map.json (codepoint -> icona)."""
import json, urllib.parse
P = {
 'star': '<polygon points="12 2.5 14.9 8.7 21.5 9.4 16.6 13.9 18 20.5 12 17.2 6 20.5 7.4 13.9 2.5 9.4 9.1 8.7"/>',
 'trophy': '<path d="M8 21h8M12 17v4M7 4h10v5a5 5 0 0 1-10 0zM7 6H4v2a3 3 0 0 0 3 3M17 6h3v2a3 3 0 0 1-3 3"/>',
 'lock': '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
 'unlock': '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 7.5-2"/>',
 'key': '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M16 7l3 3"/>',
 'hourglass': '<path d="M6 3h12M6 21h12M7 3c0 5 5 6 5 9s-5 4-5 9M17 3c0 5-5 6-5 9s5 4 5 9"/>',
 'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 'flame': '<path d="M12 3c1 4 5 5 5 10a5 5 0 0 1-10 0c0-2 1-3 2-4 0 2 1 3 2 3 0-4-1-6 1-9z"/>',
 'play': '<polygon points="7 4 20 12 7 20"/>',
 'book': '<path d="M4 4h6a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4zM20 4h-6a3 3 0 0 0-3 3v13a2 2 0 0 1 2-2h7z"/>',
 'folder': '<path d="M3 6a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
 'map': '<path d="M9 4L3 6v14l6-2 6 2 6-2V4l-6 2zM9 4v14M15 6v14"/>',
 'search': '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
 'clapper': '<rect x="3" y="9" width="18" height="12" rx="2"/><path d="M3 9l3-5h4L7 9M10 9l3-5h4l-3 5M17 9l3-5"/>',
 'video': '<rect x="3" y="6" width="14" height="12" rx="2"/><path d="M17 10l4-2v8l-4-2"/>',
 'tv': '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M8 21h8M12 18v3"/>',
 'masks': '<path d="M4 5h9v6a4.5 4.5 0 0 1-9 0zM11 14h9v-3a4.5 4.5 0 0 0-4.5-4.5M7 9h.01M10 9h.01M6.5 12c1 1 3 1 4 0"/>',
 'medal': '<circle cx="12" cy="9" r="5"/><path d="M8.5 13L7 21l5-3 5 3-1.5-8"/>',
 'chart': '<path d="M4 20V10M10 20V4M16 20v-8M22 20H2"/>',
 'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
 'swirl': '<path d="M12 12a2 2 0 1 1 2 2 4 4 0 1 1-4-4 6 6 0 1 1 6 6"/>',
 'sparkles': '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8zM19 16l.7 2 2 .7-2 .7-.7 2-.7-2-2-.7 2-.7z"/>',
 'user': '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
 'users': '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0M16 4.5a3.5 3.5 0 0 1 0 7M18 14a6 6 0 0 1 3.5 6"/>',
 'handshake': '<path d="M3 12l4-4 4 2 3-2 4 3 3-1M3 12l5 6 3-1 2 2 3-2 5-5M13 12l-2 2"/>',
 'idcard': '<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="11" r="2"/><path d="M6 16c.5-2 5.5-2 6 0M14 10h4M14 13h4"/>',
 'camera': '<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
 'dna': '<path d="M6 3c0 6 12 6 12 12M18 3c0 6-12 6-12 12M6 21c0-3 3-4 6-4M18 21c0-3-3-4-6-4M8 7h8M8 17h8"/>',
 'scroll': '<path d="M7 3h10a2 2 0 0 1 2 2v13a3 3 0 0 1-3 3H8a3 3 0 0 1-3-3V5a2 2 0 0 1 2-2zM9 8h6M9 12h6M9 16h4"/>',
 'radio': '<circle cx="12" cy="12" r="2"/><path d="M7.8 7.8a6 6 0 0 0 0 8.4M16.2 7.8a6 6 0 0 1 0 8.4M4.9 4.9a10 10 0 0 0 0 14.2M19.1 4.9a10 10 0 0 1 0 14.2"/>',
 'plus': '<path d="M12 5v14M5 12h14"/>',
 'clipboard': '<rect x="6" y="5" width="12" height="16" rx="2"/><path d="M9 5a3 3 0 0 1 6 0M9 11h6M9 15h6"/>',
 'share': '<path d="M12 15V3M7 8l5-5 5 5M5 14v5a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-5"/>',
 'scale': '<path d="M12 3v18M5 21h14M5 7h14M5 7l-3 7a3 3 0 0 0 6 0zM19 7l-3 7a3 3 0 0 0 6 0z"/>',
 'alert': '<path d="M12 3L2 20h20zM12 10v4.5M12 17.5h.01"/>',
 'info': '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5h.01"/>',
 'tag': '<path d="M3 12V4h8l10 10-8 8z"/><circle cx="8" cy="9" r="1.2"/>',
 'save': '<path d="M5 3h12l3 3v15H5zM8 3v6h8V3M8 21v-7h8v7"/>',
 'laptop': '<rect x="4" y="5" width="16" height="11" rx="1.5"/><path d="M2 20h20"/>',
 'dice': '<rect x="4" y="4" width="16" height="16" rx="3"/><path d="M8.5 8.5h.01M15.5 8.5h.01M12 12h.01M8.5 15.5h.01M15.5 15.5h.01"/>',
 'rocket': '<path d="M5 15c-1 3-1 5-1 5s2 0 5-1M14 4c4-1 6-1 6-1s0 2-1 6c-1 3-5 7-8 8l-4-4c1-3 5-7 7-9zM15 9h.01"/>',
 'web': '<circle cx="12" cy="12" r="2"/><path d="M12 2v8M12 14v8M2 12h8M14 12h8M5 5l5 5M14 14l5 5M19 5l-5 5M10 14l-5 5"/>',
 'check': '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l3 3 5-6"/>',
 'target': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
 'wand': '<path d="M4 20L16 8M14 4l1 2.5L17.5 7.5 15 8.5 14 11 13 8.5 10.5 7.5 13 6.5zM19 13l.7 1.8 1.8.7-1.8.7-.7 1.8-.7-1.8-1.8-.7 1.8-.7z"/>',
 'chev': '<path d="M9 6l6 6-6 6"/>',
 'pin': '<path d="M12 21s7-6.2 7-11.5A7 7 0 0 0 5 9.5C5 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
 'link': '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
 'note': '<path d="M4 20l1-4L16 5l3 3L8 19zM14 7l3 3"/>',
 'gem': '<path d="M6 4h12l3 5-9 11L3 9zM3 9h18M9 4l-1 5 4 11M15 4l1 5-4 11"/>',
 'building': '<path d="M5 21V4h9v17M14 9h5v12M3 21h18M8 8h3M8 12h3M8 16h3"/>',
 'eye': '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 'bolt': '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
 'swords': '<path d="M4 4l9 9M20 4l-9 9M4 20l3-3M20 20l-3-3M7 14l3 3M17 14l-3 3"/>',
 'headphones': '<path d="M4 15v-3a8 8 0 0 1 16 0v3M4 15h3v5H5a1 1 0 0 1-1-1zM20 15h-3v5h2a1 1 0 0 0 1-1z"/>',
 'gear': '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/>',
 'bulb': '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10.5c.8.8 1 1.5 1 2.5h6c0-1 .2-1.7 1-2.5A6 6 0 0 0 12 3z"/>',
 'megaphone': '<path d="M4 10v4h3l8 4V6L7 10zM18 9a4 4 0 0 1 0 6"/>',
 'wrench': '<path d="M14.5 6.5a4 4 0 0 0 5 5L10 21l-4-4zM14.5 6.5l3 3"/>',
 'repeat': '<path d="M4 11V9a3 3 0 0 1 3-3h11l-3-3M20 13v2a3 3 0 0 1-3 3H6l3 3"/>',
 'help': '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.4-1 .9-1 1.7M12 17h.01"/>',
 'crown': '<path d="M3 8l4 4 5-7 5 7 4-4-2 11H5z"/>',
 'shield': '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/>',
 'square': '<rect x="5" y="5" width="14" height="14" rx="3"/>',
}
# codepoint -> icona (emoji senza FE0F)
M = {
 0x2B50: 'star', 0x1F31F: 'sparkles', 0x2728: 'sparkles', 0x1F3C6: 'trophy', 0x1F513: 'unlock', 0x1F512: 'lock', 0x1F511: 'key',
 0x23F1: 'clock', 0x23F3: 'hourglass', 0x1F551: 'clock', 0x1F550: 'clock', 0x1F550+4: 'clock', 0x1F525: 'flame', 0x25B6: 'play',
 0x1F4D6: 'book', 0x1F4DA: 'book', 0x1F4C1: 'folder', 0x1F4C2: 'folder', 0x1F5FA: 'map', 0x1F50D: 'search', 0x1F3AC: 'clapper',
 0x1F3A5: 'video', 0x1F4FA: 'tv', 0x1F3AD: 'masks', 0x1F3C5: 'medal', 0x1F4CA: 'chart', 0x1F4C8: 'chart', 0x1F310: 'globe',
 0x1F300: 'swirl', 0x1F464: 'user', 0x1F465: 'users', 0x1F91D: 'handshake', 0x1F392: 'idcard', 0x1F4F8: 'camera', 0x1F9EC: 'dna',
 0x1F4DC: 'scroll', 0x1F4E1: 'radio', 0x2795: 'plus', 0x1F4CB: 'clipboard', 0x1F4E4: 'share', 0x2696: 'scale', 0x26A0: 'alert',
 0x2139: 'info', 0x1F3F7: 'tag', 0x1F4BE: 'save', 0x1F4BB: 'laptop', 0x1F3B2: 'dice', 0x1F680: 'rocket', 0x1F577: 'web',
 0x2705: 'check', 0x1F3AF: 'target', 0x1F9D9: 'wand', 0x1F3A4: 'clapper', 0x1F5D2: 'scroll', 0x1F578: 'web', 0x1F4C5: 'clock',
 0x1F9ED: 'map', 0x1F3C1: 'target', 0x1F9E9: 'wand', 0x1F4A5: 'sparkles',
 0x1F4CD: 'pin', 0x1F517: 'link', 0x1F4DD: 'note', 0x1F48E: 'gem', 0x1F3E2: 'building', 0x1F441: 'eye', 0x26A1: 'bolt', 0x2694: 'swords',
 0x1F3A7: 'headphones', 0x2699: 'gear', 0x1F4A1: 'bulb', 0x1F4E2: 'megaphone', 0x1F6E0: 'wrench', 0x1F504: 'repeat', 0x1F501: 'repeat',
 0x2753: 'help', 0x1F451: 'crown', 0x1F6E1: 'shield', 0x2B1C: 'square', 0x1F30C: 'swirl', 0x1F30D: 'globe', 0x1F30F: 'globe',
 0x1F52E: 'sparkles', 0x1F4D5: 'book', 0x231B: 'hourglass', 0x1F557: 'clock', 0x2604: 'sparkles', 0x1F39E: 'clapper', 0x1FA73: 'video', 0x1F9A0: 'dna',
}
DOTS = {0x1F534: '#DB777C', 0x1F535: '#6FB3D9', 0x1F7E0: '#F0954A', 0x1F7E1: '#E3C25A', 0x1F7E2: '#5FBF86', 0x1F7E3: '#B48AE0', 0x1F7E4: '#C99566', 0x1F7EC: '#D2B184'}
css = ['/* RS-ICONS-BEGIN: icone coerenti (maschere SVG) per sostituire le emoji decorative */']
for k, v in P.items():
    svg = "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'>%s</svg>" % v.replace('"', "'")
    css.append(".rs-i[data-ic=\"%s\"]{--ic:url(\"data:image/svg+xml,%s\")}" % (k, urllib.parse.quote(svg, safe="/:=' ,()")))
for cp, col in DOTS.items():
    css.append('.rs-i[data-ic="dot%x"]{background:%s;box-shadow:0 0 0 2px rgba(255,255,255,.08),0 0 8px %s}' % (cp, col, col + '88'))
css.append('/* RS-ICONS-END */')
open('/home/claude/work/tools/restyle_icons.css', 'w').write('\n'.join(css) + '\n')
mp = {str(k): v for k, v in M.items()}
for cp in DOTS: mp[str(cp)] = 'dot%x' % cp
json.dump(mp, open('/home/claude/work/tools/restyle_map.json', 'w'))
print(len(P), 'icone', len(mp), 'codepoint', sum(len(x) for x in css), 'byte css')
