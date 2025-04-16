import warnings
warnings.simplefilter(action = 'ignore',category=FutureWarning)
import pandas as pd
from datetime import datetime,timedelta,date
import datetime as dd
from tabulate import tabulate
import os
from os.path import isfile
import outputRev as out
import chardet
import pdfExport
import numpy as np

def formatFile(file_path,logger):

    try:
        with open(file_path,'r+',encoding='utf-8', errors='ignore') as txtFile:
            txt = txtFile.read()
            logger.info('file: {} opened')
            if txt.find(';') != -1:
                logger.info('file wiht ;, replacing')
                txt = txt.replace(',','_')
                txt = txt.replace(';',',')
                txtFile.seek(0)
                txtFile.write(txt)
                txtFile.truncate()
            else:
                logger.info('file {} already with commas'.format(file_path))
    except Exception as e:
        logger.info(f'Failed to open with utf-8 encoding: {str(e)}')
        with open(file_path,'r+',encoding='ISO-8859-1') as txtFile:
            txt = txtFile.read()
            logger.info('file: {} opened with ISO-8859-1 encoding')
            if txt.find(';') != -1:
                logger.info('file with ;, replacing')
                txt = txt.replace(',','_')
                txt = txt.replace(';',',')
                txtFile.seek(0)
                txtFile.write(txt)
                txtFile.truncate()
            else:
                logger.info('file {} already with commas'.format(file_path))

def parseTime(strTime,iden):
    # date str 03/07/2023
    try:
        y = int(strTime[6:10])
        m = int(strTime[3:5])
        d = int(strTime[0:2])
    except Exception as e:
        print('Error in {}'.format(iden))
        print('Error in {}'.format(strTime))
        print(e)
        y = 2050
        m = 1
        d = 1
    return date(y,m,d)

def parseTimeBD(bd,title,iden):
    for i in range(len(bd)):
        #print(i,bd.loc[i,title])
        if bd.loc[i,title] == '--' or not issubclass(type(bd.loc[i,title]),str):
            bd.loc[i,title + '_parsed'] = date(2050,1,1)
        else:
            bd.loc[i,title + '_parsed'] = parseTime(bd.loc[i,title],iden)

def printResults(titles,totals,IssuedExpected,IssuedReal,IssuedRealAndExpected,AppExpected,AppReal,responsible,logger):
    logger.info(responsible)
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
    realAndExp = ['ISSUED REAL FROM EXPECTED']
    realAndExp.extend(IssuedRealAndExpected)
    realAndExp.extend([sum(IssuedRealAndExpected)])
    realAndExp.extend(['{:.02f}'.format(100*sum(IssuedRealAndExpected)/sum(totals))])
    ae = ['APPROVED EXPECTED']
    ae.extend(AppExpected)
    ae.extend([sum(AppExpected)])
    ae.extend(['{:.02f}'.format(100*sum(AppExpected)/sum(totals))])
    ar = ['APPROVED REAL']
    ar.extend(AppReal)
    ar.extend([sum(AppReal)])
    ar.extend(['{:.02f}'.format(100*sum(AppReal)/sum(totals))])
    data = [t,e,r,realAndExp,ae,ar]

    h = ['ITEM']
    h.extend(titles)
    h.extend(['SUM'])
    h.extend(['SUM [%]'])

    logger.info('\n' + tabulate(data,headers=h,tablefmt="grid"))
    return data,h

def parseEspecialColumns(bd,outDf,logger):

    for i in range(len(bd)):
        try:
            bd.loc[i,'AREA'] = outDf.loc[outDf['Code'] == bd.loc[i,'Nomenclature']]['Area'].values[0]
            bd.loc[i,'CATEGORY'] = outDf.loc[outDf['Code'] == bd.loc[i,'Nomenclature']]['Category'].values[0]
            bd.loc[i,'SUBCATEGORY'] = outDf.loc[outDf['Code'] == bd.loc[i,'Nomenclature']]['Subcategory'].values[0]
        except:
            logger.info('Doc {}:{} not found in Output'.format(bd.loc[i,'Nomenclature'],bd.loc[i,'Description']))
            bd.loc[i,'AREA'] = 'not def'
            bd.loc[i,'CATEGORY'] = 'not def'
            bd.loc[i,'SUBCATEGORY'] = 'not def'

