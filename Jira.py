import requests
import json

class Jira:
        def __init__(self, url, username, password):
                self.url = url
                self.username = username
                self.password = password
                self.auth = requests.auth.HTTPBasicAuth(username, password)
        
        def search_by_summary(self, query, assigned_to_me=False, only_unresolved=False):
                q = []
                if query:
                        q.append('summary ~ \'{0}\''.format(query))
                if assigned_to_me:
                        q.append('assignee = currentUser()')
                if only_unresolved:
                        q.append('resolution = Unresolved')
                qstr = ' AND '.join(q)
                response = requests.get(self.url + '/rest/api/3/search?jql={0}'.format(qstr), auth=self.auth)
                data = json.loads(response.text)
                lst = []
                for i in data['issues']:
                        lst.append({'summary': i['fields']['summary'],
                                    'key': i['key'],
                                    'url': self.url + '/browse/' + i['key'],
                                    'resolution': i['fields']['resolution']})
                return lst