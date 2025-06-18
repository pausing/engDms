import os
import shutil
from timeit import default_timer as timer


startTime = timer()

planDir = '/Users/paumaq/Library/CloudStorage/OneDrive-AtlasRen/dto/Chile/07_EST-1'

oldDisciplineName = '07_BESS'
discipline = '02_BESS'

planDirPoject = os.path.join(planDir,'02_EXE','02_ENG',discipline,'00_GEN','04_PLN','02_REP','EXCEL')
print(planDirPoject)
folderBckUp = os.path.join(planDirPoject,'00_bckup')
if not os.path.exists(folderBckUp):
    os.mkdir(folderBckUp)

files = os.listdir(planDirPoject)

print('endTimeListDir',timer()-startTime)

startTime = timer()

print(len(files))

txtToFind = 'EPA_' + oldDisciplineName
txtReplaceWith = 'EPA-1_EXE_' + discipline

filesWithTxt = []
for f in files:
    if f.find(txtToFind) != -1:
        filesWithTxt.extend([f])

totalFilesToMod = len(filesWithTxt)

k = 0
for f in files:
    if k < 1500:
        if f.find(txtToFind) != -1:

            print('endTimeFindText: ',timer()-startTime)
            startTime = timer()

            print(f)
            print(f.replace(txtToFind,txtReplaceWith))
            filesWithTxt.extend([f])

            print('endTimeFindText: ',timer()-startTime)
            startTime = timer()

            shutil.copyfile(os.path.join(planDirPoject,f),os.path.join(planDirPoject,f.replace(txtToFind,txtReplaceWith)))
            print('endTimeCopyFile: ',timer()-startTime)
            startTime = timer()

            shutil.move(os.path.join(planDirPoject,f),os.path.join(folderBckUp,f))
            print('endTimeMoveFile: ',timer()-startTime)
            startTime = timer()

            #os.rename(os.path.join(folderBckUp,f),os.path.join(planDirPoject,f.replace(txtToFind,txtReplaceWith)))

            k += 1
            print('{} of {}'.format(k,totalFilesToMod))

print(len(filesWithTxt))