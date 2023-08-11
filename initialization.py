import sys
import subprocess

subprocess.check_call([sys.executable, '-m', 'pip', 'install',
'jproperties'])

subprocess.check_call([sys.executable, '-m', 'pip', 'install',
'pandas'])

subprocess.check_call([sys.executable, '-m', 'pip', 'install',
'jira'])

subprocess.check_call([sys.executable, '-m', 'pip', 'install',
'jsonpath-ng'])

subprocess.check_call([sys.executable, '-m', 'pip', 'install',
'PyGithub'])

subprocess.check_call([sys.executable, '-m', 'pip', 'install',
'GitPython'])