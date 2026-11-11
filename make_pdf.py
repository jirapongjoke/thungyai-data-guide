#!/usr/bin/env python3
"""สร้างคู่มือฉบับพิมพ์ A4: index.html -> print.html -> PDF (ใช้ Google Chrome แบบ headless)
ใช้: python3 build.py && python3 make_pdf.py"""
import pathlib, shutil, subprocess

d = pathlib.Path(__file__).parent
OUT = d / "คู่มือระบบสารสนเทศ-รร.บ้านทุ่งใหญ่.pdf"
GUIDE_URL = "https://jirapongjoke.github.io/thungyai-data-guide/"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

PRINT_CSS = """
<style>
@page { size: A4; margin: 15mm 14mm 17mm; @bottom-center { content: "คู่มือระบบสารสนเทศ โรงเรียนบ้านทุ่งใหญ่  ·  หน้า " counter(page) " / " counter(pages); font-family: "Sarabun", sans-serif; font-size: 9pt; color: #56697a; } }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-size: 14.5px; line-height: 1.6; background: #fff; }
body::before, .top, .cta, .finder, .count, .toast, summary::after { display: none !important; }
.wrap { max-width: none; padding-left: 0 !important; padding-right: 0 !important; }
.shot { box-shadow: none; }

/* หน้าปก/ส่วนหัว */
.hero { background: #fff; color: var(--ink); border-bottom: 3px solid var(--navy); }
.hero .wrap { grid-template-columns: minmax(0,1fr) auto; padding-block: 0 18px; gap: 24px; }
.hero h1 { font-size: 27px; color: var(--navy); }
.hero .lead { color: var(--muted); font-size: 15.5px; }
.eyebrow { color: var(--amber); }
.urlbox { color: var(--muted); font-size: 13px; margin-top: 10px; }
.urlbox b { color: var(--ink); }
.qr { border: 1px solid var(--line); width: 150px; padding: 10px 10px 6px; justify-self: end; }
.qr svg { width: 128px; height: 128px; }
.qr span { font-size: 11px; }

/* ส่วนเนื้อหา */
section { padding-block: 18px; }
.sec-head { margin-bottom: 12px; max-width: none; }
.sec-head h2 { font-size: 20px; color: var(--navy); break-after: avoid; }
.facts { grid-template-columns: repeat(4, minmax(0,1fr)); gap: 14px; }
.facts b { font-size: 14.5px; } .facts span { font-size: 12.5px; }
.steps { gap: 16px; }
.step { grid-template-columns: minmax(0,5fr) minmax(0,6fr) !important; gap: 20px; break-inside: avoid; }
.step h3 { font-size: 16.5px; } .step h3::before { width: 28px; height: 28px; font-size: 14px; }
figure, .sys-row, details, .roles > div, .note, .legend li, .duo { break-inside: avoid; }
#screen figure .shot { max-width: 82%; margin-inline: auto; }
.legend { grid-template-columns: repeat(4, minmax(0,1fr)); gap: 10px 16px; margin-top: 12px; }
.legend li { font-size: 12.5px; grid-template-columns: 24px minmax(0,1fr); gap: 6px; }
.legend i { width: 22px; height: 22px; font-size: 12px; }
.pin { width: 24px; height: 24px; margin: -12px 0 0 -12px; font-size: 12px; }
#systems { break-before: page; border-top: 0; padding-top: 0; }
#awards { break-inside: avoid; }
#systems .wrap > p:last-child { font-size: 12px !important; margin-top: 6px !important; break-before: avoid; }
.sys-row { padding: 3px 0; grid-template-columns: 34px minmax(0,1fr) auto !important; }
.sys-row h3 { font-size: 15px; } .sys-row p, .sys-row ul { font-size: 13px; line-height: 1.5; margin-top: 0; }
.num { font-size: 18px; }
.badge { grid-column: auto !important; font-size: 11.5px; }
.roles { grid-template-columns: repeat(4, minmax(0,1fr)) !important; gap: 14px; }
.roles h3 { font-size: 14.5px; } .roles ul { font-size: 12.5px; padding-left: 15px; line-height: 1.5; }
.duo { grid-template-columns: minmax(0,1fr) minmax(0,1fr) !important; gap: 22px; }
.duo.phone { grid-template-columns: 170px minmax(0,1fr) !important; }
.gallery { grid-template-columns: repeat(2, minmax(0,1fr)); gap: 18px; }
figcaption { font-size: 12.5px; }
.note { font-size: 13px; padding: 10px 14px; margin-top: 10px; }
#faq { break-before: page; border-top: 0; padding-top: 0; }
summary { font-size: 14.5px; padding: 9px 0 2px; cursor: default; }
details p { padding-bottom: 9px; font-size: 13.5px; max-width: none; }
.foot { background: #fff; color: var(--ink); border-top: 3px solid var(--navy) !important; margin-top: 8px; }
.foot h2 { font-size: 17px; color: var(--navy); }
.foot dl { font-size: 13.5px; margin-top: 8px; }
.foot dt { color: var(--muted); } .foot a { color: var(--ink); text-decoration: none; }
.foot .btn { display: none; }
</style>
"""

html = (d / "index.html").read_text(encoding="utf-8")
html = html.replace('<html lang="th">', '<html lang="th" data-theme="light">')
html = html.replace(' loading="lazy"', "").replace("<details>", "<details open>")
html = html.replace("</head>", PRINT_CSS + "</head>")
html = html.replace(
    '</b></p>\n    </div>\n    <div class="qr"',
    '</b><br>คู่มือออนไลน์: <b>' + GUIDE_URL + '</b></p>\n    </div>\n    <div class="qr"')
html = html.replace(">เพจโรงเรียนบ้านทุ่งใหญ่</a>", ">facebook.com/Banthungyaischool3</a>")
html = html.replace("<h2>พร้อมแล้ว ลองเปิดใช้ได้เลย</h2>", "<h2>ติดต่อโรงเรียนบ้านทุ่งใหญ่</h2>")
html = html.replace("พิมพ์สิ่งที่กำลังหา แล้วดูว่าต้องเข้าระบบหมายเลขใด", "รายการระบบทั้งหมด เอกสารที่มี และสถานะปัจจุบัน")
(d / "print.html").write_text(html, encoding="utf-8")

subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                "--virtual-time-budget=10000", f"--print-to-pdf={OUT}", (d / "print.html").as_uri()],
               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
shutil.copyfile(OUT, d / "thungyai-data-guide.pdf")  # สำเนาชื่ออังกฤษสำหรับลิงก์ดาวน์โหลดบนเว็บ
print("PDF:", OUT.name, OUT.stat().st_size // 1024, "KB")
