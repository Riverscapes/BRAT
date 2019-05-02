---
title: Step 7 - BRAT Combined Dam Capacity Model
weight: 9
---

After running the Vegetation Dam Capacity Model, you can run the Combined Dam Capacity Model tool.  This fuzzy inference system model predicts the maximum number of dams each reach could support based on 4 inputs: 1) the output of the vegetation dam capacity model 2) the low (base) flow stream power, 3) the high flow (Q2) stream power, and 4) the slope of the reach.  The model predicts dam capacity separately for historic vegetation dam capacity and existing vegetation dam capacity.

![comb_fis]({{ site.baseurl }}/assets/images/comb_fis.PNG)

Inputs and Parameters:

- **Select Project Folder** - path to the BRAT project folder
- **Input BRAT Network** - select the BRAT network that you have been using up to this point
- **Maximum DA Threshold** - this is a drainage area value above which it is assumed that the stream is too large for beaver to build dams on.  This varies from region to region and should be adjusted according to the hydrologic characteristics of the study area.
- **Save Output Network** - choose a location and name to save the output

The output network will be placed in a new folder in `Output_##` called `02_Analyses`. The output network will have the new fields `oCC_HPE` (historic combined dam capacity) and `oCC_EX` (existing combined dam capacity).  When the tool finishes running the second time it should automatically add the output to the map and symbolize the `oCC_EX` field, which represents the existing capacity to support dam building activity.

The fields `oCC_HPE` and `oCC_EX` are split into the following categories for our symbology:

- None: 0 dams
- Rare: 0-1 dams/km
- Occasional: 1-5 dams/km
- Frequent 5-15 dams/km
- Pervasive: 15-40 dams/km

Layers are created with these symbologies in the folder `01_Capacity`, which is placed in `02_Analyses`.



[![output]({{ site.baseurl }}/assets/images/output.PNG)]({{ site.baseurl }}/assets/images/hr/output.PNG)

<div align="center">
	<a class="hollow button" href="{{ site.baseurl }}/Documentation/Tutorials/StepByStep/6-BRATVegetationFIS"><i class="fa fa-arrow-circle-left"></i> Back to Step 6 </a>
	<a class="hollow button" href="{{ site.baseurl }}/Documentation/Tutorials/StepByStep/8-DataValidation"><i class="fa fa-arrow-circle-right"></i> Continue to Step 8 </a>
</div>	

------
<div align="center">

	<a class="hollow button" href="{{ site.baseurl }}/Documentation"><i class="fa fa-info-circle"></i> Back to Help </a>
	<a class="hollow button" href="{{ site.baseurl }}/"><img src="{{ site.baseurl }}/assets/images/favicons/favicon-16x16.png">  Back to BRAT Home </a>  
</div>
