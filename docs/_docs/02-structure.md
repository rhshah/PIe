---
title: "Quick-Start Guide"
permalink: /docs/structure/
excerpt: "Structure of the package."
last_modified_at: 2018-05-09T15:58:49-04:00
redirect_from:
  - /theme-setup/
toc: true
---

### Organization of the package

```bash
.
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