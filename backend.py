import warnings
warnings.simplefilter(action = 'ignore',category=FutureWarning)
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime,timedelta,date
import datetime as dd
from tabulate import tabulate
import os
from os.path import isfile
import numpy as np
import outputRev as out
import pdfExport

def formatFile(file_path):
    try:
        with open(file_path,'r+',encoding='utf-8') as txtFile:
            txt = txtFile.read()
            if txt.find(';') != -1:
                txt = txt.replace(',','_')
                txt = txt.replace(';',',')
                txtFile.seek(0)
                txtFile.write(txt)
                txtFile.truncate()
            else:
                print('file {} already with commas'.format(file_path))
    except:
        with open(file_path,'r+',encoding='ISO-8859-1') as txtFile:
            txt = txtFile.read()
            if txt.find(';') != -1:
                txt = txt.replace(',','_')
                txt = txt.replace(';',',')
                txtFile.seek(0)
                txtFile.write(txt)
                txtFile.truncate()
            else:
                print('file {} already with commas'.format(file_path))

def parseTime(strTime):
    # date str 03/07/2023
    y = int(strTime[6:10])
    m = int(strTime[3:5])
    d = int(strTime[0:2])
    return date(y,m,d)

def parseTimeBD(bd,title):
    for i in range(len(bd)):
        #print(i,bd.loc[i,title])
        if bd.loc[i,title] == '--' or not issubclass(type(bd.loc[i,title]),str):
            bd.loc[i,title + '_parsed'] = date(2050,1,1)
        else:
            bd.loc[i,title + '_parsed'] = parseTime(bd.loc[i,title])

def printResults(titles,totals,IssuedExpected,IssuedReal,AppExpected,AppReal,responsible):
    print('-----')
    print(responsible)
    print('-----')
    t = ['TOTAL']
    t.extend(totals)
    t.extend([sum(totals)])
    t.extend(['--'])
    e = ['ISSUED EXPECTED']
    e.extend(IssuedExpected)
    e.extend([sum(IssuedExpected)])
    e.extend(['{:.02f}'.format(100*sum(IssuedExpected)/sum(totals))])
    r = ['ISSUED REAL']
    r.extend(IssuedReal)
    r.extend([sum(IssuedReal)])
    r.extend(['{:.02f}'.format(100*sum(IssuedReal)/sum(totals))])
    ae = ['APPROVED EXPECTED']
    ae.extend(AppExpected)
    ae.extend([sum(AppExpected)])
    ae.extend(['{:.02f}'.format(100*sum(AppExpected)/sum(totals))])
    ar = ['APPROVED REAL']
    ar.extend(AppReal)
    ar.extend([sum(AppReal)])
    ar.extend(['{:.02f}'.format(100*sum(AppReal)/sum(totals))])
    data = [t,e,r,ae,ar]

    h = ['ITEM']
    h.extend(titles)
    h.extend(['SUM'])
    h.extend(['SUM [%]'])

    print(tabulate(data,headers=h,tablefmt="grid"))
    return data,h

def parseEspecialColumns(bd,outDf):

    for i in range(len(bd)):
        try:
            bd.loc[i,'AREA'] = outDf.loc[outDf['Code'] == bd.loc[i,'Nomenclature']]['Area'].values[0]
            bd.loc[i,'CATEGORY'] = outDf.loc[outDf['Code'] == bd.loc[i,'Nomenclature']]['Category'].values[0]
            bd.loc[i,'SUBCATEGORY'] = outDf.loc[outDf['Code'] == bd.loc[i,'Nomenclature']]['Subcategory'].values[0]
        except:
            print('Doc {}:{} not found in Output'.format(bd.loc[i,'Nomenclature'],bd.loc[i,'Description']))
            bd.loc[i,'AREA'] = 'not def'
            bd.loc[i,'CATEGORY'] = 'not def'
            bd.loc[i,'SUBCATEGORY'] = 'not def'

