import subprocess,sys,os,shutil
from optparse import OptionParser
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot,QFileSystemWatcher

class ReconstructionManager(QObject):
    # Signal initialisation
    # This signal is launched when a new ply is detected
    newPointCloud = pyqtSignal(str)

    def __init__(self):
        QObject.__init__(self)
        self.listPly = []
        # Initializattion of the folderwatcher
        self.watcherPointCloud = QFileSystemWatcher()
        # Connect the signal to the reconstruction launching method
        self.watcherPointCloud.directoryChanged.connect(self.pointCloudDetected)

    @pyqtSlot(str, str, str, str, str)
    def launchReconstruction(self,imDir,method,omvgBuildDir,outDir,pointCloudDir):
        """
        launchReconstruction function aims at launching the openMVG reconstruction. Only works under Unix based system.
        INPUT: paths to images, openMVG build and out directory where everything will be stored
        OUTPUT : None
        """
        self.pointCloudDir = pointCloudDir
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

        self.watcherPointCloud.addPath(outDir)

        # lauch the reconstruction
        subprocess.call(commandCreateList)
        subprocess.call(commandComputeMatches)
        subprocess.call(commandIncremental)

    def pointCloudDetected(self,dirPath):
        newPLYs = self.newPly(dirPath) 
        # We send the newPointCloud signal only if the added file a .ply
        if newPLYs:
            for ply in newPLYs:
                # Copy the resulting ply in the pointClouddir and
                # determine the new path
                shutil.copy(ply, self.pointCloudDir)
                path = os.path.join(self.pointCloudDir, os.path.basename(ply))
                #Emit the signal
                self.newPointCloud.emit(path)

    def newPly(self, dirPath):
        """ Return the new PLY files"""
        newPlyList = os.listdir(dirPath)
        # Transform file list in path list
        newPlyList = [os.path.join(dirPath, ply) for ply in newPlyList]
        # Filter only ply files
        endInPly = lambda path: os.path.splitext(path)[-1].lower() == ".ply"
        newPlyList = [ply for ply in newPlyList if endInPly(ply)] 
        oldPlyList = self.listPly.copy()
        # update the list
        self.listPly = newPlyList

        # Is there new files ?
        newPlyList = list(set(newPlyList).difference(set(oldPlyList)))

        return newPlyList
