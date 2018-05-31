---
title: "Introduction to cwl as to use in PIe"
permalink: /cwl/intro-to-cwl/
excerpt: "What is CWL"
last_modified_at: 2018-05-11T15:12:19-04:00
redirect_from:
  - /theme-setup/
toc: true
toc_label: "Table of Contents"
toc_icon: "cog"
---

[^Introduction-to-cwltool]: See [**Intorduction to cwltool** page]({{ "/cwl/intro-to-cwltool/" | relative_url }}) How to use cwltool to execute cwl

## What is CWL

CWL is a way to describe command line tools and connect them together to create workflows. Because CWL is a specification and not a specific piece of software, tools and workflows described using CWL are portable across a variety of platforms that support the CWL standard. 

## What to write CWL specification in ?

- JSON
- YAML
- Combination of JSON and YAML

## Simple YAML execution with cwltool

```bash
> cat 1st-tool.cwl
cwlVersion: cwl:draft-3
class: CommandLineTool
baseCommand: echo
inputs:
  - id: message
    type: string
    inputBinding:
      position: 1
outputs: []

> cat echo-job.yml
message: Hello world!

> cwl-tool 1st-tool.cwl echo-job.yml
[job 140199012414352] $ echo 'Hello world!'
Hello world!
Final process status is success

```

## Requirements

- Need Node.js in path for javascript
- Need argparse2tool, cwl-runner, cwltool and cwltoil in your path
- Need PIe package