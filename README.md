# Rabin-Research

## About this Project

- We are three senior year students i.e Virang, Utsav and Amogh who are trying to make the most comprehensive study of three asymmetrical cryptosystems (RSA, Rabin and ECC) and their modified versions and variations based on almost 28-30 different metrics.
- This project is just an implementation of this study that we are trying to build.
- As we go ahead with this journey we are super grateful to be guided by Dr. Narendra Shekokar who helped us come up with this idea on one fine afternoon cyber-secuirty lab session.

## Tree View of the directories

---

**NOTE**

I'll be updating this as and when we keep on progressing with the project, please don't kill me if you can see a folder up there and not here. Use the GitHub search instead. Works better than you referring to a outdated tree view. but anyways, here it is:

---

```bash
RABIN-RESEARCH
│   LICENSE
│   README.md
│
└───basic stuff
        rabin.py
        rabin_modified.py
        rsa.py
```

## To Set Up this project locally

- In the desired folder, git bash the following:
  > > `git clone https://github.com/VirangParekh/Rabin-Research.git`
- Set up a python virtual environment using the following commands:

```python
pip install virtualenv
python -m venv env
```

- Activate and deactivate using:

```console
.\env\Scripts\activate
 deactivate
```

- In the env, install all the requirements using:

  > > `$ pip install -r requirements.txt`

- In any case you feel like contributing:

1. Fork this repository and work on your own version of this project and send us a pull request and we'll check and have it merged.

2. If it is not a code contribution, and something seems to not be working, freely put in your issues with proper tags and correct description of what is going wrong where.

3. And if you happen to be a member of this repository and want to try something new out or anything else, just create your own branch and send a pull-request from time to time.

# To run the project

We'll come up with this as we build the project. Thanks for waiting, okay. Thankyou.

# Code styles and other things:

- Use the `black` formatter to style the text, run black using
  > `$ black .`
  > OR
  >
  ```python
  > pip install black
  > black .
  ```
