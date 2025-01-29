import pandas as pd
import platform
import general as gen
from datetime import datetime,timedelta,date
import os
import backend as bck
import export_to_pdf_det_rep as exp

def in_out_files(excelFolder,outputFolder):

    filesExcelFolder = os.listdir(excelFolder)
    filesOutputFolder = os.listdir(outputFolder)

    while True:
        print('Day of analysis')
        print('1.- Today')
        print('2.- Especific day')
        choice = input('Select option: ')
        if choice == '1':
            today = date.today()
            dayOfAnalysis = '{:04d}{:02d}{:02d}'.format(today.year,today.month,today.day)
            break
        elif choice == '2':
            # TODO
            strDate = input('Insert date [YYYY-MM-DD]: ')
            dayOfAnalysis = strDate.replace('-','')
            break
        else:
            print('Invalid, try again.')
    
    for f in filesExcelFolder:
        if f[0:8] == dayOfAnalysis and f[-4:] == 'xlsx':
            inputFile = f
            break
    
    strToFind = 'output.csv'

    print(dayOfAnalysis)

    for f in filesOutputFolder:
        if f[0:8] == dayOfAnalysis and f[-(len(strToFind)):] == strToFind:
            outputFile = f
            break

    print(inputFile,outputFile)

    return inputFile, outputFile, dayOfAnalysis

def genDetReport(inFile,outFile,project,discipline,dayOfAnalysis):
    inDf = pd.read_excel(inFile)
    outDf = pd.read_csv(outFile)
    folders = gen.colaborativoInformation()[1]

    bck.parseTimeBD(outDf,'Last Issue Date','repDet')
    bck.parseTimeBD(outDf,'Replanned First Issue Date','repDet')

    outDf= outDf.drop('Expected First Issue Date',axis=1)
    outDf= outDf.drop('Replanned First Issue Date',axis=1)
    outDf= outDf.drop('Fisrt Issue Date',axis=1)
    outDf= outDf.drop('Last Issue Date',axis=1)
    outDf= outDf.drop('Expected Approval Date',axis=1)
    outDf= outDf.drop('Replanned Expected Approval',axis=1)
    outDf= outDf.drop('MDL Revision',axis=1)
    outDf= outDf.drop('Unnamed: 18',axis=1)
    outDf= outDf.drop('Approval Date',axis=1)
    outDf= outDf.drop('Item or Sequence',axis=1)
    for i in range(len(outDf)):
        outDf.loc[i,'Description'] = outDf.loc[i,'Description'][0:50]

    changeTitles = {
        'Contractor / Supplier':'RESP',
        'Replanned First Issue Date_parsed':'EXP ISS',
        'Last Issue Date_parsed':'LAST ISS',
        'Area': 'AREA',
        'Category': 'CAT',
        'Subcategory': 'SUBCAT',
        'Revision': 'REV'
    }
    outDf.rename(columns=changeTitles,inplace=True)

    docsEng = outDf[outDf['Folder'].isin(folders)]
    docsEng[docsEng['Status'] == 'Issued For Construction_']['Status'] = 'Issued For Construction'
    cols = ['RESP','Code','Description','REV','Status','AREA','CAT','SUBCAT','EXP ISS','LAST ISS']
    docsEng = docsEng[cols]

    # Docs not issued

    docsNoIssued = docsEng[docsEng['Status'].isnull()]
    #docsNoIssued.sort_values(by=['RESP','AREA','CAT','SUBCAT'],inplace=True)
    docsNoIssued.sort_values(by=['RESP','EXP ISS'],inplace=True)
    docsNoIssued = docsNoIssued.reset_index(drop=True)
    docsNoIssued['Status'] = '--'
    docsNoIssued['LAST ISS'] = '--'
    docsNoIssued['REV'] = '--'
    docsNoIssued.insert(0,'Item',range(1,len(docsNoIssued)+1),True)

    # Docs not approved

    statusToCheck = ['Non-compliant']
    docsNoApproved = docsEng[docsEng['Status'].isin(statusToCheck)]
    docsNoApproved.sort_values(by=['RESP','AREA','CAT','SUBCAT'],inplace=True)
    docsNoApproved = docsNoApproved.reset_index(drop=True)
    docsNoApproved.insert(0,'Item',range(1,len(docsNoApproved)+1),True)

    # Docs in revision

    statusToCheck = ['For Analysis','Pre analysis','For revision']
    docsinRev = docsEng[docsEng['Status'].isin(statusToCheck)]
    docsinRev.sort_values(by=['RESP','AREA','CAT','SUBCAT'],inplace=True)
    docsinRev = docsinRev.reset_index(drop=True)
    docsinRev.insert(0,'Item',range(1,len(docsinRev)+1),True)

    exp.pdfExport_repDet(docsNoIssued,docsNoApproved,docsinRev,project,discipline,dayOfAnalysis)


if __name__ == "__main__":
    
    # update folder location based on computer u r at
    location = platform.node()

    # folder path por projects and folder to save information
    dirProjects, projectsDict, saveDir = gen.whichPath(gen.where(location))

    # list of full name of projects
    projectsFullName = gen.generalInfo()[0]
    # dict of full name of projects: acro name
    projectsAcroName = gen.generalInfo()[1]

    listAcroNames = list(projectsAcroName.values())

    projToAnalyze = input('\nWhich projects do you want to analyze {}:\n'.format(listAcroNames))
    projToAnalyze = projToAnalyze.upper()
    print('\nInput received:',projToAnalyze)
    print('\n')

    projectFolder = projectsDict[projToAnalyze]
    projectFullName = list(projectsAcroName.keys())[list(projectsAcroName.values()).index(projToAnalyze)]
    
    disciplines = gen.generalInfo()[2]
    print(disciplines[projectsAcroName[projectFullName]])
    print('\nWhich discipline: ')

    while True:
        possibleChoices = []
        for i,d in enumerate(disciplines[projectsAcroName[projectFullName]]):
            print('{}.- {}'.format(i+1,d))
            possibleChoices.append(i+1)
        choice = input('Choose discipline: ')
        try:
            if int(choice) in possibleChoices:
                discipline = disciplines[projectsAcroName[projectFullName]][int(choice)-1]
                break
            else:
                print('Invalid, try again')
        except:
            print('Invalid, try again')
    
    inputFolder = os.path.join(projectFolder,discipline,'Excel')
    outputFolder = os.path.join(projectFolder,discipline,'Output')

    inFile, outFile, dayOfAnalysis = in_out_files(inputFolder,outputFolder)

    genDetReport(os.path.join(projectFolder,discipline,'Excel',inFile),os.path.join(projectFolder,discipline,'Output',outFile),projectFullName,discipline,dayOfAnalysis)
