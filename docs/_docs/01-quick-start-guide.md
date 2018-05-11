---
title: "Quick-Start Guide"
permalink: /docs/quick-start-guide/
excerpt: "How to quickly install and setup PIe for use on linux platform."
last_modified_at: 2018-05-09T15:58:49-04:00
redirect_from:
  - /theme-setup/
toc: true
---

[^structure]: See [**Structure** page]({{ "/docs/structure/" | relative_url }}) for a list of files and what they do.
[^anaconda]: See [**Anaconda** page]({{ "/docs/anaconda/" | relative_url }}) for installing miniconda and using bioconda for bioinformatics tools.

### Installing package

Here is how to install these tools without sudo rights:

```bash
curl -LO https://github.com/NorthwellHealth-HumanGenomics/PIe/archive/master.zip
unzip master.zip
cd pie-master
python setup.py install --user
```

Add this to your `~/.bash_profile` to get access to the `pie_*` tools:

```bash
# Set PATH to include local python bin if found
if [ -d "$HOME/.local/bin" ]; then
    PATH="$HOME/.local/bin:$PATH"
fi
```