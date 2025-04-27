
def generalInfo():
    projectsFullNames = ['BESS DEL DESIERTO','SHANGRILA','LUIZ CARLOS','DRACO','ESTEPA-1','ESTEPA-2','COPIAPO','CAMPANO']
    #projectsFullNames = ['BESS DEL DESIERTO','SHANGRILA','LUIZ CARLOS','DRACO','ESTEPA']

    projectsAcroName = {
        'BESS DEL DESIERTO':'BDD',
        'SHANGRILA':'SHA',
        'LUIZ CARLOS':'LC',
        'DRACO':'DRA',
        'ESTEPA-1':'EST-1',
        'ESTEPA-2':'EST-2',
        'COPIAPO':'COP',
        'CAMPANO':'CAM',
    }

    disciplines = {
        'BDD':['01_BESS','02_HV_SDD','03_EE_INT'],
        'SHA':['01_PV','02_HV','03_LT'],
        'LC':['01_PV AREA A','02_PV AREA B','03_HV','04_LT','05_SUP'],
        'DRA':['01_PV-PRE EXEC','03_PV','04_HV','05_SUP'],
        'EST-1':['01_PV-PRE EXEC','02_HV-PRE EXEC','03_BESS-PRE EXEC','04_EWA-PV','05_PV','06_HV','07_BESS','08_SUP'],
        'EST-2':['02_BESS_PRE_EXEC'],
        'COP':['01_PV-PRE EXEC','03_BESS-PRE EXEC'],
        'CAM':['01_PV-PRE EXEC'],
    }

    disciplinesContractors = {
        'BDD':['01_BESS','02_HV_SDD','03_EE_INT'],
        'SHA':['01_PV','02_HV','03_LT'],
        'LC':['01_PV AREA A','02_PV AREA B','03_HV','04_LT','05_SUP'],
        'DRA':['03_PV','04_HV','05_SUP'],
        'EST-1':['05_PV','06_HV','07_BESS','08_SUP'],
        'CAM':[],
        'EST-2':[],
        'COP':[],
    }

    # subFolder for disciplines 05_SUP: LC,DRACO
    # projects with discipline SUP
    projectsWithSUP = ['LUIZ CARLOS','DRACO','ESTEPA-1']
    folderSup = {
        'LUIZ CARLOS':['CHINT','JINKO','NEXTRACKER','STI','SUNGROW','WEG'],
        'DRACO':['TRACKERS','INVERTERS','MODULES','POWER_TRANSFORMERS'],
        'ESTEPA-1':['INVERTERS','MODULES_LONGI','POWER_TRANSFORMERS','TRACKERS','BESS_SUPPLY'],
    }

    return projectsFullNames, projectsAcroName, disciplines, disciplinesContractors, projectsWithSUP, folderSup

