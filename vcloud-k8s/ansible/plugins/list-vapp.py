#!/usr/bin/env python3
# Pyvcloud Examples
#
# Copyright (c) 2017-2018 VMware, Inc. All Rights Reserved.
#
# This product is licensed to you under the
# Apache License, Version 2.0 (the "License").
# You may not use this product except in compliance with the License.
#
# This product may include a number of subcomponents with
# separate copyright notices and license terms. Your use of the source
# code for the these subcomponents is subject to the terms and
# conditions of the subcomponent's license, as noted in the LICENSE file.
#
# Illustrates how to list all vApps within a single vDC.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import sys
from pyvcloud.vcd.client import BasicLoginCredentials
from pyvcloud.vcd.client import Client
from pyvcloud.vcd.client import EntityType
from pyvcloud.vcd.org import Org
from pyvcloud.vcd.vdc import VDC
from pyvcloud.vcd.vapp import VApp
import requests
from pprint import pprint
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable

# Collect arguments.
#if len(sys.argv) != 6:
#    print("Usage: python3 {0} host org user password vdc".format(sys.argv[0]))
#    sys.exit(1)

host = 'vmware.cloudmandic.com.br'
org = 'Baena'
user = 'rbaena'
password = 'P0de5erV0ce!!'
vdc = 'Baena'
avapp = 'k8s-cluster'

# Disable warnings from self-signed certificates.
requests.packages.urllib3.disable_warnings()

class InventoryModule(BaseInventoryPlugin):
  NAME = 'list-vapp'

  def __init__(self):
    pass

  def verify_file(self, path):
    valid = True

  def parse(self, inventory, loader, path, cache=True):
    super(InventoryModule, self).parse(inventory, loader, path, cache)
    config = self._read_config_data(self,path)

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
    vapp = VApp(client,resource=vdc.get_vapp(avapp))

    for vm in vapp.get_all_vms():
      self.inventory.add_host(vm.get('name'))
      self.inventory.set_variable(vm.get('name', group='all'))
      #print(vm.get('name'))
    pprint(self.inventory)
    # Log out.
    client.logout()

  def show(self):
    return json.dumps(self.inventory, indent=2)

