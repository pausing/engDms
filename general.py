
def generalInfo():
    #projectsFullNames = ['BESS DEL DESIERTO','SHANGRILA','LUIZ CARLOS','DRACO','ESTEPA','CAMPANO']
    projectsFullNames = ['BESS DEL DESIERTO','SHANGRILA','LUIZ CARLOS','DRACO','ESTEPA']

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

    # subFolder for disciplines 05_SUP: LC,DRACO
    # projects with discipline SUP
    projectsWithSUP = ['LUIZ CARLOS','DRACO','ESTEPA']
    folderSup = {
        'LUIZ CARLOS':['CHINT','JINKO','NEXTRACKER','STI','SUNGROW','WEG'],
        'DRACO':['TRACKERS','INVERTERS','MODULES','POWER_TRANSFORMERS'],
        'ESTEPA':['INVERTERS','MODULES','POWER_TRANSFORMERS','TRACKERS'],
    }

    return projectsFullNames, projectsAcroName, disciplines, disciplinesContractors, projectsWithSUP, folderSup

def whichPath(where):
    planDirBESSMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/docTO/TO/Chile/01_BDD/02_EXE/03_ENG/00_Planning'
    planDirSHAMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/docTO/TO/Colombia/05_SHA/02_EXE/03_ENG/00_Planning'
    planDirLCMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/docTO/TO/Brazil/05_LC/02_EXE/03_ENG/00_Planning'
    planDirDRAMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/docTO/TO/Brazil/10_DRA/02_EXE/03_ENG/00_Planning'
    planDirESTMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/docTO/TO/Chile/07_EST/02_EXE/03_ENG/00_Planning'
    planDirCAMMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/docTO/TO/Colombia/06_CAM/02_EXE/03_ENG/00_Planning'

    saveDirMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/Documentos/02_INGENIERIA/07_ProjReport'
    #projectsMac = [planDirBESSMac,planDirSHAMac,planDirLCMac,planDirDRAMac,planDirESTMac,planDirCAMMac]
    projectsMac = [planDirBESSMac,planDirSHAMac,planDirLCMac,planDirDRAMac,planDirESTMac]

    planDirBESSPC = 'C:\\Users\\pauma\\OneDrive - AtlasRen\\docTO\\TO\\Chile\\01_BDD\\02_EXE\\03_ENG\\00_Planning'
    planDirSHAPC = 'C:\\Users\\pauma\\OneDrive - AtlasRen\\docTO\\TO\\Colombia\\05_SHA\\02_EXE\\03_ENG\\00_Planning'
    planDirLCPC = 'C:\\Users\\pauma\\OneDrive - AtlasRen\\docTO\\TO\\Brazil\\05_LC\\02_EXE\\03_ENG\\00_Planning'
    planDirDRAPC = 'C:\\Users\\pauma\\OneDrive - AtlasRen\\docTO\\TO\\Brazil\\10_DRA\\02_EXE\\03_ENG\\00_Planning'
    planDirESTPC = 'C:\\Users\\pauma\\OneDrive - AtlasRen\\docTO\\TO\\Chile\\07_EST\\02_EXE\\03_ENG\\00_Planning'
    planDirCAMPC = 'C:\\Users\\pauma\\OneDrive - AtlasRen\\docTO\\TO\\Colombia\\06_CAM\\02_EXE\\03_ENG\\00_Planning'

    saveDirPC = 'C:\\Users\\pauma\\OneDrive - AtlasRen\\Documentos\\02_INGENIERIA\\07_ProjReport'
    #projectsPC = [planDirBESSPC,planDirSHAPC,planDirLCPC,planDirDRAPC,planDirESTPC,planDirCAMPC]
    projectsPC = [planDirBESSPC,planDirSHAPC,planDirLCPC,planDirDRAPC,planDirESTPC]

    planDirBESSLap = 'C:\\Users\\PabloMaqueda\\OneDrive\\OneDrive - AtlasRen\\docTO\\TO\\Chile\\01_BDD\\02_EXE\\03_ENG\\00_Planning'
    planDirSHALap = 'C:\\Users\\PabloMaqueda\\Onedrive\\OneDrive - AtlasRen\\docTO\\TO\\Colombia\\05_SHA\\02_EXE\\03_ENG\\00_Planning'
    planDirLCLap = 'C:\\Users\\PabloMaqueda\\Onedrive\\OneDrive - AtlasRen\\docTO\\TO\\Brazil\\05_LC\\02_EXE\\03_ENG\\00_Planning'
    planDirDRALap = 'C:\\Users\\PabloMaqueda\\Onedrive\\OneDrive - AtlasRen\\docTO\\TO\\Brazil\\10_DRA\\02_EXE\\03_ENG\\00_Planning'
    planDirESTLap = 'C:\\Users\\PabloMaqueda\\Onedrive\\OneDrive - AtlasRen\\docTO\\TO\\Chile\\07_EST\\02_EXE\\03_ENG\\00_Planning'
    planDirCAMLap = 'C:\\Users\\PabloMaqueda\\Onedrive\\OneDrive - AtlasRen\\docTO\\TO\\Colombia\\06_CAM\\02_EXE\\03_ENG\\00_Planning'

    saveDirLap = 'C:\\Users\\PabloMaqueda\\Onedrive\\OneDrive - AtlasRen\\Documentos\\02_INGENIERIA\\07_ProjReport'
    projectsLap = [planDirBESSLap,planDirSHALap,planDirLCLap,planDirDRALap,planDirESTLap,planDirCAMLap]
    
    projects = []
    projectsDict = {}
    saveDir = ''

    projectsAcroName = generalInfo()[1]

    if where == 'mac':
        projects = projectsMac
        projectsDict = dict(zip(list(projectsAcroName.values()),projectsMac))
        saveDir = saveDirMac
    elif where == 'pc':
        projects = projectsPC
        projectsDict = dict(zip(list(projectsAcroName.values()),projectsPC))
        saveDir = saveDirPC
    elif where == 'lap':
        projects = projectsLap
        projectsDict = dict(zip(list(projectsAcroName.values()),projectsLap))
        saveDir = saveDirLap

    return projects, projectsDict, saveDir

def colaborativoInformation():
    approvedStatus = ['Compliant','Compliant with comments','Issued For Construction','Issued For Construction_','Pre analysis','Ready for as built'] 
    foldersEng = ['CIVIL','ELECTRICAL','ELECTROMECHANICAL','EQUIPMENT']
    foldersQA = ['CONFORMITY','PROCEDURE']

    return approvedStatus,foldersEng,foldersQA