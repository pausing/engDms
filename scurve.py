import backend as bck
import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime,timedelta,date
from timeit import default_timer as timer
import numpy as np

def draw(fileToAnalyze,project,disciplina,dateOfAnalysis):

    ExcelDir = os.path.join(os.path.dirname(fileToAnalyze),'..','Excel')
    bd = pd.read_excel(os.path.join(ExcelDir,fileToAnalyze.split(os.sep)[-1][:-4] + '.xlsx'))
    bck.parseTimeBD(bd,'Date 1st Issue', project + ' ' + disciplina)
    bck.parseTimeBD(bd,'Expected Date', project + ' ' + disciplina)
    bck.parseTimeBD(bd,'Expected Approval Date', project + ' ' + disciplina)
    bck.parseTimeBD(bd,'Approval Date', project + ' ' + disciplina)

    #minDate = min(list(bd['Expected Date_parsed']))
    #maxDate = max(list(bd['Expected Date_parsed']))
    minDate = date.today() - timedelta(30)
    maxDate = date.today() + timedelta(45)
    Folders = ['CIVIL','ELECTRICAL','ELECTROMECHANICAL','EQUIPMENT']
    maxVal = []
    for i in range(len(Folders)):
        maxVal.extend([0])

    dates = [minDate]
    difDays = maxDate - minDate

    for i in range(difDays.days+1):
        if i != 0:
            dates.extend([dates[i-1] + timedelta(1)])

    real = []
    planned = []
    colors = ['b','c','m','g']
    for f in Folders:
        realPerFolder = []
        plannedPerFolder = []
        for i in range(len(dates)):
            plannedPerFolder.extend([len(bd[(bd['Expected Date_parsed'] <= dates[i]) & (bd['Folder'] == f)])])
            realPerFolder.extend([len(bd[(bd['Date 1st Issue_parsed'] <= dates[i]) & (bd['Folder'] == f)])])
        real.extend([realPerFolder])
        planned.extend([plannedPerFolder])

    for i in range(len(Folders)):
        if maxVal[i] < planned[i][-1]:
            maxVal[i] = planned[i][-1]

    fig, ax = plt.subplots(2,2,figsize=[3*6.4,3*4.8])
    
    fig.suptitle('Planned vs Real {} {}'.format(project,disciplina),size='small')

    weeks = [-2,-1,1,2,3]
    days = [-7,-6,-5,-4,-3,-2,-1]

    for i in range(2):
        for j in range(2):
            ax[i,j].grid(True)
            ax[i,j].set_title(Folders[2*i+j],size='small')
            ax[i,j].tick_params(labelsize='x-small')
            ax[i,j].plot(dates,planned[2*i+j],colors[2*i+j]+'--',linewidth=1,label='{} planned'.format(Folders[2*i+j]))
            ax[i,j].plot(dates,real[2*i+j],colors[2*i+j],linewidth=1,label='{} real'.format(Folders[2*i+j]))
            realAtDateOfAnalysis = real[2*i+j][dates.index(dateOfAnalysis)]
            plannedAtDateOfAnalysis = planned[2*i+j][dates.index(dateOfAnalysis)]
            ax[i,j].annotate('[{}, Planned: {}]'.format(Folders[2*i+j],plannedAtDateOfAnalysis),(dateOfAnalysis,plannedAtDateOfAnalysis))
            ax[i,j].annotate('[{}, Issued: {}]'.format(Folders[2*i+j],realAtDateOfAnalysis),(dateOfAnalysis,realAtDateOfAnalysis))
            ax[i,j].plot([dateOfAnalysis,dateOfAnalysis],[0,maxVal[2*i+j]],'r',linewidth=1,label='Day Of Analysis!')
            for w in weeks:
                if w == -1:
                    ax[i,j].plot([dateOfAnalysis + timedelta(7*w),dateOfAnalysis + timedelta(7*w)],[0,maxVal[2*i+j]],'k--',linewidth=1,label='Week Intervals')
                else:
                    ax[i,j].plot([dateOfAnalysis + timedelta(7*w),dateOfAnalysis + timedelta(7*w)],[0,maxVal[2*i+j]],'k--',linewidth=1)
            for d in days:
                if d == -1:
                    ax[i,j].plot([dateOfAnalysis + timedelta(d),dateOfAnalysis + timedelta(d)],[0,maxVal[2*i+j]],'g--',linewidth=1,label='Day Intervals')
                else:
                    ax[i,j].plot([dateOfAnalysis + timedelta(d),dateOfAnalysis + timedelta(d)],[0,maxVal[2*i+j]],'g--',linewidth=1)
            ax[i,j].legend(loc='upper left',fontsize='small')
            ax[i,j].set_yticks(np.arange(0,maxVal[2*i+j],5))
    scurvePath = os.path.join(ExcelDir,'scurve {}_{}_{}_{}_{}.png'.format(project,disciplina,dateOfAnalysis.year,dateOfAnalysis.month,dateOfAnalysis.day))
    fig.savefig(scurvePath,bbox_inches='tight')
    plt.close(fig)

    return scurvePath

