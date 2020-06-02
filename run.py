#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""cisco-dnac-platform-syslog-notifications Console Script.

Copyright (c) 2018 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""

import os
import argparse
from flask import Flask, request
from flask.json import jsonify
import json
import cisco
import sys
import time

__author__ = "Robert Csapo"
__email__ = "rcsapo@cisco.com"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2018 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"
__app__ = "cisco-dnac-platform-syslog-notifications"

app = Flask(__name__)

api_url = "/api/v1"


@app.route(api_url+"/", methods=["GET"])
def root():
    return(jsonify(app=__app__, version=__version__), 200)


@app.route(api_url+"/dnac", methods=["GET", "POST"])
def dnac_v1():
    if request.method == "GET":
        settings["date"] = time.strftime('%d/%b/%Y %H:%M:%S')
        print("{} - - {} Cisco DNA Center ({}): Healthcheck".format(
            request.remote_addr,
            settings["date"],
            request.method
        ))
        return(jsonify(status="success", message="healthcheck"), 200)
    if request.method == "POST":
        json_data = request.json
        syslog_format = cisco.dnac.events.parse(payload=json_data)
        syslog = cisco.syslog.remote(format=syslog_format, settings=settings)
        settings["date"] = time.strftime('%d/%b/%Y %H:%M:%S')
        print("{} - - [{}] Cisco DNA Center ({}): Sending syslog message to {}".format(
            request.remote_addr,
            settings["date"],
            request.method,
            settings["syslog-host"]
        ))
        return(jsonify(status=syslog.status), 201)


@app.route(api_url+"/test", methods=["POST", "GET"])
def test_v1():
    if request.method == "GET":
        payload = '''
            {
            "version": null,
            "instanceId": "d81737f9-ff45-4750-a83f-31db0533fe88",
            "eventId": "NETWORK-NON-FABRIC_WIRED-1-250",
            "namespace": "ASSURANCE",
            "name": null,
            "description": null,
            "type": "NETWORK",
            "category": "ALERT",
            "domain": "Connectivity",
            "subDomain": "Non-Fabric Wired",
            "severity": 1,
            "source": "ndp",
            "timestamp": 1590086282484,
            "tags": null,
            "details": {
                "Type": "Network Device",
                "Assurance Issue Priority": "P1",
                "Assurance Issue Details": "This network device dummy.example.tld is unreachable from controller. The device role is BORDER ROUTER",
                "Device": "127.0.0.1",
                "Assurance Issue Name": "Network Device 127.0.0.1 Is Unreachable From Controller",
                "Assurance Issue Category": "Availability",
                "Assurance Issue Status": "active"
                },
                "ciscoDnaEventLink": "https://dnac.example.tld/dna/assurance/issueDetails?issueId=d81737f9-ff45-4750-a83f-31db0533fe88",
                "note": "To programmatically get more info see here - https://<ip-address>/dna/platform/app/consumer-portal/developer-toolkit/apis?apiId=8684-39bb-4e89-a6e4",
                "tntId": "",
                "context": null,
                "tenantId": ""
            }
        '''
        json_data = json.loads(payload)
        syslog_format = cisco.dnac.events.parse(payload=json_data)
        syslog = cisco.syslog.remote(format=syslog_format, settings=settings)

        settings["date"] = time.strftime('%d/%b/%Y %H:%M:%S')
        print("{} - - [{}] TEST ({}): Sending syslog message to {}".format(
            request.remote_addr,
            settings["date"],
            request.method,
            settings["syslog-host"]
        ))
        return(jsonify(status=syslog.status), 201)

    if request.method == "POST":
        json_data = request.json
        syslog_format = cisco.dnac.events.parse(payload=json_data)
        syslog = cisco.syslog.remote(format=syslog_format, settings=settings)

        settings["date"] = time.strftime('%d/%b/%Y %H:%M:%S')
        print("{} - - [{}] TEST ({}): Sending syslog message to {}".format(
            request.remote_addr,
            settings["date"],
            request.method,
            settings["syslog-host"]
        ))
        return(jsonify(status=syslog.status), 201)


def check_settings(args):
    settings = {}
    settings["status"] = "success"
    try:
        settings["syslog-host"] = os.environ["SYSLOG_HOST"]
        if len(settings["syslog-host"]) == 0:
            settings["status"] = "error"
            settings["message"] = "syslog host missing"
            return settings
    except Exception:
        try:
            settings["syslog-host"] = args.host
        except Exception:
            settings["status"] = "error"
            settings["message"] = "syslog host missing"
            return settings
    try:
        settings["syslog-port"] = os.environ["SYSLOG_PORT"]
        if len(settings["syslog-port"]) == 0:
            settings["syslog-port"] = args.port
    except Exception:
        settings["syslog-port"] = args.port
    try:
        settings["syslog-protocol"] = os.environ["SYSLOG_PROTOCOL"]
        if len(settings["syslog-protocol"]) == 0:
            settings["syslog-protocol"] = args.protocol
    except Exception:
        settings["syslog-protocol"] = args.protocol

    try:
        if os.environ["WEBHOOK_SSL"] == "True":
            settings["webhook-ssl"] = True
    except Exception:
        if args.ssl == "True":
            settings["webhook-ssl"] = True
        else:
            settings["webhook-ssl"] = False
    return settings


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__app__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
    parser.add_argument("--host", default=argparse.SUPPRESS,
                        help="Syslog Server Host")
    parser.add_argument("--port", default=514,
                        help="Syslog Server Port")
    parser.add_argument("--protocol", default="udp",
                        action="store",
                        help="The protocol to send syslog messages as")
    parser.add_argument("--ssl", default=False,
                        action="store_true",
                        help="Webhook with dummy SSL")
    parser.add_argument("--version", action="version",
                        version=__app__+" v"+__version__)

    args = parser.parse_args()

    settings = check_settings(args)
    if settings["status"] == "error":
        print(f"{settings['status']}: {settings['message']}")
        sys.exit()

    """ Print Settings """
    output = " * Settings "
    for key, value in settings.items():
        output = output + f"[{key}: {value}] "
    print(output)

    """ Self-signed/Dummy SSL with SSL Option """
    if settings["webhook-ssl"] is True:
        app.run(
            host="0.0.0.0",
            port=5000,
            threaded=True,
            debug=True,
            ssl_context="adhoc"
            )
    else:
        app.run(
            host="0.0.0.0",
            port=5000,
            threaded=True,
            debug=True
            )
