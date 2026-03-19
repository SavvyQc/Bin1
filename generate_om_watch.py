"""
Lancaster County OM Watch — PDF Report Generator
Produces a one-page professional CRE market summary.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import KeepTogether
from datetime import date
import os

# ── Color Palette ──────────────────────────────────────────────────────────────
NAVY      = colors.HexColor("#1B2B4B")
STEEL     = colors.HexColor("#2E5E8E")
SLATE     = colors.HexColor("#4A6FA5")
AMBER     = colors.HexColor("#D97706")
LIGHT_BG  = colors.HexColor("#F0F4F8")
MID_GREY  = colors.HexColor("#6B7280")
WHITE     = colors.white
BLACK     = colors.black

# ── Styles ─────────────────────────────────────────────────────────────────────
def make_styles():
    return {
        "report_title": ParagraphStyle(
            "report_title",
            fontName="Helvetica-Bold",
            fontSize=15,
            textColor=WHITE,
            alignment=TA_LEFT,
            leading=18,
            spaceAfter=2,
        ),
        "report_sub": ParagraphStyle(
            "report_sub",
            fontName="Helvetica",
            fontSize=9,
            textColor=colors.HexColor("#CBD5E1"),
            alignment=TA_LEFT,
            leading=11,
        ),
        "section_header": ParagraphStyle(
            "section_header",
            fontName="Helvetica-Bold",
            fontSize=10,
            textColor=WHITE,
            alignment=TA_LEFT,
            leading=13,
            leftIndent=6,
        ),
        "body": ParagraphStyle(
            "body",
            fontName="Helvetica",
            fontSize=8,
            textColor=BLACK,
            leading=11,
            spaceAfter=3,
        ),
        "metric_label": ParagraphStyle(
            "metric_label",
            fontName="Helvetica-Bold",
            fontSize=7.5,
            textColor=NAVY,
            leading=10,
        ),
        "metric_value": ParagraphStyle(
            "metric_value",
            fontName="Helvetica-Bold",
            fontSize=11,
            textColor=STEEL,
            leading=13,
        ),
        "metric_note": ParagraphStyle(
            "metric_note",
            fontName="Helvetica",
            fontSize=6.5,
            textColor=MID_GREY,
            leading=8,
        ),
        "outlook_body": ParagraphStyle(
            "outlook_body",
            fontName="Helvetica",
            fontSize=8,
            textColor=NAVY,
            leading=11,
            spaceAfter=0,
        ),
        "source_text": ParagraphStyle(
            "source_text",
            fontName="Helvetica",
            fontSize=6.2,
            textColor=MID_GREY,
            leading=8.5,
        ),
        "source_label": ParagraphStyle(
            "source_label",
            fontName="Helvetica-Bold",
            fontSize=6.5,
            textColor=NAVY,
            leading=8.5,
        ),
    }


def header_block(styles, report_date):
    """Dark navy header bar with title and date."""
    title = Paragraph("Lancaster County OM Watch", styles["report_title"])
    sub   = Paragraph(
        "Commercial Real Estate Market Intelligence  |  Industrial · Office · Retail",
        styles["report_sub"]
    )
    date_p = ParagraphStyle(
        "date_p", fontName="Helvetica-Bold", fontSize=8.5,
        textColor=colors.HexColor("#94A3B8"), alignment=TA_RIGHT, leading=11
    )
    date_str = Paragraph(report_date, date_p)

    tbl = Table(
        [[title, date_str], [sub, ""]],
        colWidths=[4.8*inch, 2.6*inch],
        rowHeights=[18, 13],
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,-1), NAVY),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
        ("ALIGN",       (1,0), (1,0),   "RIGHT"),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
        ("RIGHTPADDING",(0,0), (-1,-1), 10),
        ("TOPPADDING",  (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("SPAN",        (0,1), (-1,1)),
    ]))
    return tbl


def section_label(title, color, styles):
    """Colored section header bar."""
    tbl = Table(
        [[Paragraph(f"▌  {title}", styles["section_header"])]],
        colWidths=[7.4*inch],
        rowHeights=[16],
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), color),
        ("TOPPADDING",   (0,0), (-1,-1), 2),
        ("BOTTOMPADDING",(0,0), (-1,-1), 2),
        ("LEFTPADDING",  (0,0), (-1,-1), 4),
    ]))
    return tbl


def metric_cell(label, value, note, styles):
    return [
        Paragraph(label, styles["metric_label"]),
        Paragraph(value, styles["metric_value"]),
        Paragraph(note,  styles["metric_note"]),
    ]


def metrics_row(cells, styles):
    """Horizontal row of 4 key metric boxes."""
    col_data = [[Paragraph(c[0], styles["metric_label"]),
                 Paragraph(c[1], styles["metric_value"]),
                 Paragraph(c[2], styles["metric_note"])] for c in cells]

    tbl = Table(
        [col_data],
        colWidths=[1.85*inch]*4,
        rowHeights=None,
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), LIGHT_BG),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
        ("LINEAFTER",    (0,0), (2,0),   0.5, colors.HexColor("#D1D5DB")),
    ]))
    return tbl


def build_section(title, color, summary_text, metric_cells, styles):
    """Complete asset-class section: header + metrics + narrative."""
    elements = []
    elements.append(Spacer(1, 5))
    elements.append(section_label(title, color, styles))
    elements.append(Spacer(1, 4))
    elements.append(metrics_row(metric_cells, styles))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph(summary_text, styles["body"]))
    return elements


def build_report(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.6*inch,
        rightMargin=0.6*inch,
        topMargin=0.45*inch,
        bottomMargin=0.45*inch,
    )

    styles = make_styles()
    report_date = date.today().strftime("%B %d, %Y")
    story = []

    # ── Header ────────────────────────────────────────────────────────────────
    story.append(header_block(styles, report_date))
    story.append(Spacer(1, 6))

    # ── INDUSTRIAL ────────────────────────────────────────────────────────────
    ind_metrics = [
        ("VACANCY RATE",     "~1.5%",       "County avg; mfg. <1%"),
        ("AVG ASKING RENT",  "$8.67/SF",    "Warehouse avg $5.14/SF"),
        ("RENT GROWTH (YOY)","~11%",        "South Central PA avg"),
        ("INV. SALES (2025)","$419M",       "Record 12-mo. volume"),
    ]
    ind_text = (
        "Lancaster County's industrial market remains the tightest in the South Central PA region, "
        "with a countywide vacancy rate of approximately 1.5% and manufacturing space tracking below 1% — "
        "well inside the regional I-81/I-78 Corridor benchmark of 7.2% and the national average of 9.6%. "
        "Developers delivered 1.1 million SF across four projects in 2025, with an additional 927,500 SF "
        "delivered in 2024; demand absorbed supply immediately, as evidenced by Panattoni's 400,000 SF "
        "East Hempfield spec build reaching full lease-up upon delivery. Dalfen Industrial's $29M acquisition "
        "of a 251,250 SF warehouse at 791 Stony Battery Road, Landisville (~$115/SF) was among the region's "
        "largest Q3 2025 trades. Average lease rates rose ~11% YOY. Supply constraints are severe: fewer "
        "than one development-ready industrial parcel per township exists within growth boundaries, and last-mile "
        "e-commerce demand continues to accelerate. <b>Data gap:</b> Submarket-level absorption figures for "
        "Manheim Township and Ephrata corridors not publicly available at time of publication."
    )
    story += build_section(
        "INDUSTRIAL", STEEL, ind_text, ind_metrics, styles
    )

    # ── OFFICE ────────────────────────────────────────────────────────────────
    off_metrics = [
        ("AVG ASKING RENT",  "$20.10/SF",   "Class A: $23.00/SF"),
        ("CLASS B / C",      "$21.92 / $12.26", "Per SF annually"),
        ("VACANCY RANGE",    "6%–23%",      "Manheim Twp. to E. Lampeter"),
        ("STOCK AGE",        "78.5%",       "Built pre-2000"),
    ]
    off_text = (
        "Lancaster's office market reflects national post-pandemic restructuring at a compressed local scale. "
        "Vacancy ranges sharply by submarket: Manheim Township, the county's premier suburban office node, "
        "records the lowest vacancy at 6.02%, while West and East Lampeter submarkets carry vacancies as high "
        "as 22.75%, consistent with obsolete stock suffering hybrid-work pressure. Average full-service asking "
        "rents of $20.10/SF compare favorably to the national suburban average and suggest a functional, "
        "affordable market for right-sized tenants. Notably, 78.5% of county office inventory was delivered "
        "before 2000 — creating both repositioning opportunities and ongoing obsolescence risk. The most "
        "significant recent addition is Lancaster Stockyard at 1280 N. Plum Street / 1310 Marshall Avenue, "
        "a 56,500 SF adaptive-reuse development representing the largest new office delivery in the city. "
        "Conversion of older Class C assets to mixed-use or residential remains an active trend. "
        "<b>Data gap:</b> Countywide net absorption figures for 2025 were not publicly available."
    )
    story += build_section(
        "OFFICE", SLATE, off_text, off_metrics, styles
    )

    # ── RETAIL ────────────────────────────────────────────────────────────────
    ret_metrics = [
        ("AVG ASKING RENT",  "$17.00/SF",   "Lancaster city avg"),
        ("NAT'L VACANCY",    "4.3%",        "Q4 2025; shopping ctrs 5.2%"),
        ("AVG UNIT SIZE",    "3,639 SF",    "35 active listings"),
        ("ABSORPTION (NAT'L)","91M+ SF",    "Highest pace since Q2 2022"),
    ]
    ret_text = (
        "Lancaster County's retail market is demonstrating resilience driven by population growth, tourism "
        "infrastructure, and a diversified tenant base. Average asking rents in Lancaster city are approximately "
        "$17/SF annually — below the national Q4 2025 average of $26.13/SF — reflecting the county's "
        "affordability profile and suburban character. Nationally, the retail vacancy rate held at 4.3% for "
        "a third consecutive quarter, with shopping centers at 5.2%; Lancaster's local market is presumed to "
        "track near or below these benchmarks given population growth and limited new supply. The dominant "
        "trend locally is the continued shift from traditional goods-based tenants toward service, wellness, "
        "and experiential uses — fitness centers, salons, food & beverage, and healthcare — filling vacancies "
        "left by national chain rationalization. Lancaster Central Market, operational since the 1700s, anchors "
        "downtown retail vitality. National construction of new retail remains at its lowest since 2021, "
        "further supporting rent stability heading into 2026. "
        "<b>Data gap:</b> Lancaster County-specific retail vacancy and submarket absorption data is not "
        "publicly reported at the county level; figures above rely on national benchmarks and local listing data."
    )
    story += build_section(
        "RETAIL", AMBER, ret_text, ret_metrics, styles
    )

    # ── MARKET OUTLOOK ────────────────────────────────────────────────────────
    story.append(Spacer(1, 6))
    outlook_tbl = Table(
        [[Paragraph(
            "<b>Market Outlook — Lancaster County CRE | 2026</b>",
            ParagraphStyle("oh", fontName="Helvetica-Bold", fontSize=8.5,
                           textColor=NAVY, leading=11)
        )],
        [Paragraph(
            "Lancaster County enters 2026 as one of Pennsylvania's most supply-constrained industrial markets, "
            "with record investment volumes, minimal available land, and sustained rent appreciation positioning "
            "it as a regional outperformer. The office market faces a bifurcated path: well-located Class A/B "
            "suburban space will hold occupancy, while older suburban stock faces repositioning pressure or "
            "conversion. Retail fundamentals remain stable, supported by a growing population base, limited "
            "new supply nationally, and the continued shift to experiential and service tenants. Key risk "
            "factors include interest rate sensitivity on investment sales, tariff impacts on construction "
            "costs, and municipal land-use constraints limiting industrial pipeline. Overall market sentiment "
            "is cautiously optimistic, with industrial leading momentum.",
            styles["outlook_body"]
        )]],
        colWidths=[7.4*inch],
    )
    outlook_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (0,0), colors.HexColor("#E8EEF6")),
        ("BACKGROUND",   (0,1), (0,1), colors.HexColor("#F5F8FF")),
        ("LEFTPADDING",  (0,0), (-1,-1), 10),
        ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING",   (0,0), (0,0),   5),
        ("BOTTOMPADDING",(0,0), (0,0),   4),
        ("TOPPADDING",   (0,1), (0,1),   6),
        ("BOTTOMPADDING",(0,1), (0,1),   7),
        ("LINEABOVE",    (0,0), (0,0),   1.5, NAVY),
    ]))
    story.append(outlook_tbl)

    # ── SOURCES ───────────────────────────────────────────────────────────────
    story.append(Spacer(1, 5))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1")))
    story.append(Spacer(1, 3))
    story.append(Paragraph("<b>SOURCES</b>", styles["source_label"]))
    sources = (
        "ROCK Commercial Real Estate — Quarterly Market Reports (rockrealestate.net/market-reports)  ·  "
        "Bisnow — \"As Pennsylvania's Top Industrial Markets Face Constraints, Investors Jump To 2 Overlooked Counties\" (2025)  ·  "
        "CommercialCafe / Yardi Research — Lancaster Office & Industrial Market Trends  ·  "
        "CommercialSearch — Lancaster County Active Listings Data  ·  "
        "CoStar — Lancaster County Industrial Investment Volume (via Bisnow)  ·  "
        "Colliers — U.S. Retail Q4 2025 Vacancy Report (knowledge-leader.colliers.com)  ·  "
        "CommercialCafe — U.S. Industrial & Office National Reports (Feb 2026)  ·  "
        "Cushman & Wakefield — PA I-81/I-78 Corridor MarketBeat  ·  "
        "Pennsylvania DCED / PIDA — Board Minutes & Loan Approvals (Nov 2025)  ·  "
        "Lancaster City Alliance — Development Activity (lancastercityalliance.org)  ·  "
        "EDC Lancaster County (edclancaster.com)  ·  "
        "CityFeet — Lancaster PA Retail Listings  ·  "
        "Central Penn Business Journal — Industrial Market Coverage  ·  "
        "propertycashin.com — Lancaster Commercial Market Statistics 2025"
    )
    story.append(Paragraph(sources, styles["source_text"]))

    doc.build(story)
    print(f"Report written to: {output_path}")


if __name__ == "__main__":
    out = "/home/user/Bin1/Lancaster_County_OM_Watch.pdf"
    build_report(out)