def approvedPerDay(day,files,approvedStatus,Folders,excelDir,logger):

    total = 'na'
    issuedPlanned = 'na'
    approvedPlanned = 'na'
    issuedReal = 'na'
    approvedReal = 'na'

    logger.info('start approvedPerDay')
    logger.info(day)
    logger.info('start searching for file')
    start = timer()
    dateString = '{:02d}{:02d}{:02d}'.format(day.year,day.month,day.day)
    f = [f for f in files if f.startswith(dateString) and 'planejamento' in f]
    logger.info('{}'.format(f))
    logger.info('finish seaching for file {:02f} s'.format(timer()-start))

    logger.info('start filtering and adding up')
    start = timer()

    if len(f) != 0:
        bd = pd.read_excel(os.path.join(excelDir,f[0]))
        bck.parseTimeBD(bd,'Date 1st Issue',f[0])
        bck.parseTimeBD(bd,'Expected Date',f[0])
        bck.parseTimeBD(bd,'Expected Approval Date',f[0])
        bdFiltered = bd[bd['Folder'].isin(Folders)]
        approvedReal = len(bdFiltered[(bdFiltered['Workflow State'].isin(approvedStatus))])
        total = len(bdFiltered)
        issuedPlanned = len(bdFiltered[(bdFiltered['Expected Date_parsed'].values <= day)])
        issuedReal = len(bdFiltered[(bdFiltered['Date 1st Issue_parsed'].values <= day)])
        approvedPlanned = len(bdFiltered[(bdFiltered['Expected Approval Date_parsed'].values <= day)])

    logger.info('finish filtering and adding up {:02f} s'.format(timer()-start))

    #for f in files:
        #if f[0:8] == '{:02d}{:02d}{:02d}'.format(day.year,day.month,day.day) and f.find('planejamento') != -1:
            ##print('reading ',f)
            #bd = pd.read_excel(os.path.join(excelDir,f))
            #bck.parseTimeBD(bd,'Date 1st Issue')
            #bck.parseTimeBD(bd,'Expected Date')
            #bck.parseTimeBD(bd,'Expected Approval Date')
            #bck.parseTimeBD(bd,'Approval Date')
            #approvedReal = len(bd[(bd['Workflow State'].isin(approvedStatus)) & (bd['Folder'].isin(Folders))])
            #total = len(bd[(bd['Folder'].isin(Folders))])
            #issuedPlanned = len(bd[(bd['Expected Date_parsed'] <= day) & (bd['Folder'].isin(Folders))])
            #issuedReal = len(bd[(bd['Date 1st Issue_parsed'] <= day) & (bd['Folder'].isin(Folders))])
            #approvedPlanned = len(bd[(bd['Expected Approval Date_parsed'] <= day) & (bd['Folder'].isin(Folders))])

            #break

    return total, issuedPlanned, approvedPlanned, issuedReal, approvedReal

