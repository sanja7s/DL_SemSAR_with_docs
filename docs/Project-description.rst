Project description
===================


In this project, we apply deep learning (DL) models to analyze SAR data.

Introduction
------------

Imagine you are given a satellite image and you need to tell apart the different types of land cover that it represents. If it is an optical image, human eye is pretty good at telling apart water from land, and from built areas, for instance. On SAR satellite images, this becomes a bit more difficult task (such as, telling apart swamp from a water surface). 

Such task is called **image segmenation** and there are established methods in traditional computer vision, and in particular, in SAR analytics to perform it. 

The task becomes infeasible for a human if it needs to be done on the scale of 100s or 1000s of images in a limited time. Traditional computer vision aproaches suffer from a similar issue as they need to be fine-tuned and adapted to particular datasets, i.e., the human input (from the experts) is still required.

However, deep learning aproaches have a potential to remove such bottlenecks by fully automating the segmentation process.

DL in computer vision
^^^^^^^^^^^^^^^^^^^^^

On image data, in general, the DL models perform one of the three main tasks:

- classifcation
- object detection and localization
- semantic segmentation

This project focuses on the third task, i.e., the semantic *segmentation of SAR images*.

Semantic segmentation
---------------------

.. _sem_seg:

Semantic segmentation aims at assigning each pixel of the image to an object or area class. Since the revolutionary Fully Convolutional Networks (FCN) paper by Long et al. [Long2015]_, almost all the state-of-the-art approaches on semantic segmentation are based on this paradigm.

After consulting existing reviews [Garcia2017]_ and [ReviewOnline2017]_, and performing our own literature review, we select a number of the state-of-the-art DL models for semantic segmentation and test their applicability on the SAR data in this project.


Datasets
--------

Training and test: SAR data
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Synthetic aperture radar (SAR) remote sensing systems are based on a radar installed on a moving platform, in our case the satellite. The radar system transmits electromagnetic waves with high power and receives the backscattered signal. Each transmitted pulse interacts with the Earth’s surface and only a portion of it is backscattered to the receiving antenna. The received signals are procesed to form a SAR image.

The advantages of SAR radars are that they can take images at any time of the day (also night) and at any weather unlike the optical remote sensing instruments.


Some well-known SAR satellites:
  - Sentinel-1
  - RadarSAT
  - Seasat
  - TerraSAR-X 
  - Geosat
  - **ICEYE X-1**
  - ...


Some challenges for remote sensing and, in particular, for SAR data analytics are that such data are georeferenced, often multi-modal, with particular imaging geometries and there are interpretation difficulties. Given that the current most advancent semantic segmentation DL methods are **supervised**, an additional challenge for DL on the SAR data is the lack of the *ground-truth* or *label data*.


Labels: Corine data
^^^^^^^^^^^^^^^^^^^

Supervised DL methods require a set of data with ground-truth information to learn from. For semantic segmentation, in particular, it means that we need images in which each pixel is assigned to its object or area class. Such datasets are rare even for the natural/real world images. 

The most important datasets for semantic segmentation, such as VOC2012 [VOC2012]_ and MSCOCO [MSCOCO]_ are crowdsourced and human-annotated, or completely synthetically created [Synthia2016]_.


Despite the lack of label data applicable for remote sensing in general, we were happy to discover the **Corine land cover mask** of Europe [Corine1985]_ initiated in 1985 and updated since then in 2000, 2006 and 2012. 

Corine is a program by the EU and stands for *coordination of information on the environment*. Corine masks provide labeled information for the type of land cover in the EU countries divided into over 40 classes. They are created using initial automatic extraction from the satellite data and additional human experts annotation. 


Deep learning models
--------------------

As discussed in Project Description, we start from the existing reviews on semantic segmentation approaches [Garcia2017]_ and [ReviewOnline2017]_, and also perform our own literature review in order to select the DL methods to test.

DL methods tested

- FC-DenseNets [FCDenseNets]_
- DeepLabV3+ [DeepLabV3plus]_
- U-Net [UNet]_
- PSPNet [PSPNet]_
- BiSeNet [BiSeNet]_
- SegNet [SegNet]_
- FRRN-B [FRRN-B]_


Other DL methods available in the SemSegm suite 

- DeepLabV3 [DeepLabV3]_
- GCN [GCN]_
- RefineNet [RefineNet]_
- ICNet [ICNet]_
- ...


