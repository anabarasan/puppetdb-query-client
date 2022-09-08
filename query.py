#!/usr/bin/env python3
import json
import shlex
import socket
import subprocess

def execute(query):
    hostname = socket.gethostname()

    CMD = (
        """curl -X GET --cacert /etc/puppetlabs/puppet/ssl/certs/ca.pem """
        f"""--tlsv1 --cert /etc/puppetlabs/puppet/ssl/certs/{hostname}.pem """
        f"""--key /etc/puppetlabs/puppet/ssl/private_keys/{hostname}.pem  """
        f"""https://{hostname}:8082/pdb/query/v4 --data-urlencode 'query={query}'"""
    )

    args = shlex.split(CMD)

    result = {
        "error": False,
        "error_msg": None,
        "output": None,
    }

    with subprocess.Popen(args,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          encoding="utf-8") as proc:
        out, err = proc.communicate()
        return_code = proc.returncode

        print("*" * 80)
        print(return_code)
        print("*" * 80)
        print(out)
        print("*" * 80)
        print(err)
        print("*" * 80)

        if return_code != 0:
            result["error"] = True
            result["error_msg"] = err
        else:
            try:
                result["output"] = json.dumps(json.loads(out), indent=2)
            except Exception as exn:
                print(exn)
                result["error"] = True
                result["error_msg"] = out

    return result

if __name__ == "__main__":
    query = """fact_contents[value] {
        name="velocix_facts" and 
        path=["velocix_facts", "interfaces", "public"] and 
        certname="us1.vcdn14chn1s1.cdn" 
    }"""
    output = execute(query)
    print(output)
