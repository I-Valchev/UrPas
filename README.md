![Logo](http://s24.postimg.org/vb2g9mla9/Ur_Pas_Logo.png)

[![Build Status](https://travis-ci.org/I-Valchev/UrPas.svg?branch=master)](https://travis-ci.org/I-Valchev/UrPas) [![License](https://img.shields.io/hexpm/l/plug.svg)](https://img.shields.io/hexpm/l/plug.svg) ![Issues](https://img.shields.io/github/issues/I-Valchev/UrPas.svg) ![Stars](https://img.shields.io/github/stars/I-Valchev/UrPas.svg) ![Version](https://img.shields.io/badge/version-0.0.1-brightgreen.svg) 
![Coverage](https://img.shields.io/badge/coverage-56%25-yellowgreen.svg)

Borislav Rusinov and Ivo Valchev

---
#What is UrPas? 
---
It is simple password application that will allow the user to save his password via a personal account.
Other options include, but are not limited to, password generation and encryption.
A demo version is availabe for the first 5 saved and 2 random generated passwords.
Full licensed version is available for $5. 
The licensed version includes: unlimited number of saved passwords; unlimited number of password generations.

---
How to run the tests?
---

Dependencies: coverage.py (downloadable from Python's official site or by running "sudo pip install coverage"

Run the following command in the main directory: "sudo make" (root access is needed in order to start xampp, otherwise the test will FAIL!

Output is generated in htmlcov/index.html

---
Requirements
---

Python version 2.7.X

XAMPP with: user named "root", database named "UrPasDB" [XAMPP Instalation guide](http://ubuntuportal.com/2013/12/how-to-install-xampp-1-8-3-for-linux-in-ubuntu-desktop.html)

---
Documentation
---

Public methods are documented using the official python documentation tool. The HTML page is available at /doc/_build/html/main.html