def parseDateInPlanFile(file):
    print('Parsing file {}'.format(file))
    d = file[file.find('planejamento_') + len('planejamento_') : file.find('planejamento_') + len('planejamento_') + 2]
    m = file[file.find('planejamento_') + len('planejamento_') + 2 : file.find('planejamento_') + len('planejamento_') + 4]
    y = file[file.find('planejamento_') + len('planejamento_') + 4 : file.find('planejamento_') + len('planejamento_') + 8]
    print(d,m,y)
    return y,m,d

def dateFromFile(file):
    y = int(file[0:4])
    m = int(file[4:6])
    d = int(file[6:8])
    return date(y,m,d)

def analyzeFile(fileToAnalyze,subDirOutput,approvedStatus,foldersEng,foldersQA,project,projectAcro,disciplina,dateOfAnalysis):

    formatFile(fileToAnalyze)
    bd = pd.read_csv(fileToAnalyze)
    # parse information Column Custom Fields
    outDf = out.reviewOutput(subDirOutput,foldersEng,approvedStatus,dateOfAnalysis)[1]
    #parseEspecialColumns(bd,projectAcro,keyWordCol,disciplina)
    parseEspecialColumns(bd,outDf)

    listOfData = []
    listOfTitles = []

    # dir to save table of Totals
    ExcelDir = os.path.join(os.path.dirname(fileToAnalyze),'..','Excel')
    if not os.path.exists(ExcelDir):
        os.mkdir(ExcelDir)

    parseTimeBD(bd,'Date 1st Issue')
    parseTimeBD(bd,'Expected Date')
    parseTimeBD(bd,'Expected Approval Date')
    parseTimeBD(bd,'Approval Date')

    # save to excel de Input file from Colaborativo
    bd.to_excel(os.path.join(ExcelDir,fileToAnalyze.split(os.sep)[-1][:-4] + '.xlsx'))

    # Check which Responsibles have documents in the Engineering Folders
    responsibles = list(set(bd['Responsible']))
    for r in responsibles:
        count = 0
        for f in foldersEng:
            count += len(bd[(bd['Folder'] == f) & (bd['Responsible'] == r)])
        print(r,count)
        if count == 0:
            responsibles.remove(r)
    responsibles.sort()
    print('Responsibles: ',responsibles)

    #dateOfAnalysis = date(date.today().year,date.today().month,date.today().day)
    #dateOfAnalysis = dayOfAnalysis

    # Table of TOTALS
    doc1stRevPerFolder = []
    docExpectedPerFolder = []
    docApprExpectedPerFolder = []
    docApprRealPerFolder = []
    docTotalsPerFolder = []
    for f in foldersEng:
        docTotalsPerFolder.extend([len(bd[(bd['Folder'] == f)])])
        doc1stRevPerFolder.extend([len(bd[(bd['Folder'] == f) & (bd['Date 1st Issue_parsed'] <= dateOfAnalysis)])])
        docExpectedPerFolder.extend([len(bd[(bd['Folder'] == f) & (bd['Expected Date_parsed'] <= dateOfAnalysis)])])
        docApprExpectedPerFolder.extend([len(bd[(bd['Folder'] == f) & (bd['Expected Approval Date_parsed'] <= dateOfAnalysis)])])
        docApprRealPerFolder.extend([len(bd[(bd['Folder'] == f) & (bd['Workflow State'].isin(approvedStatus))])])

    print('Date of analysis: {}'.format(dateOfAnalysis))
    data, headers = printResults(foldersEng,docTotalsPerFolder,docExpectedPerFolder,doc1stRevPerFolder,docApprExpectedPerFolder,docApprRealPerFolder, 'Total')

    dataPd = pd.DataFrame(data,columns=headers)
    fileTitle = 'FolderPlan_{:04d}_{:02d}_{:02d}_{}_{}_Total.xlsx'.format(dateOfAnalysis.year,dateOfAnalysis.month,dateOfAnalysis.day,project,disciplina)
    engReportFileTitle = os.path.join(ExcelDir,'{:04d}{:02d}{:02d}_{}_{}.pdf'.format(dateOfAnalysis.year,dateOfAnalysis.month,dateOfAnalysis.day,project,disciplina))
    dataPd.to_excel(os.path.join(ExcelDir,fileTitle))
    
    # Lists to Store the tables TOTAL and per Responsables and its Titles
    listOfData.extend([dataPd])
    listOfTitles.extend(['Total'])

    for r in responsibles:
        doc1stRevPerFolder = []
        docExpectedPerFolder = []
        docApprExpectedPerFolder = []
        docApprRealPerFolder = []
        docTotalsPerFolder = []
        for f in foldersEng:
            docTotalsPerFolder.extend([len(bd[(bd['Folder'] == f) & (bd['Responsible'] == r)])])
            doc1stRevPerFolder.extend([len(bd[(bd['Folder'] == f) & (bd['Date 1st Issue_parsed'] <= dateOfAnalysis) & (bd['Responsible'] == r)])])
            docExpectedPerFolder.extend([len(bd[(bd['Folder'] == f) & (bd['Expected Date_parsed'] <= dateOfAnalysis) & (bd['Responsible'] == r)])])
            docApprExpectedPerFolder.extend([len(bd[(bd['Folder'] == f) & (bd['Expected Approval Date_parsed'] <= dateOfAnalysis) & (bd['Responsible'] == r) ])])
            docApprRealPerFolder.extend([len(bd[(bd['Folder'] == f) & (bd['Workflow State'].isin(approvedStatus)) & (bd['Responsible'] == r) ])])

        print('Date of analysis: {}'.format(dateOfAnalysis))
        #print(data)
        data, headers = printResults(foldersEng,docTotalsPerFolder,docExpectedPerFolder,doc1stRevPerFolder,docApprExpectedPerFolder,docApprRealPerFolder, r)

        dataPd = pd.DataFrame(data,columns=headers)
        #dataPd.to_excel(os.path.join(ExcelDir,fileTitle))
        listOfData.extend([dataPd])
        listOfTitles.extend([r])
    return listOfTitles, listOfData,engReportFileTitle