References
----------

[FCDenseNets] Jégou, Simon, Michal Drozdzal, David Vazquez, Adriana Romero, and Yoshua Bengio. "The one hundred layers tiramisu: Fully convolutional densenets for semantic segmentation." In Computer Vision and Pattern Recognition Workshops (CVPRW), 2017 IEEE Conference on, pp. 1175-1183. IEEE, 2017.

[FRRN-B] Pohlen, Tobias, Alexander Hermans, Markus Mathias, and Bastian Leibe. "Full-resolution residual networks for semantic segmentation in street scenes." In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, pp. 4151-4160. 2017.

[SegNet] Badrinarayanan, Vijay, Alex Kendall, and Roberto Cipolla. "Segnet: A deep convolutional encoder-decoder architecture for image segmentation." IEEE transactions on pattern analysis and machine intelligence 39, no. 12 (2017): 2481-2495.

[BiSeNet] Yu, Changqian, Jingbo Wang, Chao Peng, Changxin Gao, Gang Yu, and Nong Sang. "Bisenet: Bilateral segmentation network for real-time semantic segmentation." In Proceedings of the European Conference on Computer Vision (ECCV), pp. 325-341. 2018.

[PSPNet] Zhao, Hengshuang, Jianping Shi, Xiaojuan Qi, Xiaogang Wang, and Jiaya Jia. "Pyramid scene parsing network." In Proceedings of the IEEE conference on computer vision and pattern recognition, pp. 2881-2890. 2017.

[UNet] Ronneberger, Olaf, Philipp Fischer, and Thomas Brox. "U-net: Convolutional networks for biomedical image segmentation." In International Conference on Medical image computing and computer-assisted intervention, pp. 234-241. Springer, Cham, 2015.

[DeepLabV3] Chen, Liang-Chieh, George Papandreou, Florian Schroff, and Hartwig Adam. "Rethinking atrous convolution for semantic image segmentation." arXiv preprint arXiv:1706.05587 (2017).

[RefineNet] Lin, Guosheng, Anton Milan, Chunhua Shen, and Ian Reid. "Refinenet: Multi-path refinement networks for high-resolution semantic segmentation." In IEEE Conference on Computer Vision and Pattern Recognition (CVPR). 2017.

[ICNet] Zhao, Hengshuang, Xiaojuan Qi, Xiaoyong Shen, Jianping Shi, and Jiaya Jia. "Icnet for real-time semantic segmentation on high-resolution images." arXiv preprint arXiv:1704.08545 (2017).

[DeepLabV3plus] Chen, Liang-Chieh, Yukun Zhu, George Papandreou, Florian Schroff, and Hartwig Adam. "Encoder-decoder with atrous separable convolution for semantic image segmentation." arXiv preprint arXiv:1802.02611 (2018).

[GCN] Peng, Chao, Xiangyu Zhang, Gang Yu, Guiming Luo, and Jian Sun. "Large Kernel Matters--Improve Semantic Segmentation by Global Convolutional Network." arXiv preprint arXiv:1703.02719 (2017).

[Long2015] Long, Jonathan, Evan Shelhamer, and Trevor Darrell. "Fully convolutional networks for semantic segmentation." In Proceedings of the IEEE conference on computer vision and pattern recognition, pp. 3431-3440. 2015.

[Garcia2017] Garcia-Garcia, Alberto, Sergio Orts-Escolano, Sergiu Oprea, Victor Villena-Martinez, and Jose Garcia-Rodriguez. "A review on deep learning techniques applied to semantic segmentation." arXiv preprint arXiv:1704.06857 (2017).

[ReviewOnline2017] A 2017 Guide to Semantic Segmentation with Deep Learning, online http://blog.qure.ai/notes/semantic-segmentation-deep-learning-review

[VOC2012] Visual Object Classes Challenge 2012 , online http://host.robots.ox.ac.uk/pascal/VOC/voc2012/

[MSCOCO] Microsoft Common Objects in Context, online http://cocodataset.org/#home

[Synthia2016] Ros, German, Laura Sellart, Joanna Materzynska, David Vazquez, and Antonio M. Lopez. "The synthia dataset: A large collection of synthetic images for semantic segmentation of urban scenes." In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, pp. 3234-3243. 2016.

[Corine1985] CORINE Land Cover, online https://land.copernicus.eu/pan-european/corine-land-cover

