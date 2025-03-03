from fpdf import FPDF
import tkinter as tk
import tkinter.font as tkfont


class PDF(FPDF):
    def header(self):
        # Rendering logo:
        self.image("atlaslogo.png", 170, 8, 33)
        # Setting font: helvetica bold 15
        self.set_font("helvetica", "B", 15)
        # Moving cursor to the right:
        self.cell(80)
        # Printing title:
        self.cell(30, 10, "Title", border=1, align="C")
        # Performing a line break:
        self.ln(20)

    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", "I", 8)
        # Printing page number:
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


# Instantiation of inherited class
pdf = PDF()
pdf.add_page()
pdf.set_font("Times", size=12)
root = tk.Tk()
font = tkfont.Font(family='Times',size=12,weight='normal')
for i in range(1, 41):
    #pdf.cell(0, 10, f"Printing line number {i}", new_x="LMARGIN", new_y="NEXT")
    w = font.measure(f"Printing line number {i}")
    w2 = pdf.get_string_width(f"Printing line number {i}")
    pdf.cell(w2+2, 10, f"Printing line number {i} {w} {w2}",border=1)
    pdf.ln(10)
pdf.output("new-tuto2.pdf")