def analyzeRespAndCat(fileToAnalyze,project,disciplina,approvedStatus,foldersEng,titles,Alldata,dayOfAnalysis):
    dateOfAnalysis = dayOfAnalysis
    ExcelDir = os.path.join(os.path.dirname(fileToAnalyze),'..','Excel')
    bd = pd.read_excel(os.path.join(ExcelDir,fileToAnalyze.split(os.sep)[-1][:-4] + '.xlsx'))

    for title in ['Expected Date_parsed','Date 1st Issue_parsed','Expected Approval Date_parsed','Approval Date_parsed']:
        for i in range(len(bd)):
            if bd.loc[i,title] == '--':
                bd.loc[i,title] = date(2050,1,1)
            else:
                bd.loc[i,title] = date(bd.loc[i,title].year,bd.loc[i,title].month,bd.loc[i,title].day)

    #print(bd[bd['Folder'].isin(foldersEng)]['Responsible'])
    responsibles = list(set(bd[bd['Folder'].isin(foldersEng)]['Responsible']))
    responsibles.sort()

    workFlowStatus = list(set(bd['Workflow State']))
    workFlowStatus.sort()
    
    areas = []
    for r in responsibles:
        areas.append(list(set(bd[bd['Responsible'] == r]['AREA'])))

    subcategories = []
    for i in range(len(responsibles)):
        print(responsibles[i])
        subCategoriesArea = []
        for j in range(len(areas[i])):
            print(areas[i][j])
            subCategoriesAreaJRespI = list(set(bd[(bd['Responsible'] == responsibles[i]) & (bd['AREA'] == areas[i][j]) & (bd['Folder'].isin(foldersEng))]['SUBCATEGORY']))
            print(subCategoriesAreaJRespI)
            subCategoriesAreaJRespI.sort()
            subCategoriesArea.append(subCategoriesAreaJRespI)
        subcategories.append(subCategoriesArea)

    data = []
    k = 0
    for i in range(len(responsibles)):
        for j in range(len(areas[i])):
            for m in range(len(subcategories[i][j])):
                data.append([responsibles[i],areas[i][j],subcategories[i][j][m]])
                k += 1
    
    for i in range(len(data)):
        t = len(bd[(bd['Responsible'] == data[i][0]) & (bd['AREA'] == data[i][1]) & (bd['SUBCATEGORY'] == data[i][2]) & bd['Folder'].isin(foldersEng)])
        e = len(bd[(bd['Responsible'] == data[i][0]) & (bd['AREA'] == data[i][1]) & (bd['SUBCATEGORY'] == data[i][2]) & (bd['Expected Date_parsed'] <= dateOfAnalysis) & bd['Folder'].isin(foldersEng)])
        r = len(bd[(bd['Responsible'] == data[i][0]) & (bd['AREA'] == data[i][1]) & (bd['SUBCATEGORY'] == data[i][2]) & (bd['Date 1st Issue_parsed'] <= dateOfAnalysis) & bd['Folder'].isin(foldersEng)])
        ae = len(bd[(bd['Responsible'] == data[i][0]) & (bd['AREA'] == data[i][1]) & (bd['SUBCATEGORY'] == data[i][2]) & (bd['Expected Approval Date_parsed'] <= dateOfAnalysis) & bd['Folder'].isin(foldersEng)])
        ar = len(bd[(bd['Responsible'] == data[i][0]) & (bd['AREA'] == data[i][1]) & (bd['SUBCATEGORY'] == data[i][2]) & (bd['Workflow State'].isin(approvedStatus)) & bd['Folder'].isin(foldersEng)])
        wStatus = []
        for w in workFlowStatus:
            wStatus.extend ( [len(bd[(bd['Responsible'] == data[i][0]) & (bd['AREA'] == data[i][1]) & (bd['SUBCATEGORY'] == data[i][2]) & (bd['Workflow State'] == w) & bd['Folder'].isin(foldersEng)])])
        data[i].extend([t,e,r,ae,ar])
        data[i].extend(wStatus)
    h = ['RESP','AREA','SUBCAT','TOTAL','ISS EXP','ISS REAL','APP EXP','APP REAL'] 
    h.extend(workFlowStatus)
    #print(tabulate(data,headers=h,tablefmt="grid"))
    dataPd = pd.DataFrame(data,columns=h)
    #Subtotal per RESP
    h.pop(h.index('RESP'))
    h.pop(h.index('AREA'))
    h.pop(h.index('SUBCAT'))
    for r in responsibles:
        newLine =	{'RESP': r + ' (SUM)', 'AREA': 'SUBTOTAL', 'SUBCAT': 'SUBTOTAL'}
        for col in h:
            newLine[col] = dataPd[dataPd['RESP'] == r][col].sum()
        dataPd.loc[len(dataPd)] = newLine
    
    #Clean Issued For Construction_ state
    if 'Issued For Construction_' in h:
        print('Issued For Construction_ found!!')
        if 'Issued For Construction' in h:
            dataPd['Issued For Construction'] = dataPd['Issued For Construction'] + dataPd['Issued For Construction_']
        else:
            dataPd['Issued For Construction'] = dataPd['Issued For Construction_']  
        dataPd.drop('Issued For Construction_',axis=1,inplace=True)
        h.remove("Issued For Construction_")
    
    dataPd.sort_values(by=['RESP','AREA','SUBCAT'],inplace=True)
    dataPd = dataPd.reset_index(drop=True)
    #print(dataPd)
    dataPd.to_excel(os.path.join(ExcelDir,'SubCategoryPlan_{:04d}_{:02d}_{:02d}_{}_{}.xlsx'.format(dateOfAnalysis.year,dateOfAnalysis.month,dateOfAnalysis.day,project,disciplina)))
    titles.extend(['per AREA and SUBCATEGORY'])
    Alldata.extend([dataPd])
    return titles, Alldata

