# DotEnv

Load Configuration from .env file in current working directory

## Install

```
pip install git+git://github.com/widnyana/py-dotenv.git 
```

## Feature

this library provide ability to merge your config in `.env` file with current OS'
environment variable, with decision to override or not.


## Usage

file `.env`

```
YOUR_KEYNAME=YOUR_VALUE
YOUR_KEYNAME2 = YOUR_VALUE2

# ignored comment
```

your code `main.py`

```
import os
from dotenv import Dotenv

if __name__ == '__main__':
    
    #: not overriding OS's env var
    d = Dotenv()
    
    #: or, override OS's env var
    d = Dotenv(override=True)
    
    #: then load the .env
    d.load()

    
    #: you can get it like this 
    print os.getenv("YOUR_KEYNAME")  #: result -> YOUR_VALUE
    
    #: or like this
    print d.get("YOUR_KEYNAME", "DEFAULT_VAL")
```


## License

[MIT License](http://widnyana.mit-license.org/)