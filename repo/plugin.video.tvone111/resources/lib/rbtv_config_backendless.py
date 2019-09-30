import pyamf
from pyamf import remoting
from pyamf.flex import messaging
import requests
import json


class rbtvConfig(object):
    def __init__(self, user=""):
        self.user = user
        self.url = "https://api.backendless.com/A73E1615-C86F-F0EF-FFDC-58ED0DFC6B00/7B3DFBA7-F6CE-EDB8-FF0F-45195CF5CA00/binary"
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1; AFTM Build/LMY47O)"})

    def get_data(self):
        data = {
            "clientId": None,
            "destination": "GenericDestination",
            "correlationId": None,
            "source": "com.backendless.services.persistence.PersistenceService",
            "operation": "first",
            "messageRefType": None,
            "headers": {"application-type": "ANDROID", "api-version": "1.0"},
            "timestamp": 0,
            "body": ["AppConfigCharlie"],
            "timeToLive": 0,
            "messageId": None,
        }
        msg = messaging.RemotingMessage(**data)
        req = remoting.Request(target="null", body=[msg])
        ev = remoting.Envelope(pyamf.AMF3)
        ev["null"] = req
        resp = requests.post(self.url, data=remoting.encode(ev).getvalue(), headers={"Content-Type": "application/x-amf"})
        resp_msg = remoting.decode(resp.content)
        config = json.dumps(resp_msg.bodies[0][1].body.body, default=lambda obj: repr(obj))
        return json.loads(config)
