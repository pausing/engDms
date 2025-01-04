import backend as bck
import os
import pandas as pd
import scurve
import shutil
import outputRev as out
import pdfExport
from timeit import default_timer as timer
import general as gen
import multiprocessing
import logging

def configure_logging(project,d):
    log_filename = 'log_{}_{}.log'.format(project,d)
    logger = logging.getLogger(project)
    logger.setLevel(logging.INFO)
    # Create file handler for the worker's log file
    file_handler = logging.FileHandler(log_filename,mode='w')
    file_handler.setLevel(logging.INFO)
    # Define the log format
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    # Add the handler to the logger
    logger.addHandler(file_handler)
    return logger

def atlasdms(condesedInput):

    project, projectFullName, d = condesedInput

    logger = configure_logging(projectFullName,d)

    # general information
    projectsAcroName = gen.generalInfo()[1]
    disciplines = gen.generalInfo()[2]
    disciplinesContractors = gen.generalInfo()[3]
    projectsWithSUP = gen.generalInfo()[4]
    folderSup = gen.generalInfo()[5]

    approvedStatus = gen.colaborativoInformation()[0]
    foldersEng = gen.colaborativoInformation()[1]
    foldersQA = gen.colaborativoInformation()[2]

    startTotal = timer()
    print('start analysis project: {}, discipline: {}'.format(projectFullName,d))

    subDir = os.path.join(project,d,'Input')
    subDirOutput = os.path.join(project,d,'Output')
    bck.parsePlanDir(subDir,logger)
    file, dayOfAnalysis = bck.chooseFile(subDir)

    if  (projectFullName in projectsWithSUP) & (d.find('SUP') != -1):
        logger.info('project with SUP {}'.format(projectFullName))
        folders = folderSup[projectFullName]
    else:
        folders = foldersEng

    logger.info('{}: Analyze File Start'.format(d))
    start = timer()
    titles, data, engReportFileTitle = bck.analyzeFile(file,subDirOutput,approvedStatus,folders,foldersQA,projectFullName,projectsAcroName[projectFullName],d,dayOfAnalysis,logger)
    logger.info('{}: Analyze File Finish: {:.2f} s'.format(d,timer()-start))

    report = engReportFileTitle

    logger.info('{}: Analyze Responsables and Categories Start'.format(d))
    start = timer()
    titles, data = bck.analyzeRespAndCat(file,projectFullName,d,approvedStatus,folders,titles,data,dayOfAnalysis,logger)
    logger.info('{}: Analyze Resp and Cat Finish: {:.2f} s'.format(d,timer()-start))

    logger.info('{}: Scurve Start'.format(d))
    start = timer()
    scurvePath = scurve.drawFull(file,projectFullName,d,dayOfAnalysis,folders,approvedStatus)
    logger.info('{}: SCurve Finish: {:.2f} s'.format(d,timer()-start))

    logger.info('{}: OutputRev Start'.format(d))
    start = timer()
    data.extend([out.reviewOutput(subDirOutput,foldersEng,approvedStatus,dayOfAnalysis,logger)[0]])
    titles.extend(['OE analysis'])
    logger.info('{}: OutputRev Finish: {:.2f} s'.format(d,timer()-start))

    logger.info('{}: ExportPDF Start'.format(d))
    start = timer()
    bck.pdfExport.exportToPDF('Engineering Report {}, date: {}-{:02d}-{:02d}'.format(projectFullName,dayOfAnalysis.year,dayOfAnalysis.month,dayOfAnalysis.day),titles,data,engReportFileTitle,scurvePath,logger)
    logger.info('{}: ExportPDF Finish: {:.2f} s'.format(d,timer()-start))
    
    print('finish analysis project: {}, discipline: {} in {:.2f} s'.format(projectFullName,d,timer()-startTotal))

    return report

def generalAnalysisContractorProjects(information):

    start = timer()

    project, projectFullName = information

    print('start analysis full project {}'.format(projectFullName))

    projectsAcroName = gen.generalInfo()[1]
    disciplinesContractors = gen.generalInfo()[3]

    d = disciplinesContractors[projectsAcroName[projectFullName]][0]
    
    subDir = os.path.join(project,d,'Input')
    dayOfAnalysis = bck.chooseFile(subDir)[1]
    projectsWithSUP = gen.generalInfo()[4]
    folderSup = gen.generalInfo()[5]
    foldersEng = gen.colaborativoInformation()[1]
    approvedStatus = gen.colaborativoInformation()[0]

    if  (projectFullName in projectsWithSUP) & (d.find('SUP') != -1):
        folders = folderSup[projectFullName]
    else:
        folders = foldersEng

    dataOfProject,disciplinesDF = bck.genReportPerProject(project,disciplinesContractors[projectsAcroName[projectFullName]],projectFullName,dayOfAnalysis,foldersEng,folderSup,projectsWithSUP)
    projectScurve = scurve.drawProject(dayOfAnalysis,project,disciplinesContractors[projectsAcroName[projectFullName]],projectFullName,foldersEng,folderSup,projectsWithSUP,approvedStatus)
    projectData = (dataOfProject,disciplinesDF,projectScurve)

    print('finish analysis full project {} in {:.2f} s'.format(projectFullName,timer()-start))

    return projectData

if __name__ == "__main__":

    iniTime = timer()
    # where are u?
    where = input('\nWhere r u [mac,pc,lap]:\n')
    print('\nInput received:',where)
    print('\n')

    projects = gen.whichPath(where)[0]
    projecstDict = gen.whichPath(where)[1]
    saveDir = gen.whichPath(where)[2]

    # let the user decide which project analyze
    projectsFullName = gen.generalInfo()[0]
    projectsAcroName = gen.generalInfo()[1]
    disciplinesContractors = gen.generalInfo()[3]

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
    
    condensedProjectInformation = []
    disciplines = gen.generalInfo()[2]
    for i in range(len(projectsFullName)):
        for j in range(len(disciplines[projectsAcroName[projectsFullName[i]]])):
            condensedProjectInformation.append((projects[i],projectsFullName[i],disciplines[projectsAcroName[projectsFullName[i]]][j]))

    with multiprocessing.Pool() as pool:
        reports = pool.map(atlasdms,condensedProjectInformation)
    
    for i,r in enumerate(reports):
        completeDir = r
        fileName = completeDir.split(os.sep)[-1]
        print('{:02d}'.format(i+1),fileName)
        try:
            shutil.copy(r,os.path.join(saveDir,fileName))
        except Exception as e:
            print('Error {}, file: {}'.format(e,fileName))
        

    condensedData = []
    for i in range(len(projectsFullName)):
        if len(disciplinesContractors[projectsAcroName[projectsFullName[i]]]) != 0:
            condensedData.append((projects[i],projectsFullName[i]))

    with multiprocessing.Pool() as pool:
        projectGenData = pool.map(generalAnalysisContractorProjects,condensedData)
    
    for i,data in enumerate(projectGenData):
        print(condensedData[i][1])
        print('\n')
        print(data[0])
        print('\n')
        print(data[1])
        print('\n')

    print('Script finished in {:.2f} min'.format((timer() - iniTime)/60))