def parseDateInPlanFile(file,logger):
    logger.info('Parsing file {}'.format(file))
    d = file[file.find('planejamento_') + len('planejamento_') : file.find('planejamento_') + len('planejamento_') + 2]
    m = file[file.find('planejamento_') + len('planejamento_') + 2 : file.find('planejamento_') + len('planejamento_') + 4]
    y = file[file.find('planejamento_') + len('planejamento_') + 4 : file.find('planejamento_') + len('planejamento_') + 8]
    return y,m,d

def dateFromFile(file):
    y = int(file[0:4])
    m = int(file[4:6])
    d = int(file[6:8])
    return date(y,m,d)

def analyzeFile(fileToAnalyze,subDirOutput,approvedStatus,foldersEng,foldersQA,project,projectAcro,disciplina,dateOfAnalysis,logger):

    formatFile(fileToAnalyze,logger)
    #print(fileToAnalyze)
    bd = pd.read_csv(fileToAnalyze)
    # parse information Column Custom Fields
    outDf = out.reviewOutput(subDirOutput,foldersEng,approvedStatus,dateOfAnalysis,logger,projectAcro,disciplina)[2]
    #parseEspecialColumns(bd,projectAcro,keyWordCol,disciplina)
    parseEspecialColumns(bd,outDf,logger)

    listOfData = []
    listOfTitles = []

    # dir to save table of Totals
    ExcelDir = os.path.join(os.path.dirname(fileToAnalyze),'..','Excel')
    if not os.path.exists(ExcelDir):
        os.mkdir(ExcelDir)

    parseTimeBD(bd,'Date 1st Issue', projectAcro + ' ' + disciplina)
    parseTimeBD(bd,'Expected Date', projectAcro + ' ' + disciplina)
    parseTimeBD(bd,'Expected Approval Date', projectAcro + ' ' + disciplina)
    parseTimeBD(bd,'Approval Date', projectAcro + ' ' + disciplina)

    # save to excel de Input file from Colaborativo
    bd.to_excel(os.path.join(ExcelDir,fileToAnalyze.split(os.sep)[-1][:-4] + '.xlsx'))

    # Check which Responsibles have documents in the Engineering Folders
    total_responsibles = list(set(bd['Responsible']))
    logger.info('responsibles in the data frame {}'.format(total_responsibles))
    logger.info('responsible alternative: {}'.format(list(set(bd[bd['Folder'].isin(foldersEng)]['Responsible']))))
    responsibles = []
    for r in total_responsibles:
        count = len(bd[(bd['Folder'].isin(foldersEng)) & (bd['Responsible'] == r)])
        logger.info('responsible: {}, number of documents {}'.format(r,count))
        if count != 0:
            responsibles.extend([r])
            logger.info('adding {} to list of responsibles'.format(r))
    responsibles.sort()
    logger.info('Responsibles: {}'.format(responsibles))

    # Table of TOTALS
    doc1stRevPerFolder = []
    docExpectedPerFolder = []
    docApprExpectedPerFolder = []
    docApprRealPerFolder = []
    docTotalsPerFolder = []
    doc1stRevPerFolderAndExpected = []

    for f in foldersEng:
        filteredData = bd[(bd['Folder'] == f) & (bd['Workflow State'] != 'Cancelled')]
        docTotalsPerFolder.extend([len(filteredData)])
        doc1stRevPerFolder.extend([len(filteredData[(filteredData['Date 1st Issue_parsed'] <= dateOfAnalysis)])])
        doc1stRevPerFolderAndExpected.extend([len(filteredData[(filteredData['Date 1st Issue_parsed'] <= dateOfAnalysis) & (filteredData['Expected Date_parsed'] <= dateOfAnalysis)])])
        docExpectedPerFolder.extend([len(filteredData[(filteredData['Expected Date_parsed'] <= dateOfAnalysis)])])
        docApprExpectedPerFolder.extend([len(filteredData[(filteredData['Expected Approval Date_parsed'] <= dateOfAnalysis)])])
        docApprRealPerFolder.extend([len(filteredData[(filteredData['Workflow State'].isin(approvedStatus))])])

    data, headers = printResults(foldersEng,docTotalsPerFolder,docExpectedPerFolder,doc1stRevPerFolder,doc1stRevPerFolderAndExpected,docApprExpectedPerFolder,docApprRealPerFolder,'Total',logger)

    dataPd = pd.DataFrame(data,columns=headers)
    fileTitle = 'FolderPlan_{:04d}_{:02d}_{:02d}_{}_{}_Total.xlsx'.format(dateOfAnalysis.year,dateOfAnalysis.month,dateOfAnalysis.day,project,disciplina)
    engReportFileTitle = os.path.join(ExcelDir,'{:04d}{:02d}{:02d}_{}_{}.pdf'.format(dateOfAnalysis.year,dateOfAnalysis.month,dateOfAnalysis.day,project,disciplina))
    dataPd.to_excel(os.path.join(ExcelDir,fileTitle))
    
    # Lists to Store the tables TOTAL and per Responsables and its Titles
    listOfData.extend([dataPd])
    listOfTitles.extend(['Total'])

    for r in responsibles:
        dataPerResponsible = bd[(bd['Responsible'] == r) & (bd['Workflow State'] != 'Cancelled')]
        doc1stRevPerFolder = []
        docExpectedPerFolder = []
        docApprExpectedPerFolder = []
        docApprRealPerFolder = []
        docTotalsPerFolder = []
        doc1stRevPerFolderAndExpected = []
        for f in foldersEng:
            filteredData = dataPerResponsible[dataPerResponsible['Folder'] == f]
            docTotalsPerFolder.extend([len(filteredData)])
            doc1stRevPerFolder.extend([len(filteredData[filteredData['Date 1st Issue_parsed'] <= dateOfAnalysis])])
            doc1stRevPerFolderAndExpected.extend([len(filteredData[(filteredData['Date 1st Issue_parsed'] <= dateOfAnalysis) & (filteredData['Expected Date_parsed'] <= dateOfAnalysis)])])
            docExpectedPerFolder.extend([len(filteredData[filteredData['Expected Date_parsed'] <= dateOfAnalysis])])
            docApprExpectedPerFolder.extend([len(filteredData[filteredData['Expected Approval Date_parsed'] <= dateOfAnalysis])])
            docApprRealPerFolder.extend([len(filteredData[filteredData['Workflow State'].isin(approvedStatus)])])

        data, headers = printResults(foldersEng,docTotalsPerFolder,docExpectedPerFolder,doc1stRevPerFolder,doc1stRevPerFolderAndExpected,docApprExpectedPerFolder,docApprRealPerFolder,r,logger)

        dataPd = pd.DataFrame(data,columns=headers)

        listOfData.extend([dataPd])
        listOfTitles.extend([r])
    return listOfTitles, listOfData,engReportFileTitle

