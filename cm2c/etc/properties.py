###
# Various systemwide properties
# carlos@lacnic.net 20130901
# carlos@lacnic.net 20151217
###

import os

## System paths
srchome = os.environ.get('SRCHOME', os.getcwd())

paths = { # 'tmp': "%s/tmp" % (srchome),
          'tmp': "/tmp",
          'etc': "%s/etc" % (srchome) }

## -------------
