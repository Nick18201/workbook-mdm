import fitz # PyMuPDF
import os

pdf_path = "Programme_Bilan_de_Competences.pdf"
doc = fitz.open(pdf_path)

out_dir = r"C:\Users\nblum\.gemini\antigravity-ide\brain\d72b4d79-2f11-47df-9abf-9d25be1c5dbd"

print(f"Total pages: {len(doc)}")
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    out_png = os.path.join(out_dir, f"prog_page_{i}.png")
    pix.save(out_png)
    print(f"Saved page {i} to {out_png}")
