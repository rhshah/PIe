---
title: "Quick-Start Guide"
permalink: /docs/quick-start-guide/
excerpt: "How to quickly install and setup PIe for use on linux platform."
last_modified_at: 2018-05-11T15:12:19-04:00
redirect_from:
  - /theme-setup/
toc: true
---

[^structure]: See [**Structure** page]({{ "/docs/structure/" | relative_url }}) for a list of files and what they do.
[^anaconda]: See [**Anaconda** page]({{ "/docs/anaconda/" | relative_url }}) for installing miniconda and using bioconda for bioinformatics tools.

#### Table of Contents

- [Installing PIe](#installing-anaconda)
	- [Download](#download)
	- [Install](#install)
- [Modifying the JSON resource object](#modifying-the-json-resource-object)

## Installing PIe

To view the content of the package
==================================

Go to PIe github page: <https://github.com/NorthwellHealth-HumanGenomics/PIe>

Download
========



```bash
curl -LO https://github.com/NorthwellHealth-HumanGenomics/PIe/archive/master.zip
```

Install
=======

Install these tools **with sudo** rights:

```bash
unzip master.zip
cd PIe-master
python setup.py install
```

Install these tools **without sudo** rights:

```bash
unzip master.zip
cd PIe-master
python setup.py install --user
```

Quick Access
============

Add following to your **.bashrc** or **.bash_profile** for accessing the `pie_*` tools:

When installed **without sudo** rights:

```bash
# Set PATH to include local python bin if found
if [ -d "$HOME/.local/bin" ]; then
    PATH="$HOME/.local/bin:$PATH"
fi
```

## Modifying the JSON resource object

1. Inside the /PIe-master/pie/data there is a file called `pie_resources.json`.
2. Please modify the key:value pair as per the paths in your environment. If you have not installed you can use [Anaconda](http://docs.continuum.io/anaconda/) as shown in this [page]({{ "/docs/anaconda/" | relative_url }}).
3. Once you have modidfied the file set environment variable `PIE_RESOURCE_CONFIG` as follows:
    ```bash
    export PIE_RESOURCE_CONFIG="/path/to/pie_resources.json"
    ```

4. Now you are ready to run the scripts in the bin directory