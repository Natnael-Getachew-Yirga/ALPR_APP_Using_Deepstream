# Automatic-License-Plate-Recognition(ALPR)-For-Traffic-Control-System

Deepstream aided car license plate number recognition system used for traffic control purpose

Automatic-License-Plate-Recognition(ALPR)-For-Traffic-Control-System is an embedded system that uses the deepstream SDK to flag vehicles that are registered in a database. The system works in real time to flag vehicles and show the frame of the vehicle information on a dashboard for the user.

This project is based on the opensource codes that are provided by NVIDIA's deepstream projects on https://github.com/NVIDIA-AI-IOT/deepstream_python_apps/tree/master/apps/deepstream-imagedata-multistream

This repository represents an ongoing open source research into utilizing NVIDA's Deepsteam SDK and different object detection algorithms to design and intellignet and adaptive traffic control sustem. All the code amd models are under research and development and subject to change.

Deepstream is selected for this project due to its computational performance and accuracy. The NVIDA's Deepstream model can be found from https://docs.nvidia.com/metropolis/deepstream/dev-guide/text/DS_Quickstart.html

This pipeline is based on three TLT models below

- Car detection model https://ngc.nvidia.com/catalog/models/nvidia:tlt_trafficcamnet
- LPD (car license plate detection) model https://ngc.nvidia.com/catalog/models/nvidia:tlt_lpdnet
- LPR (car license plate recognization/text extraction) model https://ngc.nvidia.com/catalog/models/nvidia:tlt_lprnet

More details for TLT3.0 LPD and LPR models and TLT training, please refer to [TLT document](https://docs.nvidia.com/metropolis/TLT/tlt-getting-started-guide/).

## Features

- Detect and count number of vehicles.
- Localize licence plate position of cars.
- Extract licence plate information from cars.
- Users are able to search for cars in real time by feeding information to the database and the system will flag the car with its associated information when the system detects the car in real time.
- Detect and count people.
- Detect road signs.

## Prerequisition

- [DeepStream SDK 5.1](https://developer.nvidia.com/deepstream-getting-started)

  Make sure deepstream-test1 sample can run successful to verify your DeepStream installation

- Opencv
- pymongo
- PyQt5
- numpy
- python 3.6 and above

To insall opencv, pymongo, numpy and PyQt5 run the following commands:

```
pip3 install opencv
pip3 install pymongo
pip3 install numpy
pip install PyQt5
```

## Prepare Models and TensorRT engine

Download repo:

```
    git clone https://github.com/preronamajumder/deepstream-lpr-python-version
```

Download models:

```
    cd deepstream_lpr_python_app
    //for us car plate
    ./download_us.sh
    //for chinese car plate
    ./download_ch.sh
```

Download tlt-converter:

Download x86 or Jetson tlt-converter which is compatible to your platform from the following links inside the folder.

| Platform | Compute     | Link                                                    |
| -------- | ----------- | ------------------------------------------------------- |
|          |
| Jetson   | JetPack 4.4 | [link](https://developer.nvidia.com/cuda102-trt71-jp44) |
| Jetson   | JetPack 4.5 | [link](https://developer.nvidia.com/cuda102-trt71-jp45) |

```
    wget <url>
    unzip <filename>
```

Convert LPR Model:  
DS5.0.1 gst-nvinfer cannot generate TRT engine for LPR model, so generate it with tlt-converter

```
    cd <foldername>
    chmod +x tlt-converter
    ./tlt-converter -k nvidia_tlt -p image_input,1x3x48x96,4x3x48x96,16x3x48x96 \
           ../models/LP/LPR/us_lprnet_baseline18_deployable.etlt -t fp16 -e ../models/LP/LPR/lpr_us_onnx_b16.engine
    cd ..
```

if you get the following:  
[WARNING] Half2 support requested on hardware without native FP16 support, performance will be negatively affected.  
Then use fp32 instead of fp16:

```
    ./tlt-converter -k nvidia_tlt -p image_input,1x3x48x96,4x3x48x96,16x3x48x96 \
           ../models/LP/LPR/us_lprnet_baseline18_deployable.etlt -t fp32 -e ../models/LP/LPR/lpr_us_onnx_b32.engine
    cd ..
```

## Build Parser

```
    cd nvinfer_custom_lpr_parser
    make
    cd ..
```

## Devices used

Devices used to implement the system are the following:

- NVIDIA Jetson nano
- IP camera

## Project directory

```
Project
|  README.MD
|__ALPR_APP
     |  deepstream_lpr_app.py
     |  trafficcamnet_config.txt
     |  lpr_confif_sgie_us.txt
     |  lpr_config_sgie_ch.txt
     |__models
         |__LP
              |__LPD
                  |  usa_lpd_cal.bin
                  |  Usa_pruned.etlt
              |__LPR
                  |  lpr_us_onnx_b16.engine
                  |  us_lprnet_baseline18_deployable.eltl
              |__ tlt_pretrained_models
                  |__trafficcamnet
                        |  resnet18_trafficcamnet_pruned.etlt
                        |  trafficnet_int8txt.txt
|__GUI
     |  GUI.py

```

## How to Run

To run the application run the following commands :

```
cd ALRP_APP_Using_Deepstream/GUI
python3 GUI.py

```
# Using Deepstream  Docker_container
To run the app on docker container refer about Deepstream docker_containers from the link below 
<br>https://docs.nvidia.com/metropolis/deepstream/dev-guide/text/DS_docker_containers.html

## Expected output after running the application

The username and password for the login age are "nerd" and "123456" respectively
## DEMO
#
 [![IMAGE ALT TEXT HERE](https://youtu.be/Wiu7k70ORow/0.jpg)](https://youtu.be/Wiu7k70ORow)[![Alternate Text]()]( )

#






More resourse :- https://medium.com/@karthickai/using-gstreamer-plugin-to-extract-detected-object-from-nvidia-deepstream-104879cc7154
