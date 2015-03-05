import subprocess,sys,os
from optparse import OptionParser
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot,QFileSystemWatcher

class ReconstructionManager(QObject):
    # Signal initialisation
    # This signal is launched when a new ply is detected
    newPointCloud = pyqtSignal(str)

    def __init__(self):
        QObject.__init__(self)
    def launchReconstruction(self,imDir,method,omvgBuildDir,outDir,pointCloudDir):
        """
        launchReconstruction function aims at launching the openMVG reconstruction. Only works under Unix based system.
        INPUT: paths to images, openMVG build and out directory where everything will be stored
        OUTPUT : None
        """
        # check if outDir/matches exists, if not, create it.
        if not(os.path.isdir(outDir+'/matches')) :
            os.mkdir(outDir+'/matches')
        # create commands used to lauch the openMVG reconstruction
        commandCreateList = [omvgBuildDir+'/software/SfM/openMVG_main_CreateList','-i',imDir,'-d',omvgBuildDir+'/software/SfM/cameraGenerated.txt','-o',outDir+'/matches']
        if method=='long' :
            commandComputeMatches = [omvgBuildDir+'/software/SfM/openMVG_main_computeMatches','-i',imDir,'-o',outDir+'/matches','-g','f','-p','0.01','-r','0.8']
            commandIncremental = [omvgBuildDir+'/software/SfM/openMVG_main_IncrementalSfM','-i',imDir,'-m',outDir+'/matches','-o',outDir,'-c','1']
        else :
            commandComputeMatches = [omvgBuildDir+'/software/SfM/openMVG_main_computeMatches','-i',imDir,'-o',outDir+'/matches','-g','e','-p','0.01','-r','0.8','-s','1']
            commandIncremental = [omvgBuildDir+'/software/globalSfM/openMVG_main_GlobalSfM','-i',imDir,'-m',outDir+'/matches','-o',outDir,'-c','1']
        # Initializattion of the folderwatcher
        watcherPointCloud = QFileSystemWatcher()
        watcherPointCloud.addPath(outDir)
        # Connect the signal to the reconstruction launching method
        watcherPointCloud.directoryChanged.connect(self.pointCloudDetected)

        # lauch the reconstruction
        subprocess.call(commandCreateList)
        subprocess.call(commandComputeMatches)
        subprocess.call(commandIncremental)


    @pyqtSlot(str)
    def pointCloudDetected(self,filePath):
        # We send the newPointCloud signal only if the added file a .ply
        ext = os.path.splitext(filePath)[-1].lower()
        if (ext=="ply"):
            #Emit the signal
            self.newPointCloud.emit(filePath)
