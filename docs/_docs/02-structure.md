---
title: "Organization of the package"
permalink: /docs/structure/
excerpt: "Structure of the package."
last_modified_at: 2018-05-11T15:12:19-04:00
redirect_from:
  - /theme-setup/
toc: true
---

### Tree for the current organization of the package

```bash

├── CHANGES.md
├── LICENSE
├── README.md
├── bin 
│   ├── pie_bwa_mem.py
│   ├── pie_cutadapt.py
│   ├── pie_delly.py
│   ├── pie_mutect.py
│   ├── pie_picard_markduplicates.py
│   ├── pie_pindel.py
│   └── pie_vardict.py
├── cwl
│   ├── pie_cutadapt.cwl
│   └── pie_picard_markduplicates.cwl
├── docs
│   ├── Gemfile
│   ├── Gemfile.lock
│   ├── _config.yml
│   ├── _cwl
│   ├── _data
│   ├── _docs
│   ├── _includes
│   ├── _layouts
│   ├── _sass
│   ├── assets
│   ├── images
│   ├── index.md
│   └── minimal-mistakes.scss
├── pie
│   ├── __init__.py
│   ├── _version.py
│   ├── data
│   └── util.py
└── setup.py
```

### Overview of directories

- bin: contains wrapper scripts written in python
- cwl: contains cwl scripts in YAML format, this scripts generated from python wrapper in the bin folder using argparse2tool
- docs: contains documentation and web-hosting using Github-pages with [Jekyll](https://jekyllrb.com/) and [Minimal Mistakes](https://mademistakes.com/work/minimal-mistakes-jekyll-theme/)
- pie: contains utility scripts to enable the package and json resources object storing all the resource required to run certain wrappers.