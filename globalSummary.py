import os
import pandas as pd

def globalReport(day,projects,projectsAcroName,projectsFullName,disciplines):
    for p in enumerate(projects):
        iniDict = {
                'ITEM': ['TOTAL','ISSUED EXPECTED','ISSUED REAL','APPROVED EXPECTED','APPROVED REAL'],
                'CIVIL': [0,0,0,0,0],
                'ELECTRICAL': [0,0,0,0,0],
                'ELECTROMECHANICAL': [0,0,0,0,0],
                'EQUIPMENT': [0,0,0,0,0],
                'SUM': [0,0,0,0,0],
                'SUM[%]': ['--',0,0,0,0],
                'TOTAL PROGRESS [%]': ['--','--','--',0,0]
        }

        df = pd.DataFrame(iniDict)

        for d in disciplines[projectsAcroName[projectsFullName[p[0]]]]:
            dirs = os.listdir(os.path.join(p,d,'Excel'))

