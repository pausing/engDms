import backend as bck
import os
from os.path import isfile
import pandas as pd
from datetime import timedelta, datetime

def cleanColumns(file):
    with open(file,'r+',encoding='utf-8') as txtFile:
        buffer = ''
        for line in txtFile:
            lSplitted = line.strip().split(',')
            for i in range(18):
                buffer = buffer + lSplitted[i] + ','
            buffer = buffer + '\n'
    #print(buffer)

    if file.find('_output') == -1:
        newfile = file[0:-4] + '_output.csv'
    else:
        newfile = file
    buffer = buffer.replace('\u2026','')
    
    with open(newfile,'w',encoding='utf-8') as newTxtFile:
        newTxtFile.write(buffer)

    return newfile
    
def reviewOutput(directory,folders,approvedStatus,dayOfAnalysis,logger,project,discipline):
    p = project
    d = discipline
    file = bck.chooseFile(directory)[0]
    logger.info('reviewOutput - analyzing {}'.format(file))
    bck.formatFile(file,logger)
    file = cleanColumns(file)

    bd = pd.read_csv(file)

    bck.parseTimeBD(bd,'Expected First Issue Date', p + ' ' + d)
    bck.parseTimeBD(bd,'Replanned First Issue Date', p + ' ' + d)
    bck.parseTimeBD(bd,'Fisrt Issue Date', p + ' ' + d)
    bck.parseTimeBD(bd,'Last Issue Date', p + ' ' + d)
    bck.parseTimeBD(bd,'Expected Approval Date', p + ' ' + d)
    bck.parseTimeBD(bd,'Replanned Expected Approval', p + ' ' + d)
    bd = bd.drop('Expected First Issue Date',axis=1)
    bd = bd.drop('Replanned First Issue Date',axis=1)
    bd = bd.drop('Fisrt Issue Date',axis=1)
    bd = bd.drop('Last Issue Date',axis=1)
    bd = bd.drop('Expected Approval Date',axis=1)
    bd = bd.drop('Replanned Expected Approval',axis=1)
    bd = bd.drop('MDL Revision',axis=1)
    bd = bd.drop('Unnamed: 18',axis=1)
    bd = bd.drop('Approval Date',axis=1)
    bd = bd.drop('Expected First Issue Date_parsed',axis=1)
    bd = bd.drop('Replanned First Issue Date_parsed',axis=1)
    bd = bd.drop('Expected Approval Date_parsed',axis=1)
    bd = bd.drop('Replanned Expected Approval_parsed',axis=1)
    bd = bd.drop('Item or Sequence',axis=1)
    for i in range(len(bd)):
        bd.loc[i,'Description'] = bd.loc[i,'Description'][0:40]

    changeTitles = {
        'Contractor / Supplier':'Responsible',
        'Fisrt Issue Date_parsed':'1st ISS',
        'Last Issue Date_parsed':'LAST ISS',
    }
    bd.rename(columns=changeTitles,inplace=True)
    bd['DaysNoAnswer'] = dayOfAnalysis - bd['LAST ISS']
    statusToCheck = ['For Analysis','Pre analysis']

    # list of documents to be reviewed by Reviewer

    bdFiltered = bd[(bd['Folder'].isin(folders)) & ((bd['Status'].isin(statusToCheck)))]
    bdFiltered = bdFiltered.sort_values(by=['DaysNoAnswer'])
    bdFiltered = bdFiltered.reset_index(drop=True)
    bdFiltered.insert(0,'Item',range(1,len(bdFiltered)+1),True)

    # list of documents to be reviewed by Contractor

    statusToCheck = ['Non-compliant','For revision']

    bdContractorPending = bd[(bd['Folder'].isin(folders)) & ((bd['Status'].isin(statusToCheck)))]
    bdContractorPending = bdContractorPending.sort_values(by=['DaysNoAnswer'])
    bdContractorPending = bdContractorPending.reset_index(drop=True)
    bdContractorPending.insert(0,'Item',range(1,len(bdContractorPending)+1),True)

    return bdFiltered,bdContractorPending,bd
