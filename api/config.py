# Presentation
userlist_header='Age Authors'

# Versions of the engine this DB instance will support
acceptable_game_versions = ['70.2', '70.3']

# API paths
ages_path='/ages'
users_path='/authors'
files_path='/files'
forms_path='/forms'

# server paths
agefiles_path='/home/branan/ages/'

# Webhost
domain='127.0.0.1:8080'

# Age database
agedb = {
#    'user':'dbuser',
#    'pw':'dbpass',
    'db':'agedb',
    'dbn':'sqlite' # also available: postgres, mysql, firebird, mssql, oracle
}

# Users database
userdb = {
#    'user':'dbuser',
#    'pw':'dbpass',
    'db':'userdb',
    'dbn':'sqlite' # also available: postgres, mysql, firebird, mssql, oracle
}

usertable = 'users'


# RE sanity checks
import re
re.UNICODE = False
re.LOCALE = False
