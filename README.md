# data-spec-loupe

<img width="300" height="300" alt="Image" src="https://github.com/user-attachments/assets/91697ea5-8b37-4cb1-9069-b246cb662217" />

Easily and with little setup inspect your data that you see in your plots!!

## Installation

We are using mamba to install dependencies and python environment:
- `git clone --recurse-submodules https://github.com/Fafa87/data-spec-loupe.git`
- `cd data-spec-loupe`
- `mamba env create -f environment.yml`
- `mamba activate data-spec-loupe`
- `pip install -e external/napari-feature-visualization`

## Usage

The usage is designed to be very simple:
- prepare the data in given format (images folder and tsv)
- run cli or create explorer class

For example to show image from `example_data/views` corresponding to data from `example_data/data_tracked.tsv`:
```
python -m dataspecloupe.cli.gui example_data/views example_data/data_tracked.tsv 
```

### Explorer class 

It is the main class used to set up and control the napari viewer.  

Main features:
- specify subset of features to load and present


### Images data format (tif folders)

This is a simple hierarchy of folders for each channel, e.g. we can have 3 folder:
- `GFP`
- `Trans`
- `UNIQUE_LABEL` (required)

Each (e.g. Trans) having files named like:
- `view_0_channel_Trans.tif`
- `view_1_channel_Trans.tif`

Each of the folders is loaded as a separate layer in `napari`. Only `UNIQUE_LABEL` is loaded as a label layer rest as
image layer.

### Numerical data format (tsv)

There are only a few constrains and required fields - the rest is treated as a features with some being categorical and some treated as continuous numbers:
- identification fields
- features fields

### Data specification yaml (optional)

TODO - this allows to specify types of data columns (categorical / continuous)


## Example

There is a full usage example prepared for exploring the numerical data calculated on the MOMA dataset:
- original sample of the MoMA data:
  - https://github.com/junlabucsd/mother-machine-data/tree/main/external_data
  - https://drive.google.com/file/d/1YEvhkNB2lWOGFAuG1bmV7ZcwFE1FiDaR/view?usp=drive_link
- processed data (images and tsv):
  - https://drive.google.com/drive/folders/1MN2iOsjAyIdIGThpcx6QAK7Aj98sMecr?usp=sharing


<img width="1085" height="658" alt="Image" src="https://github.com/user-attachments/assets/7c4648b7-506c-414f-8edb-c4fe7fa42b2c" />


<img width="1083" height="660" alt="Image" src="https://github.com/user-attachments/assets/b9cb9a7b-fb30-41ed-84a0-e58ac372a995" />


## Roadmap

One thing to add would be to have an option to specify which features to show as points in napari. They will be placed
at the mean position of the selected feature.
