__author__ = "Jonathan Carlton"

import facebook

access_token = '46bbbb8e9a13626614da53ec2017054d'

graph = facebook.GraphAPI(access_token)
friends = graph.get_connections(id='me', connection_name='friends')
print friends

# need user permission to even start using this!
