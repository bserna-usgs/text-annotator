## Text Annotator 

This is a simple python Flask web application that allows users to verify and annotate text passages. This was created to add a human-in-the-loop component of a scientific information extraction process that was paired with a question answering system. The goal is to give domain experts the opportunity to give a stamp of approval to certain knowledge that was extracted. 

Future efforts will hopefully include methods that allow for users to read a text passage and ask certain topic-focused queries against and aswer from the passage to feed back into the system. 

### Quick Start

##### Requirements

Use python 3.6 and install the requirements found in the ```requirements.txt``` file

* Python 3.6
* MongoDB

##### Configuration

To make this quick to plug and play there will be a lot of configuration that can be changed within the yaml files. 

##### Run Flask Development Server

```sh
python run.py
```

##### Provisional Software Disclaimer Under USGS Software Release Policy, the software codes here are considered preliminary, not released officially, and posted to this repo for informal sharing among colleagues.

This software is preliminary or provisional and is subject to revision. It is being provided to meet the need for timely best science. The software has not received final approval by the U.S. Geological Survey (USGS). No warranty, expressed or implied, is made by the USGS or the U.S. Government as to the functionality of the software and related material nor shall the fact of release constitute any such warranty. The software is provided on the condition that neither the USGS nor the U.S. Government shall be held liable for any damages resulting from the authorized or unauthorized use of the software.