# cisco-dnac-platform-syslog-notifications

## Receive Events from Cisco DNA Center and push the information to Syslog Server

## Disclaimer
* This solution isn't using Username/Password header with Cisco DNA Center
* You need to use HTTPS with Cisco DNA Center for Events API
	- It's recommended to use this service with non-https and have a loadbalancer infront (https)
	- SSL is now supported (ad-hoc) on this service (without LB) - not recommended for production

## How to setup

### Python Webhook

#### Prerequisites
* Docker support
* Syslog Server

### Start Python Webhook

```
docker run -d -p 5000:5000 \
-e SYSLOG_HOST="10.1.1.1" \
robertcsapo/cisco-dnac-platform-syslog-notifications
```

If SSL is need

```
docker run -d -p 5000:5000 \
-e SYSLOG_HOST="10.1.1.1" \
-e WEBHOOK_SSL="True" \
robertcsapo/cisco-dnac-platform-syslog-notifications
```

## Demo
```
tail -f var/log/messages
Jun  1 11:02:46 172.17.0.3 [2020-05-21 18:38:02] [Cisco DNA Center] 1 ALERT active [NETWORK-NON-FABRIC_WIRED-1-250] 127.0.0.1 This network device dummy.example.tld is unreachable from controller. The device role is BORDER ROUTER https://dnac.example.tld/dna/assurance/issueDetails?issueId=d81737f9-ff45-4750-a83f-31db0533fe88
```

### Cisco DNA Center
#### Prerequisites
* Enable Cisco DNA Center as a Platform
	- How-To Guide https://www.cisco.com/c/en/us/td/docs/cloud-systems-management/network-automation-and-management/dna-center-platform/1-3-1-0/user_guide/b_dnac_platform_ug_1_3_1_0/b_dnac_platform_ug_1_3_1_0_chapter_010.html
* Configure Cisco DNA Center Events (https://<dnac-ip>/dna/systemSettings/settings?settings-item=dnacp-events-settings)
	- How-To Guide https://www.cisco.com/c/en/us/td/docs/cloud-systems-management/network-automation-and-management/dna-center-platform/1-3-1-0/user_guide/b_dnac_platform_ug_1_3_1_0/b_dnac_platform_ug_1_3_1_0_chapter_010.html

## URI

### Cisco DNA Center
Point your Cisco DNA Center Events Destination towards ```https://<yourhost>:<port>/dnac```

### Test Function

#### GET
```
curl https://<yourhost>:<port>/test
```

This will make the service send a test message to your syslog in same format as Cisco DNA Center.

#### POST
```
curl --location --request POST 'https://<yourhost>:<port>/test' \
--header 'Content-Type: application/json' \
--data-raw '{
            "version": null,
            "instanceId": "d81737f9-ff45-4750-a83f-31db0533fe88",
            "eventId": "NETWORK-NON-FABRIC_WIRED-1-250",
            "namespace": "ASSURANCE",
            "name": null,
            "description": null,
            "type": "NETWORK",
            "category": "ERROR",
            "domain": "Connectivity",
            "subDomain": "Non-Fabric Wired",
            "severity": 1,
            "source": "ndp",
            "timestamp": 1590086282484,
            "tags": null,
            "details": {
                "Type": "Network Device",
                "Assurance Issue Priority": "P1",
                "Assurance Issue Details": "This network device example.tld is unreachable from controller. The device role is BORDER ROUTER",
                "Device": "10.1.2.3",
                "Assurance Issue Name": "Network Device 10.1.2.3 Is Unreachable From Controller",
                "Assurance Issue Category": "Availability",
                "Assurance Issue Status": "active"
                },
                "ciscoDnaEventLink": "https://<your-cisco-dna-center>/dna/assurance/issueDetails?issueId=d81737f9-ff45-4750-a83f-31db0533fe88",
                "note": "To programmatically get more info see here - https://<ip-address>/dna/platform/app/consumer-portal/developer-toolkit/apis?apiId=8684-39bb-4e89-a6e4",
                "tntId": "",
                "context": null,
                "tenantId": ""
            }'
```

## Help
```
docker run --rm -it robertcsapo/cisco-dnac-platform-syslog-notifications --help

usage: run.py [-h] [--host HOST] [--port PORT] [--protocol PROTOCOL] [--ssl] [--version]

cisco-dnac-platform-syslog-notifications

optional arguments:
  -h, --help           show this help message and exit
  --host HOST          Syslog Server Host
  --port PORT          Syslog Server Port (default: 514)
  --protocol PROTOCOL  The protocol to send syslog messages as (default: udp)
  --ssl                Webhook with dummy SSL (default: False)
  --version            show program's version number and exit
```

## Technologies & Frameworks Used

**Cisco Products & Services:**

- Cisco DNA Center

**Third-Party Products & Services:**

- Syslog Server

**Tools & Frameworks:**

- Python
- Flask
- Docker

## Authors & Maintainers

- Robert Csapo <rcsapo@cisco.com>

## Credits

Inspired by Oren Brigg at Cisco repo about syslog and Cisco DNA Center
https://github.com/obrigg/cisco-dnac-platform-syslog-audit

## License

This project is licensed to you under the terms of the [Cisco Sample
Code License](./LICENSE).
