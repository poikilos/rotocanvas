# PyRotoCanvas
https://github.com/poikilos/pyrotocanvas

This project may serve as a backend or companion or replacement for the
[RotoCanvasPaint](https://github.com/poikilos/RotoCanvasPaint), project
where you can find more information about the goals and scope of the
project.

## Requires
- opencv for certain features such as AI super resolution
  - See tests/rcsource_tests.py under `except ImportError` for how to
    install it.
- pretrained models
  - Before using super resolution methods, you must add pb files via:
    ```
from RCSettings import settings
settings.addModel(pbFilePath)
```


## Tasks
- [ ] for upscaling VHS (tested using Rebel Assault IX), use one of the
  following G'MIC plugins after upscaling:
  - "Sharpen [Richardson-Lucy]"; Sigma: 1.25; Iterations: 10 (default);
    Blur: Gaussian (default); cut: True (default)
  - Sharpen [Octave Sharpening]; Parallel Processing: Four Threads (or
    more--use a global setting); (others: default)
  - Simple Local Contrast (seems to add noise or false detail, but may
    be ok); Edge Sensitivity: 4.05; Iterations: 1; (others: default)
- [ ] Try making the "Smart Sharpening" tutorial into a script:
  https://www.gimp.org/tutorials/Smart_Sharpening/
- [ ] Try TecoGAN
  - Docker version: https://github.com/tom-doerr/TecoGAN-Docker
- [ ] Try enhancenet-pretrained:
  ~/Videos/Demo_Reel-Recovered-SD_but_2nd_Gen/enhancenet_pretrained/
- [ ] Try RealSR (requires Vulkan):
```
wget https://github.com/nihui/realsr-ncnn-vulkan/releases/download/20200818/realsr-ncnn-vulkan-20200818-linux.zip
unzip realsr-ncnn-vulkan-20200818-linux.zip
cd realsr-ncnn-vulkan-20200818-linux
mkdir -p $HOME/bin/realsr-ncnn-vulkan-models
cp -r models-DF2K models-DF2K_JPEG $HOME/bin/realsr-ncnn-vulkan-models
cp realsr-ncnn-vulkan $HOME/bin
```
  -<https://linuxreviews.org/RealSR#Installation>
- [ ] Automatically download models from [ONNX Model
  Zoo](https://github.com/onnx/models) (OpenCV allows loading ONNX
  models via `cv2.dnn.readNetFromONNX(`--See [Super Resolution with
  OpenCV](https://bleedai.com/super-resolution-with-opencv/))

## Authors

### super_res_image_save
super_res_image_save is based on super_res_image.py
  by Adrian Rosebrock (conformed to PEP8 by Jake "Poikilos" Gustafson)

[OpenCV Super Resolution with Deep
Learning](https://www.pyimagesearch.com/2020/11/09/opencv-super-resolution-with-deep-learning/)
by Adrian Rosebrock on November 9, 2020

I requested for the Wayback Machine to archive it:
- [snapshot](https://web.archive.org/web/20201109211028/https://www.pyimagesearch.com/2020/11/09/opencv-super-resolution-with-deep-learning/)
- [screen shot](https://web.archive.org/web/20201109211028/http://web.archive.org/screenshot/https://www.pyimagesearch.com/2020/11/09/opencv-super-resolution-with-deep-learning/)

> ...there are super resolution deep neural networks that are both:
>
> 1. Pre-trained (meaning you don’t have to train them yourself on a dataset)
> 2. Compatible with OpenCV
> However, OpenCV’s super resolution functionality is actually “hidden”
> in a submodule named in `dnn_superres` in an obscure function called
> `DnnSuperResImpl_create`.


> Photoshop, GIMP, Image Magick, OpenCV (via the cv2.resize function),
> etc. all use classic interpolation techniques and algorithms (ex.,
> nearest neighbor interpolation, linear interpolation, bicubic
> interpolation)

Related methods and corresponding papers:
> - _**EDSR:** [Enhanced Deep Residual Networks for Single Image Super-Resolution](https://arxiv.org/abs/1707.02921) ([implementation](https://github.com/Saafke/EDSR_Tensorflow))_
> - **ESPCN:** _[Real-Time Single Image and Video Super-Resolution Using an Efficient Sub-Pixel Convolutional Neural Network](https://arxiv.org/abs/1609.05158)_ ([implementation](https://github.com/fannymonori/TF-ESPCN))
> - **FSRCNN:** _[Accelerating the Super-Resolution Convolutional Neural Network](https://arxiv.org/abs/1608.00367)_ ([implementation](https://github.com/Saafke/FSRCNN_Tensorflow))
> - **LapSRN:** _[Fast and Accurate Image Super-Resolution with Deep Laplacian Pyramid Networks](https://arxiv.org/abs/1710.01992)_ ([implementation](https://github.com/fannymonori/TF-LAPSRN))
> A big thank you to Taha Anwar from BleedAI for putting together
> [his guide](https://bleedai.com/super-resolution-going-from-3x-to-8x-resolution-in-opencv/)
> on OpenCV super resolution, which curated much of this information —
> it was immensely helpful when authoring this piece.


## Developer Notes

### RCSource
- if `_first` is `None`, it is a single image.
  - Use `self.os.path.split(self._vidPathNoExt)[1]` not `_prefix` to
    generate a name (along with `self._ext`).
  - `self.getFrameName` will still work but will always return the same
    image file name.

### First-time Setup of This Repo
(running some of these steps again may not be necessary)

```
#python3 -m pip install --user virtualenv
REPO_PATH=`pwd`
python3 -m venv ../opencvenv
source ../opencvenv/bin/activate
pip install opencv-contrib-python
# Rosebrock recommends `pip install opencv-contrib-python==4.1.0.25`
# at https://www.pyimagesearch.com/2018/09/19/pip-install-opencv/
# pip install --upgrade pip
mkdir ../super-resolution-implementations
cd ../super-resolution-implementations
git clone https://github.com/Saafke/EDSR_Tensorflow.git
git clone https://github.com/fannymonori/TF-ESPCN.git
git clone https://github.com/Saafke/FSRCNN_Tensorflow.git
git clone https://github.com/fannymonori/TF-LAPSRN.git
cd $REPO_PATH
cd ..
REPOS_PATH=`pwd`
cd $REPO_PATH
mkdir models
ln -s $REPOS_PATH/super-resolution-implementations/EDSR_Tensorflow/models/EDSR_x4.pb models/
ln -s $REPOS_PATH/super-resolution-implementations/TF-ESPCN/export/ESPCN_x4.pb models/
ln -s $REPOS_PATH/super-resolution-implementations/FSRCNN_Tensorflow/models/FSRCNN_x3.pb models/
ln -s $REPOS_PATH/super-resolution-implementations/TF-LAPSRN/export/LapSRN_x8.pb models/

deactivate
```
