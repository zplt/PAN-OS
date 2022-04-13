import requests, urllib3, json, re
from bs4 import BeautifulSoup as bs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Rules:
    def __init__(self, fw_ip, fw_user, fw_passwd, rule, src_zone, src_ip, dst_zone, dst_ip, app, service="application-default",
                 action="Deny"):
        self.rule = rule
        self.src_zone = src_zone
        self.src_ip = src_ip
        self.dst_zone = dst_zone
        self.dst_ip = dst_ip
        self.app = app
        self.service = service
        self.action = action
        self.fw_ip = fw_ip
        self.fw_user = fw_user
        self.fw_passwd = fw_passwd

    def Create_Rules(self, url, json_data, api):
        header = {"X-PAN-KEY": f"{api}"}
        r = requests.post(url, headers=header, data=json.dumps(json_data), verify=False)
        response = r.text
        print(response)

    def Get_Api(self):
        try:
            api = ""
            url = f"https://{self.fw_ip}/api/?type=keygen&user={self.fw_user}&password={self.fw_passwd}"
            r = requests.get(url, verify=False)
            soup = bs(r.text, "html.parser")
            api = soup.find("key").contents[0]
            return api
        except Exception as err:
            print("ERROR : Connecting to " + self.fw_ip + ". Check the Firewall IP address or Credentials.")
            print("Error Kod: ", err)

    def Create_Object(self):
        # You can get more information about the json structure from the rest-api doc
        url = f"https://{self.fw_ip}/restapi/v10.1/Policies/SecurityRules?location=vsys&vsys=vsys1&name={self.rule}"
        json_data = {"entry": {"@name": self.rule,
                               "from": {"member": self.src_zone},
                               "source": {"member": self.src_ip},
                               "to": {"member": self.dst_zone},
                               "destination": {"member": self.dst_ip},
                               "application": {"member": self.app},
                               "service": {"member": self.service}, "action": self.action}}
        api = self.Get_Api()
        self.Create_Rules(url, json_data, api)



fw_ip = str(input("fw_ip : ")).strip("")
fw_user = str(input("fw_user : ")).strip("")
fw_passwd = str(input("fw_passwd : ")).strip("")

while True:
    try:
        rule = str(input("rule : ")).strip("")
        src_zone = str(input("src_zone : ")).strip("")
        src_ip = str(input("src_ip : ")).strip("")
        dst_zone = str(input("dst_zone : ")).strip("")
        dst_ip = str(input("dst_ip : ")).strip("")
        app = str(input("app : ")).strip("")
        service = str(input("service : ")).strip("")
        action = str(input("action : ")).strip("")
        rule = Rules(fw_ip, fw_user, fw_passwd, rule, src_zone, src_ip, dst_zone, dst_ip, app, service, action)
        rule.Create_Object()
        q = input("Do you want to continue (y/n) :   ")
        if q.lower() == "y":
            continue
        else:
            break
    except Exception as err:
        print("Error", err)
