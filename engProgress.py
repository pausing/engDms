import backend as bck
import os
import pandas as pd
import scurve
import shutil
import outputRev as out
import pdfExport
from timeit import default_timer as timer

planDirBESSMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/docTO/TO/Chile/01_BDD/02_EXE/03_ENG/00_Planning'
planDirSHAMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/docTO/TO/Colombia/05_SHA/02_EXE/03_ENG/00_Planning'
planDirLCMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/docTO/TO/Brazil/05_LC/02_EXE/03_ENG/00_Planning'
planDirDRAMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/docTO/TO/Brazil/10_DRA/02_EXE/03_ENG/00_Planning'
planDirESTMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/docTO/TO/Chile/07_EST/02_EXE/03_ENG/00_Planning'
planDirCAMMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/docTO/TO/Colombia/06_CAM/02_EXE/03_ENG/00_Planning'

saveDirMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/Documentos/02_INGENIERIA/07_ProjReport'
projectsMac = [planDirBESSMac,planDirSHAMac,planDirLCMac,planDirDRAMac,planDirESTMac,planDirCAMMac]

planDirBESSPC = 'C:\\Users\\pauma\\OneDrive - AtlasRen\\docTO\\TO\\Chile\\01_BDD\\02_EXE\\03_ENG\\00_Planning'
planDirSHAPC = 'C:\\Users\\pauma\\OneDrive - AtlasRen\\docTO\\TO\\Colombia\\05_SHA\\02_EXE\\03_ENG\\00_Planning'
planDirLCPC = 'C:\\Users\\pauma\\OneDrive - AtlasRen\\docTO\\TO\\Brazil\\05_LC\\02_EXE\\03_ENG\\00_Planning'
planDirDRAPC = 'C:\\Users\\pauma\\OneDrive - AtlasRen\\docTO\\TO\\Brazil\\10_DRA\\02_EXE\\03_ENG\\00_Planning'
planDirESTPC = 'C:\\Users\\pauma\\OneDrive - AtlasRen\\docTO\\TO\\Chile\\07_EST\\02_EXE\\03_ENG\\00_Planning'
planDirCAMPC = 'C:\\Users\\pauma\\OneDrive - AtlasRen\\docTO\\TO\\Colombia\\06_CAM\\02_EXE\\03_ENG\\00_Planning'

saveDirPC = 'C:\\Users\\pauma\\OneDrive - AtlasRen\\Documentos\\02_INGENIERIA\\07_ProjReport'
projectsPC = [planDirBESSPC,planDirSHAPC,planDirLCPC,planDirDRAPC,planDirESTPC,planDirCAMPC]

planDirBESSLap = 'C:\\Users\\PabloMaqueda\\OneDrive\\OneDrive - AtlasRen\\docTO\\TO\\Chile\\01_BDD\\02_EXE\\03_ENG\\00_Planning'
planDirSHALap = 'C:\\Users\\PabloMaqueda\\Onedrive\\OneDrive - AtlasRen\\docTO\\TO\\Colombia\\05_SHA\\02_EXE\\03_ENG\\00_Planning'
planDirLCLap = 'C:\\Users\\PabloMaqueda\\Onedrive\\OneDrive - AtlasRen\\docTO\\TO\\Brazil\\05_LC\\02_EXE\\03_ENG\\00_Planning'
planDirDRALap = 'C:\\Users\\PabloMaqueda\\Onedrive\\OneDrive - AtlasRen\\docTO\\TO\\Brazil\\10_DRA\\02_EXE\\03_ENG\\00_Planning'
planDirESTLap = 'C:\\Users\\PabloMaqueda\\Onedrive\\OneDrive - AtlasRen\\docTO\\TO\\Chile\\07_EST\\02_EXE\\03_ENG\\00_Planning'
planDirCAMLap = 'C:\\Users\\PabloMaqueda\\Onedrive\\OneDrive - AtlasRen\\docTO\\TO\\Colombia\\06_CAM\\02_EXE\\03_ENG\\00_Planning'

