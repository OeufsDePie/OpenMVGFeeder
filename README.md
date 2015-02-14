# OpenMVGFeeder
Python script to manipulate openMVG

## OpenMVG compilation


First, download openMVG source as a submodule from github :

```
git submodule update --init --recursive
```

Then follow the instruction from the *BUILD* file in the openMVG folder. In summary, here is what you have to do :

```
sudo apt-get install libpng-dev libjpeg-dev libtiff-dev libxxf86vm1 libxxf86vm-dev libxi-dev libxrandr-dev
```

```
git clone --recursive https://github.com/openMVG/openMVG.git
```

```
cd openMVG
```

```
ls
```

```
AUTHORS BUILD  docs  logo  README  src  ...
```

```
cd ..
```

```
mkdir openMVG_Build
```

```
cd openMVG_Build
```

```
cmake -DCMAKE_BUILD_TYPE=RELEASE . ../openMVG/src/
```

```
make -j *NBCORE*
```

## How to use reconstruction.py
You must specify several directories to run the **python 3** script :

* -i : image directory
* -s : openMVG source directory
* -b : openMVG build directory
* -o : out directory where everything will be stored
* -m : optional arguement to specify long or short method for the reconstruction

