
import json
import re

LINK_PATTERN = re.compile(r"<a.*</a>")


a = json.load(open("Model\\intents.json", "r"))


for i in a["intents"]:
    res = i["responses"]
    for j in res:
        if "href" in j:
            link_part = re.findall(LINK_PATTERN, j)[0]
            parts = j.split(link_part)
            
            prefix = parts[0].strip()
            suffix = parts[1].strip()


            link = link_part.strip('</a>').strip().split('">')
            hyper_link = link.pop().strip()
            link = link[0].split('"').pop()

            res.append({
                "web": j,
                "telegram": j,
                "discord": f"{prefix} [{hyper_link}]({link}) {suffix}"
            })
            res.remove(j)
    print(res)

json.dump(a, open("Model\\intents.json", "w"))