# MW-HEALPix
---
This repository contains all the code relevant to running HEALPix as part of the Multiwave Demonstrator Case.


## Introduction


Need to include the purpose of the code in the repo
A description of the repo and and the code in it

## Hardware and Software




## Directory Structure

When the code is run the first argument is a working directory. Within this directory the code is expecting to find a `/Data` directory, under which the outputs will appear in the `/hp` directory. 

As the following arguments are the input catalogues these should be stored in the `/Data` directory.

```bash

working_directory
├── Data
│   ├── hp
│   │ 

```



## Inputs and outputs

*The inputs are:*

The code currently takes in four inputs. These are:

1.	The base directory you wish to work from
2.	The optical catalogue to healpix stored in your `/Data` directory
3.	The radio catalogue to healpix stored in your `/Data` directory
4.	The radio Gaussian catalogue to healpix stored in your `/Data` directory

A `/Data` directory will need to exist to run the code as this is where the outputs will go, but if the inputs are somewhere else that is fine. Just be aware this will change the input pathways that you type.

*The outputs are:*

The output of the healpix code is currently saving to `/yourbase/projectarea/Data/hp/`. The `/hp` folder is created and the `/Data` folder is expected to already exist. You will have to go into the script and change the word `Data`, if you want it to save to a different folder, within your “working from directory”.

There are currently six catalogues outputted, where hp# is the number of the healpix region:

1.	radio_hp#.fits		The radio catalogue of all sources in healpix region
2.	gaussian_hp#.fits	The radio catalogue of all Gaussians in healpix region
3.	optical_hp#.fits	The optical catalogue of all sources in healpix region
4.	radio_hp#_nn.fits	The radio catalogue of all sources in healpix region and nearest neighbour regions
5.	gaussian_hp#_nn.fits	The radio catalogue of all Gaussians in healpix region and nearest neighbour regions
6.	optical_hp#_nn.fits	The optical catalogue of all sources in healpix region and nearest neighbour regions


Within each radio source catalogue (radio_hp# and radio_hp#_nn) there is a column `rhpix`, which contains the healpix region number associated to the source.
Within each radio Gaussian catalogue (gaussian_hp# and gaussian_hp#_nn) there is a column `ghpix`, which contains the healpix region number associated to the source.
Within each optical source catalogue (optical_hp# and optical_hp#_nn) there is a column `ohpix`, which contains the healpix region number associated to the source.

When it runs it will print onscreen which catalogues have been created, and which already exist. If a catalogue already exists, the code does not re-create it.



## Running MW-HEALPix




## Future Work


The code maybe adjusted so that it creates directories for each HEALPix area. This would mean that the six output catalogues would go into an individual directory, identified by HEALPix number, inside the original output directory. This change maybe added as a way to allow for easier batching in step further down the pipeline.


## External links

*The relevant Jira tickets are as follows:*

* [TEAL-685: Initial HEALPix Code](https://jira.skatelescope.org/browse/TEAL-745)
    * This ticket looks at the creation of the above HEALPix code
* [TEAL-685: Explore HEALPix Areas for LR](https://jira.skatelescope.org/browse/TEAL-685)
    * This ticket looks at the initial work done into using the HEALPix areas in the likelihood ratio code


## List of developers and Collaborators


Barkus, B.

Hardcastle, M. J.
