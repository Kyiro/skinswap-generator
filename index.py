import requests
import requests_cache

requests_cache.install_cache('cache')

SearchURL = 'https://fortnite-api.com/v2/cosmetics/br/search?backendType=AthenaCharacter&matchMethod=contains&name='
PropertiesURL = 'https://benbotfn.tk/api/v1/assetProperties?path='

class GetCP:
    def __init__(self, name):
        if not "/HID_" in name:
            Search = requests.get(SearchURL + name).json()
            HID = Search['data']['definitionPath']
            CID = Search['data']['path']
            CID = CID.replace("FortniteGame/Content", "/Game")
            CID = CID + "." + Search['data']['id']
        else:
            HID = name
            CID = ""
        HSsearch = requests.get(PropertiesURL + HID).json()
        if "/HS_" in HSsearch["export_properties"][0]["Specializations"][0]["assetPath"]:
            HS = HSsearch["export_properties"][0]["Specializations"][0]["assetPath"].split(".")[0]
        else:
            print("Couldn't find the HS")
        CPsearch = requests.get(PropertiesURL + HS).json()
        x = 0
        CPs = []
        for len in CPsearch["export_properties"][0]["CharacterParts"]:
            item = CPsearch["export_properties"][0]["CharacterParts"][x]["assetPath"]
            if "Bodies" in item:
                CPs.insert(0, item)
            elif "Head" in item:
                CPs.insert(1, item)
            elif "FaceAcc" or "Hat" in item:
                CPs.insert(2, item)
            else:
                CPs.insert(3, item)
            x += 1
        NormalCP = CPs[1].split("/")[-1].split(".")[0]
        BrokenCP = NormalCP.replace("CP_", "1P_")
        self.replaceCPs = [NormalCP, BrokenCP]
        self.array = CPs
        self.CID = CID

print('What skin do you want to Replace? (use "Recruit" for the default skins)')
Base = str(input()).lower()
if Base == "recruit":
    Base = 1
else:
    Base = GetCP(Base)
print("What skin do you want to swap for?")
Replace = GetCP(input())

if len(Replace.array) > 2:
    print(Replace.array)
    print(f"\nWhich CP/CPs would you like to remove? {len(Replace.array) - 2} CP/CPs to remove")
    while len(Replace.array) > 2:
        number = int(input()) - 1
        Replace.array.pop(number)

file = open("output.txt","w+")

file.write("Generated using Kyiro#6468 skin swap tool\n")
if Base == 1:
    file.write("CP_Body_Commando_F_RebirthDefaultA" + "\n")
    file.write("1P_Body_Commando_F_RebirthDefaultA" + "\n\n")
    file.write("CP_Athena_Body_M_RebirthSoldier" + "\n")
    file.write("1P_Athena_Body_M_RebirthSoldier" + "\n\n")
else:
    file.write(Base.replaceCPs[0] + "\n")
    file.write(Base.replaceCPs[1] + "\n\n")
file.write("/Game/Athena/Heroes/Meshes/Bodies/CP_Body_Commando_F_RebirthDefaultA.CP_Body_Commando_F_RebirthDefaultA" + "\n")
file.write(Replace.array[0] + "\n\n")
file.write("/Game/Characters/CharacterParts/Female/Medium/Heads/CP_Head_F_RebirthDefaultA.CP_Head_F_RebirthDefaultA" + "\n")
file.write(Replace.array[1] + "\n")