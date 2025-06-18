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
import pdf_export_general_rep as expGen
import platform


def configure_logging(project,d):
    log_filename = 'log_{}_{}.log'.format(project,os.path.split(d)[1])
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
    if 'EXE' in os.path.split(d)[0]:
        disciplineName = 'EXE_'+ os.path.split(d)[1]
    else:
        disciplineName = 'DEV_'+ os.path.split(d)[1]

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

    subDir = os.path.join(project,d,'00_GEN','04_PLN','02_REP','INPUT')
    subDirOutput= os.path.join(project,d,'00_GEN','04_PLN','02_REP','OUTPUT')
    bck.parsePlanDir(subDir,logger)
    file, dayOfAnalysis = bck.chooseFile(subDir)

    if  (projectFullName in projectsWithSUP) & (d.find('SUP') != -1):
        logger.info('project with SUP {}'.format(projectFullName))
        folders = folderSup[projectFullName]
    else:
        folders = foldersEng

    logger.info('{}: Analyze File Start'.format(d))
    start = timer()
    titles, data, engReportFileTitle = bck.analyzeFile(file,subDirOutput,approvedStatus,folders,foldersQA,projectFullName,projectsAcroName[projectFullName],disciplineName,dayOfAnalysis,logger)
    logger.info('{}: Analyze File Finish: {:.2f} s'.format(d,timer()-start))

    report = engReportFileTitle

    logger.info('{}: Analyze Responsables and Categories Start'.format(d))
    start = timer()
    titles, data = bck.analyzeRespAndCat(file,projectFullName,disciplineName,approvedStatus,folders,titles,data,dayOfAnalysis,logger)
    logger.info('{}: Analyze Resp and Cat Finish: {:.2f} s'.format(d,timer()-start))

    logger.info('{}: Scurve Start'.format(d))
    start = timer()
    scurvePath = scurve.drawFull(file,projectFullName,disciplineName,dayOfAnalysis,folders,approvedStatus,logger)
    logger.info('{}: SCurve Finish: {:.2f} s'.format(d,timer()-start))

    logger.info('{}: OutputRev Start'.format(d))
    start = timer()
    oePending, contractorPending, bd = out.reviewOutput(subDirOutput,folders,approvedStatus,dayOfAnalysis,logger,projectFullName,disciplineName)
    data.extend([oePending,contractorPending])
    titles.extend(['OE analysis','Contractor pending'])
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
    disciplinePath = os.path.join('02_EXE','02_ENG',disciplinesContractors[projectsAcroName[projectFullName]][0])
    
    subDir = os.path.join(project,disciplinePath,'00_GEN','04_PLN','02_REP','INPUT')
    dayOfAnalysis = bck.chooseFile(subDir)[1]
    projectsWithSUP = gen.generalInfo()[4]
    if (projectFullName in projectsWithSUP):
        folderSup = gen.generalInfo()[5][projectFullName]
    else:
        folderSup = []
    foldersEng = gen.colaborativoInformation()[1]
    approvedStatus = gen.colaborativoInformation()[0]

    dataOfProject,disciplinesDF = bck.genReportPerProject(project,disciplinesContractors[projectsAcroName[projectFullName]],projectFullName,dayOfAnalysis,foldersEng,folderSup,projectsWithSUP)
    projectScurve = scurve.drawProject(dayOfAnalysis,project,disciplinesContractors[projectsAcroName[projectFullName]],projectFullName,foldersEng,folderSup,projectsWithSUP,approvedStatus)
    projectData = (dataOfProject,disciplinesDF,projectScurve,dayOfAnalysis)

    print('finish analysis full project {} in {:.2f} s'.format(projectFullName,timer()-start))

    return projectData

if __name__ == "__main__":

    iniTime = timer()

    # update folder location based on computer u r at
    location = platform.node()

    # folder path por projects and folder to save information
    projectsOrigin, projectsDict, saveDir, projects_rep_Dir = gen.whichPath(gen.where(location))

    # let the user decide which project analyze
    projectsFullName = gen.generalInfo()[0]
    projectsAcroName = gen.generalInfo()[1]
    disciplinesEXE = gen.generalInfo()[6]
    disciplinesDEV = gen.generalInfo()[7]
    print('disciplinesDEV',disciplinesDEV)
    disciplinesContractors = gen.generalInfo()[3]

    listAcroNames = list(projectsAcroName.values())
    listAcroNames.extend(['ALL'])

    projToAnalyze = input('\nWhich projects do you want to analyze {}:\n'.format(listAcroNames))
    projToAnalyze = projToAnalyze.upper()
    print('\nInput received:',projToAnalyze)
    print('\n')

    # if no all projects modify list of projects folder and projectsFullName 
    if projToAnalyze != 'ALL':
        projects = [projectsDict[projToAnalyze]]
        projectsFullName = [list(projectsAcroName.keys())[list(projectsAcroName.values()).index(projToAnalyze)]]
    
    print('projects',projects)
    print('projectsFullName',projectsFullName)
    
    condensedProjectInformation = []

    for i in range(len(projectsFullName)):
        for j in range(len(disciplinesDEV[projectsAcroName[projectsFullName[i]]])):
            discip = os.path.join('01_DEV','02_ENG',disciplinesDEV[projectsAcroName[projectsFullName[i]]][j])
            condensedProjectInformation.append((projects[i],projectsFullName[i],discip))

        for j in range(len(disciplinesEXE[projectsAcroName[projectsFullName[i]]])):
            discip = os.path.join('02_EXE','02_ENG',disciplinesEXE[projectsAcroName[projectsFullName[i]]][j])
            condensedProjectInformation.append((projects[i],projectsFullName[i],discip))

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

    print('Pdf Reports finished in {:.2f} min'.format((timer() - iniTime)/60))

    # for the general report, the project has to have subcontractors disciplines (no preexec)
    projectsWithSubcontractors = False

    if projToAnalyze != 'ALL':
        if len(disciplinesContractors[projectsAcroName[projectsFullName[0]]]) == 0:
            print('project with no subContractor disciplines')
        else:
            projectsWithSubcontractors = True
    else:
        projectsWithSubcontractors = True

    if projectsWithSubcontractors == True: 
        condensedData = []
        for i in range(len(projectsFullName)):
            if len(disciplinesContractors[projectsAcroName[projectsFullName[i]]]) != 0:
                condensedData.append((projects[i],projectsFullName[i]))

        with multiprocessing.Pool() as pool:
            # generalAnalysisContractorProjects returns sum of all data of the project, data of the contractor disciplines, scurve image path and dayOfAnalysis
            projectGenData = pool.map(generalAnalysisContractorProjects,condensedData)
    
        expGen.pdfExport_generalReport(condensedData,projectGenData)
    
        for i,data in enumerate(projectGenData):
            print(condensedData[i][1])
            print('\n')
            print(data[0])
            print('\n')
            print(data[1])
            print('\n')

    print('Script finished in {:.2f} min'.format((timer() - iniTime)/60))
    