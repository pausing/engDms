import shutil
import os
import pandas as pd
from datetime import datetime,timedelta,date
import matplotlib.pyplot as plt
from tkinter import messagebox
import numpy as np
import string
import copy
#from win32com.client import Dispatch

def parseTime(strTime):
    # date str 03/07/2023
    y = int(strTime[6:10])
    m = int(strTime[3:5])
    d = int(strTime[0:2])
    return date(y,m,d)


def formatFile(file_path):
    with open(file_path,'r+',encoding='utf-8') as txtFile:
        txt = txtFile.read()
        txt = txt.replace(',','_')
        txt = txt.replace(';',',')
        txtFile.seek(0)
        txtFile.write(txt)
        txtFile.truncate()

def getFolders(file):
    bd = pd.read_excel(file)
    folders = list(bd['Pasta'])
    uniqueFolders = list(set(folders))
    uniqueFolders.sort()
    return uniqueFolders

def seekSubFolder(codDoc,database):
    subFolderSeries = database[database['Codificação'] == codDoc]['SubFolder']
    if len(subFolderSeries) == 1:
        subFolder = subFolderSeries.values[0]
    else:
        subFolder = 'noSubFolder'
    return subFolder

def seekArea(codDoc,database):
    areaSeries = database[database['Codificação'] == codDoc]['Area']
    if len(areaSeries) == 1:
        area = areaSeries.values[0]
    else:
        area = 'noArea'
    return area

def getSubFolders(bd,folder,area):
    subFolder = bd[(bd['Pasta'] == folder) & (bd['Area'] == area)]['SubFolder'].values
    uniqueSubFolder = list(set(subFolder))
    uniqueSubFolder.sort()
    return uniqueSubFolder

def getAreas(database):
    areas = list(database['Area'])
    uniqueAreas =list(set(areas))
    uniqueAreas.sort()
    return uniqueAreas
    
def getTotals(bd,folders):

    numDocTotal = []
    for f in folders:
        numDocTotal.extend([len(bd[bd['Pasta'] == f])])
    
    return numDocTotal

def getPlanned(bd,folders,tarjDate):
    
    numPlannedTotal = []
    for i in range(len(folders)):
        count = 0
        for j in range(len(bd)):
                docDate = parseTime(str(bd.loc[j,'Data Prevista']))
                if bd.loc[j,'Pasta'] == folders[i] and docDate < tarjDate:
                    count += 1
        numPlannedTotal.extend([count])
    return numPlannedTotal

def getReal(bd,folders,tarjDate):
    numPlannedTotal = []
    for i in range(len(folders)):
        count = 0
        for j in range(len(bd)):
                if bd.loc[j,'Data 1° Emissão'] != '--':
                    docDate = parseTime(str(bd.loc[j,'Data 1° Emissão']))
                    if bd.loc[j,'Pasta'] == folders[i] and docDate < tarjDate:
                        count += 1
        numPlannedTotal.extend([count])
    return numPlannedTotal

def getTotalsOfFolderArea(bd,subFolders,folder,area,database):

    totalDocSubFolders = []

    for i in range(len(subFolders)):
        count = 0
        for j in range(len(bd)):
            #cond1 = seekArea(bd.loc[j,'Codificação'],database) == area
            cond1 = bd.loc[j,'Area'] == area
            #cond2 = seekSubFolder(bd.loc[j,'Codificação'],database) == subFolders[i]
            cond2 = bd.loc[j,'SubFolder'] == subFolders[i]
            cond3 = bd.loc[j,'Pasta'] == folder
            if cond1 and cond2 and cond3:
                count += 1
        totalDocSubFolders.extend([count])
    
    return totalDocSubFolders

