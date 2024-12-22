import backend as bck
import os
import pandas as pd
import scurve
import shutil
import outputRev as out
import pdfExport
from timeit import default_timer as timer
import general as gen


# where are u?
where = input('\nWhere r u [mac,pc,lap]:\n')
print('\nInput received:',where)
print('\n')

projects = gen.whichPath(where)[0]
projecstDict = gen.whichPath(where)[1]
saveDir = gen.whichPath(where)[2]

# general information
projectsFullName = gen.generalInfo()[0]
projectsAcroName = gen.generalInfo()[1]
disciplines = gen.generalInfo()[2]
disciplinesContractors = gen.generalInfo()[3]
projectsWithSUP = gen.generalInfo()[4]
folderSup = gen.generalInfo()[3]

approvedStatus = gen.colaborativoInformation()[0]
foldersEng = gen.colaborativoInformation()[1]
foldersQA = gen.colaborativoInformation()[2]

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
