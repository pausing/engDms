import os
import shutil
import general as gen  
import platform

def countryFromProject(projectReport):

    location = platform.node()

    saveDir= gen.whichPath(gen.where(location))[2]

    pathGenReports = gen.whichPath(gen.where(location))[4]

    projectsFullNames = gen.generalInfo()[0] # list of full names
    projectsAcroNames = gen.generalInfo()[1] # dict of {full name: acronym}
    projectsPerCountry = gen.generalInfo()[8] # dict of {Country: projects acronym}

    country = 'NotFound'

    for p in projectsFullNames:
        if projectReport.find(p) != -1:
            projectAcro = projectsAcroNames[p]
            for c in projectsPerCountry.keys():
                if projectAcro in projectsPerCountry[c]:
                    country = c
                    break
            break

    return country