def analyzeRespAndCat(fileToAnalyze,project,disciplina,approvedStatus,foldersEng,titles,Alldata,dayOfAnalysis,logger):
    dateOfAnalysis = dayOfAnalysis
    ExcelDir = os.path.join(os.path.dirname(fileToAnalyze),'..','Excel')
    bd = pd.read_excel(os.path.join(ExcelDir,fileToAnalyze.split(os.sep)[-1][:-4] + '.xlsx'))

    # TODO make generic
    for title in ['Expected Date_parsed','Date 1st Issue_parsed','Expected Approval Date_parsed','Approval Date_parsed']:
        for i in range(len(bd)):
            if bd.loc[i,title] == '--':
                bd.loc[i,title] = date(2050,1,1)
            else:
                bd.loc[i,title] = date(bd.loc[i,title].year,bd.loc[i,title].month,bd.loc[i,title].day)

    #print(bd[bd['Folder'].isin(foldersEng)]['Responsible'])
    responsibles = list(set(bd[bd['Folder'].isin(foldersEng)]['Responsible']))
    logger.info('responsibles: {}'.format(responsibles))
    for r in responsibles:
        count = len(bd[(bd['Folder'].isin(foldersEng)) & (bd['Responsible'] == r)])
        logger.info('responsible: {}, number of documents {}'.format(r,count))
        if count == 0:
            responsibles.remove(r)
    responsibles.sort()
    logger.info('responsibles: {}'.format(responsibles))

    workFlowStatus = list(set(bd['Workflow State']))
    for s in workFlowStatus:
        if not issubclass(type(s),str):
            workFlowStatus.remove(s)
            logger.info('workflow status {} not a string'.format(s))
    workFlowStatus.sort()
    
    areas = []
    for r in responsibles:
        areas.append(list(set(bd[bd['Responsible'] == r]['AREA'])))

    subcategories = []
    for i in range(len(responsibles)):
        logger.info(responsibles[i])
        subCategoriesArea = []
        for j in range(len(areas[i])):
            logger.info(areas[i][j])
            subCategoriesAreaJRespI = list(set(bd[(bd['Responsible'] == responsibles[i]) & (bd['AREA'] == areas[i][j]) & (bd['Folder'].isin(foldersEng))]['SUBCATEGORY']))
            logger.info(subCategoriesAreaJRespI)
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
        firstExpDate = bd[(bd['Responsible'] == data[i][0]) & (bd['AREA'] == data[i][1]) & (bd['SUBCATEGORY'] == data[i][2]) & bd['Folder'].isin(foldersEng)]['Expected Date_parsed'].min()
        lastExpDate = bd[(bd['Responsible'] == data[i][0]) & (bd['AREA'] == data[i][1]) & (bd['SUBCATEGORY'] == data[i][2]) & bd['Folder'].isin(foldersEng)]['Expected Date_parsed'].max()

        data[i].extend([t,e,r,ae,ar])
        data[i].extend(wStatus)
        data[i].extend([firstExpDate,lastExpDate])


    h = ['RESP','AREA','SUBCAT','TOTAL','ISS EXP','ISS REAL','APP EXP','APP REAL'] 
    h.extend(workFlowStatus)
    h.extend(['1stExpDate','LastExpDate'])
    #print(tabulate(data,headers=h,tablefmt="grid"))
    dataPd = pd.DataFrame(data,columns=h)
    #Subtotal per RESP
    h.pop(h.index('RESP'))
    h.pop(h.index('AREA'))
    h.pop(h.index('SUBCAT'))
    h.pop(h.index('1stExpDate'))
    h.pop(h.index('LastExpDate'))

    for r in responsibles:
        newLine =	{'RESP': r + ' (SUM)', 'AREA': 'SUBTOTAL', 'SUBCAT': 'SUBTOTAL'}
        for col in h:
            newLine[col] = dataPd[dataPd['RESP'] == r][col].sum()
        
        newLine['1stExpDate'] = '--'
        newLine['LastExpDate'] = '--'
        
        dataPd.loc[len(dataPd)] = newLine
    
    #Clean Issued For Construction_ state
    if 'Issued For Construction_' in h:
        logger.info('Issued For Construction_ found!!')
        if 'Issued For Construction' in h:
            dataPd['Issued For Construction'] = dataPd['Issued For Construction'] + dataPd['Issued For Construction_']
        else:
            dataPd['Issued For Construction'] = dataPd['Issued For Construction_']  
            h.append('Issued For Construction')
        dataPd.drop('Issued For Construction_',axis=1,inplace=True)
        h.remove("Issued For Construction_")
    
    columns = list(dataPd.columns.values)
    columns.remove('1stExpDate')
    columns.remove('LastExpDate')

    columns.append('1stExpDate')
    columns.append('LastExpDate')

    dataPd = dataPd[columns]
    
    dataPd.sort_values(by=['RESP','AREA','SUBCAT'],inplace=True)
    dataPd = dataPd.reset_index(drop=True)
    #print(dataPd)
    dataPd.to_excel(os.path.join(ExcelDir,'SubCategoryPlan_{:04d}_{:02d}_{:02d}_{}_{}.xlsx'.format(dateOfAnalysis.year,dateOfAnalysis.month,dateOfAnalysis.day,project,disciplina)))
    titles.extend(['per AREA and SUBCATEGORY'])
    Alldata.extend([dataPd])
    return titles, Alldata

