"""
Red Rose Appraisals — Email Signature Generator
Produces:
  1. email_signature.html  — paste into Gmail / Outlook HTML editor
  2. Email_Signature_Guide.pdf — brand standard doc with usage instructions
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from datetime import date

# ── Brand palette ──────────────────────────────────────────────────────────────
ROSE_DEEP  = colors.HexColor("#8B1A1A")
ROSE_MID   = colors.HexColor("#B22222")
ROSE_LIGHT = colors.HexColor("#F5EDED")
GOLD       = colors.HexColor("#B8860B")
CHARCOAL   = colors.HexColor("#1E1E1E")
SLATE      = colors.HexColor("#4A4A4A")
WARM_WHITE = colors.HexColor("#FAF7F5")
MID_GREY   = colors.HexColor("#9CA3AF")
RULE_LINE  = colors.HexColor("#D4A0A0")
WHITE      = colors.white


# ══════════════════════════════════════════════════════════════════════════════
# 1.  HTML Signature
# ══════════════════════════════════════════════════════════════════════════════

HTML_SIGNATURE = """\
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"></head>
<body>
<!--
  RED ROSE APPRAISALS — Email Signature
  Standard version  |  Generated {date}
  Instructions:
    Gmail  → Settings → See all settings → General → Signature → Create new
             → paste entire block between the hr tags below
    Outlook → File → Options → Mail → Signatures → New
             → switch editor to HTML view → paste entire block
  Do NOT alter fonts, colors, or layout without brand approval.
-->
<table cellpadding="0" cellspacing="0" border="0"
       style="font-family: Helvetica, Arial, sans-serif; max-width: 480px; width: 100%;">

  <!-- Divider bar -->
  <tr>
    <td colspan="3"
        style="background-color: #8B1A1A; height: 3px; padding: 0;"></td>
  </tr>

  <!-- Main row: name block | rule | contact block -->
  <tr>
    <!-- Name + title block -->
    <td style="padding: 12px 16px 12px 0; vertical-align: top; width: 54%;">
      <div style="font-size: 15px; font-weight: bold; color: #8B1A1A;
                  letter-spacing: 0.02em; line-height: 1.2;">
        Chandra Mast
      </div>
      <div style="font-size: 8px; font-weight: bold; color: #B8860B;
                  letter-spacing: 0.08em; text-transform: uppercase;
                  margin-top: 1px; line-height: 1.4;">
        CGA &nbsp;·&nbsp; BCA
      </div>
      <div style="font-size: 8.5px; color: #4A4A4A; margin-top: 3px; line-height: 1.5;">
        Certified General Appraiser &mdash; PA, MD, VA<br>
        Business Certified Appraiser
      </div>
      <div style="font-size: 8px; color: #9CA3AF; margin-top: 4px; line-height: 1.5;">
        Secretary, PA State Board of<br>
        Certified Real Estate Appraisers
      </div>
    </td>

    <!-- Vertical rule -->
    <td style="width: 1px; background-color: #D4A0A0; padding: 0; margin: 0;"></td>

    <!-- Contact block -->
    <td style="padding: 12px 0 12px 16px; vertical-align: top;">
      <div style="font-size: 13px; font-weight: bold; color: #1E1E1E;
                  line-height: 1.2;">
        Red Rose Appraisals
      </div>
      <div style="font-size: 7.5px; color: #9CA3AF; margin-top: 1px;
                  letter-spacing: 0.04em; text-transform: uppercase;">
        Certified Women's Owned Business
      </div>
      <div style="font-size: 8.5px; color: #4A4A4A; margin-top: 6px; line-height: 1.8;">
        <a href="tel:+17173144635"
           style="color: #4A4A4A; text-decoration: none;">
          (717) 314-4635
        </a><br>
        <a href="mailto:chandra@redroseappraisals.com"
           style="color: #B22222; text-decoration: none;">
          chandra@redroseappraisals.com
        </a><br>
        <a href="https://www.redroseappraisals.com"
           style="color: #B22222; text-decoration: none;">
          redroseappraisals.com
        </a><br>
        <span style="color: #9CA3AF;">
          148 Mason Drive, Ephrata, PA 17522
        </span>
      </div>
    </td>
  </tr>

  <!-- Bottom accent bar -->
  <tr>
    <td colspan="3"
        style="background-color: #F5EDED; padding: 5px 0 5px 0;">
      <div style="font-size: 6.5px; color: #9CA3AF; text-align: center;
                  letter-spacing: 0.06em;">
        CERTIFIED GENERAL APPRAISER &nbsp;|&nbsp; PENNSYLVANIA &nbsp;&middot;&nbsp;
        MARYLAND &nbsp;&middot;&nbsp; VIRGINIA
      </div>
    </td>
  </tr>

