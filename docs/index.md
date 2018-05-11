---
layout: splash
classes:
  - landing
  - dark-theme
excerpt: "Precision Informatics engine (PIe) help documents"
tags: [python, cwl, json, toil]
header:
  image: /assets/images/background.jpg
  caption: "Photo credit: [**Canva**](https://www.canva.com/)"
---
# Welcome to Precision Informatics engine (PIe) help documents

PIe came into existence because of the need to write flexible, portable and easy to use tools.

## PIe components

1. **JSON based configuration** : JSON object is where we store all the resources with their versions.
2. **Python Wrapper** : The concept here is to write wrapper in python around bioinformatics tools that allow you to execute the tools more easily by pre-selecing certain parameters. The presection happens using the JSON based configuration.
3. **Containers** : In future, we will be using singularity and docker containers for the bioinformatics tools. But to start with we will use Bioconda.
4. **Common Workflow Language (CWL)** : Convert the python wrapper to common workflow language specification.
5. **Workflow of workflow** : We will join multiple CWL workflows togather to create a final workflow.

### Installing package

Here is how to install these tools without sudo rights:

```bash
curl -LO https://github.com/NorthwellHealth-HumanGenomics/PIe/archive/master.zip
unzip PIe-master.zip
cd PIe-master
python setup.py install --user
```

Add this to your `~/.bash_profile` to get access to the `pie_*` tools:

```bash
# Set PATH to include local python bin if found
if [ -d "$HOME/.local/bin" ]; then
    PATH="$HOME/.local/bin:$PATH"
fi
```