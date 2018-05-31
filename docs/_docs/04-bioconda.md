---
title: "Using Bioconda and packages with PIe"
permalink: /docs/bioconda/
excerpt: "Using bioconda to install bioinformatics tools."
last_modified_at: 2018-05-31T15:12:19-04:00
redirect_from:
  - /theme-setup/
toc: true
---
# Bioconda

This tutorial assumes you will be using a Linux distribution.

**Please refer to [Bioconda](https://bioconda.github.io/) website for more information.**

### Setting bioconda

After installing conda you will need to add the bioconda channel as well as the
other channels bioconda depends on. **It is important to add them in this
order** so that the priority is set correctly (that is, bioconda is highest
priority).

The `conda-forge` channel contains many general-purpose packages not already
found in the `defaults` channel. The `r` channel is only included due to
backward compatibility.  It is not mandatory, but without the `r` channel
packages compiled against R 3.3.1 might not work.

```bash
conda config --add channels defaults
conda config --add channels conda-forge
conda config --add channels bioconda
```

### Install Packages

Bioconda is now enabled, so any packages on the bioconda channel can be installed into the current conda environment:

    `conda install bwa`

Or a new environment can be created:

    `conda create -n aligners bwa bowtie hisat star`

## JSON object

### Edit JSON object

As we talked in introduction about JSON object which allows the scripts to know where the executables are located.

Thus now edit/add items in json object as required.

You can make a copy of JSON object located here: `/PIe-master/pie/data/pie_resources.json`
or modify it directly.

### Set enviornmental variable

For PIe package to know the location of the JSON object file please set the enviormental variable.

Example:

```bash
export PIE_RESOURCE_CONFIG="/PIe-master/pie/data/pie_resources.json"
```