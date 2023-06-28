# Scrabble

## How to run the game

The game must be executed in a virtual environment. The steps to run it aredescribed below:

**IMPORTANT: TO EXECUTE THE COMMANDS DESCRIBED BELOW, STAY IN `CODE/` DIRECTORY**

#### 1. Installing virtualenv

```
`pip install virtualenv `
```

This command uses the python package manager to install the virtual environment in your machine

#### 2. Naming your virtual env

```
virtualenv scrabble
```

This command will create a new environment and give a name to it.

#### 3. Activating the virtual env

To activate the environment to your current directory, run the command:

* In Linux and macOS:

```
source scrabble/bin/activate
```

* In Windows:

```
scrabble/Scripts/Activate
```

Then, with the virtual environment activated, you have to install the projects dependencies. In this case, all of the Scrabble requirements are listed in `requirements.txt` file. So, just run:

```
pip install -r requirements.txt
```

Finally, you can run the game:

```
python3 app.py
```

### Implementation NOTES:

* The `Restart game` use case was replaced by `Reset game` use case.
* Some little rules were modified, in order to let the implementation functional and the Specifying Requirements Document was reviewed according to that.
  * E.g.: The special first world rule was changed from accept more than one card in first word to accept more than two cards (we do not have words with two letters in the validation dictionary).
