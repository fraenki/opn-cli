import base64
import re
import requests
import json
from json import JSONDecodeError
from urllib3.exceptions import InsecureRequestWarning
from opnsense_cli.exceptions.api import APIException

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

HTTP_SUCCESS = (200, 201, 202, 203, 204, 205, 206, 207)


class ApiClient(object):
    def __init__(self, api_key, api_secret, base_url, ssl_verify_cert, ca, timeout):
        self._api_key = api_key
        self._api_secret = api_secret
        self._base_url = base_url
        self._ssl_verify_cert = ssl_verify_cert
        self._timeout = timeout
        self._ca = ca

    @property
    def ssl_verify_cert(self):
        if self._ssl_verify_cert:
            return self._ca
        return self._ssl_verify_cert

    def _process_response(self, response):
        if response.status_code in HTTP_SUCCESS:
            #print("DEBUG 2000")
            #print(f"XXX {response.text}")
            #print(f"XXX {response.headers['content-type']}")
            #print(f"XXX {response.headers}")
            try:
                return json.loads(response.text)
            except JSONDecodeError:
                #print("DEBUG 2200")
                # Convert response to base64.
                response_bytes = response.text.encode("utf-8")
                content = base64.b64encode(response_bytes)
                #print("DEBUG 2210")
                # Not a JSON response, wrap the content into base64.
                if 'Content-Disposition' in response.headers.keys():
                    #print("DEBUG 2220")
                    # Looks like a file.
                    filename = re.findall('filename=(.+)', response.headers['Content-Disposition'])[0]
                    #print(f"DEBUG filename: {filename}")
                    # Create a json string.
                    response_json = f"'{{\"filename\": \"{filename}\", \"content\": \"{content}\", \"encoding\": \"base64\"}}'"
                else:
                    #print("DEBUG 2230")
                    # Create a json string.
                    response_json = f"'{{\"content\": \"{content}\", \"encoding\": \"base64\"}}'"
                #print("DEBUG 2300")
                #print(f"YYY {response_json}")
                #return response.text
                #return json.loads(response.text)
                return json.loads(response_json)
        else:
            raise APIException(response=response.status_code, resp_body=response.text, url=response.url)

    def _get_endpoint_url(self, *args, **kwargs):
        endpoint = f"{kwargs['module']}/{kwargs['controller']}/{kwargs['command']}".lower()
        endpoint_params = '/'.join(args)
        if endpoint_params:
            return f"{endpoint}/{endpoint_params}"
        return endpoint

    def _get(self, endpoint):
        req_url = '{}/{}'.format(self._base_url, endpoint)
        #print("DEBUG 1000")
        response = requests.get(req_url, verify=self.ssl_verify_cert,
                                auth=(self._api_key, self._api_secret),
                                timeout=self._timeout)
        #print("DEBUG 1000 B")
        return self._process_response(response)

    def _post(self, endpoint, json=None):
        req_url = '{}/{}'.format(self._base_url, endpoint)
        response = requests.post(req_url, json=json, verify=self.ssl_verify_cert,
                                 auth=(self._api_key, self._api_secret),
                                 timeout=self._timeout)
        return self._process_response(response)

    def execute(self, *args, json=None, **kwargs):
        endpoint = self._get_endpoint_url(*args, **kwargs)
        try:
            if kwargs['method'] == 'get':
                return self._get(endpoint)
            elif kwargs['method'] == 'post':
                return self._post(endpoint, json)
            else:
                raise NotImplementedError(f"Unkown HTTP method: {kwargs['method']}")
        except Exception as e:
            raise APIException(resp_body=e)
