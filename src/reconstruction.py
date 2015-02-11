#!/usr/bin/python3
import subprocess,sys,os
from optparse import OptionParser

def main(imDir,method,omvgBuilDir,omvgSrcDir,outDir):


	commandCreateList = ['./'+omvgBuilDir+'/software/SfM/openMVG_main_CreateList','-i',imDir,'-d',omvgSrcDir+'/src/software/SfM/cameraSensorWidth/cameraGenerated.txt','-o',outDir+'/matches']
	if method=='long' :
		commandComputeMatches = ['./'+omvgBuilDir+'/software/SfM/openMVG_main_computeMatches','-i',imDir,'-o',outDir+'/matches','-g','f','-p','0.01','-r','0.8']
		commandIncremental = ['./'+omvgBuilDir+'/software/SfM/openMVG_main_IncrementalSfM','-i',imDir,'-m',outDir+'/matches','-o',outDir,'-c','1']
	else :
		commandComputeMatches = ['./'+omvgBuildDir+'/software/SfM/openMVG_main_computeMatches','-i',imDir,'-o',outDir+'/matches','-g','e','-p','0.01','-r','0.8','-s','1']
		commandIncremental = ['./'+omvgBuildDir+'/software/globalSfM/openMVG_main_GlobalSfM','-i',imDir,'-m',outDir+'/matches','-o',outDir,'-c','1']

	subprocess.call(commandCreateList)
	subprocess.call(commandComputeMatches)
	subprocess.call(commandIncremental)

if __name__ == "__main__":
	parser = OptionParser()
	parser.add_option('-i', '--imgDir', action='store',dest='im',
		          type='string',help='image directory', metavar='IMDIR')
	parser.add_option('-m', '--method', action='store', dest='method', default='long',
		          type='string',help='method used for the reconstruction (long or short)',metavar='METHOD')
	parser.add_option('-b', '--buildDir', action='store', dest='build',
		          type='string',help='openMVG_Build directory',metavar='BUILDDIR')
	parser.add_option('-s', '--srcDir', action='store', dest='src',
		          type='string',help='openMVG (source from github) directory',metavar='SRCDIR')
	parser.add_option('-o', '--outDir', action='store', dest='out',
			  type='string',help='out directory for the reconstruction',metavar='OUTDIR')
	(opts, args) = parser.parse_args()
	
	if opts.im==None or not(os.path.exists(opts.im)) :
		parser.error('You must specify a correct image directory, use --help option...')
	if opts.build==None or not(os.path.exists(opts.build)) :c
		parser.error('You must specify a correct openMVG build directory, use --help option...')
	if opts.src==None or not(os.path.exists(opts.src)) :
		parser.error('You must specify a correct openMVG source directory, use --help option...')
	if opts.out==None or not(os.path.exists(opts.out)) :
		parser.error('You must specify a correct out directory, use --help option...')
	if not(opts.method in ('long','short')) :
		parser.error("Method must be either long or short, use --help option...")	
	
	opts.im = os.path.relpath(opts.im)
	opts.src = os.path.relpath(opts.src)
	opts.build = os.path.relpath(opts.build)
	opts.out = os.path.relpath(opts.out)

	main(opts.im,opts.method,opts.build,opts.src,opts.out)
