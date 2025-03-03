from fpdf import FPDF
from datetime import date
import os
import general as gen
import platform

class PDF(FPDF):
    def header(self):
        # Rendering logo:
        if self.cur_orientation == 'P':
            self.image("atlaslogo.png", 170, 8, 33)
        else:
            self.image("atlaslogo.png", 245, 8, 33)
        # Setting font: helvetica bold 15
        self.set_font("Arial", "B", 16)
        # Performing a line break:
        self.ln(10)

    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("Arial", "I", 8)
        # Printing page number:
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def output_df_to_pdf(pdf,df,fontSize,tabletitle):

    table_cell_height = 6
    num_rows = len(df)

    pdf.set_font('Arial','B',fontSize)
    cols = df.columns

    widthCol = []

    # col width depending on the max width of the elements of the col
    for col in cols:
        widthRows = []
        widthRows.extend([pdf.get_string_width(col)])
        for i in range(num_rows):
            widthRows.extend([pdf.get_string_width(str(df.loc[i,col]))])
        widthCol.extend([max(widthRows)+2])

    for i,col in enumerate(cols):
        pdf.cell(widthCol[i],table_cell_height,col,align='C',border=1)
    
    pdf.ln(table_cell_height)
    pdf.set_font('Arial','',fontSize)

    for row in range(num_rows):

        if pdf.get_y() + table_cell_height > pdf.page_break_trigger:
            pdf.set_font('Arial','B',fontSize)
            for j,col in enumerate(cols):
                pdf.cell(widthCol[j],table_cell_height,col,align='C',border=1)

            pdf.set_font('Arial','',fontSize)
            pdf.ln(table_cell_height)

        if tabletitle == 'DOCS NOT ISSUED':
            strDate = df.loc[row,'EXP ISS']
            if strDate <= date.today():
                pdf.set_text_color(255,0,0)

        for i,col in enumerate(cols):
            value = df.loc[row,col]
            pdf.cell(widthCol[i],table_cell_height,str(value),align='C',border=1)
        
        pdf.set_text_color(0,0,0)

        pdf.ln(table_cell_height)
    

def pdfExport_repDet(docsNotIssued,docsNotApproved,docsInRev,project,discipline,dayOfAnalysis):

    pdf = PDF()
    pdf.add_page(orientation='landscape')
    pdf.set_font('Arial','B',16)

    pdf.ln(10)
    pdf.cell(40,10,'Detailed Report: {} / {} / {}'.format(project,discipline,dayOfAnalysis))
    pdf.ln(20)

    tables = [docsNotIssued,docsNotApproved,docsInRev]
    titles = ['DOCS NOT ISSUED','DOCS NOT COMPLIANT','DOCS IN REV']

    for i,t in enumerate(tables):
        if i != 0:
            pdf.add_page(orientation='landscape')
        pdf.set_font('Arial','',10)
        fontSize = 5
        pdf.cell(40,10,titles[i])
        pdf.ln(10)
        output_df_to_pdf(pdf,t,fontSize,titles[i])

    repName = 'detReport_{}_{}_{}.pdf'.format(dayOfAnalysis,project,discipline)
    path_save = os.path.join(gen.whichPath(gen.where(platform.node()))[2],'detailed_reports',repName)
    pdf.output(path_save,'F')