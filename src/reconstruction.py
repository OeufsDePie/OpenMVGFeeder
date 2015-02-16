#!/usr/bin/python3
import subprocess,sys,os
from optparse import OptionParser

"""
main function aims at launching the openMVG reconstruction. Only works under Unix based system.
INPUT: paths to images, openMVG build and out directory where everything will be stored
OUTPUT : None
"""
def main(imDir,method,omvgBuildDir,outDir):

	# check if outDir/matches exists, if not, create it.
	if not(os.path.isdir(outDir+'/matches')) :
		os.mkdir(outDir+'/matches')
	# create commands used to lauch the openMVG reconstruction
	commandCreateList = ['./'+omvgBuildDir+'/software/SfM/openMVG_main_CreateList','-i',imDir,'-d',omvgBuildDir+'/software/SfM/cameraGenerated.txt','-o',outDir+'/matches']
	if method=='long' :
		commandComputeMatches = ['./'+omvgBuildDir+'/software/SfM/openMVG_main_computeMatches','-i',imDir,'-o',outDir+'/matches','-g','f','-p','0.01','-r','0.8']
		commandIncremental = ['./'+omvgBuildDir+'/software/SfM/openMVG_main_IncrementalSfM','-i',imDir,'-m',outDir+'/matches','-o',outDir,'-c','1']
	else :
		commandComputeMatches = ['./'+omvgBuildDir+'/software/SfM/openMVG_main_computeMatches','-i',imDir,'-o',outDir+'/matches','-g','e','-p','0.01','-r','0.8','-s','1']
		commandIncremental = ['./'+omvgBuildDir+'/software/globalSfM/openMVG_main_GlobalSfM','-i',imDir,'-m',outDir+'/matches','-o',outDir,'-c','1']
	# lauch the reconstruction
	subprocess.call(commandCreateList)
	subprocess.call(commandComputeMatches)
	subprocess.call(commandIncremental)

if __name__ == "__main__":
	# create the parser : allow user to use this python script with arguments
	parser = OptionParser()
	parser.add_option('-i', '--imgDir', action='store',dest='im',
		          type='string',help='image directory', metavar='IMDIR')
	parser.add_option('-m', '--method', action='store', dest='method', default='long',
		          type='string',help='method used for the reconstruction (long or short)',metavar='METHOD')
	parser.add_option('-b', '--buildDir', action='store', dest='build',
		          type='string',help='openMVG_Build directory',metavar='BUILDDIR')
	parser.add_option('-o', '--outDir', action='store', dest='out',
			  type='string',help='out directory for the reconstruction',metavar='OUTDIR')
	(opts, args) = parser.parse_args()
	
	if opts.im==None or not(os.path.exists(opts.im)) :
		parser.error('You must specify a correct image directory, use --help option...')
	if opts.build==None or not(os.path.exists(opts.build)) :
		parser.error('You must specify a correct openMVG build directory, use --help option...')
	if opts.out==None or not(os.path.exists(opts.out)) :
		parser.error('You must specify a correct out directory, use --help option...')
	if not(opts.method in ('long','short')) :
		parser.error("Method must be either long or short, use --help option...")	
	
	# normalisation of paths specified by user
	opts.im = os.path.relpath(opts.im)
	opts.build = os.path.relpath(opts.build)
	opts.out = os.path.relpath(opts.out)
	
	# lauch the main function
	main(opts.im,opts.method,opts.build,opts.out)
