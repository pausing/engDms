
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

def projectData_to_pdf(pdf,df,fontSize,tabletitle):

    table_cell_height = 6
    num_rows = len(df)

    pdf.set_font('Arial','B',fontSize)
    cols = df.columns
    df.fillna('--',inplace=True)

    numberOfDisciplines = int(len(df)/7)
    colWithIntNumbers = ['CIVIL','ELECTRICAL','ELECTROMECHANICAL','EQUIPMENT','SUM']
    rowWithIntNumbersBlockType = [0,1,2,3,4]
    rowWithIntNumbers = []
    for i in range(numberOfDisciplines):
        for r in rowWithIntNumbersBlockType:
            rowWithIntNumbers.append(i*7+r)
    rowWithFloatNumbersBlockType = [5,6]
    rowWithFloatNumbers = []
    for i in range(numberOfDisciplines):
        for r in rowWithFloatNumbersBlockType:
            rowWithFloatNumbers.append(i*7+r)
    colWithFloatNumbers = ['SUM [%]']

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

        for i,col in enumerate(cols):

            value = df.loc[row,col]

            if (col in colWithIntNumbers) and (row in rowWithIntNumbers):
                value = int(value)
            elif col in colWithFloatNumbers:
                try:
                    value = float(value)
                    value = '{:.2f}'.format(value)
                except:
                    value = '--'
            elif (col == 'SUM') and (row in rowWithFloatNumbers):
                value = '--'
            elif (col in ['CIVIL','ELECTRICAL','ELECTROMECHANICAL','EQUIPMENT']) and (row in rowWithFloatNumbers):
                try:
                    value = '{:.2f}'.format(value)
                except:
                    value = '--'
            pdf.cell(widthCol[i],table_cell_height,str(value),align='C',border=1)
        
        pdf.set_text_color(0,0,0)

        pdf.ln(table_cell_height)
    
def disciplineData_to_table(pdf,df,fontSize,tabletitle):

#Data type:
#+-------------------+---------+--------------+---------------------+-------------+-------+-----------+
#| ITEM              |   CIVIL |   ELECTRICAL |   ELECTROMECHANICAL |   EQUIPMENT |   SUM | SUM [%]   |
#+===================+=========+==============+=====================+=============+=======+===========+
#| TOTAL             |      68 |           59 |                  51 |         122 |   300 | --        |
#+-------------------+---------+--------------+---------------------+-------------+-------+-----------+
#| ISSUED EXPECTED   |      68 |           59 |                  51 |         122 |   300 | 100.00    |
#+-------------------+---------+--------------+---------------------+-------------+-------+-----------+
#| ISSUED REAL       |      66 |           58 |                  51 |         112 |   287 | 95.67     |
#+-------------------+---------+--------------+---------------------+-------------+-------+-----------+
#| APPROVED EXPECTED |      66 |           59 |                  51 |         122 |   298 | 99.33     |
#+-------------------+---------+--------------+---------------------+-------------+-------+-----------+
#| APPROVED REAL     |      62 |           56 |                  45 |          86 |   249 | 83.00     |
#+-------------------+---------+--------------+---------------------+-------------+-------+-----------+
#| TOTAL EXPECTED [%]|   66.33 |        59.33 |               51.33 |       122.33| 298.33| 99.33     |
#+-------------------+---------+--------------+---------------------+-------------+-------+-----------+
#| TOTAL REAL [%]    |   62.33 |        56.21 |               45.33 |       86.33 | 249.32| 83.00     |
#+-------------------+---------+--------------+---------------------+-------------+-------+-----------+

    colWithIntNumbers = ['CIVIL','ELECTRICAL','ELECTROMECHANICAL','EQUIPMENT','SUM']
    rowWithIntNumbers = [0,1,2,3,4]
    colWithFloatNumbers = ['SUM [%]']

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

        for i,col in enumerate(cols):
            value = df.loc[row,col]
            if (col in colWithIntNumbers) and (row in rowWithIntNumbers):
                value = int(value)
            elif col in colWithFloatNumbers:
                value = '{:.2f}'.format(value)
            elif (col == 'SUM') and (row in [5,6]):
                value = '--'
            elif (col in ['CIVIL','ELECTRICAL','ELECTROMECHANICAL','EQUIPMENT']) and (row in [5,6]):
                value = '{:.2f}'.format(value)

                
            pdf.cell(widthCol[i],table_cell_height,str(value),align='C',border=1)
        
        pdf.set_text_color(0,0,0)

        pdf.ln(table_cell_height)
    
def pdfExport_generalReport(projects,data):

    projectsAcroNames = []
    projectsFullName = []

    for i, p in enumerate(projects):
        projectsAcroNames.append(p[0])
        projectsFullName.append(p[1])

    dataOfProjects = []
    disciplinesData  = []
    projectScurve = []
    dayOfAnalysis = []

    for i, d in enumerate(data):
        dataOfProjects.append(d[0])
        disciplinesData.append(d[1])
        projectScurve.append(d[2])
        dayOfAnalysis.append(d[3])

    pdf = PDF()
    pdf.add_page(orientation='portrait')
    pdf.set_font('Arial','B',16)

    pdf.ln(10)
    pdf.cell(40,10,'General Report, {}'.format(dayOfAnalysis[0]))
    pdf.ln(20)

    for i,p in enumerate(projectsFullName):
        #if i != 0:
            #pdf.add_page(orientation='landscape')
        pdf.set_font('Arial','',10)
        fontSize = 5
        pdf.cell(40,10,p)
        pdf.ln(10)
        pdf.cell(40,10,'Expected Progress: {} %, Real Progress: {} %'.format(dataOfProjects[i].loc[5,'SUM [%]'],dataOfProjects[i].loc[6,'SUM [%]']))
        pdf.ln(10)
        disciplineData_to_table(pdf,dataOfProjects[i],fontSize,projectsFullName)
        pdf.ln(10)

    for i,p in enumerate(projectsFullName):

        pdf.add_page(orientation='landscape')
        pdf.set_font('Arial','',10)
        fontSize = 5
        pdf.cell(40,10,p)
        pdf.ln(10)
        projectData_to_pdf(pdf,disciplinesData[i],fontSize,projectsFullName)
        pdf.add_page(orientation='landscape')
        pdf.image(projectScurve[i],10,10,220)

    repName = 'generalReport {}.pdf'.format(dayOfAnalysis[0])
    path_save = os.path.join(gen.whichPath(gen.where(platform.node()))[2],'general_reports',repName)
    pdf.output(path_save,'F')