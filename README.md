# OPCP9
## LitReview
Lit Review is a web app using the Django framework allowing users to exchange and publish reviews about books.

### Overview

Goal: Building a network with a database where users can register, post data and review data from the users they follow.
      Data Management with sqlite
      Creation of a feed algorithm


### Tools Used
Python with the Django Framework

### Installing & How to use

Clone the repository:


Activate the virtual environment:
```bash
env\Scripts\activate
```

Verify that Django is installed:
```bash
python -m django version
```
If it is not installed:
```bash
pip install django
```
You may also have to install pillow which is a package allowing to manage images:
```bash
python -m pip install pillow
```
If you want to be sure about the requirements in the shell run:
```bash
pip install -r requirements.txt
```

Then got to mysite folder:
```bash
cd mysite
```
Run the script:
```bash
python .\manage.py runserver
```