def getPlannedOfFolderArea(bd,subFolders,folder,area,database,tarjDate):

    numPlannedSubFolders = []

    for i in range(len(subFolders)):
        count = 0
        for j in range(len(bd)):
            docDate = parseTime(str(bd.loc[j,'Data Prevista']))
            cond1 = bd.loc[j,'Area'] == area
            cond2 = bd.loc[j,'SubFolder'] == subFolders[i]
            cond3 = bd.loc[j,'Pasta'] == folder
            cond4 = docDate < tarjDate
            if cond1 and cond2 and cond3 and cond4:
                count += 1
        numPlannedSubFolders.extend([count])
    
    return numPlannedSubFolders

def getRealOfFolderArea(bd,subFolders,folder,area,database,tarjDate):

    numRealSubFolders = []

    for i in range(len(subFolders)):
        count = 0
        for j in range(len(bd)):
            if bd.loc[j,'Data 1° Emissão'] != '--':
                docDate = parseTime(str(bd.loc[j,'Data 1° Emissão']))
                #cond1 = seekArea(bd.loc[i,'Codificação'],database) == area
                cond1 = bd.loc[j,'Area'] == area
                #cond2 = seekSubFolder(bd.loc[i,'Codificação'],database) == subFolders[i]
                cond2 = bd.loc[j,'SubFolder'] == subFolders[i]
                cond3 = bd.loc[j,'Pasta'] == folder
                cond4 = docDate < tarjDate
                if cond1 and cond2 and cond3 and cond4:
                    count += 1
        numRealSubFolders.extend([count])
    
    return numRealSubFolders

def getDetReview(bd,database,folders,areas,tarjDate):

    totals = []
    planned = []
    real = []
    print(folders)
    print(areas)

    for f in folders:
        totalFolder = []
        plannedFolder = []
        realFolder = []
        for a in areas:
            subFolders = getSubFolders(bd,f,a)
            print(subFolders)
            t = getTotalsOfFolderArea(bd,subFolders,f,a,database)
            print(t)
            p = getPlannedOfFolderArea(bd,subFolders,f,a,database,tarjDate)
            print(p)
            r = getRealOfFolderArea(bd,subFolders,f,a,database,tarjDate)
            print(r)

            totalFolder.append(t)
            plannedFolder.append(p)
            realFolder.append(r)
        totals.append(totalFolder)
        planned.append(plannedFolder)
        real.append(realFolder)

    return (totals,planned,real)

def iniStruct(bd,folders,areas):

    struct = []
    subFolders = []
    for f in folders:
        subFolder_f = []
        struct_f_a = []
        for a in areas:
            subFolders_f_a = getSubFolders(bd,f,a)
            subFolder_f.append(subFolders_f_a)

            struct_f_a.append([0 for i in subFolders_f_a])

        subFolders.append(subFolder_f)
        
        struct.append(struct_f_a)

    return subFolders, struct

def add1(struct,subFolders,folders,areas,docFolder,docArea,docSubFolder):

    indexArea = areas.index(docArea)
    indexFolder = folders.index(docFolder)
    indexSubFolder = subFolders[indexFolder][indexArea].index(docSubFolder)

    struct[indexFolder][indexArea][indexSubFolder] = struct[indexFolder][indexArea][indexSubFolder] + 1 

    return struct
    
def getDetReviewOp (bd, database, folders, areas, tarjDate):

    subFolders, struct = iniStruct(bd,folders,areas)
    
    structTotals = copy.deepcopy(struct)
    structPlanned = copy.deepcopy(struct)
    structReal = copy.deepcopy(struct)

    for i in range(len(bd)):
        docArea = bd.loc[i,'Area']
        docFolder = bd.loc[i,'Pasta']
        docSubFolder = bd.loc[i,'SubFolder']
        if bd.loc[i,'Data 1° Emissão'] != '--':
            docRealDate = parseTime(str(bd.loc[i,'Data 1° Emissão']))
        else:
            docRealDate = parseTime('12/12/2025')
        docPlanDate = parseTime(str(bd.loc[i,'Data Prevista']))
        if (docFolder in folders) and (docArea in areas):
            i = folders.index(docFolder) # index Folder
            j = areas.index(docArea) # index Area
            k = subFolders[i][j].index(docSubFolder) # index SubFolder
            # agregar + 1 en totales de docArea, docFolder, docSubFolder
            structTotals[i][j][k] = structTotals[i][j][k] + 1
            if docPlanDate < tarjDate:
                structPlanned[i][j][k] = structPlanned[i][j][k] + 1
            #i agregar + 1 en real de docArea, docFolder, docSubFolder if realDate menor q trajDate
            if docRealDate < tarjDate:
                structReal[i][j][k] = structReal[i][j][k] + 1

    return structTotals, structPlanned, structReal

