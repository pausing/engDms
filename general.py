
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
        'EST-2':['02_BESS_PRE_EXEC','05_SUP'],
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
        'EST-2':['05_SUP'],
        'COP':[],
    }

    # subFolder for disciplines 05_SUP: LC,DRACO
    # projects with discipline SUP
    projectsWithSUP = ['LUIZ CARLOS','DRACO','ESTEPA-1','ESTEPA-2']
    folderSup = {
        'LUIZ CARLOS':['CHINT','JINKO','NEXTRACKER','STI','SUNGROW','WEG'],
        'DRACO':['TRACKERS','INVERTERS','MODULES','POWER_TRANSFORMERS'],
        'ESTEPA-1':['INVERTERS','MODULES_LONGI','POWER_TRANSFORMERS','TRACKERS','BESS_SUPPLY'],
        'ESTEPA-2':['POWER_TRANSFORMER'],
    }

    return projectsFullNames, projectsAcroName, disciplines, disciplinesContractors, projectsWithSUP, folderSup

def whichPath(where):

    # folder path for PMC mac lap
        # folder path de la informacion del proyecto
    planDirBESSMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/dto/Chile/01_BDD/02_EXE/03_ENG/00_Planning'
    planDirSHAMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/dto/Colombia/05_SHA/02_EXE/03_ENG/00_Planning'
    planDirLCMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/dto/Brazil/05_LC/02_EXE/03_ENG/00_Planning'
    planDirDRAMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/dto/Brazil/10_DRA/02_EXE/03_ENG/00_Planning'
    planDirESTMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/dto/Chile/07_EST-1/02_EXE/03_ENG/00_Planning'
    planDirEST_2_Mac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/dto/Chile/08_EST-2/02_EXE/03_ENG/00_Planning'
    planDirCOPMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/dto/Chile/10_COP/02_EXE/03_ENG/00_Planning'
    planDirCAMMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/dto/Colombia/06_CAM/02_EXE/03_ENG/00_Planning'

        # folder path de proyecto para copiar los reportes
    repDirBESSMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/dto/Chile/01_BDD/02_EXE/03_ENG/00_Reporting'
    repDirSHAMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/dto/Colombia/05_SHA/02_EXE/03_ENG/00_Reporting'
    repDirLCMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/dto/Brazil/05_LC/02_EXE/03_ENG/00_Reporting'
    repDirDRAMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/dto/Brazil/10_DRA/02_EXE/03_ENG/00_Reporting'
    repDirESTMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/dto/Chile/07_EST-1/02_EXE/03_ENG/00_Reporting'
    repDirEST_2_Mac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/dto/Chile/08_EST-2/02_EXE/03_ENG/00_Reporting'
    repDirCOPMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/dto/Chile/10_COP/02_EXE/03_ENG/00_Reporting'
    repDirCAMMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/dto/Colombia/06_CAM/02_EXE/03_ENG/00_Reporting'

    saveDirMac = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/Documentos/02_INGENIERIA/07_ProjReport'
    projectsMac = [planDirBESSMac,planDirSHAMac,planDirLCMac,planDirDRAMac,planDirESTMac,planDirEST_2_Mac,planDirCOPMac,planDirCAMMac]
    reportingDir_Mac_lap = [repDirBESSMac,repDirSHAMac,repDirLCMac,repDirDRAMac,repDirESTMac,repDirEST_2_Mac,repDirCOPMac,repDirCAMMac]

    # folder path for PMC PC
        # folder path de la informacion del proyecto
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

    # folder path for PMC windows lap
        # folder path de la informacion del proyecto
    planDirBESSLap = 'C:\\Users\\PabloMaqueda\\OneDrive\\OneDrive - AtlasRen\\docTO\\TO\\Chile\\01_BDD\\02_EXE\\03_ENG\\00_Planning'
    planDirSHALap = 'C:\\Users\\PabloMaqueda\\Onedrive\\OneDrive - AtlasRen\\docTO\\TO\\Colombia\\05_SHA\\02_EXE\\03_ENG\\00_Planning'
    planDirLCLap = 'C:\\Users\\PabloMaqueda\\Onedrive\\OneDrive - AtlasRen\\docTO\\TO\\Brazil\\05_LC\\02_EXE\\03_ENG\\00_Planning'
    planDirDRALap = 'C:\\Users\\PabloMaqueda\\Onedrive\\OneDrive - AtlasRen\\docTO\\TO\\Brazil\\10_DRA\\02_EXE\\03_ENG\\00_Planning'
    planDirESTLap = 'C:\\Users\\PabloMaqueda\\Onedrive\\OneDrive - AtlasRen\\docTO\\TO\\Chile\\07_EST\\02_EXE\\03_ENG\\00_Planning'
    planDirCAMLap = 'C:\\Users\\PabloMaqueda\\Onedrive\\OneDrive - AtlasRen\\docTO\\TO\\Colombia\\06_CAM\\02_EXE\\03_ENG\\00_Planning'

    saveDirLap = 'C:\\Users\\PabloMaqueda\\Onedrive\\OneDrive - AtlasRen\\Documentos\\02_INGENIERIA\\07_ProjReport'
    projectsLap = [planDirBESSLap,planDirSHALap,planDirLCLap,planDirDRALap,planDirESTLap,planDirCAMLap]

    # folder path for SGS windows lap
        # folder path de la informacion del proyecto
    planDirBESS_SGS_lap = 'C:\\Users\\González\\OneDrive - Atlas Renewable Energy\\TO\\Chile\\01_BDD\\02_EXE\\03_ENG\\00_Planning'
    planDirSHA_SGS_lap = 'C:\\Users\\González\\OneDrive - Atlas Renewable Energy\\TO\\Colombia\\05_SHA\\02_EXE\\03_ENG\\00_Planning'
    planDirLC_SGS_lap = 'C:\\Users\\González\\OneDrive - Atlas Renewable Energy\\TO\\Brazil\\05_LC\\02_EXE\\03_ENG\\00_Planning'
    planDirDRA_SGS_lap = 'C:\\Users\\González\\OneDrive - Atlas Renewable Energy\\TO\\Brazil\\10_DRA\\02_EXE\\03_ENG\\00_Planning'
    planDirEST1_SGS_lap = 'C:\\Users\\González\\OneDrive - Atlas Renewable Energy\\TO\\Chile\\07_EST-1\\02_EXE\\03_ENG\\00_Planning'
    planDirEST2_SGS_lap = 'C:\\Users\\González\\OneDrive - Atlas Renewable Energy\\TO\\Chile\\08_EST-2\\02_EXE\\03_ENG\\00_Planning'
    planDirCOP_SGS_lap = 'C:\\Users\\González\\OneDrive - Atlas Renewable Energy\\TO\\Chile\\10_COP\\02_EXE\\03_ENG\\00_Planning'
    planDirCAM_SGS_lap = 'C:\\Users\\González\\OneDrive - Atlas Renewable Energy\\TO\\Colombia\\06_CAM\\02_EXE\\03_ENG\\00_Planning'

        # folder path de proyecto para copiar los reportes
    repDirBESS_SGS_lap='C:\\Users\\González\\OneDrive - Atlas Renewable Energy\\TO\Chile\\01_BDD\\02_EXE\\03_ENG\\00_Reporting'
    repDirSHA_SGS_lap='C:\\Users\\González\\OneDrive - Atlas Renewable Energy\\TO\\Colombia\\05_SHA\\02_EXE\\03_ENG\\00_Reporting'
    repDirLC_SGS_lap='C:\\Users\\González\\OneDrive - Atlas Renewable Energy\\TO\\Brazil\\05_LC\\02_EXE\\03_ENG\\00_Reporting'
    repDirDRA_SGS_lap='C:\\Users\\González\\OneDrive - Atlas Renewable Energy\\TO\\Brazil\\10_DRA\\02_EXE\\03_ENG\\00_Reporting'
    repDirEST1_SGS_lap='C:\\Users\\González\\OneDrive - Atlas Renewable Energy\\TO\Chile\\07_EST-1\\02_EXE\\03_ENG\\00_Reporting'
    repDirEST2_SGS_lap='C:\\Users\\González\\OneDrive - Atlas Renewable Energy\\TO\\Chile\\08_EST-2\\02_EXE\\03_ENG\\00_Reporting'
    repDirCOP_SGS_lap='C:\\Users\\González\\OneDrive - Atlas Renewable Energy\\TO\\Chile\\10_COP\\02_EXE\\03_ENG\\00_Reporting'
    repDirCAM_SGS_lap='C:\\Users\\González\\OneDrive - Atlas Renewable Energy\\TO\\Colombia\\06_CAM\\02_EXE\\03_ENG\\00_Reporting'

        # folder path personal para copiar los reportes
    saveDir_SGS_lap = 'C:\\Users\\González\\\\OneDrive - AtlasRen\\Documentos\\02_INGENIERIA\\07_ProjReport'

    projects_SGS_lap = [planDirBESS_SGS_lap,planDirSHA_SGS_lap,planDirLC_SGS_lap,planDirDRA_SGS_lap,planDirEST1_SGS_lap,planDirEST2_SGS_lap,planDirCOP_SGS_lap,planDirCAM_SGS_lap]
    reportingDir_SGS_lap = [repDirBESS_SGS_lap,repDirSHA_SGS_lap,repDirLC_SGS_lap,repDirDRA_SGS_lap,repDirEST1_SGS_lap,repDirEST2_SGS_lap,repDirCOP_SGS_lap,repDirCAM_SGS_lap]
    
    projects = []
    projectsDict = {}
    saveDir = ''
    reportingDir = []

    projectsAcroName = generalInfo()[1]

    if where == 'mac':
        projects = projectsMac
        projectsDict = dict(zip(list(projectsAcroName.values()),projectsMac))
        saveDir = saveDirMac
        reportingDir = reportingDir_Mac_lap
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
        reportingDir = reportingDir_SGS_lap

    return projects, projectsDict, saveDir, reportingDir

def where(location):
    if location == 'Pablos-Laptop.local':
        return 'mac'
    if location == 'DESKTOP-00OQQTF':
        return 'pc'
    if location == 'LAPTOP-MP2C40V0':
        return 'SGS_lap'


def colaborativoInformation():
    approvedStatus = ['Compliant','Compliant with comments','Issued For Construction','Issued For Construction_','Pre analysis','Ready for as built','As built','As built for revision','Final As built','For revision'] 
    foldersEng = ['CIVIL','ELECTRICAL','ELECTROMECHANICAL','EQUIPMENT']
    foldersQA = ['CONFORMITY','PROCEDURE']

    return approvedStatus,foldersEng,foldersQA