import sys
sys.path.insert(1, 'bin')
sys.path.insert(1, 'functional')

from rest import server


server('functional')