def parsePlanDir(dir):
    files = os.listdir(dir)
    for f in files:
        if isfile(os.path.join(dir,f)) and f[-3:] == 'csv':
            if (f[0:4] == '2024') or (f[0:4] == '2025'):
                continue
                print('File: {} ok'.format(f))
            else:
                y,m,d = parseDateInPlanFile(os.path.join(dir,f))
                print(y,m,d)
                print('renaming: ')
                print(os.path.join(dir,f))
                print(os.path.join(dir,y+m+d+'_'+f))
                os.rename(os.path.join(dir,f),os.path.join(dir,y+m+d+'_'+f))

def chooseFile(dir):
    elements = os.listdir(dir)
    files = []
    for e in elements:
        if isfile(os.path.join(dir,e)):
            files.extend([e])
    files.sort()
    #print(dateFromFile(files[-1]))
    return os.path.join(dir,files[-1]), dateFromFile(files[-1])

def genReportPerProject(dirProject,disciplines,projectFullName,dayOfAnalysis,foldersEng,folderSup,projectsWithSUP):
    
    iniData = {
        'ITEM': ['TOTAL','ISSUED EXPECTED','ISSUED REAL','APPROVED EXPECTED','APPROVED REAL'],
        'CIVIL': [0,0,0,0,0],
        'ELECTRICAL': [0,0,0,0,0],
        'ELECTROMECHANICAL': [0,0,0,0,0],
        'EQUIPMENT': [0,0,0,0,0],
        'SUM': [0,0,0,0,0],
        'SUM [%]': [0,0,0,0,0],
    }

    # ini :
    totalDF = pd.DataFrame(iniData)
    #print(totalDF)

    text = 'FolderPlan_{:04d}_{:02d}_{:02d}'.format(dayOfAnalysis.year,dayOfAnalysis.month,dayOfAnalysis.day)

    for d in disciplines:
        subDir = os.path.join(dirProject,d,'Excel')
        files = os.listdir(subDir)
        for f in files:
            if text in f:
                #print(f)
                file = os.path.join(subDir,f)
        
                totalDiscipline = pd.read_excel(file)
                #print(totalDiscipline)

                if  (projectFullName in projectsWithSUP) & (d.find('SUP') != -1):
                    #print('project with SUP', projectFullName)
                    for f in folderSup[projectFullName]:
                        totalDF['EQUIPMENT'] += totalDiscipline[f]

                else:
                    totalDF['CIVIL'] += totalDiscipline['CIVIL']
                    totalDF['ELECTRICAL'] += totalDiscipline['ELECTRICAL']
                    totalDF['ELECTROMECHANICAL'] += totalDiscipline['ELECTROMECHANICAL']
                    totalDF['EQUIPMENT'] += totalDiscipline['EQUIPMENT']
                break
    
    totalDF['SUM'] = totalDF['CIVIL'] + totalDF['ELECTRICAL'] + totalDF['ELECTROMECHANICAL'] + totalDF['EQUIPMENT']
    for i in range(1,len(totalDF)):
        if totalDF.loc[0,'SUM'] == 0:
            totalDF.loc[1,'SUM [%]'] = 0
        else:
            totalDF.loc[i,'SUM [%]'] = 100 * totalDF.loc[i,'SUM'] / totalDF.loc[0,'SUM']
    
    totalDF['SUM [%]'] = totalDF['SUM [%]'].apply(lambda x : round(x,2))

    #print('----------------------------------- TOTAL DF')
    #print(totalDF)
        
    return totalDF