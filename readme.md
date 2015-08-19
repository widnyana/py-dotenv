# DotEnv

Load Configuration from .env file in current working directory

## Install

```
pip install git+git://github.com/widnyana/py-dotenv.git 
```

## Usage

```
from dotenv import Dotenv

if __name__ == '__main__':
    d = Dotenv()
    print d.load()

```
