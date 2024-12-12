import os


directory = 'C:\\Users\\pauma\\OneDrive - AtlasRen\\Documentos\\02_INGENIERIA\\07_ProjReport'

files = os.listdir(directory)
print(files)

def parseFile(file):

    fmod = file.replace('engReport_','')
    y = fmod[0:4]
    m = fmod[5:7]
    d = fmod[8:10]

    fmod = f'{y}{m}{d}' + fmod[10:len(fmod)]

    return fmod

for f in files:
    os.rename(os.path.join(directory,f),os.path.join(directory,parseFile(f)))