def parsePlanDir(dir,logger):
    files = os.listdir(dir)
    for f in files:
        if isfile(os.path.join(dir,f)) and f[-3:] == 'csv':
            if (f[0:4] == '2024') or (f[0:4] == '2025'):
                continue
            else:
                y,m,d = parseDateInPlanFile(os.path.join(dir,f),logger)
                logger.info('remaning: {} to {}'.format(f,y+m+d+'_'+f))
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

    weightIssued = 0.7
    weightApproved = 0.3

    dir = os.path.join(dirProject,'00_ProjectReports')
    if not os.path.exists(dir):
        os.makedirs(dir)

    items = ['TOTAL','ISSUED EXPECTED','ISSUED REAL','ISSUED REAL FROM EXPECTED','APPROVED EXPECTED','APPROVED REAL','TOTAL EXPECTED [%]','TOTAL REAL [%]']
    columns = ['CIVIL','ELECTRICAL','ELECTROMECHANICAL','EQUIPMENT','SUM','SUM [%]']

    # ini :
    iniData = {
        'ITEM': items,
        'CIVIL': [0 for i in items],
        'ELECTRICAL': [0 for i in items],
        'ELECTROMECHANICAL': [0 for i in items],
        'EQUIPMENT': [0 for i in items],
        'SUM': [0 for i in items],
        'SUM [%]': [0 for i in items],
    }
    totalDF = pd.DataFrame(iniData)
    disciplinesDF = []

    # Calc of pos of lines
    # total of docs
    totalDocs = items.index('TOTAL')
    # total expected [%] line
    totalExp = items.index('TOTAL EXPECTED [%]')
    # total real [%] line
    totalReal = items.index('TOTAL REAL [%]')
    # issued expected [numDocs] line
    issuedExp = items.index('ISSUED EXPECTED')
    # approved expected [numDocs] line
    appExp = items.index('APPROVED EXPECTED')
    # issued real [numDocs] line
    issuedReal = items.index('ISSUED REAL')
    # approved real [numDocs] line
    appReal = items.index('APPROVED REAL')

    for d in disciplines:
        subDir = os.path.join(dirProject,d,'Excel')
        text = 'FolderPlan_{:04d}_{:02d}_{:02d}_{}_{}_Total.xlsx'.format(dayOfAnalysis.year,dayOfAnalysis.month,dayOfAnalysis.day,projectFullName,d)
        files = os.listdir(subDir)
        file = None
        try:
            idx_file = files.index(text)
            file = os.path.join(subDir,files[idx_file])        
        except:
            # File not found
            continue
            
        if file:
            #long_file = os.path.join(subDir,file)
            totalDiscipline = pd.read_excel(file)

            if len(totalDiscipline) != 6:
                totalDiscipline.loc[5] = totalDiscipline.loc[4]
                totalDiscipline.loc[4] = totalDiscipline.loc[3]
                totalDiscipline.loc[3] = [0 for i in totalDiscipline.columns]

            if  (projectFullName in projectsWithSUP) & (d.find('SUP') != -1):
                newTotalDiscipline = pd.DataFrame(iniData)
                for i in range(len(newTotalDiscipline)-2): # for lines total, issuedExp,issuedExpFromReal, issuedReal, appExp, appReal sum of all equipment folder to equipment category to std format // all lines except last 2
                    newTotalDiscipline.loc[i,'EQUIPMENT'] = totalDiscipline.loc[i,'SUM']
                    newTotalDiscipline.loc[i,'SUM'] = totalDiscipline.loc[i,'SUM']
                    if i !=0:
                        newTotalDiscipline.loc[i,'SUM [%]'] =  100 * newTotalDiscipline.loc[i,'SUM'] / newTotalDiscipline.loc[0,'SUM']

                # calc of total expected in column EQUIPMENT
                newTotalDiscipline.loc[totalExp,'EQUIPMENT'] = 100 * (newTotalDiscipline.loc[issuedExp,'EQUIPMENT'] * weightIssued + newTotalDiscipline.loc[appExp,'EQUIPMENT'] * weightApproved) / newTotalDiscipline.loc[totalDocs,'EQUIPMENT']
                # calc of total real in column EQUIPMENT
                newTotalDiscipline.loc[totalReal,'EQUIPMENT'] = 100 * (newTotalDiscipline.loc[issuedReal,'EQUIPMENT'] * weightIssued + newTotalDiscipline.loc[appReal,'EQUIPMENT'] * weightApproved) / newTotalDiscipline.loc[totalDocs,'EQUIPMENT']

                # calc of total expected in column SUM [%]
                newTotalDiscipline.loc[totalExp,'SUM [%]'] = float(newTotalDiscipline.loc[issuedExp,'SUM [%]']) * weightIssued + float(newTotalDiscipline.loc[appExp,'SUM [%]']) * weightApproved
                # calc of total real in column SUM [%]
                newTotalDiscipline.loc[totalReal,'SUM [%]'] = float(newTotalDiscipline.loc[issuedReal,'SUM [%]']) * weightIssued + float(newTotalDiscipline.loc[appReal,'SUM [%]']) * weightApproved

                newTotalDiscipline['DISCIP'] = d
                disciplinesDF.append(newTotalDiscipline)
                    
            else:
                totalDiscipline = totalDiscipline.drop(columns=totalDiscipline.columns[0])
                totalDiscipline.loc[len(totalDiscipline),'ITEM'] = 'TOTAL EXPECTED [%]'
                totalDiscipline.loc[len(totalDiscipline),'ITEM'] = 'TOTAL REAL [%]'
                for i in range(len(columns)-2): # all of the COLUMNS less SUM and SUM  [%]
                    if totalDiscipline.loc[totalDocs,columns[i]] != 0:
                        totalDiscipline.loc[totalExp,columns[i]] = 100 * (totalDiscipline.loc[issuedExp,columns[i]] * weightIssued + totalDiscipline.loc[appExp,columns[i]] * weightApproved) / totalDiscipline.loc[totalDocs,columns[i]]
                        totalDiscipline.loc[totalReal,columns[i]] = 100 * (totalDiscipline.loc[issuedReal,columns[i]] * weightIssued + totalDiscipline.loc[appReal,columns[i]] * weightApproved) / totalDiscipline.loc[totalDocs,columns[i]]
                totalDiscipline.loc[totalExp,'SUM [%]'] = float(totalDiscipline.loc[issuedExp,'SUM [%]']) * weightIssued + float(totalDiscipline.loc[appExp,'SUM [%]']) * weightApproved
                totalDiscipline.loc[totalReal,'SUM [%]'] = float(totalDiscipline.loc[issuedReal,'SUM [%]']) * weightIssued + float(totalDiscipline.loc[appReal,'SUM [%]']) * weightApproved
                totalDiscipline['DISCIP'] = d

                disciplinesDF.append(totalDiscipline)

            #if  (projectFullName in projectsWithSUP) & (d.find('SUP') != -1):
                ##print('project with SUP', projectFullName)
                ##for f in folderSup[projectFullName]:
                    ##try:
                        ##totalDF['EQUIPMENT'] += totalDiscipline[f]
                    ##except:
                        ##for j in range(len(totalDiscipline)):
                            ##totalDF.loc[j,'EQUIPMENT'] += 0
            #else:
            if  (projectFullName in projectsWithSUP) & (d.find('SUP') != -1):
                totalDF['EQUIPMENT'] += newTotalDiscipline['EQUIPMENT']
            else:
                totalDF['EQUIPMENT'] += totalDiscipline['EQUIPMENT']
                totalDF['CIVIL'] += totalDiscipline['CIVIL']
                totalDF['ELECTRICAL'] += totalDiscipline['ELECTRICAL']
                totalDF['ELECTROMECHANICAL'] += totalDiscipline['ELECTROMECHANICAL']
    
    if len(disciplinesDF) !=0: # if day not found create a empty data set
        allDiscDF = pd.concat(disciplinesDF,axis=0,ignore_index=True)
        allDiscDF.to_excel(os.path.join(dir,'{:04d}{:02d}{:02d}_totalsPerDiscipline_{}.xlsx'.format(dayOfAnalysis.year,dayOfAnalysis.month,dayOfAnalysis.day,projectFullName)))
    else:
        allDiscDF = pd.DataFrame(iniData)

    
    totalDF['SUM'] = totalDF['CIVIL'] + totalDF['ELECTRICAL'] + totalDF['ELECTROMECHANICAL'] + totalDF['EQUIPMENT']
    for i in range(1,len(totalDF)):
        if totalDF.loc[0,'SUM'] == 0:
            totalDF.loc[1,'SUM [%]'] = 0
        else:
            totalDF.loc[i,'SUM [%]'] = 100 * totalDF.loc[i,'SUM'] / totalDF.loc[0,'SUM']
    
    # calculate total expected per category, ( 0.7 * issued exp (line 1) + 0.3 * approved expected (line 3) ) / total (line 0)
    # calculate total real per category, ( 0.7 * issued real (line 1) + 0.3 * approved real (line 3) ) / total (line 0)

    for i in range(len(columns)-2): # all of the COLUMNS less SUM and SUM  [%]
        if totalDF.loc[totalDocs,columns[i]] != 0:
            totalDF.loc[totalExp,columns[i]] = round(100 * (totalDF.loc[issuedExp,columns[i]] * weightIssued + totalDF.loc[appExp,columns[i]] * weightApproved) / totalDF.loc[totalDocs,columns[i]],2)
            totalDF.loc[totalReal,columns[i]] = round(100 * (totalDF.loc[issuedReal,columns[i]] * weightIssued + totalDF.loc[appReal,columns[i]] * weightApproved) / totalDF.loc[totalDocs,columns[i]],2)

    totalDF.loc[totalExp,'SUM [%]'] = totalDF.loc[issuedExp,'SUM [%]'] * weightIssued + totalDF.loc[appExp,'SUM [%]'] * weightApproved
    totalDF.loc[totalReal,'SUM [%]'] = totalDF.loc[issuedReal,'SUM [%]'] * weightIssued + totalDF.loc[appReal,'SUM [%]'] * weightApproved
    
    totalDF['SUM [%]'] = totalDF['SUM [%]'].apply(lambda x : round(x,2))

    totalDF.to_excel(os.path.join(dir,'{:04d}{:02d}{:02d}_TOTAL_{}.xlsx'.format(dayOfAnalysis.year,dayOfAnalysis.month,dayOfAnalysis.day,projectFullName)))
    
    return totalDF, allDiscDF