saveDirLap = 'C:\\Users\\PabloMaqueda\\Onedrive\\OneDrive - AtlasRen\\Documentos\\02_INGENIERIA\\07_ProjReport'
projectsLap = [planDirBESSLap,planDirSHALap,planDirLCLap,planDirDRALap,planDirESTLap,planDirCAMLap]

projectsFullName = ['BESS DEL DESIERTO','SHANGRILA','LUIZ CARLOS','DRACO','ESTEPA','CAMPANO']

projectsAcroName = {
    'BESS DEL DESIERTO':'BDD',
    'SHANGRILA':'SHA',
    'LUIZ CARLOS':'LC',
    'DRACO':'DRA',
    'ESTEPA':'EST',
    'CAMPANO':'CAM',
}

disciplines = {
    'BDD':['01_BESS','02_HV_SDD','03_EE_INT'],
    'SHA':['01_PV','02_HV','03_LT'],
    'LC':['01_PV AREA A','02_PV AREA B','03_HV','04_LT','05_SUP'],
    'DRA':['01_PV-PRE EXEC','03_PV','04_HV','05_SUP'],
    'EST':['01_PV-PRE EXEC','02_HV-PRE EXEC','03_BESS-PRE EXEC','04_EWA-PV','06_HV','08_SUP'],
    'CAM':['02_PV_PRE_EXEC'],
}

disciplinesContractors = {
    'BDD':['01_BESS','02_HV_SDD','03_EE_INT'],
    'SHA':['01_PV','02_HV','03_LT'],
    'LC':['01_PV AREA A','02_PV AREA B','03_HV','04_LT','05_SUP'],
    'DRA':['03_PV','04_HV','05_SUP'],
    'EST':['06_HV','08_SUP'],
    'CAM':[],
}

approvedStatus = ['Compliant','Compliant with comments','Issued For Construction','Issued For Construction_','Pre analysis','Ready for as built'] 
foldersEng = ['CIVIL','ELECTRICAL','ELECTROMECHANICAL','EQUIPMENT']
# subFolder for disciplines 05_SUP: LC,DRACO
# projects with discipline SUP

projectsWithSUP = ['LUIZ CARLOS','DRACO','ESTEPA']
folderSup = {
    'LUIZ CARLOS':['CHINT','JINKO','NEXTRACKER','STI','SUNGROW','WEG'],
    'DRACO':['TRACKERS','INVERTERS','MODULES','POWER_TRANSFORMERS'],
    'ESTEPA':['INVERTERS','MODULES','POWER_TRANSFORMERS','TRACKERS'],
}
foldersQA = ['CONFORMITY','PROCEDURE']

# where are u?
where = input('\nWhere r u [mac,pc,lap]:\n')
print('\nInput received:',where)
print('\n')

if where == 'mac':
    projects = projectsMac
    projecstDict = dict(zip(list(projectsAcroName.values()),projectsMac))
    saveDir = saveDirMac
elif where == 'pc':
    projects = projectsPC
    projecstDict = dict(zip(list(projectsAcroName.values()),projectsPC))
    saveDir = saveDirPC
elif where == 'lap':
    projects = projectsLap
    projecstDict = dict(zip(list(projectsAcroName.values()),projectsLap))
    saveDir = saveDirLap

# let the user decide which project analyze
listAcroNames = list(projectsAcroName.values())
listAcroNames.extend(['ALL'])

projToAnalyze = input('\nWhich projects do you want to analyze {}:\n'.format(listAcroNames))
projToAnalyze = projToAnalyze.upper()
print('\nInput received:',projToAnalyze)
print('\n')

# if no all projects modify list of projects folder and projectsFullName 
if projToAnalyze != 'ALL':
    projects = [projecstDict[projToAnalyze]]
    projectsFullName = [list(projectsAcroName.keys())[list(projectsAcroName.values()).index(projToAnalyze)]]

print(projects)
print(projectsFullName)

reports = []
projectData = []
projectDataPerDisciplines = []
projectScurve = []
iniTime = timer()

