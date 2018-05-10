---
title: "About"
permalink: /
excerpt: "About PIe."
last_modified_at: 2018-05-09T15:58:49-04:00
redirect_from:
  - /theme-setup/
toc: true
---
# Precision Informatics engine (PIe)

### PIe has three components in it:
1. JSON based configuration
2. Python
3. Common Workflow Language

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

 

