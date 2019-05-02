#!/usr/bin/env python
import requests
import json
from requests.auth import HTTPBasicAuth


class RestClient:
    def __init__(self, server, user='csproot', password='csproot'):
        self.server = server
        self.user = user
        self.password = password
        self.apiKey = ''
        self.headers = \
            {"X-Nuage-Organization": "csp", "Content-Type": "application/json; charset=UTF-8"}

    def login(self):
        loginUrl = self.server + "/me"
        print 'Rest Client loginUrl: {}'.format(loginUrl)
        r = requests.get(loginUrl,
                         headers=self.headers,
                         auth=HTTPBasicAuth(self.user, self.password),
                         verify=False)
        if (r.status_code != 200):
            return (False, None)
        else:
            print r.text
            data = json.loads(r.text)
            data1 = data[0]
            self.apiKey = data1['APIKey']
            return (True, data1['enterpriseID'])

    def server(self):
        return self.server

    def appendHeaders(self, key, value):
        self.headers[key] = value

    def get(self, url):
        if (self.apiKey == ""):
            self.login()
        print url
        r = requests.get(url,
                         headers=self.headers,
                         auth=HTTPBasicAuth(self.user, self.apiKey),
                         verify=False)
        print r.status_code
        print r.text
        return r

    def delete(self, url):
        if (self.apiKey == ""):
            self.login()
        r = requests.delete(url,
                            headers=self.headers,
                            auth=HTTPBasicAuth(self.user, self.apiKey),
                            verify=False)
        return r

    def put(self, url, data):
        if (self.apiKey == ""):
            self.login()
        print url
        print data
        r = requests.put(url,
                         data=data,
                         headers=self.headers,
                         auth=HTTPBasicAuth(self.user, self.apiKey),
                         verify=False)
        print r.status_code
        print r.text
        return r

    def post(self, url, data):
        if (self.apiKey == ""):
            self.login()
        print url
        print data
        r = requests.post(url,
                          data=data,
                          headers=self.headers,
                          auth=HTTPBasicAuth(self.user, self.apiKey),
                          verify=False)
        print r.status_code
        print r.text
        return r


class VsdClient(object):
    def __init__(self,
                 server,
                 user=u'csproot',
                 password=u'csproot',
                 port=8443,
                 prefix="/nuage/api/v4_0",
                 protocol='https://'):
        self.prefix = prefix
        self.protocol = protocol
        self.port = port
        self.server = self.protocol + str(server) + ":" + str(self.port) + self.prefix
        self.restclient = RestClient(self.server, user, password)
        _is_conn, data = self.restclient.login()
        if _is_conn:
            self.enterprise_id = data
            return
        raise Exception('VSD authentication failed')

    def get_domains(self):
        response = self.restclient.get(self.server + '/domains')
        if (response.status_code == 200):
            if response.text is unicode(''):
                print "No Domain present"
                return
            return json.loads(response.text)

    def get_subnets(self):
        response = self.restclient.get(self.server + '/subnets')
        if (response.status_code == 200):
            if response.text is unicode(''):
                print "No subnet present"
                return
            return json.loads(response.text)

    def get_vPorts(self):
        response = self.restclient.get(self.server + '/vports')
        if (response.status_code == 200):
            if response.text is unicode(''):
                print "No vPort present"
                return
            return json.loads(response.text)

    def get_vms(self):
        response = self.restclient.get(self.server + '/vms')
        if (response.status_code == 200):
            if response.text is unicode(''):
                print "No VM present"
                return
            return json.loads(response.text)

    def install_license(self, license_str):
        licenseDict = {}
        licenseDict['license'] = license_str
        response = self.restclient.post(self.server + '/licenses/', json.dumps(licenseDict))
        if (response.status_code != 201):
            if 'The license already exists' not in response.text:
                raise Exception("license install failed")

    def add_csproot_to_cms_group(self):
        resp = self.restclient.get(self.server +
                                   '/enterprises/{}/groups'.format(self.enterprise_id))
        groups = json.loads(resp.text)
        cms_group_id = None
        csproot_user_id = None

        for group in groups:
            print 'group:: {}'.format(group)
            if group['name'] == 'CMS Group':
                cms_group_id = group['ID']

        resp = self.restclient.get(self.server +
                                   '/enterprises/{}/users'.format(self.enterprise_id))
        users = json.loads(resp.text)
        for user in users:
            if user['userName'] == 'csproot':
                csproot_user_id = user['ID']
            print 'user:: {}'.format(user)
        resp = self.restclient.get(self.server + '/groups/{}/users'.format(cms_group_id))
        print resp.text
        userlist = ['{}'.format(csproot_user_id)]
        resp = self.restclient.put(self.server +
                                   '/groups/{}/users'.format(cms_group_id), json.dumps(userlist))
        resp = self.restclient.get(self.server + '/groups/{}/users'.format(cms_group_id))
        print resp.text