for j,p in enumerate(projects):
    print('----')
    print(projectsFullName[j])
    print('----')

    for d in disciplines[projectsAcroName[projectsFullName[j]]]:
        print('----')
        print(projectsFullName[j] + ' //// ' + d)
        print('----')

        subDir = os.path.join(p,d,'Input')
        subDirOutput = os.path.join(p,d,'Output')
        bck.parsePlanDir(subDir)
        file, dayOfAnalysis = bck.chooseFile(subDir)

        if  (projectsFullName[j] in projectsWithSUP) & (d.find('SUP') != -1):
            print('project with SUP', projectsFullName[j])
            folders = folderSup[projectsFullName[j]]
        else:
            folders = foldersEng

        start = timer()
        print('\n----------- Analyze File Start\n')
        start = timer()
        start = timer()
        titles, data, engReportFileTitle = bck.analyzeFile(file,subDirOutput,approvedStatus,folders,foldersQA,projectsFullName[j],projectsAcroName[projectsFullName[j]],d,dayOfAnalysis)
        print('\n----------- Analyze File Finish: {:.2f} s\n'.format(timer()-start))

        reports.append(engReportFileTitle)

        start = timer()
        print('\n----------- Analyze Resp and Cat Start\n')
        titles, data = bck.analyzeRespAndCat(file,projectsFullName[j],d,approvedStatus,folders,titles,data,dayOfAnalysis)
        print('\n----------- Analyze Resp and Cat Finish: {:.2f} s\n'.format(timer()-start))

        start = timer()
        print('\n----------- SCurve Start\n')
        scurvePath = scurve.drawFull(file,projectsFullName[j],d,dayOfAnalysis,folders,approvedStatus)
        print('\n----------- SCurve Finish: {:.2f} s\n'.format(timer()-start))

        start = timer()
        print('\n----------- OutputRev Start\n')
        data.extend([out.reviewOutput(subDirOutput,foldersEng,approvedStatus,dayOfAnalysis)[0]])
        titles.extend(['OE analysis'])
        print('\n----------- OutputRev Finish: {:.2f} s\n'.format(timer()-start))

        start = timer()
        print('\n----------- ExportPDF Start\n')
        bck.pdfExport.exportToPDF('Engineering Report {}, date: {}-{:02d}-{:02d}'.format(projectsFullName[j],dayOfAnalysis.year,dayOfAnalysis.month,dayOfAnalysis.day),titles,data,engReportFileTitle,scurvePath)
        print('----------- ExportPDF Finish: {:.2f} s\n'.format(timer()-start))

    if len(disciplinesContractors[projectsAcroName[projectsFullName[j]]]) != 0:
        dataOfProject,disciplinesDF = bck.genReportPerProject(p,disciplinesContractors[projectsAcroName[projectsFullName[j]]],projectsFullName[j],dayOfAnalysis,foldersEng,folderSup,projectsWithSUP)
        projectData.extend([dataOfProject])
        projectDataPerDisciplines.extend([disciplinesDF])
        projectScurve.extend([scurve.drawProject(dayOfAnalysis,p,disciplinesContractors[projectsAcroName[projectsFullName[j]]],projectsFullName[j],foldersEng,folderSup,projectsWithSUP,approvedStatus)])

for i in range(len(projects)):
    print('\n')
    print(projectsFullName[i])
    print(disciplinesContractors[projectsAcroName[projectsFullName[i]]])
    if len(disciplinesContractors[projectsAcroName[projectsFullName[i]]]) != 0:
        print('\n')
        print(projectData[i])
        print('\n')
        print(projectDataPerDisciplines[i])
        print('\n')
    else:
        print('\nNo contractors in this project\n')

for i,r in enumerate(reports):
    completeDir = r
    fileName = completeDir.split(os.sep)[-1]
    print('{:02d}'.format(i+1),fileName)
    try:
        shutil.copy(r,os.path.join(saveDir,fileName))
    except Exception as e:
        print('Error {}, file: {}'.format(e,fileName))

print('Script finished in {:.2f} min'.format((timer() - iniTime)/60))
