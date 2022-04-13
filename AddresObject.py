import requests,urllib3,json,re
from bs4 import BeautifulSoup as bs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

Liste=[]
# ipaddress is text file which you put your ip address in
with open("ipaddres", "r") as file:
    Liste=file.readlines()
    file.close()


def Get_Api():
    fw_ip = str(input("Firewall Ip: ")).strip(" ")
    api=""
    user=str(input("User : "))
    paswd=str(input("password : "))
    # with this url can get your api addres even you can use your browser
    url=f"https://{fw_ip}/api/?type=keygen&user={user}&password={paswd}"
    r=requests.get(url, verify=False)
    soup=bs(r.text,"html.parser")
    api=soup.find("key").contents[0]
    print("(+) Adding the ip address")
    add_bulkAdress(fw_ip,api)


def add_bulkAdress(fw_ip,api):
    j=0
    for i in Liste:
        i=str(i).strip("\n")
        j +=1
        # Address object name you can change whatever you want
        address_name = f"Spiderman{j}"
        address_ip = i
        url=f"https://{fw_ip}/restapi/v10.1/Objects/Addresses?location=vsys&vsys=vsys1&name={address_name}"
        header={"X-PAN-KEY":f"{api}"}
        json_data = {"entry": {"@name": address_name, "ip-netmask": f"{i}"}}
        r=requests.post(url,headers=header,data=json.dumps(json_data),verify=False)
        print(r.text)
        # basic error handling process :)
        if "Invalid Query Parameter" in r.text:
            break
        else:
            continue


if __name__=="__main__":
    Get_Api()