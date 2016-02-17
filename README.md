# Library to track Robots via Webcam

## Installing OpenCV
- Install requirements
- `sudo apt-get install build-essential`
- `sudo apt-get install cmake git libgtk2.0-dev pkg-config
     libavcodec-dev libavformat-dev libswscale-dev`
- `sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev
     libjpeg-dev libpng-dev libtiff-dev libjasper-dev
     libdc1394-22-dev`
- Clone the repositories
- `cd ~/`
- `git clone https://github.com/itseez/opencv`
- `git clone https://github.com/itseez/opencv_contrib`
- `cd opencv`
- `mkdir build && cd build`
- `cmake -D CMAKE_BUILD_TYPE=Release -D
   CMAKE_INSTALL_PREFIX=/usr/local -D
   OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules ..`
- `make -j4`
- `sudo make install`

### Testing OpenCV
- `cd ~/`
- `git clone git:itseez/opencv_extra`
- `export OPENCV_TEST_DATA_PATH=~/opencv_extra`
- `cd ~/opencv/build/bin/`
- `./opencv_test_core`
