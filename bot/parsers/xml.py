from bs4 import BeautifulSoup
from typing import Any


class xmlParser:
    @classmethod
    def parseNode(cls, nodeName: str):
        with open(f"bot/github/blazium/doc/classes/{nodeName}", "r") as file:
            xml_content = file.read()


        soup = BeautifulSoup(xml_content, "xml")
        root = soup.find('class')


        tutorials: list[dict[str, str]] = []

        for link in root.find('tutorials').find_all('link'): # type: ignore
            title = link['title']# type: ignore
            url:str = link.text.strip()# type: ignore
            url:str = url.replace("$DOCS_URL", "https://docs.blazium.app")# type: ignore
            tutorials.append({"title": title, "url": url}) # type: ignore
        

        returnData: dict[str, Any] = {
            "name": root['name'],# type: ignore
            "inherits": root['inherits'],# type: ignore
            "description": root.find("description").text.strip(),# type: ignore
            "brief_desc": root.find('brief_desciprtion'),# type: ignore
            "tutorials": tutorials,
        }

        return returnData

