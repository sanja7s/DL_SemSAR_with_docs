How To Use This Repo
====================


Project structure
-----------------
* data
* src
* manuscript
* build
* docs

The description of the structure and processing steps follows.



Datasets
^^^^^^^^
* data

  * SAR_preprocess
  * DL_models
  * DL_output
  * DL_prepare


The *data* folder holds all the data used in the project. Below, we discuss each of the subfolders under it.

SAR preprocessing
"""""""""""""""""
_SARprep:
* SAR_preprocess

	* orig-data
	* RES
	* finn_dem_WGS84.tif

This folder holds the data needed for the first step in the pipeline, i.e., for SAR data preprocessing. In this step, we take SAR images with two polarisation channels (single, such as HH or VV and cross-pol, such as HV and VH) and multilook, calibrate, terrain-flatten and terrain-correct them. Finally, we produce the resulting RGB composites of them so that each of the *Gamma0* channels is saved in the first two bands, and the corresponding digital elevation model (DEM) is saved in the last band.

*SAR_preprocess* holds original SAR images in *orig-data* and the DEM model *finn_dem_WGS84.tif* used for the terrain correction. 

SAR image preprocessing is performed using the ESA *snap tool*. The preprocessing graph *SAR_preprocessing_Graph_v1.xml*, which can be used by the tool, is found under *src/SAR-data-preprocess/code_snap*. You can perform the preprocessing by first opening the downloaded SAR images in SNAP (you can open even without decompressing them, i.e., in the original *.zip* format). Then select *Tools -> Batch Processing* and press the second "+" sign from the top to populate the batch with all the images. After that, press *Load Graph* and open the graph file *SAR_preprocessing_Graph_v1.xml*. Make sure that the output directory points to *SAR_preprocess/RES* on your machine and that the type of output files selected under *Save as:* is *GeoTIFF-BigTIFF*. This is needed because the processing graph creates large RGB composites, the size of which is often more then 4GB. Then press *Run*. Depending on the number of input images and your machine, this might take several hours.

After they are produced, the resulting RGB composite tiff files can be MOVED TO *DL_prepare/prepared-SAR-tiffs* for the additional preprocessing step required by the DL models.

Preprocesing for DL
"""""""""""""""""""
* DL_prepare

	* Corine
	* cropped-SAR-tiffs
	* labels
	* prepared-SAR-tiffs
	* train

It is generally a good idea to prepare the images for the DL models in the following way. Most of the models expect square-shaped images, so we crop each tiff file into a number of square pieces that have the size around 1000x1000 pixels, but not smaller then 800 pixels in any of the dimensions (the number is chosen in our case also because of the limitation of the GPU computing resources, and it can be changed on other machines). 

Converting SAR band values into *decibels* is a regular SAR preprocessing step, however, due to a more convenient implementation like this, we perform that step under preprocessing for DL.
In addition, each band should be *normalized* so that the distribution of the pixel values would resemble a Gaussian distribution centered at zero. This makes convergence faster while training the DL models. Data normalization is done by subtracting the mean from each pixel, and then dividing the result by the standard deviation. In addition, given that our DL models expect pixel values in the range (0,255), we then apply *scaling* the normalized data to that range. Such preprocessed data are then found in the folder *train*.

Also, we need to provide the labels for each training/test image, and this is done by cropping corrsponding pieces of the Corine mask (found in the folder *Corine*). The pieces should correspond to the geographic area of the respective train/test images. Resulting label images are stored in the folder *labels*. Note that training/test images and corresponding labels have *exactly the same names*, as that is what the DL models suite we use expects for their input.

Finally, the ready data are fed into *DL_models* directory using the script *divide_train_test.py*. This scripts will split the data into train, test, and validation sets.

Deep Learning models
""""""""""""""""""""
* DL_models

	* Semantic-Segmentation-Suite


All the models that we use come from the `Semantic Segmentation Suite GitHub repository <https://github.com/GeorgeSeif/Semantic-Segmentation-Suite>`_. 

In order for one to use this semantic segmentation suite, the data should be placed in a folder within the root directory *Semantic-Segmentation-Suite* (we call this folder *Corine-Sentinel-DEM*) and structured as follows:

* Semantic-Segmentation-Suite/Corine-Sentinel-DEM
	* test
	* test-labels
	* train
	* train-labels
	* val
	* val-labels
	* class_dict.csv

Invoking the script *src/prepare-data-for-DL/divide_train_test.py* populates the folder structure above. The file *class_dict.csv* provides the mapping between the class names and the label rgb colors.

With such a structure ready, we can invoke and test a number of the algorithms available under the suite using its *main.py* script with the appropriate arguments. The *Readme* file of the *Semantic-Segmentation-Suite* itself provides more information on this for each model.


Deep Learning Results
"""""""""""""""""""""
* DL_output

	* orig
	* gt
	* pred

Once you have developed and tested the models, you can receive results of the best/selected among them to the folder *DL_output*. This is done by invoking the script *src/postprocess-DL-res/georef_results.sh*, which in addition to copying select outputs also georefernces the results (prediction outputs) so that we can visualize them using GIS tools. 


Source code
^^^^^^^^^^^
* src

	* postprocess-DL-res
	* prepare-data-for-DL
	* SAR-data-preprocess

SAR data preprocessing 
""""""""""""""""""""""
This folder holds only the .xml file for the processing graph to be used in SNAP, as described under SAR preprocessing.


Preparing data for DL 
"""""""""""""""""""""
* prepare-data-for-DL

	* main.py
	* ...
	* divide_train_test.py

Invoking *main.py* will run the preprocessing steps described above (see Preprocesing for DL), and invoking *divide_train_test.py* will place those data in the right folder and proportions under *Semantic-Segmentation-Suite/Corine-Sentinel-DEM*.


Postprocessing data after DL
""""""""""""""""""""""""""""
* postprocess-DL-res

The script *georef_and_copy_results.py* will georefernce results (prediction .pngs) and place them under *data/DL_output*. It will also crop the test files to the same dimensions as the predicitons (1024x1024) and copy all to corresponding folders in *DL_output*.




Documentation
^^^^^^^^^^^^^
* docs

  * _build
  * _static
  * _templates
  * conf.py
  * .txt



The *docs* folder holds resources for this documentation you are reading. We use *sphinx* + *.rst* to create it. In *_build* you can find the root documentation file *index.html*. Starting from it, you get the links to the rest of the documentation.




