---
layout: splash
classes:
  - landing
  - dark-theme
excerpt: "Precision Informatics engine (PIe) help documents"
tags: [python, cwl, json, toil]
header:
  overlay_image: /assets/images/background.jpg
  overlay_filter: 0.5
  #credit: Canva
  #creditlink: https://www.canva.com/
---

## PIe has three components

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