import requests,urllib3,json,re
from bs4 import BeautifulSoup as bs

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

Liste=[]
with open("text", "r") as file:
    Liste=file.readlines()
    file.close()


def Get_Api():
    try:
        fw_ip = str(input("Firewall Ip: ")).strip(" ")
        api=""
        user=str(input("User : "))
        paswd=str(input("password : "))
        url=f"https://{fw_ip}/api/?type=keygen&user={user}&password={paswd}"
        r=requests.get(url, verify=False)
        soup=bs(r.text,"html.parser")
        api=soup.find("key").contents[0]
        add_bulkAdress(fw_ip,api)
    except Exception as err:
        print("ERROR : Connecting to " + fw_ip + ". Check the Firewall IP address or Credentials.")
        print("Error Kod: ",err)

def add_bulkAdress(fw_ip,api):
    try:
        j=0
        for i in Liste:
            i=str(i).strip("\n")
            j +=1
            address_name = f"Uptime{j}"
            address_ip = i
            url=f"https://{fw_ip}/restapi/v10.1/Objects/Addresses?location=vsys&vsys=vsys1&name={address_name}"
            header={"X-PAN-KEY":f"{api}"}
            json_data = {"entry": {"@name": address_name, "ip-netmask": f"{i}"}}
            r=requests.post(url,headers=header,data=json.dumps(json_data),verify=False)
            print(r.text)
            if "Invalid Query Parameter" in r.text:
                break
            else:
                continue
    except Exception as err:
        print("Error Kod: ", err)

if __name__=="__main__":
    Get_Api()
