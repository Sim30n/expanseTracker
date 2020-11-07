# Simple Expanse tracker

This is a simple command line expanse tracker to keep track on your expanses.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pandas.

```bash
pip install pandas
```

## Usage example

```bash

#To add new transactions to the database.
#-a <comment> <amount>
python3 app.py -a "mc donalds" 7.18

#To print all the transactions.
python3 app.py -p

#To delete transaction.
#-d <id>
python3 app.py -d 12

#To add new transactions to the database.
#-e <id> <description> <amount>
python3 app.py -e 1 "burger king" 9.20

#To print total spending and daily average.
python3 app.py -c

#To print readme file.
python3 app.py -help

```
