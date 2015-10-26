# DotEnv

Load Configuration from .env file in current working directory

## Install

```
pip install git+git://github.com/widnyana/py-dotenv.git 
```

## Usage

file `.env`
```
YOUR_KEYNAME=YOUR_VALUE
```

your code `main.py`
```
import os
from dotenv import Dotenv

if __name__ == '__main__':
    d = Dotenv()
    d.load()

    print os.getenv("YOUR_KEYNAME")  #: result -> YOUR_VALUE
```

Kindly check the test directory for more detailed usage.