def whichPath(where):
    planDirBESSMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/dto/Chile/01_BDD/02_EXE/03_ENG/00_Planning'
    planDirSHAMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/dto/Colombia/05_SHA/02_EXE/03_ENG/00_Planning'
    planDirLCMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/dto/Brazil/05_LC/02_EXE/03_ENG/00_Planning'
    planDirDRAMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/dto/Brazil/10_DRA/02_EXE/03_ENG/00_Planning'
    planDirESTMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/dto/Chile/07_EST-1/02_EXE/03_ENG/00_Planning'
    planDirEST_2_Mac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/dto/Chile/08_EST-2/02_EXE/03_ENG/00_Planning'
    planDirCOPMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/dto/Chile/10_COP/02_EXE/03_ENG/00_Planning'
    planDirCAMMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/dto/Colombia/06_CAM/02_EXE/03_ENG/00_Planning'

    saveDirMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/Documentos/02_INGENIERIA/07_ProjReport'
    projectsMac = [planDirBESSMac,planDirSHAMac,planDirLCMac,planDirDRAMac,planDirESTMac,planDirEST_2_Mac,planDirCOPMac,planDirCAMMac]

    planDirBESSPC = 'C:\\Users\\pauma\\OneDrive - AtlasRen\\dto\\Chile\\01_BDD\\02_EXE\\03_ENG\\00_Planning'
    planDirSHAPC = 'C:\\Users\\pauma\\OneDrive - AtlasRen\\dto\\Colombia\\05_SHA\\02_EXE\\03_ENG\\00_Planning'
    planDirLCPC = 'C:\\Users\\pauma\\OneDrive - AtlasRen\\dto\\Brazil\\05_LC\\02_EXE\\03_ENG\\00_Planning'
    planDirDRAPC = 'C:\\Users\\pauma\\OneDrive - AtlasRen\\dto\\Brazil\\10_DRA\\02_EXE\\03_ENG\\00_Planning'
    planDirESTPC = 'C:\\Users\\pauma\\OneDrive - AtlasRen\\dto\\Chile\\07_EST-1\\02_EXE\\03_ENG\\00_Planning'
    planDirEST_2PC = 'C:\\Users\\pauma\\OneDrive - AtlasRen\\dto\\Chile\\08_EST-2\\02_EXE\\03_ENG\\00_Planning'
    planDirCOPPC = 'C:\\Users\\pauma\\OneDrive - AtlasRen\\dto\\Chile\\10_COP\\02_EXE\\03_ENG\\00_Planning'
    planDirCAMPC = 'C:\\Users\\pauma\\OneDrive - AtlasRen\\dto\\Colombia\\06_CAM\\02_EXE\\03_ENG\\00_Planning'

    saveDirPC = 'C:\\Users\\pauma\\OneDrive - AtlasRen\\Documentos\\02_INGENIERIA\\07_ProjReport'
    projectsPC = [planDirBESSPC,planDirSHAPC,planDirLCPC,planDirDRAPC,planDirESTPC,planDirEST_2PC,planDirCOPPC,planDirCAMPC]

    planDirBESSLap = 'C:\\Users\\PabloMaqueda\\OneDrive\\OneDrive - AtlasRen\\docTO\\TO\\Chile\\01_BDD\\02_EXE\\03_ENG\\00_Planning'
    planDirSHALap = 'C:\\Users\\PabloMaqueda\\Onedrive\\OneDrive - AtlasRen\\docTO\\TO\\Colombia\\05_SHA\\02_EXE\\03_ENG\\00_Planning'
    planDirLCLap = 'C:\\Users\\PabloMaqueda\\Onedrive\\OneDrive - AtlasRen\\docTO\\TO\\Brazil\\05_LC\\02_EXE\\03_ENG\\00_Planning'
    planDirDRALap = 'C:\\Users\\PabloMaqueda\\Onedrive\\OneDrive - AtlasRen\\docTO\\TO\\Brazil\\10_DRA\\02_EXE\\03_ENG\\00_Planning'
    planDirESTLap = 'C:\\Users\\PabloMaqueda\\Onedrive\\OneDrive - AtlasRen\\docTO\\TO\\Chile\\07_EST\\02_EXE\\03_ENG\\00_Planning'
    planDirCAMLap = 'C:\\Users\\PabloMaqueda\\Onedrive\\OneDrive - AtlasRen\\docTO\\TO\\Colombia\\06_CAM\\02_EXE\\03_ENG\\00_Planning'

    saveDirLap = 'C:\\Users\\PabloMaqueda\\Onedrive\\OneDrive - AtlasRen\\Documentos\\02_INGENIERIA\\07_ProjReport'
    projectsLap = [planDirBESSLap,planDirSHALap,planDirLCLap,planDirDRALap,planDirESTLap,planDirCAMLap]

    planDirBESS_SGS_lap = 'C:\\Users\\González\\OneDrive - Atlas Renewable Energy\\TO\\Chile\\01_BDD\\02_EXE\\03_ENG\\00_Planning'
    planDirSHA_SGS_lap = 'C:\\Users\\González\\OneDrive - Atlas Renewable Energy\\TO\\Colombia\\05_SHA\\02_EXE\\03_ENG\\00_Planning'
    planDirLC_SGS_lap = 'C:\\Users\\González\\OneDrive - Atlas Renewable Energy\\TO\\Brazil\\05_LC\\02_EXE\\03_ENG\\00_Planning'
    planDirDRA_SGS_lap = 'C:\\Users\\González\\\\OneDrive - Atlas Renewable Energy\\TO\\Brazil\\10_DRA\\02_EXE\\03_ENG\\00_Planning'
    planDirEST_SGS_lap = 'C:\\Users\\González\\\\OneDrive - Atlas Renewable Energy\\TO\\Chile\\07_EST\\02_EXE\\03_ENG\\00_Planning'
    planDirCAM_SGS_lap = 'C:\\Users\\González\\\\OneDrive - Atlas Renewable Energy\\TO\\Colombia\\06_CAM\\02_EXE\\03_ENG\\00_Planning'

    # poner carpeta de SGS
    saveDir_SGS_lap = 'C:\\Users\\González\\\\OneDrive - Atlas Renewable Energy\\Documentos\\02_INGENIERIA\\07_ProjReport'
    projects_SGS_lap = [planDirBESS_SGS_lap,planDirSHA_SGS_lap,planDirLC_SGS_lap,planDirDRA_SGS_lap,planDirEST_SGS_lap,planDirCAM_SGS_lap]
    
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
    elif where == 'SGS_lap':
        projects = projects_SGS_lap
        projectsDict = dict(zip(list(projectsAcroName.values()),projects_SGS_lap))
        saveDir = saveDir_SGS_lap

    return projects, projectsDict, saveDir

def where(location):
    if location == 'Pablos-Laptop.local':
        return 'mac'
    if location == 'DESKTOP-00OQQTF':
        return 'pc'
    if location == 'LAPTOP-MP2C40V0':
        return 'SGS_lap'


def colaborativoInformation():
    approvedStatus = ['Compliant','Compliant with comments','Issued For Construction','Issued For Construction_','Pre analysis','Ready for as built','For revision'] 
    foldersEng = ['CIVIL','ELECTRICAL','ELECTROMECHANICAL','EQUIPMENT']
    foldersQA = ['CONFORMITY','PROCEDURE']

    return approvedStatus,foldersEng,foldersQA