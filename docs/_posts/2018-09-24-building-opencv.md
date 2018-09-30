---
title:   "Building OpenCV on MacOSX High Sierra with Python3, QT and contrib"
date:    2018-09-24 12:24:10 +0200
excerpt:
    Homebrew stopped supporting configurable OpenCV source builds and I
    need QT and contrib.
---
At the time of writing this, I had actually successfully built and installed
OpenCV earlier but after havimg upgraded brew packages at some time or other,
the version I had built stopped working due to no longer having access to
an old version of libhdf5.

I have cloned the [OpenCV](https://github.com/opencv/opencv) and
[OpenCV contrib](https://github.com/opencv/opencv_contrib) repos. In this
particular case, I also want to go from version 3.4.2 to 3.4.3.


First, make sure we have the necessary dependencies, although I'm not quite
sure the below covers everything we need.

```
brew install eigen ffmpeg harfbuzz hdf5 lapack libpng libsvg libtiff numpy
     openblas openjpg python qt tbb
```

Now, retrieve and checkout the 3.4.3 branch in the opencv repo

```
cd opencv
git checkout master
git pull
git checkout 3.4.3
git checkout -b my-3.4.3
```

Then we do the same thing for contrib

```
cd ../opencv_contrib
git checkout master
git pull
git checkout 3.4.3
git checkout -b my-3.4.3
cd ../opencv
```

I have previously setup a virtualenv with `pyenv` for Python 3.7.0 and pip
installed `numpy`, `imutils` and `pyyaml`

```
pyenv activate opencv
```

In the opencv repo, if this is not an upgrade

````
mkdir build
cd build
vim build.sh
```

where `build.sh` should contain

```
PREFIX_MAIN=`pyenv virtualenv-prefix`
PREFIX=`pyenv prefix`
cmake .. \
    -DCMAKE_BUILD_TYPE=RELEASE \
    -DCMAKE_INSTALL_PREFIX="$PREFIX" \
    -DOPENCV_ENABLE_NONFREE=ON \
    -DWITH_OPENGL=ON \
    -DWITH_OPENVX=ON \
    -DWITH_QT=ON \
    -DWITH_OPENCL=ON \
    -DBUILD_PNG=ON \
    -DBUILD_TIFF=ON \
    -DOPENCV_EXTRA_MODULES_PATH=~/src/opencv_root/opencv_contrib/modules \
    -DWITH_1394=OFF \
    -DWITH_AVFOUNDATION=ON \
    -DWITH_QUICKTIME=OFF \
    -DWITH_CUDA=OFF \
    -DBUILD_opencv_python2=OFF \
    -DBUILD_opencv_python3=ON \
    -DPYTHON3_EXECUTABLE="$PREFIX"/bin/python3.7 \
    -DPYTHON3_PACKAGES_PATH="$PREFIX"/lib/python3.7/site-packages \
    -DPYTHON3_LIBRARY="$PREFIX_MAIN"/lib/libpython3.7m.dylib \
    -DPYTHON3_INCLUDE_PATH="$PREFIX_MAIN"/include/python3.7m \
    -DPYTHON3_NUMPY_INCLUDE_DIRS="$PREFIX"/lib/python3.7/site-packages/numpy/core/include
\
    -DINSTALL_C_EXAMPLES=OFF \
    -DINSTALL_PYTHON_EXAMPLES=OFF \
    -DINSTALL_NAME_DIR="${CMAKE_INSTALL_PREFIX}/lib"
```

Now, better be safe than sorry (external dependencies might have changed
since we built last time)

```
rm CMakeCache.txt
make clean
```

and then

```
./build.sh
make install
```

Test the install by running

```
$ python
Python 3.7.0 (default, Jul 31 2018, 23:01:49)
[Clang 6.0.1 (tags/RELEASE_601/final)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import cv2
>>> import numpy as np
>>> cv2.namedWindow("image", cv2.WINDOW_NORMAL)
>>> cv2.imshow("image", np.array([0, 128, 255]))
>>> cv2.waitKey(0)
```

If the QT window shows up -- success!
