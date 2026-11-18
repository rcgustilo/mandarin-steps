"""Builds sessions.tsv for Mandarin Steps: 1000 sessions of 5 items.

Sessions use the starter course in curriculum.txt first, then HSK 2.0 vocabulary
levels 1 to 6 (most frequent words first within each level). Every 7th session
is a review of 5 items drawn from the 6 sessions before it.

Vocabulary: complete-hsk-vocabulary by Yanis Zafirópulos (MIT licence).
Columns: session, topic, hanzi, (unused), pinyin, meaning
"""
import json, random, re, sys

TOTAL, PER = 1000, 5
here = sys.argv[1] if len(sys.argv) > 1 else "."
rng = random.Random(42)

# ---- starter course ----
lessons, cur = [], None
for line in open(f"{here}/curriculum.txt", encoding="utf-8"):
    line = line.strip()
    if not line:
        continue
    if line.startswith("#"):
        cur = (line[1:], []); lessons.append(cur)
    else:
        h, p, m = line.split("|")
        cur[1].append((h, p, m))
assert all(len(l[1]) == PER for l in lessons), [l[0] for l in lessons if len(l[1]) != PER]
seen = {h for _, items in lessons for h, _, _ in items}

# ---- HSK vocabulary ----
words = json.load(open(f"{here}/raw/complete.json", encoding="utf-8"))
def level(w):
    for l in w["level"]:
        if l.startswith("old-"):
            return int(l[4:])
    return None

VOWEL = set("aeoāáǎàēéěèōóǒò")
def join_pinyin(p):
    parts = p.split()
    out = parts[0] if parts else ""
    for q in parts[1:]:
        out += ("'" if q[:1].lower() in VOWEL else "") + q
    return out

def clean_meaning(ms):
    out = []
    for m in ms:
        m = re.sub(r"\bCL:.*", "", m).replace("(bound form) ", "").strip(" ;,")
        m = re.sub(r"\s+", " ", m)
        if m and m not in out:
            out.append(m)
        if len(out) == 2:
            break
    s = "; ".join(out)
    return s if len(s) <= 70 else s[:67].rsplit(" ", 1)[0] + "…"

hsk = []
for w in words:
    lv = level(w)
    if lv is None or w["simplified"] in seen:
        continue
    forms = w["forms"]
    f = next((x for x in forms if not x["transcriptions"]["pinyin"][:1].isupper()), forms[0])
    p = join_pinyin(f["transcriptions"]["pinyin"])
    m = clean_meaning(f["meanings"])
    if not m:
        continue
    seen.add(w["simplified"])
    hsk.append((lv, w.get("frequency") or 10**9, w["simplified"], p, m))
hsk.sort(key=lambda x: (x[0], x[1]))
chunks = [(t, items) for t, items in lessons]
for i in range(0, len(hsk), PER):
    part = hsk[i:i + PER]
    if len(part) < PER:
        break
    lv = part[0][0]
    chunks.append((f"HSK {lv} vocabulary", [(h, p, m) for _, _, h, p, m in part]))

# ---- lay out sessions ----
rows, history, ci = [], [], 0
for s in range(1, TOTAL + 1):
    if s % 7 == 0:
        pool = [it for sess in history[-6:] for it in sess]
        items = rng.sample(pool, PER)
        topic = "Review"
    else:
        topic, items = chunks[ci]; ci += 1
    history.append(items)
    for h, p, m in items:
        rows.append(f"{s}\t{topic}\t{h}\t\t{p}\t{m}")

open(f"{here}/sessions.tsv", "w", encoding="utf-8").write("\n".join(rows) + "\n")
last = chunks[ci - 1][0]
print(f"lessons={len(lessons)} hsk_words={len(hsk)} rows={len(rows)} last_topic={last} used_chunks={ci}")
