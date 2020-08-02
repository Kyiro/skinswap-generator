#I know the code is kinda messy. It's made just to work for now
import requests

SearchURL = 'https://fortnite-api.com/v2/cosmetics/br/search?backendType=AthenaCharacter&matchMethod=contains&name='
PropertiesURL = 'https://benbotfn.tk/api/v1/assetProperties?path='

def check(data):
    try:
        if data["error"]:
            print("\nSomething went wrong!")
            print(data)
            exit()
    except KeyError:
        return

def GetCP(Skin):
    if not "/HID_" in Skin:
        SearchRequest = requests.get(SearchURL + Skin)
        SearchJson = SearchRequest.json()
        check(SearchJson)

        HID = SearchJson['data']['definitionPath']
    else:
        HID = Skin
    HidRequest = requests.get(PropertiesURL + HID)
    HidJson = HidRequest.json()
    check(HidJson)
    if "/HS_" in HidJson["export_properties"][0]["Specializations"][0]["assetPath"]:
        HS = HidJson["export_properties"][0]["Specializations"][0]["assetPath"]
    else:
        print("Couldn't find the HS")

    HsRequest = requests.get(PropertiesURL + HS)
    HsJson = HsRequest.json()
    check(HidJson)
    x = 0
    CPs = []
    for len in HsJson["export_properties"][0]["CharacterParts"]:
        CPs.append(HsJson["export_properties"][0]["CharacterParts"][x]["assetPath"])
        x += 1
    return CPs

print("What skin do you want to replace?")
BaseSkin = input()
print("What skin do you want to swap for?")
ReplaceSkin = input()
Base = GetCP(BaseSkin)
Replace = GetCP(ReplaceSkin)

if len(Replace) > 2:
    print(Replace)
    print(f"\nWhich CP/CPs would you like to remove? {len(Replace) - 2} CP/CPs to remove")
    while len(Replace) > 2:
        number = int(input()) - 1
        Replace.pop(number)



file = open("output.txt","w+")
#x = 0
#for len in Replace:
#    file.write(Replace[x] + "\n")
#    x += 1

#I know this part of the code is terrible and hardcoded but i'll fix it later
NormalCP = Base[0].split("/")
NormalCP = NormalCP[len(NormalCP) - 1].split(".")[0]
BrokenCP = NormalCP.replace("CP_", "1P_")

file.write("Generated using Kyiro#6468 skin swap tool\n")
file.write(NormalCP + "\n")
file.write(BrokenCP + "\n\n")
file.write("/Game/Athena/Heroes/Meshes/Bodies/CP_Body_Commando_F_RebirthDefaultA.CP_Body_Commando_F_RebirthDefaultA" + "\n")
file.write(Replace[0] + "\n\n")
file.write("/Game/Characters/CharacterParts/Female/Medium/Heads/CP_Head_F_RebirthDefaultA.CP_Head_F_RebirthDefaultA" + "\n")
file.write(Replace[1])


