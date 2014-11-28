#!/usr/bin/env python3

import yr.libyr
print u'/home/pm/.local/lib/python3.4/site-packages/yr/libyr.py' # ~> is wrong!
print u'/usr/local/lib/python3.4/dist-packages/yr/libyr.py' # ~> is ok!
print yr.libyr.__file__
