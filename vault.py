import os
import urllib2
import json
import sys
import hvac
from urlparse import urljoin
from subprocess import check_output

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase


class LookupModule(LookupBase):

    def run(self, terms, variables, **kwargs):
        key = terms[0]
        try:
            field = terms[1]
        except:
            field = None

        user_id = os.getenv('VAULT_USER_ID')
        if not user_id:
	  user_id = check_output(['sudo dmidecode -s system-uuid'], shell=True).rstrip()

        url = os.getenv('VAULT_ADDR')
        if not url:
            raise AnsibleError('VAULT_ADDR environment variable is missing')

        app_id = os.getenv('VAULT_APP_ID')
        if not app_id:
            raise AnsibleError('VAULT_APP_ID environment variable is missing')

	client = hvac.Client(url=url)
	client.auth_app_id(app_id, user_id)

	result = client.read(key)

        return [result['data'][field]] if field is not None else [result['data']]
