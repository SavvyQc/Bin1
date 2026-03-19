"""
Red Rose Appraisals — Brand Playbook Generator
Produces a multi-page PDF brand guide.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect, Circle, String
from reportlab.platypus import Flowable
from datetime import date

# ── Brand Color Palette ────────────────────────────────────────────────────────
# Anchored to Lancaster County's "Red Rose City" heritage + professional CRE
ROSE_DEEP     = colors.HexColor("#8B1A1A")   # Primary — deep crimson rose
ROSE_MID      = colors.HexColor("#B22222")   # Secondary — firebrick red
ROSE_LIGHT    = colors.HexColor("#F5EDED")   # Background tint — blush white
GOLD          = colors.HexColor("#B8860B")   # Accent — dark goldenrod
GOLD_LIGHT    = colors.HexColor("#F5E6C8")   # Accent light
CHARCOAL      = colors.HexColor("#1E1E1E")   # Primary text
SLATE         = colors.HexColor("#4A4A4A")   # Secondary text
WARM_WHITE    = colors.HexColor("#FAF7F5")   # Page background / light panels
MID_GREY      = colors.HexColor("#9CA3AF")   # Muted / captions
RULE_LINE     = colors.HexColor("#D4A0A0")   # Decorative rule
WHITE         = colors.white


class ColorSwatch(Flowable):
    """Renders a labeled color swatch block."""
    def __init__(self, hex_color, name, hex_code, use_label, width=90, height=70):
        super().__init__()
        self.color = hex_color
        self.name = name
        self.hex_code = hex_code
        self.use_label = use_label
        self.width = width
        self.height = height

    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(0, self.height - 48, self.width, 48, fill=1, stroke=0)
        self.canv.setFillColor(colors.HexColor("#1E1E1E"))
        self.canv.setFont("Helvetica-Bold", 7.5)
        self.canv.drawString(0, self.height - 60, self.name)
        self.canv.setFont("Helvetica", 6.5)
        self.canv.setFillColor(colors.HexColor("#4A4A4A"))
        self.canv.drawString(0, self.height - 69, self.hex_code)
        self.canv.setFont("Helvetica", 6)
        self.canv.setFillColor(colors.HexColor("#9CA3AF"))
        self.canv.drawString(0, self.height - 78, self.use_label)


def make_styles():
    return {
        "cover_title": ParagraphStyle(
            "cover_title", fontName="Helvetica-Bold", fontSize=28,
            textColor=WHITE, leading=34, alignment=TA_LEFT,
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub", fontName="Helvetica", fontSize=11,
            textColor=colors.HexColor("#F5EDED"), leading=15, alignment=TA_LEFT,
        ),
        "cover_meta": ParagraphStyle(
            "cover_meta", fontName="Helvetica", fontSize=8,
            textColor=colors.HexColor("#D4A0A0"), leading=11, alignment=TA_LEFT,
        ),
        "section_num": ParagraphStyle(
            "section_num", fontName="Helvetica-Bold", fontSize=9,
            textColor=GOLD, leading=11, alignment=TA_LEFT,
        ),
        "section_title": ParagraphStyle(
            "section_title", fontName="Helvetica-Bold", fontSize=16,
            textColor=ROSE_DEEP, leading=20, spaceAfter=4, alignment=TA_LEFT,
        ),
        "subsection": ParagraphStyle(
            "subsection", fontName="Helvetica-Bold", fontSize=10,
            textColor=CHARCOAL, leading=13, spaceBefore=8, spaceAfter=3,
        ),
        "body": ParagraphStyle(
            "body", fontName="Helvetica", fontSize=8.5,
            textColor=SLATE, leading=13, spaceAfter=5,
        ),
        "body_bold": ParagraphStyle(
            "body_bold", fontName="Helvetica-Bold", fontSize=8.5,
            textColor=CHARCOAL, leading=13, spaceAfter=3,
        ),
        "callout": ParagraphStyle(
            "callout", fontName="Helvetica-BoldOblique", fontSize=10,
            textColor=ROSE_DEEP, leading=14, spaceAfter=6, leftIndent=12,
        ),
        "tag": ParagraphStyle(
            "tag", fontName="Helvetica-Bold", fontSize=7,
            textColor=WHITE, leading=9, alignment=TA_CENTER,
        ),
        "footer": ParagraphStyle(
            "footer", fontName="Helvetica", fontSize=7,
            textColor=MID_GREY, leading=9, alignment=TA_CENTER,
        ),
        "table_head": ParagraphStyle(
            "table_head", fontName="Helvetica-Bold", fontSize=8,
            textColor=WHITE, leading=10,
        ),
        "table_cell": ParagraphStyle(
            "table_cell", fontName="Helvetica", fontSize=8,
            textColor=CHARCOAL, leading=11,
        ),
        "table_cell_bold": ParagraphStyle(
            "table_cell_bold", fontName="Helvetica-Bold", fontSize=8,
            textColor=CHARCOAL, leading=11,
        ),
    }


def page_header(styles, section_num, section_name):
    rule = HRFlowable(width="100%", thickness=1.5, color=ROSE_DEEP, spaceAfter=4)
    num  = Paragraph(f"0{section_num}", styles["section_num"])
    name = Paragraph(section_name, styles["section_title"])
    return [rule, num, name]


def cover_page(styles):
    """Full-bleed dark cover."""
    # Cover block
    cover = Table(
        [[Paragraph("Red Rose\nAppraisals", styles["cover_title"])],
         [Spacer(1, 6)],
         [Paragraph("Brand Playbook", styles["cover_sub"])],
         [Spacer(1, 12)],
         [HRFlowable(width="100%", thickness=1, color=RULE_LINE)],
         [Spacer(1, 10)],
         [Paragraph(
             "Visual identity, voice, and brand standards for Red Rose Appraisals Ltd.\n"
             "Ephrata, Pennsylvania  ·  Certified Women's Owned Business",
             styles["cover_meta"])],
         [Spacer(1, 6)],
         [Paragraph(
             f"Issued: {date.today().strftime('%B %Y')}  ·  redroseappraisals.com  ·  "
             "(717) 314-4635  ·  chandra@redroseappraisals.com",
             styles["cover_meta"])],
        ],
        colWidths=[7.4*inch],
    )
    cover.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), ROSE_DEEP),
        ("LEFTPADDING",   (0,0), (-1,-1), 30),
        ("RIGHTPADDING",  (0,0), (-1,-1), 30),
        ("TOPPADDING",    (0,0), (0,0),   48),
        ("TOPPADDING",    (0,1), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (-1,-1), (-1,-1), 36),
    ]))
    return [cover, PageBreak()]


def brand_story_section(styles):
    els = page_header(styles, 1, "Brand Story & Positioning")
    els.append(Spacer(1, 8))

    els.append(Paragraph("Who We Are", styles["subsection"]))
    els.append(Paragraph(
        "Red Rose Appraisals Ltd. is a Lancaster County-based certified real estate appraisal firm "
        "founded and led by Chandra Mast, CGA BCA — a Certified General Appraiser licensed in "
        "Pennsylvania, Maryland, and Virginia, and a Business Certified Appraiser. The firm is a "
        "Certified Women's Owned Business headquartered at 148 Mason Drive, Ephrata, PA.",
        styles["body"]
    ))

    els.append(Paragraph("Our Name & Heritage", styles["subsection"]))
    els.append(Paragraph(
        "The red rose is Lancaster County's historic symbol — rooted in the Wars of the Roses, "
        "where the House of Lancaster carried the red rose as its emblem. Lancaster has been called "
        "\"The Red Rose City\" for centuries. Our name honors that heritage while signaling precision, "
        "beauty, and deep local rootedness. A rose also implies care, expertise, and cultivation — "
        "qualities that define our appraisal practice.",
        styles["body"]
    ))

    els.append(Paragraph("Brand Positioning Statement", styles["subsection"]))
    els.append(Paragraph(
        "\"For investors, attorneys, lenders, and property owners who require defensible, "
        "data-forward valuations — Red Rose Appraisals delivers expert certified appraisals "
        "anchored in econometrics, AI-augmented analysis, and 20+ years of Lancaster County "
        "market knowledge. We are the region's most technically rigorous appraisal practice.\"",
        styles["callout"]
    ))

    els.append(Paragraph("Core Differentiators", styles["subsection"]))
    differentiators = [
        ("Technical Rigor", "Econometrics and trend analysis embedded in every report. "
         "No guesswork — only defensible, data-supported conclusions."),
        ("AI + UAS Integration", "Drone imagery and artificial intelligence tools augment "
         "site analysis and market data synthesis, delivering deeper accuracy."),
        ("Breadth of Property Types", "Industrial, commercial, agricultural, equestrian, historic, "
         "and special-purpose properties — including complex going concern valuations."),
        ("Regulatory Authority", "Chandra Mast serves as Secretary of the PA State Board of "
         "Certified Real Estate Appraisers, reflecting the firm's standing in the profession."),
        ("Local Depth", "Exclusively focused on South Central PA (Lancaster, Lebanon, Berks, "
         "Dauphin, York) with deep submarket knowledge no national firm can replicate."),
    ]
    tbl_data = [[Paragraph(d[0], styles["table_cell_bold"]),
                 Paragraph(d[1], styles["table_cell"])] for d in differentiators]
    tbl = Table(tbl_data, colWidths=[1.6*inch, 5.6*inch])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (0,-1), ROSE_LIGHT),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("LINEBELOW",     (0,0), (-1,-2), 0.5, RULE_LINE),
    ]))
    els.append(tbl)
    return els


def color_section(styles):
    els = [PageBreak()]
    els += page_header(styles, 2, "Color Palette")
    els.append(Spacer(1, 8))

    els.append(Paragraph(
        "The Red Rose Appraisals palette is anchored by Lancaster County's historic crimson rose, "
        "paired with warm gold to signal credibility and achievement, and grounded by charcoal and "
        "warm white for professional readability. Never use the primary red on large text blocks — "
        "reserve it for headers, accents, and graphic elements.",
        styles["body"]
    ))
    els.append(Spacer(1, 10))

    swatches = [
        (ROSE_DEEP,  "Rose Deep",    "#8B1A1A", "Primary / Headers"),
        (ROSE_MID,   "Rose Mid",     "#B22222", "Accents / Dividers"),
        (GOLD,       "Lancaster Gold","#B8860B", "Accent / Highlight"),
        (CHARCOAL,   "Charcoal",     "#1E1E1E", "Body Text"),
        (SLATE,      "Slate",        "#4A4A4A", "Secondary Text"),
        (WARM_WHITE, "Warm White",   "#FAF7F5", "Page Background"),
        (ROSE_LIGHT, "Blush",        "#F5EDED", "Panel Fill"),
        (MID_GREY,   "Stone",        "#9CA3AF", "Captions / Muted"),
    ]

    sw_row = [[ColorSwatch(c, n, h, u) for c, n, h, u in swatches[:4]],
              [ColorSwatch(c, n, h, u) for c, n, h, u in swatches[4:]]]

    for row in sw_row:
        tbl = Table([row], colWidths=[1.85*inch]*4)
        tbl.setStyle(TableStyle([
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING", (0,0), (-1,-1), 2),
            ("RIGHTPADDING", (0,0), (-1,-1), 2),
        ]))
        els.append(tbl)
        els.append(Spacer(1, 16))

    els.append(Paragraph("Color Usage Rules", styles["subsection"]))
    rules = [
        ["DO", "Use Rose Deep (#8B1A1A) for all section headers and key graphic elements."],
        ["DO", "Use Lancaster Gold (#B8860B) sparingly — metric callouts, key data highlights."],
        ["DO", "Use Warm White (#FAF7F5) as the primary background on all documents."],
        ["DO", "Use Charcoal (#1E1E1E) for all body text to ensure readability."],
        ["DON'T", "Place red text on colored backgrounds — use white or charcoal instead."],
        ["DON'T", "Use more than 2 brand colors in a single design element or panel."],
        ["DON'T", "Substitute bright/neon reds or pinks — the rose must read as deep and rich."],
    ]
    tbl_data = [[Paragraph(r[0], ParagraphStyle("do",
                    fontName="Helvetica-Bold", fontSize=7.5,
                    textColor=WHITE if r[0]=="DO" else colors.HexColor("#7F1D1D"),
                    alignment=TA_CENTER, leading=10)),
                 Paragraph(r[1], styles["table_cell"])] for r in rules]
    tbl = Table(tbl_data, colWidths=[0.6*inch, 6.6*inch])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (0,-1), ROSE_DEEP),
        ("BACKGROUND",    (0,4), (0,-1), ROSE_LIGHT),
        ("LEFTPADDING",   (0,0), (-1,-1), 7),
        ("RIGHTPADDING",  (0,0), (-1,-1), 7),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("LINEBELOW",     (0,0), (-1,-2), 0.4, RULE_LINE),
    ]))
    els.append(tbl)
    return els


def typography_section(styles):
    els = [PageBreak()]
    els += page_header(styles, 3, "Typography")
    els.append(Spacer(1, 8))

    els.append(Paragraph(
        "Red Rose Appraisals uses a clean, authoritative type system. "
        "Helvetica (system-safe) is the standard for all digital and print documents. "
        "For premium printed materials, substitute <b>Playfair Display</b> (serif) for display "
        "headings to invoke historical gravitas consistent with the Lancaster County heritage narrative.",
        styles["body"]
    ))

    type_data = [
        [Paragraph("Role", styles["table_head"]),
         Paragraph("Typeface", styles["table_head"]),
         Paragraph("Weight", styles["table_head"]),
         Paragraph("Size", styles["table_head"]),
         Paragraph("Color", styles["table_head"])],
        ["Display Headline", "Playfair Display / Helvetica-Bold", "Bold", "24–32pt", "Rose Deep or White"],
        ["Section Header",   "Helvetica-Bold",                    "Bold", "12–16pt", "Rose Deep"],
        ["Subheading",       "Helvetica-Bold",                    "Bold", "9–11pt",  "Charcoal"],
        ["Body Copy",        "Helvetica",                         "Regular","8–9pt", "Slate"],
        ["Captions / Notes", "Helvetica",                         "Regular","6.5–7pt","Stone"],
        ["Data Callouts",    "Helvetica-Bold",                    "Bold", "14–18pt", "Lancaster Gold"],
        ["Legal / Footnotes","Helvetica",                         "Regular","6–7pt", "Stone"],
    ]
    col_w = [1.4*inch, 1.9*inch, 1*inch, 0.8*inch, 1.7*inch]
    formatted_rows = []
    for i, row in enumerate(type_data):
        if i == 0:
            formatted_rows.append(row)  # already Paragraphs
        else:
            formatted_rows.append([Paragraph(str(c), styles["table_cell"]) for c in row])
    tbl = Table(formatted_rows, colWidths=col_w)
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  ROSE_DEEP),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WARM_WHITE, ROSE_LIGHT]),
        ("LINEBELOW",     (0,0), (-1,-2), 0.4, RULE_LINE),
        ("LEFTPADDING",   (0,0), (-1,-1), 7),
        ("RIGHTPADDING",  (0,0), (-1,-1), 7),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    els.append(tbl)
    els.append(Spacer(1, 10))

    els.append(Paragraph("Type Hierarchy Example", styles["subsection"]))
    demo = Table([
        [Paragraph("Red Rose Appraisals", ParagraphStyle("d1",
            fontName="Helvetica-Bold", fontSize=22, textColor=ROSE_DEEP, leading=26))],
        [Paragraph("Lancaster County Commercial Market Intelligence", ParagraphStyle("d2",
            fontName="Helvetica-Bold", fontSize=11, textColor=CHARCOAL, leading=14))],
        [Paragraph(
            "Expert certified appraisals anchored in econometrics, AI-augmented analysis, "
            "and 20+ years of local market knowledge.",
            ParagraphStyle("d3", fontName="Helvetica", fontSize=8.5,
                           textColor=SLATE, leading=12))],
        [Paragraph("Source: ROCK CRE Q4 2025  ·  CommercialCafe / Yardi  ·  CoStar",
            ParagraphStyle("d4", fontName="Helvetica", fontSize=6.5,
                           textColor=MID_GREY, leading=9))],
    ], colWidths=[7.4*inch])
    demo.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), ROSE_LIGHT),
        ("LEFTPADDING",   (0,0), (-1,-1), 14),
        ("RIGHTPADDING",  (0,0), (-1,-1), 14),
        ("TOPPADDING",    (0,0), (0,0),   14),
        ("TOPPADDING",    (0,1), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-2), 4),
        ("BOTTOMPADDING", (-1,-1),(-1,-1),12),
        ("LINEABOVE",     (0,0), (0,0),   2.5, ROSE_DEEP),
    ]))
    els.append(demo)
    return els


def voice_section(styles):
    els = [PageBreak()]
    els += page_header(styles, 4, "Voice & Tone")
    els.append(Spacer(1, 8))

    els.append(Paragraph(
        "Red Rose Appraisals communicates with the confidence of a recognized expert and the "
        "clarity of a trusted local advisor. Every word should reinforce three qualities: "
        "<b>precision, authority, and accessibility.</b> We never oversimplify or condescend — "
        "our clients are sophisticated. We never overreach or speculate beyond our data.",
        styles["body"]
    ))

    els.append(Paragraph("Voice Pillars", styles["subsection"]))
    pillars = [
        ("Data-Forward",
         "Lead with numbers, sourced facts, and defensible conclusions. "
         "Opinions are earned through evidence, not asserted."),
        ("Expert but Approachable",
         "Chandra Mast holds the highest credentials in the field and sits on the state board. "
         "The brand communicates that authority without jargon or gatekeeping."),
        ("Local Authority",
         "Deep Lancaster County knowledge is a core differentiator. "
         "Reference local geography, submarkets, and history with familiarity."),
        ("Technologically Fluent",
         "AI and drone technology are normalizing in appraisal. "
         "Use clear, confident language around these tools — not hype."),
        ("Ethically Grounded",
         "USPAP compliance, independence, and integrity are non-negotiable. "
         "The brand communicates these as standards, not marketing claims."),
    ]
    for p in pillars:
        inner = Table([[
            Paragraph(p[0], ParagraphStyle("pl",
                fontName="Helvetica-Bold", fontSize=8.5,
                textColor=ROSE_DEEP, leading=11)),
            Paragraph(p[1], styles["body"])
        ]], colWidths=[1.5*inch, 5.7*inch])
        inner.setStyle(TableStyle([
            ("VALIGN",        (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING",   (0,0), (-1,-1), 8),
            ("RIGHTPADDING",  (0,0), (-1,-1), 8),
            ("TOPPADDING",    (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ("LINEBELOW",     (0,0), (-1,-1), 0.4, RULE_LINE),
            ("BACKGROUND",    (0,0), (0,-1),  ROSE_LIGHT),
        ]))
        els.append(inner)
        els.append(Spacer(1, 2))

    els.append(Paragraph("Do / Don't Language Examples", styles["subsection"]))
    examples = [
        ("DO SAY",   "\"Industrial vacancy in Lancaster County held below 1.5% through Q4 2025, "
                     "representing the tightest submarket in the South Central PA corridor.\""),
        ("DON'T SAY","\"The market is really hot right now and properties are flying off shelves!\""),
        ("DO SAY",   "\"Our drone-assisted site analysis provides high-resolution imagery that "
                     "informs both site-specific and market-wide evaluations.\""),
        ("DON'T SAY","\"We use cutting-edge tech to give you the best appraisal possible.\""),
        ("DO SAY",   "\"Data for this submarket segment is limited at time of publication; "
                     "the gap is noted explicitly rather than estimated.\""),
        ("DON'T SAY","\"Based on our experience, we believe values are probably around...\""),
    ]
    ex_tbl = Table(
        [[Paragraph(e[0], ParagraphStyle("el",
              fontName="Helvetica-Bold", fontSize=7.5, textColor=WHITE,
              alignment=TA_CENTER, leading=10)),
          Paragraph(e[1], styles["table_cell"])] for e in examples],
        colWidths=[0.85*inch, 6.35*inch]
    )
    ex_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (0,-1), ROSE_DEEP),
        ("BACKGROUND",    (0,1), (0,1),  ROSE_LIGHT),
        ("BACKGROUND",    (0,3), (0,3),  ROSE_LIGHT),
        ("BACKGROUND",    (0,5), (0,5),  ROSE_LIGHT),
        ("LEFTPADDING",   (0,0), (-1,-1), 7),
        ("RIGHTPADDING",  (0,0), (-1,-1), 7),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("LINEBELOW",     (0,0), (-1,-2), 0.4, RULE_LINE),
    ]))
    els.append(ex_tbl)
    return els


def applications_section(styles):
    els = [PageBreak()]
    els += page_header(styles, 5, "Brand Applications & Standards")
    els.append(Spacer(1, 8))

    els.append(Paragraph("Document Standards", styles["subsection"]))
    els.append(Paragraph(
        "All client-facing reports, market intelligence summaries, and proposals produced by "
        "Red Rose Appraisals must adhere to these layout standards:",
        styles["body"]
    ))
    doc_rules = [
        ("Page Background",     "Warm White (#FAF7F5) — never pure white or grey"),
        ("Header Bar",          "Rose Deep (#8B1A1A) with white title text"),
        ("Section Dividers",    "Rose Deep 1.5pt rule above each major section"),
        ("Metric Callouts",     "Lancaster Gold (#B8860B) for key data figures"),
        ("Body Text",           "Charcoal (#1E1E1E) or Slate (#4A4A4A), 8–9pt Helvetica"),
        ("Source Citations",    "Clickable hyperlinks in Rose Mid (#B22222), 6.5–7pt"),
        ("Margins",             "0.6in all sides minimum on letter-size pages"),
        ("Footer",              "Company name · URL · Phone · Page number in Stone (#9CA3AF)"),
    ]
    tbl = Table(
        [[Paragraph(r[0], styles["table_cell_bold"]),
          Paragraph(r[1], styles["table_cell"])] for r in doc_rules],
        colWidths=[1.8*inch, 5.4*inch]
    )
    tbl.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [WARM_WHITE, ROSE_LIGHT]),
        ("LEFTPADDING",    (0,0), (-1,-1), 8),
        ("RIGHTPADDING",   (0,0), (-1,-1), 8),
        ("TOPPADDING",     (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",  (0,0), (-1,-1), 5),
        ("LINEBELOW",      (0,0), (-1,-2), 0.4, RULE_LINE),
        ("BACKGROUND",     (0,0), (0,-1),  ROSE_LIGHT),
    ]))
    els.append(tbl)
    els.append(Spacer(1, 10))

    els.append(Paragraph("Report Header Template", styles["subsection"]))
    els.append(Paragraph(
        "Every client-facing document opens with the following structured header block:",
        styles["body"]
    ))
    hdr_demo = Table([
        [Paragraph("Red Rose Appraisals", ParagraphStyle("hd1",
             fontName="Helvetica-Bold", fontSize=14, textColor=WHITE, leading=17)),
         Paragraph("[Document Title]", ParagraphStyle("hd1r",
             fontName="Helvetica-Bold", fontSize=9, textColor=colors.HexColor("#D4A0A0"),
             alignment=TA_RIGHT, leading=11))],
        [Paragraph("Certified Real Estate Appraisers  ·  Ephrata, PA  ·  redroseappraisals.com",
             ParagraphStyle("hd2", fontName="Helvetica", fontSize=7.5,
                            textColor=colors.HexColor("#F5EDED"), leading=10)),
         Paragraph("[Date]", ParagraphStyle("hd2r", fontName="Helvetica", fontSize=7.5,
             textColor=colors.HexColor("#D4A0A0"), alignment=TA_RIGHT, leading=10))],
    ], colWidths=[4.6*inch, 2.6*inch])
    hdr_demo.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), ROSE_DEEP),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("RIGHTPADDING",  (0,0), (-1,-1), 12),
        ("TOPPADDING",    (0,0), (0,-1),  8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("ALIGN",         (1,0), (1,-1),  "RIGHT"),
    ]))
    els.append(hdr_demo)
    els.append(Spacer(1, 10))

    els.append(Paragraph("Contact Block Standard", styles["subsection"]))
    contact = Table([[
        Paragraph(
            "<b>Red Rose Appraisals Ltd.</b><br/>"
            "Chandra Mast, CGA BCA<br/>"
            "148 Mason Drive, Ephrata, PA 17522",
            ParagraphStyle("cb", fontName="Helvetica", fontSize=8.5,
                           textColor=CHARCOAL, leading=12)
        ),
        Paragraph(
            "<b>(717) 314-4635</b><br/>"
            "chandra@redroseappraisals.com<br/>"
            "redroseappraisals.com",
            ParagraphStyle("cb2", fontName="Helvetica", fontSize=8.5,
                           textColor=CHARCOAL, leading=12, alignment=TA_RIGHT)
        ),
    ]], colWidths=[3.7*inch, 3.7*inch])
    contact.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), ROSE_LIGHT),
        ("LINEABOVE",     (0,0), (-1,0),  2, ROSE_DEEP),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("RIGHTPADDING",  (0,0), (-1,-1), 12),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ]))
    els.append(contact)
    return els


def build_playbook(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.6*inch,
        rightMargin=0.6*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch,
    )
    styles = make_styles()
    story = []
    story += cover_page(styles)
    story += brand_story_section(styles)
    story += color_section(styles)
    story += typography_section(styles)
    story += voice_section(styles)
    story += applications_section(styles)
    doc.build(story)
    print(f"Brand playbook written to: {output_path}")


if __name__ == "__main__":
    build_playbook("/home/user/Bin1/Red_Rose_Brand_Playbook.pdf")