def scurveGeneral(bd,minDate,maxDate,approvedStatus,excelDir,project,discipline,dateOfAnalysis,Folders,logger):

    maxVal = 110

    dates = [minDate]
    difDays = maxDate - minDate

    for i in range(difDays.days+1):
        if i != 0:
            dates.extend([dates[i-1] + timedelta(1)])

    # weights 
    weightIssued = 70
    weightApproved = 30

    # list of files sorted
    files = os.listdir(excelDir)
    files.sort()

    # 2 Scurves, 1 with the numbers of last report (except for approvals), 2 with numbers of each report at each day

    # calculation of Scurve1_ 
    Scurve1_total = []
    Scurve1_issuedReal = []
    Scurve1_issuedPlanned = []
    Scurve1_approvedPlanned = []
    Scurve1_approvedReal = []

    logger.info('start of scurve1')
    start = timer()


    bdFiltered = bd[bd['Folder'].isin(Folders)]

    # calculation of Scurve2_ : using for each day the current planning file (not the last)
    # SCurve2 = [total, issuedPlanned, approvedPlanned, issuedReal, issuedPlanned]

    Scurve2 = [[],[],[],[],[]]

    for i in range(len(dates)):
        Scurve1_total.extend([len(bdFiltered)])
        Scurve1_issuedPlanned.extend([len(bdFiltered[(bdFiltered['Expected Date_parsed'].values <= dates[i])])])
        Scurve1_issuedReal.extend([len(bdFiltered[(bdFiltered['Date 1st Issue_parsed'].values <= dates[i])])])
        Scurve1_approvedPlanned.extend([len(bdFiltered[(bdFiltered['Expected Approval Date_parsed'].values <= dates[i])])])
        if dates[i] <= dateOfAnalysis:
            approvedAux = approvedPerDay(dates[i],files,approvedStatus,Folders,excelDir,logger)
            if approvedAux[4] == 'na':
                if len(Scurve1_approvedReal) == 0:
                    Scurve1_approvedReal.extend([0])
                else:
                    Scurve1_approvedReal.extend([Scurve1_approvedReal[i-1]])
            else:
                Scurve1_approvedReal.extend([approvedAux[4]])

            # Scurve 2 calculation

            for j in range(len(approvedAux)):
                if approvedAux[j] == 'na':
                    if len(Scurve2[j]) == 0:
                        Scurve2[j].extend([0])
                    else:
                        Scurve2[j].extend([Scurve2[j][i-1]])
                else:
                    Scurve2[j].extend([approvedAux[j]])
        
        else:
            # Scurve1 calculation

            Scurve1_approvedReal.extend([Scurve1_approvedReal[i-1]])
    
            # Scurve 2 calculation

            for j in range(5):
                Scurve2[j].extend([Scurve2[j][i-1]])

    # calculation of progress in % for Scurve1

    Scurve1_progressPlanned = []
    Scurve1_progressReal = []
    for i in range(len(dates)):
        Scurve1_progressPlanned.extend([weightIssued*(Scurve1_issuedPlanned[i]/Scurve1_total[i]) + weightApproved*(Scurve1_approvedPlanned[i]/Scurve1_total[i])])
        Scurve1_progressReal.extend([weightIssued*(Scurve1_issuedReal[i]/Scurve1_total[i]) + weightApproved*(Scurve1_approvedReal[i]/Scurve1_total[i])])
    
    # calculation of progress in % for Scurve2

    Scurve2_progressPlanned = []
    Scurve2_progressReal = []
    for i in range(len(dates)):
        if Scurve2[0][i] != 0:
            Scurve2_progressPlanned.extend([weightIssued*(Scurve2[1][i]/Scurve2[0][i]) + weightApproved*(Scurve2[2][i]/Scurve2[0][i])])
            Scurve2_progressReal.extend([weightIssued*(Scurve2[3][i]/Scurve2[0][i]) + weightApproved*(Scurve2[4][i]/Scurve2[0][i])])
        else:
            if i == 0:
                Scurve2_progressPlanned.extend([0])
                Scurve2_progressReal.extend([0])
            else:
                Scurve2_progressPlanned.extend([Scurve2_progressPlanned[i-1]])
                Scurve2_progressReal.extend([Scurve2_progressReal[i-1]])

    fig, ax = plt.subplots(1,1,figsize=[3*6.4,3*4.8])
    colors = ['b','c','m','g']

    
    fig.suptitle('{} // {}: Total Progress Planned vs Real'.format(project,discipline),size='large')

    weeks = [-2,-1,1,2,3]
    days = [-7,-6,-5,-4,-3,-2,-1]

    ax.grid(True)
    ax.set_title('Total Progress',size='small')
    ax.tick_params(labelsize='x-small')
    ax.plot(dates,Scurve1_progressPlanned,colors[0]+'--',linewidth=1,label='Scurve 1: Total Progress Planned [%]')
    ax.plot(dates,Scurve1_progressReal,colors[0],linewidth=1,label='Scurve 1: Total Progress Real[%]')
    ax.plot(dates,Scurve2_progressPlanned,colors[1]+'--',linewidth=1,label='Scurve 2: Total Progress Planned [%]')
    ax.plot(dates,Scurve2_progressReal,colors[1],linewidth=1,label='Scurve 2: Total Progress Real[%]')
    realAtDateOfAnalysis = Scurve1_progressReal[dates.index(dateOfAnalysis)]
    plannedAtDateOfAnalysis = Scurve1_progressPlanned[dates.index(dateOfAnalysis)]
    ax.annotate('[Planned: {:.2f}]'.format(plannedAtDateOfAnalysis),(dateOfAnalysis,plannedAtDateOfAnalysis))
    ax.annotate('[Real: {:.2f}]'.format(realAtDateOfAnalysis),(dateOfAnalysis,realAtDateOfAnalysis))
    ax.plot([dateOfAnalysis,dateOfAnalysis],[0,maxVal],'r',linewidth=1,label='Day Of Analysis!')
    realAtDateOfAnalysis2 = Scurve2_progressReal[dates.index(dateOfAnalysis)]
    plannedAtDateOfAnalysis2 = Scurve2_progressPlanned[dates.index(dateOfAnalysis)]
    ax.annotate('[Planned: {:.2f}]'.format(plannedAtDateOfAnalysis2),(dateOfAnalysis,plannedAtDateOfAnalysis2))
    ax.annotate('[Real: {:.2f}]'.format(realAtDateOfAnalysis2),(dateOfAnalysis,realAtDateOfAnalysis2))
    for w in weeks:
        if w == -1:
            ax.plot([dateOfAnalysis + timedelta(7*w),dateOfAnalysis + timedelta(7*w)],[0,maxVal],'k--',linewidth=1,label='Week Intervals')
        else:
            ax.plot([dateOfAnalysis + timedelta(7*w),dateOfAnalysis + timedelta(7*w)],[0,maxVal],'k--',linewidth=1)
    for d in days:
        if d == -1:
            ax.plot([dateOfAnalysis + timedelta(d),dateOfAnalysis + timedelta(d)],[0,maxVal],'g--',linewidth=1,label='Day Intervals')
        else:
            ax.plot([dateOfAnalysis + timedelta(d),dateOfAnalysis + timedelta(d)],[0,maxVal],'g--',linewidth=1)
    ax.legend(loc='upper left',fontsize='small')
    ax.set_yticks(np.arange(0,maxVal,5))

    path = os.path.join(excelDir,'ProgressScurve {}_{}_{}_{}_{}.jpg'.format(project,discipline,dateOfAnalysis.year,dateOfAnalysis.month,dateOfAnalysis.day))

    fig.savefig(path,bbox_inches='tight')

    return path

