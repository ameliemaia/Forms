# Forms

Forms is a Python package for Maya that provides helpful scripts for creating generative 3D geometry and curves. It also includes utilities for modifying meshes.


## About

This library originally started out as a way for me to learn Python scripting in Maya. I've known and used Maya for several years but never got round to learning [MEL](http://en.wikipedia.org/wiki/Maya_Embedded_Language "Maya Embedded Language") in that time.

My first experiments with PyMEL investigated Sierpinski fractal meshes.
From these experiments I learnt the limitations and performance issues that one would encounter when generating highly dense polygons meshes. These techniques and processes are now used throughout the library, enabling the output of bigger and more complex meshes.

These experiments are the foundation of this library, and it will grow further and larger the more I experiment with generative 3D algorithms.  


## Example

To generate a Menger Sponge simply copy and paste the following in Maya's script editor and hit Execute.

```
from forms.geometry import *

x = hexahedron.Sierpinski().generate( size = 30, iterations = 3, grid = 3 )

print( x )

# Result: [nt.Transform(u'Sierpinski_Iteration_3')]
```

For more information on Form's packages and modules browse the [source code](https://github.com/davidpaulrosser/Forms "source code").


## Requirements

I've only tested so far on Python ```2.6.4``` in Autodesk Maya ```2013 x64```

To check your Python and Maya version run:

```
import sys
from pymel import versions

print sys.version    
print versions.fullName()

# Result: 2.6.4 (r264:75706, Nov  3 2009, 11:26:40) ...
# Result: 2013 x64
```

I would be interested to know if the library works in older versions of Maya and PyMEL.


## Installation

Download or clone the repository

``git clone https://github.com/davidpaulrosser/Forms.git``


Theres two ways to add Forms to Maya's Python script path. The recommended way is to append the library path to Python's system path in your userSetup.py. This enables you to keep the library anywhere on your computer.

**userSetup.py**

``/Users/<user>/Library/Preferences/Autodesk/maya/<version>/scripts/userSetup.py``

```
import sys

sys.path.append( 'path/to/forms' ) 
```

Or you can place the library directly in your scripts directory:

``/Users/<user>/Library/Preferences/Autodesk/maya/<version>/scripts``

And that's it. The next time you launch Maya you should be able to access the Forms package.

```
import forms

help( forms ) 
```

## Contributors

For feature requests and bugs file an issue.

## License

[MIT Licensed](https://github.com/davidpaulrosser/Forms/blob/master/README.md "MIT Licensed")


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/davidpaulrosser/forms/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