def getGenReview (bd, folders, tarjDate):

    totalFolderCount = getTotals(bd,folders)
    numDocPlanned = getPlanned(bd,folders,tarjDate)
    numDocReal = getReal(bd,folders,tarjDate)

    return totalFolderCount, numDocPlanned, numDocReal

def getTotals3Cat(db,area,category,subcategory):
        docTotal = len(db.loc[(db['Area'] == area) & (db['Category'] == category) & (db['SubCategory'] == subcategory)])
        return docTotal

def getPlan3Cat(db,fileToAnalyze,tarjDate,area,category,subcategory):
    docs = list(db.loc[(db['Area'] == area) & (db['Category'] == category) & (db['SubCategory'] == subcategory)]['Codificação'])
    print(fileToAnalyze)
    print(docs)
    planned = 0
    #Columna es: Data Prevista
    for i in range(len(docs)):
        print(fileToAnalyze.loc[fileToAnalyze['Codificação'] == docs[i]]['Data Prevista'])
        if parseTime(fileToAnalyze.loc[fileToAnalyze['Codificação'] == docs[i]]['Data Prevista'].values[0]) < tarjDate:
            planned += 1
    return planned

def getReal3Cat(db,fileToAnalyze,tarjDate,area,category,subcategory):
    docs = list(db.loc[(db['Area'] == area) & (db['Category'] == category) & (db['SubCategory'] == subcategory)]['Codificação'])
    real = 0
    #Columna es: Data Prevista
    for i in range(len(docs)):
        if fileToAnalyze.loc[fileToAnalyze['Codificação'] == docs[i]]['Data 1° Emissão'].values[0] != '--':
            if parseTime(fileToAnalyze.loc[fileToAnalyze['Codificação'] == docs[i]]['Data 1° Emissão'].values[0]) < tarjDate:
                real += 1
    return real

def getApproved3Cat(db,fileToAnalyze,area,category,subcategory):
    #aproved states: 
    approvedStates = ['Liberado para Obra','Conforme','Conforme com Comentários']
    docs = list(db.loc[(db['Area'] == area) & (db['Category'] == category) & (db['SubCategory'] == subcategory)]['Codificação'])
    statusDocs = []
    for i in range(len(docs)):
        statusDocs.extend([fileToAnalyze.loc[fileToAnalyze['Codificação'] == docs[i]]['Estado Workflow'].values[0]])
    approved = 0
    for i in range(len(statusDocs)):
        if statusDocs[i] in approvedStates:
            approved += 1
    return approved

def fileSeguimientoVsDB(fileToAnalyze,db):
    #check all docs in filleToAnalyze are in dataBase
    k = 0
    dbCheck = 'all docs in FileToAnalyze are in db'
    check = True
    Pastas = ['CIVIL','ELETRICA', 'ELETROMECANICA']
    for pasta in Pastas:
        for i in range(len(fileToAnalyze)):
            if fileToAnalyze.loc[i,'Pasta'] == pasta:
                cod = fileToAnalyze.loc[i,'Codificação']
                doc = fileToAnalyze.loc[i,'Descricao']
                if cod not in list(db['Codificação']):
                    check = False
                    dbCheck = 'docs in FileToAnalyze not found in db'
                    k += 1
                    print('{:03} Document not found in DataBase: {}\t{}'.format(k,cod, doc))

    k = 0
    fileToAnalyzeCheck = 'all docs in db are in FileToAnalyze'
    for i in range(len(db)):
        cod = db.loc[i,'Codificação']
        doc = db.loc[i,'Descricao do Documento']
        if cod not in list(fileToAnalyze['Codificação']):
            check = False
            fileToAnalyzeCheck = 'docs db are not found in FileToAnalyze'
            k += 1
            print('{:03} Document not found in FileToAnalyze: {}\t{}'.format(k,cod, doc))
    
    return check, dbCheck, fileToAnalyzeCheck


