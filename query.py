#!/usr/bin/env python3
import json
import socket
import urllib.parse

import requests

class Db:

    def __init__(self, host=None, ssl_dir="/etc/puppetlabs/puppet/ssl"):
        self.host = socket.gethostname() if host is None else host
        self.ca = f"{ssl_dir}/certs/ca.pem"
        self.cert = (f"{ssl_dir}/certs/{self.host}.pem",
                     f"{ssl_dir}/private_keys/{self.host}.pem")

    def execute(self, query):
        result = {
            "error": False,
            "error_msg": None,
            "output": None,
        }
        headers = {
            'Accept': 'application/json',
            'Content-type': 'application/json',
        }
        params = urllib.parse.urlencode({"query": query})
        url = f"https://{self.host}:8082/pdb/query/v4?{params}"

        response = requests.get(url, verify=self.ca, cert=self.cert, headers=headers)
        try:
            response.raise_for_status()
            result["output"] = json.dumps(response.json(), indent=2)
        except Exception as exn:
            result["error"] = True
            result["error_msg"] = response.text

        return result

if __name__ == "__main__":
    query = """fact_contents[value] {
        name="velocix_facts" and
        path=["velocix_facts", "interfaces", "public"] and
        certname="us1.vcdn14chn1s1.cdn"
    }"""
    db = Db()
    output = db.execute(query)
    print(output)