</table>
</body>
</html>
""".format(date=date.today().strftime("%B %Y"))


# ══════════════════════════════════════════════════════════════════════════════
# 2.  PDF Brand Standard Guide
# ══════════════════════════════════════════════════════════════════════════════

def make_styles():
    return {
        "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=16,
                             textColor=ROSE_DEEP, leading=20, spaceAfter=4),
        "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10,
                             textColor=CHARCOAL, leading=13, spaceBefore=10, spaceAfter=3),
        "body": ParagraphStyle("body", fontName="Helvetica", fontSize=8.5,
                               textColor=SLATE, leading=13, spaceAfter=5),
        "body_bold": ParagraphStyle("body_bold", fontName="Helvetica-Bold", fontSize=8.5,
                                    textColor=CHARCOAL, leading=13, spaceAfter=3),
        "code": ParagraphStyle("code", fontName="Courier", fontSize=7,
                               textColor=CHARCOAL, leading=10, spaceAfter=3,
                               leftIndent=8, backColor=colors.HexColor("#F5EDED")),
        "caption": ParagraphStyle("caption", fontName="Helvetica", fontSize=7,
                                  textColor=MID_GREY, leading=9, spaceAfter=3),
        "section_num": ParagraphStyle("sn", fontName="Helvetica-Bold", fontSize=9,
                                      textColor=GOLD, leading=11),
        "table_head": ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=8,
                                     textColor=WHITE, leading=10),
        "table_cell": ParagraphStyle("tc", fontName="Helvetica", fontSize=8,
                                     textColor=CHARCOAL, leading=11),
        "table_cell_bold": ParagraphStyle("tcb", fontName="Helvetica-Bold", fontSize=8,
                                          textColor=CHARCOAL, leading=11),
        "footer": ParagraphStyle("footer", fontName="Helvetica", fontSize=7,
                                 textColor=MID_GREY, alignment=TA_CENTER, leading=9),
    }


def branded_header(title, subtitle=None):
    """Reusable dark header bar matching the OM Watch / playbook style."""
    rows = [[Paragraph(title, ParagraphStyle("ht", fontName="Helvetica-Bold",
                                             fontSize=14, textColor=WHITE, leading=17))]]
    if subtitle:
        rows.append([Paragraph(subtitle, ParagraphStyle("hs", fontName="Helvetica",
                                                        fontSize=8, textColor=ROSE_LIGHT,
                                                        leading=10))])
    tbl = Table(rows, colWidths=[7.4 * inch])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), ROSE_DEEP),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
        ("TOPPADDING",    (0, 0), (0, 0),   10),
        ("TOPPADDING",    (0, 1), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    return tbl


def sig_preview_table(styles):
    """Renders the HTML signature as a visual preview table in the PDF."""
    name_block = Table([
        [Paragraph("Chandra Mast", ParagraphStyle("sn",
            fontName="Helvetica-Bold", fontSize=13, textColor=ROSE_DEEP, leading=16))],
        [Paragraph("CGA  ·  BCA", ParagraphStyle("scred",
            fontName="Helvetica-Bold", fontSize=7, textColor=GOLD,
            leading=9))],
        [Paragraph("Certified General Appraiser — PA, MD, VA<br/>Business Certified Appraiser",
            ParagraphStyle("stitle", fontName="Helvetica", fontSize=8,
                           textColor=SLATE, leading=11))],
        [Spacer(1, 3)],
        [Paragraph("Secretary, PA State Board of<br/>Certified Real Estate Appraisers",
            ParagraphStyle("sboard", fontName="Helvetica", fontSize=7,
                           textColor=MID_GREY, leading=10))],
    ], colWidths=[3.0 * inch])
    name_block.setStyle(TableStyle([
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("TOPPADDING",    (0,0), (-1,-1), 2),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
    ]))

    contact_block = Table([
        [Paragraph("Red Rose Appraisals", ParagraphStyle("scname",
            fontName="Helvetica-Bold", fontSize=12, textColor=CHARCOAL, leading=14))],
        [Paragraph("Certified Women's Owned Business", ParagraphStyle("scwob",
            fontName="Helvetica", fontSize=7, textColor=MID_GREY, leading=9))],
        [Spacer(1, 4)],
        [Paragraph("(717) 314-4635", ParagraphStyle("scc",
            fontName="Helvetica", fontSize=8.5, textColor=SLATE, leading=13))],
        [Paragraph("chandra@redroseappraisals.com", ParagraphStyle("scc2",
            fontName="Helvetica", fontSize=8.5, textColor=ROSE_MID, leading=13))],
        [Paragraph("redroseappraisals.com", ParagraphStyle("scc3",
            fontName="Helvetica", fontSize=8.5, textColor=ROSE_MID, leading=13))],
        [Paragraph("148 Mason Drive, Ephrata, PA 17522", ParagraphStyle("scaddr",
            fontName="Helvetica", fontSize=8, textColor=MID_GREY, leading=11))],
    ], colWidths=[4.0 * inch])
    contact_block.setStyle(TableStyle([
        ("LEFTPADDING",   (0,0), (-1,-1), 14),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0),
        ("TOPPADDING",    (0,0), (-1,-1), 2),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
        ("LINERIGHT",     (0,0), (0,-1),  1, RULE_LINE),
    ]))

    rule_cell = Table([[""]], colWidths=[1])
    rule_cell.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), RULE_LINE),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING",(0,0), (-1,-1), 0),
    ]))

    outer = Table(
        [[name_block, rule_cell, contact_block]],
        colWidths=[3.0*inch, 0.08*inch, 4.0*inch],
    )
    outer.setStyle(TableStyle([
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0),
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ("LINEABOVE",     (0,0), (-1,0),  2.5, ROSE_DEEP),
        ("LINEBELOW",     (0,-1),(-1,-1), 0.5, ROSE_LIGHT),
    ]))

    bottom_bar = Table(
        [[Paragraph(
            "CERTIFIED GENERAL APPRAISER  |  PENNSYLVANIA  ·  MARYLAND  ·  VIRGINIA",
            ParagraphStyle("cb", fontName="Helvetica", fontSize=6.5,
                           textColor=MID_GREY, alignment=TA_CENTER, leading=9)
        )]],
        colWidths=[7.08 * inch]
    )
    bottom_bar.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), ROSE_LIGHT),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]))

    wrapper = Table(
        [[outer], [bottom_bar]],
        colWidths=[7.4 * inch]
    )
    wrapper.setStyle(TableStyle([
        ("LEFTPADDING",   (0,0), (-1,-1), 14),
        ("RIGHTPADDING",  (0,0), (-1,-1), 14),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("BACKGROUND",    (0,0), (-1,-1), WARM_WHITE),
        ("BOX",           (0,0), (-1,-1), 0.5, RULE_LINE),
    ]))
    return wrapper


def installation_table(styles):
    steps = [
        ("Gmail",
         "Settings (gear) → See all settings → General tab → Signature → Create new\n"
         "Name it \"Red Rose Standard\" → click the </> (source/HTML) icon if available,\n"
         "or paste directly into the rich-text editor. Save changes."),
        ("Outlook (desktop)",
         "File → Options → Mail → Signatures → New → name it \"Red Rose Standard\"\n"
         "Switch to HTML view → paste the full HTML block → OK → set as default."),
        ("Outlook (web)",
         "Settings (gear) → View all Outlook settings → Mail → Compose and reply\n"
         "→ paste HTML into the signature box → Save."),
        ("Apple Mail",
         "Mail → Preferences → Signatures → + new signature → uncheck\n"
         "\"Always match my default message font\" → paste HTML → close."),
    ]
    rows = [[Paragraph(s[0], styles["table_cell_bold"]),
             Paragraph(s[1].replace("\n", "<br/>"), styles["table_cell"])]
            for s in steps]
    tbl = Table(rows, colWidths=[1.3*inch, 6.1*inch])
    tbl.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [WARM_WHITE, ROSE_LIGHT]),
        ("BACKGROUND",     (0,0), (0,-1),  ROSE_LIGHT),
        ("LINEBELOW",      (0,0), (-1,-2), 0.4, RULE_LINE),
        ("LEFTPADDING",    (0,0), (-1,-1), 8),
        ("RIGHTPADDING",   (0,0), (-1,-1), 8),
        ("TOPPADDING",     (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",  (0,0), (-1,-1), 6),
        ("VALIGN",         (0,0), (-1,-1), "TOP"),
    ]))
    return tbl


def rules_table(styles):
    rules = [
        ("DO",     "Use the standard signature on every external email without modification."),
        ("DO",     "Update the HTML file if phone/address changes — regenerate via brand_playbook.py."),
        ("DO",     "Keep the 3px Rose Deep top bar — it visually frames the signature."),
        ("DON'T",  "Change fonts, colors, or sizes. Helvetica/Arial only, no custom web fonts."),
        ("DON'T",  "Add social media icons, banners, or promotional images without brand approval."),
        ("DON'T",  "Use a plain-text fallback that omits the title block — credentials matter."),
        ("DON'T",  "Add legal disclaimers inline — attach a separate confidentiality footer if needed."),
    ]
    rows = [[Paragraph(r[0], ParagraphStyle("do", fontName="Helvetica-Bold", fontSize=7.5,
                           textColor=WHITE, alignment=TA_CENTER, leading=10)),
             Paragraph(r[1], styles["table_cell"])] for r in rules]
    tbl = Table(rows, colWidths=[0.65*inch, 6.75*inch])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (0,1),  ROSE_DEEP),
        ("BACKGROUND",    (0,2), (0,-1), ROSE_LIGHT),
        ("LINEBELOW",     (0,0), (-1,-2), 0.4, RULE_LINE),
        ("LEFTPADDING",   (0,0), (-1,-1), 7),
        ("RIGHTPADDING",  (0,0), (-1,-1), 7),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    return tbl


def build_pdf(output_path, styles):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.6*inch, rightMargin=0.6*inch,
        topMargin=0.5*inch,  bottomMargin=0.5*inch,
    )
    story = []

    # ── Cover header ──
    story.append(branded_header(
        "Red Rose Appraisals",
        "Email Signature Standard  ·  Brand Asset  ·  " + date.today().strftime("%B %Y")
    ))
    story.append(Spacer(1, 14))

    # ── Purpose ──
    story.append(HRFlowable(width="100%", thickness=1.5, color=ROSE_DEEP, spaceAfter=4))
    story.append(Paragraph("01", ParagraphStyle("sn", fontName="Helvetica-Bold", fontSize=9,
                                                 textColor=GOLD, leading=11)))
    story.append(Paragraph("Purpose & Scope", styles["h1"]))
    story.append(Paragraph(
        "This document defines the standard email signature for Red Rose Appraisals. "
        "The signature is the brand's most frequently seen asset — every email is a touchpoint "
        "with clients, attorneys, lenders, and peers. Consistency is not optional.",
        styles["body"]
    ))
    story.append(Paragraph(
        "The file <b>email_signature.html</b> in this repository is the single source of truth. "
        "Do not improvise alternate versions. All team members use the same layout; "
        "only the name, credentials, and direct contact number change per person.",
        styles["body"]
    ))

    # ── Signature preview ──
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=ROSE_DEEP, spaceAfter=4))
    story.append(Paragraph("02", ParagraphStyle("sn", fontName="Helvetica-Bold", fontSize=9,
                                                 textColor=GOLD, leading=11)))
    story.append(Paragraph("Standard Signature", styles["h1"]))
    story.append(Paragraph(
        "Below is the approved signature layout, rendered at exact brand spec:",
        styles["body"]
    ))
    story.append(Spacer(1, 6))
    story.append(sig_preview_table(styles))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Elements: 3px Rose Deep (#8B1A1A) top bar  ·  Name in Rose Deep 15px Bold  ·  "
        "Credentials in Lancaster Gold 8px  ·  Titles in Slate  ·  Vertical rule in Blush  ·  "
        "Links in Rose Mid (#B22222)  ·  Blush bottom bar with license states",
        styles["caption"]
    ))

    # ── Installation ──
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=ROSE_DEEP, spaceAfter=4))
    story.append(Paragraph("03", ParagraphStyle("sn", fontName="Helvetica-Bold", fontSize=9,
                                                 textColor=GOLD, leading=11)))
    story.append(Paragraph("Installation Instructions", styles["h1"]))
    story.append(Spacer(1, 4))
    story.append(installation_table(styles))

    # ── Rules ──
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=ROSE_DEEP, spaceAfter=4))
    story.append(Paragraph("04", ParagraphStyle("sn", fontName="Helvetica-Bold", fontSize=9,
                                                 textColor=GOLD, leading=11)))
    story.append(Paragraph("Usage Rules", styles["h1"]))
    story.append(Spacer(1, 4))
    story.append(rules_table(styles))

    # ── Customization for additional staff ──
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=ROSE_DEEP, spaceAfter=4))
    story.append(Paragraph("05", ParagraphStyle("sn", fontName="Helvetica-Bold", fontSize=9,
                                                 textColor=GOLD, leading=11)))
    story.append(Paragraph("Customizing for Additional Team Members", styles["h1"]))
    story.append(Paragraph(
        "To create a variant for another appraiser or staff member, change only the "
        "following five values in <b>email_signature.html</b>:",
        styles["body"]
    ))
    fields = [
        ("Full Name",      "Replace \"Chandra Mast\" — same font/color/size"),
        ("Credentials",    "Replace \"CGA  ·  BCA\" — keep Gold, 8px Bold, uppercase"),
        ("License line",   "Update license states if different from PA · MD · VA"),
        ("Phone",          "Replace (717) 314-4635 with direct line"),
        ("Email address",  "Replace chandra@ with staff member's address"),
    ]
    f_tbl = Table(
        [[Paragraph(f[0], styles["table_cell_bold"]),
          Paragraph(f[1], styles["table_cell"])] for f in fields],
        colWidths=[1.5*inch, 5.7*inch]
    )
    f_tbl.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [WARM_WHITE, ROSE_LIGHT]),
        ("BACKGROUND",     (0,0), (0,-1),  ROSE_LIGHT),
        ("LINEBELOW",      (0,0), (-1,-2), 0.4, RULE_LINE),
        ("LEFTPADDING",    (0,0), (-1,-1), 8),
        ("RIGHTPADDING",   (0,0), (-1,-1), 8),
        ("TOPPADDING",     (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",  (0,0), (-1,-1), 5),
        ("VALIGN",         (0,0), (-1,-1), "TOP"),
    ]))
    story.append(f_tbl)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Never change layout structure, colors, spacing, or the company name block. "
        "The main website, address, and company phone always remain as shown.",
        styles["body"]
    ))

    # ── Footer ──
    story.append(Spacer(1, 14))
    story.append(HRFlowable(width="100%", thickness=0.5, color=RULE_LINE))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Red Rose Appraisals Ltd.  ·  148 Mason Drive, Ephrata, PA 17522  ·  "
        "(717) 314-4635  ·  redroseappraisals.com  ·  Certified Women's Owned Business",
        styles["footer"]
    ))

    doc.build(story)
    print(f"PDF guide written to: {output_path}")


def main():
    # Write HTML
    html_path = "/home/user/Bin1/email_signature.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(HTML_SIGNATURE)
    print(f"HTML signature written to: {html_path}")

    # Write PDF guide
    styles = make_styles()
    build_pdf("/home/user/Bin1/Email_Signature_Guide.pdf", styles)


if __name__ == "__main__":
    main()
