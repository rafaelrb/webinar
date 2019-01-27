#!/usr/bin/env python3

import sys
from pyvcloud.vcd.client import BasicLoginCredentials
from pyvcloud.vcd.client import Client
from pyvcloud.vcd.client import EntityType
from pyvcloud.vcd.org import Org
from pyvcloud.vcd.vdc import VDC
from pyvcloud.vcd.vapp import VApp
import requests
from pprint import pprint
import json
import configparser
import os

# Disable warnings from self-signed certificates.
requests.packages.urllib3.disable_warnings()

def main():
  config = configparser.ConfigParser()
  config_file = '~/.ansible/plugins/inventory/vcd-vapp.ini'
  if not os.path.expanduser(config_file):
    sys.stderr.write('Faltando arquivo de configuracao. ( %s )' % config_file)
    sys.exit(1)
 
  config.read(os.path.expanduser(config_file))
  
  host = config['default']['url'] #'vmware.cloudm ndic.com.br'
  org = config['default']['org'] #'Baena'
  user = config['default']['username'] #'rbaena'
  password = config['default']['password'] #'P0de5erV0ce!!'
  vdc = config['default']['vdc'] #'Baena'

  # Login. SSL certificate verification is turned off to allow self-signed
  # certificates.  You should only do this in trusted environments.
  client = Client(host,
              api_version='29.0',
              verify_ssl_certs=False,
              log_file='pyvcloud.log',
              log_requests=True,
              log_headers=True,
              log_bodies=True)
  client.set_credentials(BasicLoginCredentials(user, org, password))

  org_resource = client.get_org()
  org = Org(client, resource=org_resource)
  vdc_resource = org.get_vdc(vdc)
  vdc = VDC(client, resource=vdc_resource)
  vapps = vdc.list_resources(EntityType.VAPP)
  data = {}

  for app in vapps:
    vapp = VApp(client,resource=vdc.get_vapp(app.get('name')))
    hosts = []
    for vm in vapp.get_all_vms():
      hosts.append(vm.get('name'))
    data[app.get('name')] = {'hosts' : hosts }

  print( json.dumps(data, sort_keys=True, indent=2) )

  client.logout()

if __name__ == '__main__':
  main()

