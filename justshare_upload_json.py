#!/usr/bin/python
import base64
import hashlib
import json
import datetime
import os
import urllib2


def send_file(url, apikey, recipients, file, subject,
              message="As Requested ..."):
    data = None
    checksum = None
    expire = datetime.datetime.now() + datetime.timedelta(hours=24)
    auth = "Basic " + base64.b64encode(apikey + ":x").rstrip()
    with open(file, "rb") as data_file:
        raw = data_file.read()
        data = base64.b64encode(raw)
        checksum = hashlib.md5(raw).hexdigest()
    payload = {
        "message": {
            "recipients": recipients,
            "subject": subject,
            "message": message,
            "expires_at": expire.strftime("%Y-%m-%d"),
            "send_email": "true",
            "authorization": 3,
            "attachments": [{
                "filename": os.path.basename(file),
                "data": data,
                "checksum": checksum
            }]
        }
    }
    req = urllib2.Request(url=url, data=json.dumps(payload))
    req.add_header("Authorization", auth)
    req.add_header("Content-Type", "application/json")
    response = urllib2.urlopen(req)


send_file(
    "https://test.host/message",
    "KYdR1BRyoHhlESPLkoPYN9",
    ["someone@somewhere.com", ],
    "/tmp/hello.txt",
    "Hello World!"
)
