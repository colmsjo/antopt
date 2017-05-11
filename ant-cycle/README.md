Setup
=====

* First init `virtualenv` for Python3: `virtualenv -p python3 venv3` (`virutalenv needs to be installed)
* Activate `virtualenv`: `source venv3/bin/activate`
* Install the necessary Python packages: `pip3 install -r requirements.txt`


Run the program
==============

* Activate `virtualenv`: `source venv3/bin/activate`
* Run the program: `python ants.py MAP1.txt`


Development
===========

* In case new Python packages are installed, make sure to save the setup: `pip3 freeze > requirements.txt`
* Run the unit test: `./build.sh`


NOTE
===

A common source of problems is conflicting python environments. For instance use `pip3` instead of `pip` when using Python 3.X instead of 2.X.


