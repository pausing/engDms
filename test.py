file = '04_UFV_LUIZ_CARLOS_PV_AREA_B-planejamento_09072024_082827_9367.csv'
posRef = file.find('planejamento_')
lenKeyWord = len('planejamento_')
posIni = posRef + lenKeyWord
print(file[posIni:posIni+2])
print(file[posIni+2:posIni+2+2])
print(file[posIni+4:posIni+4+4])
d = file[file.find('planejamento_') + len('planejamento_') : file.find('planejamento_') + len('planejamento_') + 2]
m = file[file.find('planejamento_') + len('planejamento_') + 3 : file.find('planejamento_') + len('planejamento_') + 3 + 2]
y = file[file.find('planejamento_') + len('planejamento_') + 3 + 3 : file.find('planejamento_') + len('planejamento_') + 3 + 3 + 4]
