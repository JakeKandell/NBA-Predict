import os

def setCurrentWorkingDirectory(directoryName):

    programDirectory = os.path.dirname(os.path.abspath(__file__))
    newCurrentWorkingDirectory = os.path.join(programDirectory, directoryName)
    os.chdir(newCurrentWorkingDirectory)