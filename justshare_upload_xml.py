#!/usr/bin/python
import base64
import hashlib
from lxml import etree
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
    element_message = etree.Element('message')
    element_recipients = etree.Element("recipients", type="array")
    for r in recipients:
        element_recipient = etree.Element("recipient")
        element_recipient.text = r
        element_recipients.append(element_recipient)
    element_message.append(element_recipients)
    element_expires_at = etree.Element("expires_at")
    element_expires_at.text = expire.strftime("%Y-%m-%d")
    element_message.append(element_expires_at)
    element_subject = etree.Element("subject")
    element_subject.text = subject
    element_message.append(element_subject)
    element_message_body = etree.Element("message")
    element_message_body.text = message
    element_message.append(element_message_body)
    element_attachments = etree.Element("attachments", type="array")
    element_attachment = etree.Element("attachment")
    element_filename = etree.Element("filename")
    element_filename.text = os.path.basename(file)
    element_attachment.append(element_filename)
    element_data = etree.Element("data")
    element_data.text = data
    element_attachment.append(element_data)
    element_checksum = etree.Element("checksum")
    element_checksum.text = checksum
    element_attachment.append(element_checksum)
    element_attachments.append(element_attachment)
    element_message.append(element_attachments)
    element_send_email = etree.Element("send_email")
    element_send_email.text = "true"
    element_message.append(element_send_email)
    element_authorization = etree.Element("authorization")
    element_authorization.text = "3"
    element_message.append(element_authorization)
    payload = etree.tostring(element_message)
    req = urllib2.Request(url=url, data=payload)
    req.add_header("Authorization", auth)
    req.add_header("Content-Type", "text/xml")
    response = urllib2.urlopen(req)


send_file(
    "https://test.host/message",
    "KYdR1BRyoHhlESPLkoPYN9",
    ["someone@somewhere.com", ],
    "/tmp/hello.txt",
    "Hello world!"
)
