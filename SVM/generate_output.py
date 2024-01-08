import sys
import xml.etree.ElementTree as ET

results = []
note_map = {
    "0": "5,0",
    "1": "4,5",
    "2": "4,0",
    "3": "3,5",
    "4": "3,0",
    "5": "2,5",
    "6": "2,0",
    "7": "1,5",
    "8": "1,0",
    "9": "0,5" 
}

tree = ET.parse(sys.argv[1])
root = tree.getroot()
data = root.findall(".//comment")

for comment in data:
    comment_id = str(comment.find("review_id").text)
    results.append(comment_id)

with open("out.txt", mode="r", encoding="utf-8") as out_file:
    current = 0
    for row in out_file:
        results[current] += " " + note_map[row.rstrip("\n")]
        current += 1

with open("final_output.txt", "w") as f:
    f.write("\n".join(results))
