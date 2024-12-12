from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Rendering logo:
        if self.cur_orientation == 'P':
            self.image("atlaslogo.png", 170, 8, 33)
        else:
            self.image("atlaslogo.png", 245, 8, 33)
        # Setting font: helvetica bold 15
        self.set_font("Arial", "B", 16)
        # Moving cursor to the right:
        #self.cell(40,10,Title)
        # Printing title:
        #self.cell(30, 10, "Title", border=1, align="C")
        # Performing a line break:
        self.ln(10)

    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("Arial", "I", 8)
        # Printing page number:
        self.cell(0, 10, f"Page {self.page_no()}/{len(self.pages)}", align="C")

def output_df_to_pdf(pdf,df,fontSize):

    table_cell_width = 25
    table_cell_height = 6
    num_rows = len(df)

    pdf.set_font('Arial','B',fontSize)
    cols = df.columns

    widthCol = []

    for col in cols:
        sepIniUpper = 3
        sepIni = 1
        divSep = 18

        #numCharsCol = []
        #numCharsCol.extend([len(col)])
        #for i in range(num_rows):
            #numCharsCol.extend([len(str(df.loc[i,col]))])
        #if col.isupper() == True:
            #widthCol.extend([sepIniUpper+(max(numCharsCol)/divSep)*table_cell_width])
        #else:
            #widthCol.extend([sepIni+(max(numCharsCol)/divSep)*table_cell_width])
        
        widthRows = []
        widthRows.extend([pdf.get_string_width(col)])
        for i in range(num_rows):
            widthRows.extend([pdf.get_string_width(str(df.loc[i,col]))])
        widthCol.extend([max(widthRows)+2])

    i = 0
    for col in cols:
        #pdf.cell(widthCol[i]*fontSize/6,table_cell_height,col,align='C',border=1)
        pdf.cell(widthCol[i],table_cell_height,col,align='C',border=1)
        i += 1
    
    pdf.ln(table_cell_height)
    pdf.set_font('Arial','',fontSize)

    for row in range(num_rows):
        i = 0

        if pdf.get_y() + table_cell_height > pdf.page_break_trigger:
            pdf.set_font('Arial','B',fontSize)
            j = 0
            for col in cols:
                #pdf.cell(widthCol[j]*fontSize/6,table_cell_height,col,align='C',border=1)
                pdf.cell(widthCol[j],table_cell_height,col,align='C',border=1)
                j += 1
            pdf.set_font('Arial','',fontSize)
            pdf.ln(table_cell_height)

        for col in cols:
            value = df.loc[row,col]
            if col == 'DaysNoAnswer':
                value = value.days
            #pdf.cell(widthCol[i]*fontSize/6,table_cell_height,str(value),align='C',border=1)
            pdf.cell(widthCol[i],table_cell_height,str(value),align='C',border=1)
            i += 1
        pdf.ln(table_cell_height)

def exportToPDF(Title,titles,tables,fileTitle,scurvePath):

    pdf = PDF()
    pdf.add_page()
    #pdf.image("atlaslogo.png", 170, 8, 33)
    pdf.set_font('Arial','B',16)

    pdf.ln(10)

    pdf.cell(40,10,Title)

    pdf.ln(20)

    i = 0
    for t in tables:
        fontSize = 6
        pdf.set_font('Arial','',16)
        if i!=0:
            pdf.ln(14)
        if titles[i].find('SUBCATE') != -1 or titles[i].find('OE') != -1:
            pdf.add_page(orientation='landscape')
            fontSize = 5
        pdf.cell(40,10,'Progress {}'.format(titles[i]),)
        pdf.ln(10)
        output_df_to_pdf(pdf,t,fontSize)
        i += 1

    for image in scurvePath:
        pdf.add_page(orientation='landscape')
        pdf.image(image,10,10,220)

    pdf.output(fileTitle,'F')
