import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os
import shutil
import ldBackEnd as bck
from tkcalendar import DateEntry
from datetime import datetime,timedelta
from datetime import date
import string
import time
import matplotlib.pyplot as plt

class ScrollableFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)

        #self.canvas = tk.Canvas(self, height=400, width=1850, borderwidth=10, highlightthickness=10,bg='blue')
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

class Application (tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("1900x400")
        self.master.title('ATLAS VISTA ALEGRE ENG REVIEW')
        #self.grid()
        self.create_widgetsIni()
        # para efectos de pruebas se hardcodea los archivos de fileToAnalyze y DataBase
        # indice documentos actual
        #C:\Users\PabloMaqueda\OneDrive - Atlas Renewable Energy\TO\Brazil\04_VA\02_EXE\03_ENG\01_PV\00_INDICE DOCUMENTOS\01_PlanCSV
        # base de datos
        #C:\Users\PabloMaqueda\OneDrive - Atlas Renewable Energy\TO\Brazil\04_VA\02_EXE\03_ENG\01_PV\00_INDICE DOCUMENTOS\00_Python
        parentFolder = os.getcwd() + os.sep + os.pardir
        dirPlanCSV = os.path.join(parentFolder,'00_PlanCSV')
        #dirPlanCSV = os.path.join('C:\\','Users','PabloMaqueda','OneDrive - Atlas Renewable Energy','TO','Brazil','04_VA', \
                                          #'02_EXE','03_ENG','01_PV','00_INDICE DOCUMENTOS','00_PlanCSV')
        dirAnalisisIndice = os.path.join(os.getcwd(),'01_Analisis')
        #dirAnalisisIndice = os.path.join('C:\\','Users','PabloMaqueda','OneDrive - Atlas Renewable Energy','TO','Brazil','04_VA', \
                                          #'02_EXE','03_ENG','01_PV','00_INDICE DOCUMENTOS','00_Python','01_Analisis')
        
        listaPlanCSVs = os.listdir(dirPlanCSV)
        listaPlanCSVs.sort()
        listaAnalisisIndices = os.listdir(dirAnalisisIndice)
        self.fileToAnalyze = os.path.join(dirPlanCSV,listaPlanCSVs[len(listaPlanCSVs)-1])
        self.DataBase = os.path.join(dirAnalisisIndice,listaAnalisisIndices[len(listaAnalisisIndices)-1])
        #self.lblDatabase.config(text='Database: ' + self.DataBase.split(os.path.sep)[len(self.DataBase.split(os.path.sep))-1])
        self.lblDatabase.config(text='Database: ' + self.DataBase.split(os.path.sep)[len(self.DataBase.split(os.path.sep))-1])
        #self.lblFileChosen.config(text='File: ' + self.fileToAnalyze.split('\\')[len(self.fileToAnalyze.split('\\'))-1])
        self.lblFileChosen.config(text='File: ' + self.fileToAnalyze.split(os.path.sep)[len(self.fileToAnalyze.split(os.path.sep))-1])
        #tarjDate = self.cal1.get_date()
        #bck.compareFileToAnalyzeVsDB(self.fileToAnalyze,self.DataBase,tarjDate)
    
    def create_widgetsIni(self):
        self.frame = ScrollableFrame(self.master)

        self.btnChooseFile = tk.Button(self.frame.scrollable_frame,text='Choose File',command=self.chooseFile)
        self.btnRefreshGen = tk.Button(self.frame.scrollable_frame,text='Refresh General',command=self.refreshGen)
        self.btnRefreshDet = tk.Button(self.frame.scrollable_frame,text='Refresh Detailed',command=self.statusEng)
        self.btnFormatFile = tk.Button(self.frame.scrollable_frame,text='Format File',command=self.formatFile)
        self.btnChooseDatabase = tk.Button(self.frame.scrollable_frame,text='Choose DataBase',command=self.chooseDatabase)
        self.btnGraphGen = tk.Button(self.frame.scrollable_frame,text='Plan vs Real',command=self.graphGen)

        self.cal1 = DateEntry(self.frame.scrollable_frame,width=12,background='darkblue',foreground='white',borderwidth=2)
        self.cal2 = DateEntry(self.frame.scrollable_frame,width=12,background='darkblue',foreground='white',borderwidth=2)

        self.lblFileChosen = tk.Label(self.frame.scrollable_frame,text="File: not defined")
        self.lblDatabase = tk.Label(self.frame.scrollable_frame,text="Database: not defined")
        self.lblDateRefresh = tk.Label(self.frame.scrollable_frame,text='Not refreshed yet')
        self.lblDateOfAnalysis = tk.Label(self.frame.scrollable_frame,text='Date of Analysis: ')

        self.btnChooseFile.grid(row=0,column=0)
        self.btnChooseDatabase.grid(row=0,column=5)
        self.btnRefreshGen.grid(row=1,column=0)
        self.btnRefreshDet.grid(row=2,column=0)
        self.btnFormatFile.grid(row=0,column=4)
        self.btnGraphGen.grid(row=1,column=5)

        self.lblFileChosen.grid(row=0,column=1)
        self.lblDatabase.grid(row=0,column=6)
        self.lblDateRefresh.grid(row=1,column=1)
        self.lblDateOfAnalysis.grid(row=1,column=2)
        self.cal1.grid(row=1,column=4)
        self.cal2.grid(row=2,column=4)
        self.frame.pack(fill='both',expand=True)

    def statusEng(self):
        tarjStartDate = self.cal1.get_date()
        tarjEndDate = self.cal2.get_date()
        bck.compareFileToAnalyzeVsDB(self.fileToAnalyze,self.DataBase,tarjEndDate)
        #bck.finalReport(self.fileToAnalyze,self.DataBase,tarjStartDate,tarjEndDate)
    
    def formatFile(self):
        bck.formatFile(self.fileToAnalyze)
    
    def chooseFile(self):
        self.fileToAnalyze = filedialog.askopenfilename()
        print(self.fileToAnalyze)
        self.lblFileChosen.config(text='File: ' + self.fileToAnalyze.split('/')[len(self.fileToAnalyze.split('/'))-1])

    def chooseDatabase(self):
        self.DataBase = filedialog.askopenfilename()
        self.lblDatabase.config(text='Database: ' + self.DataBase.split('/')[len(self.DataBase.split('/'))-1])
    
    def createGeneral(self,folders,totalFolderDocCount,numDocPlanned,numDocReal):
        self.lblGenReview = tk.Label(self.frame.scrollable_frame,text='GENERAL REVIEW')
        self.lblTitleFolder = tk.Label(self.frame.scrollable_frame,text='CATEGORY')
        self.lblTitleFolderCount = tk.Label(self.frame.scrollable_frame,text='TOTAL')
        self.lblTitleFolderPlanned = tk.Label(self.frame.scrollable_frame,text='PLANNED')
        self.lblTitleFolderReal = tk.Label(self.frame.scrollable_frame,text='REAL')
        self.lblTitlePercenDiff = tk.Label(self.frame.scrollable_frame,text='DIFF [%]')
        self.lblTotalDocCount = tk.Label(self.frame.scrollable_frame,text=sum(totalFolderDocCount))
        self.lblTotalDocPlanned = tk.Label(self.frame.scrollable_frame,text=sum(numDocPlanned))
        self.lblTotalDocReal = tk.Label(self.frame.scrollable_frame,text=sum(numDocReal))
        self.lblTotalPercenDiff = tk.Label(self.frame.scrollable_frame,text= '{:.2f} %'.format(100*(sum(numDocReal)-sum(numDocPlanned))/sum(numDocPlanned)))
        self.lblTotalPlannedPercen = tk.Label(self.frame.scrollable_frame,text= '{:.2f} %'.format(100*sum(numDocPlanned)/sum(totalFolderDocCount)))
        self.lblTotalRealPercen = tk.Label(self.frame.scrollable_frame,text= '{:.2f} %'.format(100*sum(numDocReal)/sum(totalFolderDocCount)))

        self.lblFolders = []
        self.lblTotalFoldersCount = []
        self.lblTotalFoldersPlanned = []
        self.lblTotalFoldersReal = []
        self.lblPercenDiff = []
        for i in range(len(folders)):
            self.lblFolders.extend([tk.Label(self.frame.scrollable_frame,text=folders[i])])
            self.lblTotalFoldersCount.extend([tk.Label(self.frame.scrollable_frame,text='{}'.format(totalFolderDocCount[i]))])
            self.lblTotalFoldersPlanned.extend([tk.Label(self.frame.scrollable_frame,text='{}'.format(numDocPlanned[i]))])
            self.lblTotalFoldersReal.extend([tk.Label(self.frame.scrollable_frame,text='{}'.format(numDocReal[i]))])
            self.lblPercenDiff.extend([tk.Label(self.frame.scrollable_frame,text='{:.2f} %'.format(100*(numDocReal[i]-numDocPlanned[i])/numDocPlanned[i]))])
        
        self.lblGenReview.grid(row=5,column=0)
        self.lblTitleFolder.grid(row=6,column=1)
        self.lblTitleFolderCount.grid(row=6,column=2)
        self.lblTitleFolderPlanned.grid(row=6,column=3)
        self.lblTitleFolderReal.grid(row=6,column=4)
        self.lblTitlePercenDiff.grid(row=6,column=5)
        self.lblTotalDocCount.grid(row=6+len(totalFolderDocCount)+1,column=2)
        self.lblTotalDocPlanned.grid(row=6+len(totalFolderDocCount)+1,column=3)
        self.lblTotalDocReal.grid(row=6+len(totalFolderDocCount)+1,column=4)
        self.lblTotalPercenDiff.grid(row=6+len(totalFolderDocCount)+1,column=5)
        self.lblTotalPlannedPercen.grid(row=6+len(totalFolderDocCount)+1+1,column=3)
        self.lblTotalRealPercen.grid(row=6+len(totalFolderDocCount)+1+1,column=4)

        for i in range(len(folders)):
            self.lblFolders[i].grid(row=6+i+1,column=1)
            self.lblTotalFoldersCount[i].grid(row=6+i+1,column=2)
            self.lblTotalFoldersPlanned[i].grid(row=6+i+1,column=3)
            self.lblTotalFoldersReal[i].grid(row=6+i+1,column=4)
            self.lblPercenDiff[i].grid(row=6+i+1,column=5)

    def CreateSub(self,iniRow,iniCol,totals,subFolders,planned,real):
        
        self.lblTitleTotal = tk.Label(self.frame.scrollable_frame,text='TOTAL')
        self.lblTitlePlanned = tk.Label(self.frame.scrollable_frame,text='PLANNED')
        self.lblTitleReal = tk.Label(self.frame.scrollable_frame,text='REAL')
        self.lblTitlePercenDiff = tk.Label(self.frame.scrollable_frame,text='DIFF [%]')
        self.lblSubFolder = [tk.Label(self.frame.scrollable_frame,text=x) for x in subFolders]
        self.lblTotals = [tk.Label(self.frame.scrollable_frame,text=x) for x in totals]
        self.lblPlanned = [tk.Label(self.frame.scrollable_frame,text=x) for x in planned]
        self.lblReal = [tk.Label(self.frame.scrollable_frame,text=x) for x in real]
        self.lblPercenDiff = []
        for i in range(len(subFolders)):
            if planned[i] != 0:
                self.lblPercenDiff.extend([tk.Label(self.frame.scrollable_frame,text='{:.2f} %'.format(100*(real[i]-planned[i])/planned[i]))])
            else:
                self.lblPercenDiff.extend([tk.Label(self.frame.scrollable_frame,text='NA')])
        
        self.lblTotalSum = tk.Label(self.frame.scrollable_frame,text = sum(totals))
        self.lblTotalReal = tk.Label(self.frame.scrollable_frame,text = sum(real))
        self.lblTotalPlanned = tk.Label(self.frame.scrollable_frame,text = sum(planned))
        self.lblPlannedPercen = tk.Label(self.frame.scrollable_frame,text='{:.2f} %'.format(100*sum(planned)/sum(totals)))
        self.lblRealPercen = tk.Label(self.frame.scrollable_frame,text='{:.2f} %'.format(100*sum(real)/sum(totals)))
        
        self.lblTitleTotal.grid(row=iniRow,column=iniCol+1)
        self.lblTitlePlanned.grid(row=iniRow,column=iniCol+1+1)
        self.lblTitleReal.grid(row=iniRow,column=iniCol+1+1+1)
        self.lblTitlePercenDiff.grid(row=iniRow,column=iniCol+1+1+1+1)

        for i in range(len(self.lblSubFolder)):
            self.lblSubFolder[i].grid(row=iniRow+1+i,column=iniCol)
            self.lblTotals[i].grid(row=iniRow+1+i,column=iniCol+1)
            self.lblPlanned[i].grid(row=iniRow+1+i,column=iniCol+1+1)
            self.lblReal[i].grid(row=iniRow+1+i,column=iniCol+1+1+1)
            self.lblPercenDiff[i].grid(row=iniRow+1+i,column=iniCol+1+1+1+1)
        
        self.lblTotalSum.grid(row=iniRow+len(subFolders)+1 ,column=iniCol+1)
        self.lblTotalPlanned.grid(row=iniRow+len(subFolders)+1 ,column=iniCol+1+1)
        self.lblTotalReal.grid(row=iniRow+len(subFolders)+1 ,column=iniCol+1+1+1)

        self.lblPlannedPercen.grid(row=iniRow+len(subFolders)+1+1 ,column=iniCol+1+1)
        self.lblRealPercen.grid(row=iniRow+len(subFolders)+1+1 ,column=iniCol+1+1+1)

    def createReview(self,folders,foldersFormatted,areas,areasFormatted,tarjDate,bd,database):
        
        print('calculation det review, start: ')
        start = time.time()
        totals, planned, real = bck.getDetReviewOp(bd,database,folders,areas,tarjDate)
        end = time.time()
        print('finish det review, time: ',end-start)

        iniRowDetReview = 6+len(folders)+1+1+2
        iniColFolders = 0
        self.lblDetReview = tk.Label(self.frame.scrollable_frame,text='DETAILED REVIEW')
        
        self.lblTitleFolders = [tk.Label(self.frame.scrollable_frame,text=x) for x in foldersFormatted]
        self.lblTitleAreas = [tk.Label(self.frame.scrollable_frame,text=x) for x in areas]


        self.lblDetReview.grid(row=iniRowDetReview,column=0)
        for i in range(len(areas)):
            self.lblTitleAreas[i].grid(row=iniRowDetReview + 2 + i*15,column=iniColFolders + 1 )
        print('creating subs, start: ')
        start = time.time()
        for i in range(len(self.lblTitleFolders)):
            self.lblTitleFolders[i].grid(row=iniRowDetReview + 1,column=iniColFolders + i*10)
            for j in range(len(areas)):
                self.CreateSub(iniRowDetReview + 3 + j*15,iniColFolders + 2 + i*10,totals[i][j],bck.getSubFolders(bd,folders[i],areas[j]),planned[i][j],real[i][j])
        end = time.time()
        print('finish creating sub, time: ',end-start)

    def graphGen(self):
        folders = ['CIVIL','ELETRICA','ELETROMECANICA']
        bd = pd.read_csv(self.fileToAnalyze,sep=';')
        
        tarjDateStart = self.cal1.get_date()
        tarjDateEnd = self.cal2.get_date()
        print('from {} to {}'.format(tarjDateStart,tarjDateEnd))

        dates = [tarjDateStart]
        difDays = tarjDateEnd - tarjDateStart

        for i in range(difDays.days+1):
            if i != 0:
                dates.extend([dates[i-1] + timedelta(1)])
        
        planned = []
        real = []

        for d in dates:
            planned.extend([sum(bck.getPlanned(bd,folders,d))])
            real.extend([sum(bck.getReal(bd,folders,d))])
        
        fig, ax = plt.subplots(1,1,figsize=[3*6.4,3*4.8])
        ax.grid(True)
        ax.set_title('Planned vs Real',size='small')
        ax.tick_params(labelsize='xx-small')
        ax.plot(dates,real,'r',linewidth=1,label='Docs Real')
        ax.plot(dates,planned,'k',linewidth=1,label='Docs Planned')
        ax.legend(loc='upper right',fontsize='small')
        fig.show()

    def refreshGen(self):
        start = time.time()
        today = datetime.now()
        self.lblDateRefresh.config(text='Last refresh: '+ str(today))
        #folders = bck.getFolders(self.fileToAnalyze)
        folders = ['CIVIL','ELETRICA','ELETROMECANICA']
        #foldersFormatted = [string.capwords(x) for x in folders]
        foldersFormatted = folders
        bd = pd.read_csv(self.fileToAnalyze,sep=';')

        tarjDate = self.cal1.get_date()

        totalFolderDocCount, numDocPlanned, numDocReal = bck.getGenReview(bd,folders,tarjDate)
        #totalFolderDocCount = bck.getTotals(bd,folders)
        #numDocPlanned = bck.getPlanned(bd,folders,tarjDate)
        #numDocReal = bck.getReal(bd,folders,tarjDate)

        self.createGeneral(foldersFormatted,totalFolderDocCount,numDocPlanned,numDocReal)
        print(time.time() - start)

    def refreshDet(self):
        start = time.time()
        today = datetime.now()
        self.lblDateRefresh.config(text='Last refresh: '+ str(today))
        #folders = bck.getFolders(self.fileToAnalyze)
        folders = ['CIVIL','ELETRICA','ELETROMECANICA']
        #foldersFormatted = [string.capwords(x) for x in folders]
        foldersFormatted = folders
        database = pd.read_excel(self.DataBase)
        bd = pd.read_csv(self.fileToAnalyze,sep=';')
        for i in range(len(bd)):
            bd.loc[i,'Area'] = bck.seekArea(bd.loc[i,'Codificação'],database)
            bd.loc[i,'SubFolder'] = bck.seekSubFolder(bd.loc[i,'Codificação'],database)
        
        #print(bd)

        areas = bck.getAreas(database)
        print(areas)
        #areas = ['GENERAL','VISTA ALEGRE 10','VISTA ALEGRE 3']
        areasFormatted = [string.capwords(x) for x in areas]
        areasFormatted = areas

        tarjDate = self.cal1.get_date()

        self.createReview(folders,foldersFormatted,areas,areasFormatted,tarjDate,bd,database)
        end = time.time()
        print(end-start)

def main():
    root = tk.Tk()
    #root.iconbitmap('atlaslogo.ico')
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()