def compareFileToAnalyzeVsDB(PathfileToAnalyze,PathDatabase,tarjDate):
    fileToAnalyze = pd.read_csv(PathfileToAnalyze,sep=';')
    dataBase = pd.read_excel(PathDatabase)
    print(tarjDate)
    #print(fileToAnalyze)
    #print(dataBase)

    Pastas = ['CIVIL','ELETRICA', 'ELETROMECANICA']
    #Pastas = list(set(fileToAnalyze['Pasta']))
    Pastas.sort()

    NumDocsFileToAnalyze = getTotals(fileToAnalyze,Pastas)
    NumDocsDataBase = getTotals(dataBase,Pastas)

    totalDocFileToAnalyze = sum(NumDocsFileToAnalyze)
    totalDocDataBase = sum(NumDocsDataBase)

    check, mens1, mens2 = fileSeguimientoVsDB(fileToAnalyze,dataBase)

    if not check:
        print(mens1)
        print(mens2)
    else:
    
        areas = list(set(dataBase['Area']))
        areas.sort()
        #print(areas)

        categories = []
        for area in areas:
            category = list(set(dataBase[dataBase['Area'] == area]['Category']))
            category.sort()
            categories.append(category)
    
        #print(categories)

        subCategories = []

        for i in range(len(areas)):
            subCatAreaAndCat = []
            for j in range(len(categories[i])):
                subCategory = list(set(dataBase.loc[(dataBase['Area'] == areas[i]) & (dataBase['Category'] == categories[i][j])]['SubCategory']))
                subCategory.sort()
                subCatAreaAndCat.append(subCategory)
            subCategories.append(subCatAreaAndCat)

        #print(subCategories)

        planillaSeguimiento = pd.DataFrame(columns = ['AREA','CATEGORY','SUBCATEGORY'])

        count = 0
        for i in range(len(areas)):
            for j in range(len(categories[i])):
                for k in range(len(subCategories[i][j])):
                    planillaSeguimiento = pd.concat([planillaSeguimiento,pd.DataFrame([[areas[i],categories[i][j],subCategories[i][j][k]]],columns=planillaSeguimiento.columns)],ignore_index=True)
        print(planillaSeguimiento)

        for i in range(len(planillaSeguimiento)):
            area = planillaSeguimiento.loc[i,'AREA']
            category = planillaSeguimiento.loc[i,'CATEGORY']
            subcategory = planillaSeguimiento.loc[i,'SUBCATEGORY']
            #Totales 
            docTotal = getTotals3Cat(dataBase,area,category,subcategory)
            planillaSeguimiento.loc[i,'TOTAL'] = docTotal
            #EMISION Planificado
            docPlanEmi = getPlan3Cat(dataBase,fileToAnalyze,tarjDate,area,category,subcategory)
            planillaSeguimiento.loc[i,'EMISION PLANI'] = docPlanEmi
            #EMISIOM Real
            docRealEmi = getReal3Cat(dataBase,fileToAnalyze,tarjDate,area,category,subcategory)
            planillaSeguimiento.loc[i,'EMISION REAL'] = docRealEmi
            #APROBACION
            docApproved = getApproved3Cat(dataBase,fileToAnalyze,area,category,subcategory)
            planillaSeguimiento.loc[i,'APPROVED'] = docApproved
            #Fecha Max Obra
    
        print(planillaSeguimiento)
        planillaSeguimiento.to_excel(os.path.join('02_EstadoIngenieria','estatusIng_{:04d}{:02d}{:02d}.xlsx'.format(date.today().year,date.today().month,date.today().day)),index=False)

        #xl = Dispatch('Excel.Application')
        #xl.Visible = True
        #wb = xl.Workbooks.Open(os.path.join(os.getcwd(),'02_EstadoIngenieria',os.listdir('02_EstadoIngenieria')[len(os.listdir('02_EstadoIngenieria'))-1]))

