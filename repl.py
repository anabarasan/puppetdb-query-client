#!/usr/bin/env python3
import os

from bottle import route, run, debug, template, request, static_file

import query

debug(True)

APP_DIR = os.path.dirname(os.path.abspath(__file__))

@route("/static/<filename:path>")
def static_routes(filename):
    print(__name__)
    print(APP_DIR)
    print(filename)
    return static_file(filename, root=f"{APP_DIR}/static")

@route("/", method=["GET", "POST"])
def home():
     
    if request.method == "POST":
        #myquery = """fact_contents[value] {
        #    name="velocix_facts" and 
        #    path=["velocix_facts", "interfaces", "public"] and 
        #    certname="us1.ag1chn1s1.cdn" 
        #}"""
        myquery = request.forms.get("txt_query")
        result = query.execute(myquery)
        output = template('repl', query=myquery, result=result)
        return output
    return template('repl', query="", result={})

run(host="0.0.0.0", port=5000, reloader=True)