def drawFull(fileToAnalyze,project,discipline,dateOfAnalysis,foldersEng,approvedStatus,logger):

    ExcelDir = os.path.join(os.path.dirname(fileToAnalyze),'..','Excel')
    bd = pd.read_excel(os.path.join(ExcelDir,fileToAnalyze.split(os.sep)[-1][:-4] + '.xlsx'))
    bck.parseTimeBD(bd,'Date 1st Issue',project + ' ' + discipline)
    bck.parseTimeBD(bd,'Expected Date',project + ' ' + discipline)
    bck.parseTimeBD(bd,'Expected Approval Date',project + ' ' + discipline)
    bck.parseTimeBD(bd,'Approval Date',project + ' ' + discipline)

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
    #print(responsibles)

    #minDate = min(list(bd['Expected Date_parsed']))
    #maxDate = max(list(bd['Expected Date_parsed']))
    minDate = date.today() - timedelta(60)
    maxDate = date.today() + timedelta(60)
    #Folders = ['CIVIL','ELECTRICAL','ELECTROMECHANICAL','EQUIPMENT']
    Folders = foldersEng

    scurvePath = []
    
    # S curve general

    logger.info('start scurveGeneral')
    start = timer()

    scurvePath.extend([scurveGeneral(bd,minDate,maxDate,approvedStatus,ExcelDir,project,discipline,dateOfAnalysis,foldersEng,logger)])

    logger.info('finish scurveGeneral in {:.2f} s'.format(timer()-start))
    
    # S curve for each responsible and category

    logger.info('start scurve for each responsible')
    start = timer()

    for r in responsibles:
        #print(project,disciplina,r)
        maxVal = []
        for i in range(len(Folders)):
            maxVal.extend([0])

        dates = [minDate]
        difDays = maxDate - minDate

        for i in range(difDays.days+1):
            if i != 0:
                dates.extend([dates[i-1] + timedelta(1)])

        real = []
        planned = []
        colors = ['b','c','m','g','b','c']
        for f in Folders:
            realPerFolder = []
            plannedPerFolder = []
            for i in range(len(dates)):
                plannedPerFolder.extend([len(bd[(bd['Expected Date_parsed'] <= dates[i]) & (bd['Folder'] == f) & (bd['Responsible'] == r)])])
                realPerFolder.extend([len(bd[(bd['Date 1st Issue_parsed'] <= dates[i]) & (bd['Folder'] == f) & (bd['Responsible'] == r)])])
            real.extend([realPerFolder])
            planned.extend([plannedPerFolder])

        for i in range(len(Folders)):
            if maxVal[i] < planned[i][-1]:
                maxVal[i] = planned[i][-1]
        
        colNumber = int(np.ceil(len(Folders)/2))

        fig, ax = plt.subplots(2,colNumber,figsize=[3*6.4,3*4.8])
        fig.suptitle('{} // {} // {}: Planned vs Real'.format(project,discipline,r),size='large')

        logger.info('start matplotlib Part of responsible {}'.format(r))
        startGraph = timer()

        weeks = [-2,-1,1,2,3]
        days = [-7,-6,-5,-4,-3,-2,-1]

        if colNumber > 1: 
            fig, ax = plt.subplots(2,colNumber,figsize=[3*6.4,3*4.8])
            fig.suptitle('{} // {} // {}: Planned vs Real'.format(project,discipline,r),size='large')
            for i in range(2):
                for j in range(colNumber):
                    ax[i,j].grid(True)
                    ax[i,j].set_title(Folders[2*i+j],size='small')
                    ax[i,j].tick_params(labelsize='x-small')
                    ax[i,j].plot(dates,planned[2*i+j],colors[2*i+j]+'--',linewidth=1,label='{} planned'.format(Folders[2*i+j]))
                    ax[i,j].plot(dates,real[2*i+j],colors[2*i+j],linewidth=1,label='{} real'.format(Folders[2*i+j]))
                    realAtDateOfAnalysis = real[2*i+j][dates.index(dateOfAnalysis)]
                    plannedAtDateOfAnalysis = planned[2*i+j][dates.index(dateOfAnalysis)]
                    ax[i,j].annotate('[{}, Planned: {}]'.format(Folders[2*i+j],plannedAtDateOfAnalysis),(dateOfAnalysis,plannedAtDateOfAnalysis))
                    ax[i,j].annotate('[{}, Issued: {}]'.format(Folders[2*i+j],realAtDateOfAnalysis),(dateOfAnalysis,realAtDateOfAnalysis))
                    ax[i,j].plot([dateOfAnalysis,dateOfAnalysis],[0,maxVal[2*i+j]],'r',linewidth=1,label='Day Of Analysis!')
                    for w in weeks:
                        if w == -1:
                            ax[i,j].plot([dateOfAnalysis + timedelta(7*w),dateOfAnalysis + timedelta(7*w)],[0,maxVal[2*i+j]],'k--',linewidth=1,label='Week Intervals')
                        else:
                            ax[i,j].plot([dateOfAnalysis + timedelta(7*w),dateOfAnalysis + timedelta(7*w)],[0,maxVal[2*i+j]],'k--',linewidth=1)
                    for d in days:
                        if d == -1:
                            ax[i,j].plot([dateOfAnalysis + timedelta(d),dateOfAnalysis + timedelta(d)],[0,maxVal[2*i+j]],'g--',linewidth=1,label='Day Intervals')
                        else:
                            ax[i,j].plot([dateOfAnalysis + timedelta(d),dateOfAnalysis + timedelta(d)],[0,maxVal[2*i+j]],'g--',linewidth=1)
                    ax[i,j].legend(loc='upper left',fontsize='small')
                    ax[i,j].set_yticks(np.arange(0,maxVal[2*i+j],5))
        else:
                fig, ax = plt.subplots(1,colNumber,figsize=[3*6.4,3*4.8])
                fig.suptitle('{} // {} // {}: Planned vs Real'.format(project,discipline,r),size='large')
                ax.grid(True)
                ax.set_title(Folders[0],size='small')
                ax.tick_params(labelsize='x-small')
                ax.plot(dates,planned[0],colors[0]+'--',linewidth=1,label='{} planned'.format(Folders[0]))
                ax.plot(dates,real[0],colors[0],linewidth=1,label='{} real'.format(Folders[0]))
                realAtDateOfAnalysis = real[0][dates.index(dateOfAnalysis)]
                plannedAtDateOfAnalysis = planned[0][dates.index(dateOfAnalysis)]
                ax.annotate('[{}, Planned: {}]'.format(Folders[0],plannedAtDateOfAnalysis),(dateOfAnalysis,plannedAtDateOfAnalysis))
                ax.annotate('[{}, Issued: {}]'.format(Folders[0],realAtDateOfAnalysis),(dateOfAnalysis,realAtDateOfAnalysis))
                ax.plot([dateOfAnalysis,dateOfAnalysis],[0,maxVal[0]],'r',linewidth=1,label='Day Of Analysis!')
                for w in weeks:
                    if w == -1:
                        ax.plot([dateOfAnalysis + timedelta(7*w),dateOfAnalysis + timedelta(7*w)],[0,maxVal[0]],'k--',linewidth=1,label='Week Intervals')
                    else:
                        ax.plot([dateOfAnalysis + timedelta(7*w),dateOfAnalysis + timedelta(7*w)],[0,maxVal[0]],'k--',linewidth=1)
                for d in days:
                    if d == -1:
                        ax.plot([dateOfAnalysis + timedelta(d),dateOfAnalysis + timedelta(d)],[0,maxVal[0]],'g--',linewidth=1,label='Day Intervals')
                    else:
                        ax.plot([dateOfAnalysis + timedelta(d),dateOfAnalysis + timedelta(d)],[0,maxVal[0]],'g--',linewidth=1)
                ax.legend(loc='upper left',fontsize='small')
                ax.set_yticks(np.arange(0,maxVal[0],5))

        path = os.path.join(ExcelDir,'scurve {}_{}_{}_{}_{}_{}.jpg'.format(project,discipline,r,dateOfAnalysis.year,dateOfAnalysis.month,dateOfAnalysis.day))
        scurvePath.extend([path])
        fig.savefig(path,bbox_inches='tight')
        plt.close(fig)

        logger.info('finish matplotlib part of responsible {} in {:.2f} s'.format(r,timer()-startGraph))
    logger.info('finish scurve for each responsible in {:.2f} s'.format(timer()-start))

    return scurvePath