def createTable(total, planned, real, approved):
    rows = []
    for i in range(len(total)):
        diff = '{:.2f}'.format(100*(real[i]-planned[i])/planned[i])
        rows.append([total[i],planned[i],real[i],diff,approved[i]])
    return rows

def getApproved(db,categories):
    #aproved states: 
    approvedStates = ['Liberado para Obra','Conforme','Conforme com Comentários']
    approvedMatrix = []
    for category in categories:
        statusDocs = list(db.loc[db['Pasta'] == category]['Estado Workflow'])
        approved = 0
        for i in range(len(statusDocs)):
            if statusDocs[i] in approvedStates:
                approved += 1
        approvedMatrix.extend([approved])
    return approvedMatrix

def finalReport(PathfileToAnalyze,PathDatabase,tarjStartDate,tarjEndDate):
    fileToAnalyze = pd.read_csv(PathfileToAnalyze,sep=';')
    dataBase = pd.read_excel(PathDatabase)

    reportFolderName = os.path.join('03_Reports','EngReports_{:04d}{:02d}{:02d}_{:02d}{:02d}'.format(date.today().year,date.today().month,date.today().day,datetime.today().hour,datetime.today().minute))

    if not os.path.exists(reportFolderName):
        try:
            os.makedirs(reportFolderName)
            print('Folder created: {}'.format(reportFolderName))
        except:
            print('Error creating: {}'.format(reportFolderName))
    
    print('Reports from {} to {}'.format(tarjStartDate,tarjEndDate))

    dates = [tarjStartDate]
    difDays = tarjEndDate - tarjStartDate

    for i in range(difDays.days+1):
        if i != 0:
            dates.extend([dates[i-1] + timedelta(1)])

    # general report
    # 2 zones, issued and approved
    # issued

    pastas = ['CIVIL','ELETRICA', 'ELETROMECANICA'] # categorias del csv del PV, habria q hacer automatico en funcion del indice
    total = getTotals(fileToAnalyze, pastas)
    plannedTarjDate = getPlanned(fileToAnalyze, pastas, tarjEndDate)
    realTarjDate = getReal(fileToAnalyze, pastas, tarjEndDate)
    approvedTarjDate = getApproved(fileToAnalyze,pastas)

    valuesForTable = createTable(total, plannedTarjDate, realTarjDate,approvedTarjDate)
    print(valuesForTable)
    row_labels = pastas 
    col_labels = ['TOTAL','PLANNED','REAL','DIFF [%]','AFC']
    print(col_labels)

    planned = []
    real = []

    for i in range(len(dates)):
        planned.extend([sum(getPlanned(fileToAnalyze, pastas, dates[i]))])
        real.extend([sum(getReal(fileToAnalyze, pastas, dates[i]))])
    


    fig, ax = plt.subplots(1,1,figsize=[3*6.4,3*4.8])
    
    ax.grid(True)
    ax.set_title('Planned vs Real',size='small')
    ax.tick_params(labelsize='xx-small')
    ax.plot(dates,real,'r',linewidth=1,label='Docs Real')
    ax.plot(dates,planned,'k',linewidth=1,label='Docs Planned')
    ax.legend(loc='upper right',fontsize='small')
    table = ax.table(cellText=valuesForTable,colWidths=[0.1] * 5,rowLabels=row_labels,colLabels=col_labels,loc='lower right',rowLoc = 'center',colLoc = 'center')
    table.scale(1,4)
    fig.show()
    
    # details reports for areas

    # details reports for categories

    return 0