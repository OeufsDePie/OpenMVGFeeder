# OpenMVGFeeder
Python script to manipulate openMVG

To clone the repository, use the `--recursive` option to download submodules as well :

```
git clone --recursive https://github.com/OeufsDePie/OpenMVGFeeder.git
``` 

## OpenMVG compilation

Follow the instruction from the *BUILD* file in the openMVG folder. In summary, here is what you have to do :

```
sudo apt-get install libpng-dev libjpeg-dev libtiff-dev libxxf86vm1 libxxf86vm-dev libxi-dev libxrandr-dev
```

Check if all files have been downloaded and compile openMVG : 

```
cd openMVG
ls
AUTHORS BUILD  docs  logo  README  src  ...
cd ..
mkdir openMVG_Build
cd openMVG_Build
cmake -DCMAKE_BUILD_TYPE=RELEASE . ../openMVG/src/
make -j NBCORE
```
Now copy cameraGenerated.txt from the openMVG source folder :
```
cp ../openMVG/src/software/SfM/cameraSensorWidth/cameraGenerated.txt .
```
You can now safely delete the openMVG folder since we won't be using it again :
```
rm -r ../openMVG
```
You are now all set to use **openMVG** from the **openMVG_Build** directory. 

## How to use reconstruction.py
You must specify several directories to run the **python 3** script :

* -i : image directory
* -s : openMVG source directory
* -b : openMVG build directory
* -o : out directory where everything will be stored
* -m : optional arguement to specify long or short method for the reconstruction