def drawProject(dayOfAnalysis,projectDir,disciplines,projectFullName,foldersEng,folderSup,projectsWithSup,approvedStatus):

    #dir = os.path.join(projectDir,'00_ProjectReports')
    dir = os.path.join(projectDir,'02_EXE','02_ENG','00_GEN','00_ProjectReports')
    
    minDate = date.today() - timedelta(30)
    maxDate = date.today() + timedelta(60)

    dates = [minDate]
    difDays = maxDate - minDate

    for i in range(difDays.days+1):
        if i != 0:
            dates.extend([dates[i-1] + timedelta(1)])

    weightIssued = 70/100
    weightApproved = 30/100

    # files to review in dates > dayOfAnalysis
    futureDataFrames = []
    for d in disciplines:
        #futurePlanningDir = os.path.join(projectDir,d,'Input')
        futurePlanningDir = os.path.join(projectDir,'02_EXE','02_ENG',d,'00_GEN','04_PLN','02_REP','INPUT')
        file, dayOfFile = bck.chooseFile(futurePlanningDir)
        df = pd.read_csv(os.path.join(futurePlanningDir,file))
        futureDataFrames.extend([df])

    progressPlanned = []
    progressReal = []

    for i in range(len(dates)):
        if dates[i] <= dayOfAnalysis:
            totalData = bck.genReportPerProject(projectDir,disciplines,projectFullName,dates[i],foldersEng,folderSup,projectsWithSup)[0]
            planned = totalData.loc[1,'SUM [%]'] * weightIssued + totalData.loc[4,'SUM [%]'] * weightApproved
            real = totalData.loc[2,'SUM [%]'] * weightIssued + totalData.loc[5,'SUM [%]'] * weightApproved

        else:
            planned = 0
            total = 0
            issuedExpected = 0
            approvedExpected = 0

            for j,data in enumerate(futureDataFrames):
                if (projectFullName in projectsWithSup) & (disciplines[j].find('SUP') != -1):
                    folders = folderSup
                else:
                    folders = foldersEng

                bck.parseTimeBD(data,'Expected Date',projectFullName + ' ' + d)
                bck.parseTimeBD(data,'Expected Approval Date',projectFullName + ' ' + d)
                dfFiltered = data[(data['Folder'].isin(folders)) & (data['Workflow State'] != 'Cancelled')]

                total += len(dfFiltered)
                issuedExpected += len(dfFiltered[(dfFiltered['Expected Date_parsed'].values <= dates[i])])
                approvedExpected += len(dfFiltered[(dfFiltered['Expected Approval Date_parsed'].values <= dates[i])])

            planned = 100 * ((weightIssued*issuedExpected + weightApproved*approvedExpected)/total)

            real = progressReal[-1]

        if planned == 0:
            if len(progressPlanned) == 0:
                progressPlanned.extend([0])
            else:
                progressPlanned.extend([progressPlanned[-1]])
        else:
            progressPlanned.extend([planned])
        if real == 0:
            if len(progressReal) == 0:
                progressReal.extend([0])
            else:
                progressReal.extend([progressReal[-1]])
        else:
            progressReal.extend([real])

    fig, ax = plt.subplots(1,1,figsize=[3*6.4,3*4.8])
    colors = ['b','c','m','g']
    
    fig.suptitle('{} // {}: Total Progress Planned vs Real'.format(projectFullName,dayOfAnalysis),size='large')

    maxVal = 110

    weeks = [-4,-3,-2,-2,1,2,3]
    days = [-7,-6,-5,-4,-3,-2,-1]

    ax.grid(True)
    ax.set_title('Total Progress',size='small')
    ax.tick_params(labelsize='x-small')
    ax.plot(dates,progressPlanned,colors[0]+'--',linewidth=1,label='Scurve 1: Total Progress Planned [%]')
    ax.plot(dates,progressReal,colors[1],linewidth=1,label='Scurve 1: Total Progress Real [%]')
    realAtDateOfAnalysis = progressReal[dates.index(dayOfAnalysis)]
    plannedAtDateOfAnalysis = progressPlanned[dates.index(dayOfAnalysis)]
    ax.annotate('[Planned: {:.2f}]'.format(plannedAtDateOfAnalysis),(dayOfAnalysis,plannedAtDateOfAnalysis))
    ax.annotate('[Real: {:.2f}]'.format(realAtDateOfAnalysis),(dayOfAnalysis,realAtDateOfAnalysis))
    ax.plot([dayOfAnalysis,dayOfAnalysis],[0,maxVal],'r',linewidth=1,label='Day Of Analysis!')
    for w in weeks:
        if w == -1:
            ax.plot([dayOfAnalysis + timedelta(7*w),dayOfAnalysis + timedelta(7*w)],[0,maxVal],'k--',linewidth=1,label='Week Intervals')
        else:
            ax.plot([dayOfAnalysis + timedelta(7*w),dayOfAnalysis + timedelta(7*w)],[0,maxVal],'k--',linewidth=1)
    for d in days:
        if d == -1:
            ax.plot([dayOfAnalysis + timedelta(d),dayOfAnalysis + timedelta(d)],[0,maxVal],'g--',linewidth=1,label='Day Intervals')
        else:
            ax.plot([dayOfAnalysis + timedelta(d),dayOfAnalysis + timedelta(d)],[0,maxVal],'g--',linewidth=1)
    ax.legend(loc='upper left',fontsize='small')
    ax.set_yticks(np.arange(0,maxVal,5))

    graphPath = os.path.join(dir,'totalProjectProgress {}_{}_{}_{}.png'.format(projectFullName,dayOfAnalysis.year,dayOfAnalysis.month,dayOfAnalysis.day))

    fig.savefig(graphPath,bbox_inches='tight')

    return graphPath