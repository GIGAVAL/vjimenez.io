"""Draws the Nolita and Berkshire charts as SVG from the numbers in the 2018 model and paper.
Run: python3 charts.py <portfolio dir>. The asserts fail if any figure stops adding up."""
import sys, os

OUT = sys.argv[1]
W, H = 1600, 1067
INK, LIME, GREY, MID, PALE = '#0b0b0b', '#E8FF3A', '#8a8a8a', '#c9c9c9', '#ededed'
FONT = "font-family=\"'Helvetica Neue', Helvetica, Arial, sans-serif\""


def t(x, y, s, size=28, weight=400, fill=INK, anchor='start', ls=0):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{ls}">{s}</text>'


def rect(x, y, w, h, fill, stroke=None):
    st = f' stroke="{stroke}" stroke-width="2"' if stroke else ''
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}"{st}/>'


def save(name, body):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" {FONT}>' \
          f'{rect(0, 0, W, H, "#ffffff")}{"".join(body)}</svg>'
    path = os.path.join(OUT, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').write(svg)
    print(name, len(svg))


def money(v):
    return f'${v / 1e6:.1f}M' if v >= 1e6 else f'${v:,.0f}'


# ---------- Nolita: capital stack ----------
SOURCES = [('First mortgage', 14_500_000, INK), ('Second mortgage', 18_000_000, '#3a3a3a'),
           ('LIRP loan', 4_350_000, '#6b6b6b'), ('Community space loan', 5_549_750, '#9a9a9a'),
           ('Deferred developer fee', 4_500_000, MID), ('Tax credit equity', 15_379_800, LIME)]
USES = [('Hard cost', 42_750_000, INK), ('Contingency', 1_325_020, '#6b6b6b'),
        ('Soft cost', 13_500_000, '#9a9a9a'), ('Developer fee', 4_500_000, MID),
        ('Reserves', 204_528, PALE), ('Land', 2, LIME)]
TDC = 62_279_550
assert sum(v for _, v, _ in SOURCES) == TDC and sum(v for _, v, _ in USES) == TDC
UNITS = 76
assert round(TDC / UNITS) == 819_468  # per apartment; the model's $372,931 divides by a different count, so it is not shown


def column(x, title, items, top=250, height=700, width=200, label_side='right'):
    out = [t(x + width / 2, top - 28, title, 24, 700, INK, 'middle', 3)]
    y = top + height
    floor = top + height + 60  # top edge of the label below; labels are pushed up so they never overlap
    for name, v, fill in items:
        h = max(height * v / TDC, 3)
        y -= h
        out.append(rect(x, y, width, h, fill, INK))
        lx = x + width + 22 if label_side == 'right' else x - 22
        anc = 'start' if label_side == 'right' else 'end'
        if h < 30:  # thin slices: one line
            ly = min(y + h / 2 + 8, floor - 10)
            out.append(t(lx, ly, f'{name}  {money(v)}', 22, 400, INK, anc))
            floor = ly - 24
        else:
            ly = min(y + h / 2 - 2, floor - 40)
            out.append(t(lx, ly, name, 24, 700, INK, anc))
            out.append(t(lx, ly + 30, f'{money(v)}  /  {v / TDC * 100:.0f}%', 22, 400, GREY, anc))
            floor = ly - 26
    return out


body = [t(70, 110, 'CAPITAL STACK', 24, 700, GREY, ls=4),
        t(64, 300, '$62.3M', 190, 800, INK, ls=-8),
        rect(70, 335, 470, 26, LIME),
        t(70, 425, '76 affordable apartments', 38, 700),
        t(70, 473, 'for seniors, over a retail base', 38, 700),
        t(70, 560, 'Nolita, Manhattan', 26, 400, GREY),
        t(70, 596, '20,265 sf city-owned through lot', 26, 400, GREY),
        t(70, 632, 'Land at $2. Zoning C6-2, R8 equivalent.', 26, 400, GREY),
        t(70, 760, 'Six sources.', 34, 700), t(70, 804, 'One quarter is tax credit equity.', 34, 700),
        t(70, 985, 'Redrawn 2026 from the 2018 team model', 20, 400, GREY, ls=1)]
body += column(900, 'SOURCES', SOURCES, label_side='left')
body += column(1130, 'USES', USES, label_side='right')
save('images/development/nolita/capital-stack.svg', body)

# ---------- Nolita: unit mix ----------
MIX = [('Studio', 16, 350, 20), ('1 bed', 12, 600, 60), ('2 bed', 20, 750, 60), ('3 bed', 16, 950, 60), ('4 bed', 12, 1150, 60)]
assert sum(u for _, u, _, _ in MIX) == UNITS
RENT_ROLL = sum(u * r * 12 for _, u, r, _ in MIX)
assert RENT_ROLL == 681_600
RETAIL = 1_550_000
body = [t(70, 110, 'UNIT MIX AND INCOME', 24, 700, GREY, ls=4),
        t(66, 240, '76 units', 120, 800, INK, ls=-4),
        t(70, 300, 'Rents from $350 to $1,150 a month, set at 20% and 60% of area median income', 28, 400, GREY)]
x0, base, bw, gap, scale = 90, 760, 150, 46, 17
for i, (name, u, r, ami) in enumerate(MIX):
    x = x0 + i * (bw + gap)
    h = u * scale
    body += [rect(x, base - h, bw, h, LIME if ami == 20 else INK, INK),
             t(x + bw / 2, base - h - 16, str(u), 44, 800, INK, 'middle'),
             t(x + bw / 2, base + 40, name, 26, 700, INK, 'middle'),
             t(x + bw / 2, base + 74, f'${r:,} / month', 22, 400, GREY, 'middle'),
             t(x + bw / 2, base + 104, f'{ami}% AMI', 22, 400, GREY, 'middle')]
# income comparison, same scale for both bars
ix, iw = 1130, 400
body += [t(ix, 400, 'ANNUAL INCOME', 22, 700, GREY, ls=3)]
for j, (name, v, fill) in enumerate([('Retail lease', RETAIL, INK), ('Apartment rent roll', RENT_ROLL, LIME)]):
    y = 440 + j * 170
    body += [rect(ix, y, iw * v / RETAIL, 64, fill, INK),
             t(ix, y + 104, name, 26, 700), t(ix + iw, y + 104, f'${v:,}', 26, 400, GREY, 'end')]
body += [t(ix, 830, f'The retail base earns {RETAIL / RENT_ROLL:.1f}x', 32, 700),
         t(ix, 872, 'the apartments above it.', 32, 700),
         t(70, 985, 'Redrawn 2026 from the 2018 team model', 20, 400, GREY, ls=1)]
save('images/development/nolita/unit-mix.svg', body)

# ---------- Berkshire: population change by age ----------
AGE = [('65 and over', 24_674, 28_605), ('18 to 24', 11_584, 12_237), ('25 to 34', 13_507, 13_816),
       ('45 to 64', 40_030, 37_349), ('35 to 44', 15_829, 12_795)]
body = [t(70, 110, 'BERKSHIRE COUNTY, MA  /  POPULATION BY AGE, 2010 TO 2017', 24, 700, GREY, ls=4),
        t(66, 250, 'An aging county', 120, 800, INK, ls=-4),
        t(70, 312, 'Residents 65 and over grew by 16%. The 35 to 44 group, the first-home buyers, fell by 19%.', 28, 400, GREY)]
zero, unit, y0, rowh = 800, 26, 400, 104
body.append(f'<line x1="{zero}" y1="{y0 - 20}" x2="{zero}" y2="{y0 + rowh * len(AGE) - 10}" stroke="{INK}" stroke-width="2"/>')
for i, (name, a, b) in enumerate(AGE):
    pct = (b - a) / a * 100
    y = y0 + i * rowh
    w = abs(pct) * unit
    x = zero if pct >= 0 else zero - w
    body += [rect(x, y, w, 62, LIME if i == 0 else INK, INK)]
    if pct >= 0:
        body += [t(zero - 24, y + 42, name, 30, 700, INK, 'end'), t(x + w + 20, y + 44, f'+{pct:.0f}%', 40, 800),
                 t(x + w + 150, y + 42, f'{a:,} to {b:,}', 22, 400, GREY)]
    else:
        body += [t(zero + 24, y + 42, name, 30, 700, INK, 'start'), t(x - 20, y + 44, f'{pct:.0f}%'.replace('-', '−'), 40, 800, INK, 'end'),
                 t(zero + 200, y + 42, f'{a:,} to {b:,}', 22, 400, GREY)]
body.append(t(70, 985, 'Redrawn 2026 from the tables in the 2018 study. Source data: US Census, American Community Survey', 20, 400, GREY, ls=1))
save('images/development/berkshire/aging-county.svg', body)

# ---------- Berkshire: occupied vs vacant homes ----------
YEARS = list(range(2010, 2018))
OCC = [56_517, 55_230, 55_420, 54_963, 54_706, 55_497, 54_204, 54_193]
VAC = [11_985, 13_270, 12_929, 13_285, 13_627, 12_909, 14_247, 15_047]
vp, op = (VAC[-1] - VAC[0]) / VAC[0] * 100, (OCC[-1] - OCC[0]) / OCC[0] * 100
assert round(vp) == 26 and round(op) == -4
body = [t(70, 110, 'BERKSHIRE COUNTY, MA  /  HOUSING UNITS, 2010 TO 2017', 24, 700, GREY, ls=4),
        t(66, 250, f'Vacant homes +{vp:.0f}%', 120, 800, INK, ls=-4),
        t(70, 312, f'Occupied homes fell {abs(op):.0f}% over the same years. The gap is the second-home market.', 28, 400, GREY)]
x0, base, bw, gap, scale = 110, 880, 120, 56, 0.0066
for i, yr in enumerate(YEARS):
    x = x0 + i * (bw + gap)
    ho, hv = OCC[i] * scale, VAC[i] * scale
    body += [rect(x, base - ho, bw, ho, INK, INK), rect(x, base - ho - hv, bw, hv, LIME, INK),
             t(x + bw / 2, base + 38, str(yr), 24, 700, INK, 'middle'),
             t(x + bw / 2, base - ho - hv - 14, f'{VAC[i]:,}', 22, 700, INK, 'middle'),
             t(x + bw / 2, base - 18, f'{OCC[i]:,}', 20, 400, '#ffffff', 'middle')]
body += [rect(1220, 170, 26, 26, LIME, INK), t(1260, 192, 'Vacant, including seasonal', 22),
         rect(1220, 210, 26, 26, INK), t(1260, 232, 'Occupied', 22),
         t(70, 985, 'Redrawn 2026 from the tables in the 2018 study. Source data: US Census, American Community Survey', 20, 400, GREY, ls=1)]
save('images/development/berkshire/vacant-homes.svg', body)

# ---------- Berkshire: property tax against bordering counties ----------
TAX = [('Sullivan, NY', 2.31), ('New Haven, CT', 2.23), ('Hillsborough, NH', 2.20), ('Providence, RI', 1.73), ('Berkshire, MA', 1.30)]
body = [t(70, 110, 'PROPERTY TAX RATE  /  BERKSHIRE AGAINST FOUR BORDERING COUNTIES', 24, 700, GREY, ls=4),
        t(66, 250, 'Lowest tax of five', 120, 800, INK, ls=-4),
        t(70, 312, 'A 1.3% rate beside counties at 1.7% to 2.3%: one reason second-home buyers cross the state line.', 28, 400, GREY)]
for i, (name, v) in enumerate(TAX):
    y = 400 + i * 104
    w = v * 430
    body += [t(400, y + 42, name, 30, 700, INK, 'end'), rect(430, y, w, 62, LIME if 'Berkshire' in name else INK, INK),
             t(430 + w + 20, y + 44, f'{v:.2f}%', 40, 800)]
body.append(t(70, 985, 'Redrawn 2026 from the table in the 2018 study', 20, 400, GREY, ls=1))
save('images/development/berkshire/property-tax.svg', body)
