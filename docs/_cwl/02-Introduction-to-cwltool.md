---
title: "Installing cwltool to execute cwl YAML"
permalink: /cwl/intro-to-cwltool/
excerpt: "How to use cwltool to execute cwl"
last_modified_at: 2018-05-11T15:12:19-04:00
redirect_from:
  - /theme-setup/
toc: true
toc_label: "Table of Contents"
toc_icon: "cog"
---
# cwltool

## Installation of cwltool

### Create a new virtual environment

- This can be done using `conda` or `virtualenv`

```bash
virtualenv ~/my_virtual_env
#Or use
conda new --name my_virtual_env python=2.7
```

### Source the virtual environment

```bash
source ~/my_virtual_env/bin/activate
#Now when you do
echo $PATH
#you should see
~/my_virtual_env/bin
#listed as an entry
```

## Install toil

`pip install toil'[cwl]'==3.15.0`

### Install the python tool you made (optional, only needed if trying to test with setup.py)

```bash
python setup.py install && python setup.py clean
```

This will install the example python script into your virtualenvironment's `/bin` folder
This makes it so it can be referenced from your terminal, as well as from the cwl files

So now, whenever you want to run a command, that python file will be found (because all commands are just files found in the $PATH variable)

### Try to run your file

```bash
cwltool example_cwl_tool_that_calls_python_script.cwl inputs.yaml
#Because the tool's
baseCommand
#param has the python script listed inside, the runner will find it and run it.
```

### With `cwltoil`

```bash
cwltoil sometool.cwl inputs.yaml --outdir /place_for_outputs
```