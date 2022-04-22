import requests, urllib3, json, re
from bs4 import BeautifulSoup as bs

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Service:
    def __init__(self, fw_ip, fw_user, fw_passwd):
        self.fw_ip = fw_ip
        self.fw_user = fw_user
        self.fw_passwd = fw_passwd
        self.service = ""

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

    def tcp(self,List):
        api = self.Get_Api()
        for i in List:
            i=str(i).strip("\n")
            self.service = f"TCP-{i}"
            url = f"https://{self.fw_ip}/restapi/v10.1/Objects/Services?location=vsys&vsys=vsys1&name={self.service}"
            json_data = {"entry": {"@name": self.service,
                                   "protocol": {
                                       "tcp": {
                                           "port": f"{i}",
                                       }}}}
            header = {"X-PAN-KEY": f"{api}"}
            r = requests.post(url, headers=header, data=json.dumps(json_data), verify=False)
            response = r.text
            print(response)
    def udp(self,List):
        api = self.Get_Api()
        for i in List:
            i = str(i).strip("\n")
            self.service = f"UDP-{i}"
            url = f"https://{self.fw_ip}/restapi/v10.1/Objects/Services?location=vsys&vsys=vsys1&name={self.service}"
            json_data = {"entry": {"@name": self.service,
                                   "protocol": {
                                       "udp": {
                                           "port": f"{i}",
                                       }}}}
            header = {"X-PAN-KEY": f"{api}"}
            r = requests.post(url, headers=header, data=json.dumps(json_data), verify=False)
            response = r.text
            print(response)
    def Create_Service_Object(self):
        List = ""
        api = self.Get_Api()
        with open("services", "r") as file:
            List = file.readlines()
            file.close()
            url = f"https://{self.fw_ip}/restapi/v10.1/Objects/Services?location=vsys&vsys=vsys1&name={self.service}"
            while True:
                try:
                    q = str(input("Tyep TCP or UDP (T/U) Type 'E' for exit : "))
                    if q.lower() == "t":
                        self.tcp(List)
                    elif q.lower() == "u":
                        self.udp(List)
                    elif q.lower() == "e":
                        break
                    else:
                        print("please type 'T' , 'U' or 'E'")
                except Exception as err:
                    print("Error",err)

fw_ip = str(input("fw_ip : ")).strip("")
fw_user = str(input("fw_user : ")).strip("")
fw_passwd = str(input("fw_passwd : ")).strip("")

s = Service(fw_ip, fw_user, fw_passwd)
s.Create_Service_Object()
