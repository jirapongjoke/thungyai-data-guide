#!/usr/bin/env python3
"""สร้างไฟล์คู่มือ: src.html -> guide.html (สำหรับ Artifact) และ index.html (ไฟล์เดี่ยว เปิด/อัปโหลดที่ไหนก็ได้)"""
import base64, re, pathlib
d = pathlib.Path(__file__).parent
src = (d / "src.html").read_text(encoding="utf-8")
def img(m):
    b = (d / "shots" / (m.group(1) + ".jpg")).read_bytes()
    return "data:image/jpeg;base64," + base64.b64encode(b).decode()
out = re.sub(r"\{\{img:(\w+)\}\}", img, src)
(d / "guide.html").write_text(out, encoding="utf-8")
head, body = out.split("<!--BODY-->", 1)
full = ('<!DOCTYPE html>\n<html lang="th">\n<head>\n<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n'
        + head + "</head>\n<body>\n" + body + "\n</body>\n</html>\n")
(d / "index.html").write_text(full, encoding="utf-8")
print("guide.html", len(out) // 1024, "KB | index.html", len(full) // 1024, "KB")
