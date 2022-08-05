import os
import json
import requests
import time

try:
    os.mkdir("downpdf")
except:
    pass

with open("names.json", "r") as f:
    names = json.load(f)

for name in names:
    response = requests.get("https://diploma.oznakn.com/gen/", params={"name": name})

    with open(f"downpdf/{name}.pdf", "wb") as f:
        f.write(response.content)
        time.sleep(0.2)
