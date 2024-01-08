import sys
import xml.etree.ElementTree as ET
import re
import emoji


# Text normalization
def normalize(text):
    words = []

    # ONLY KEEP WHOLE WORDS
    words = emoji.get_emoji_regexp().split(text)
    words = re.split(r"([,.!?\"])|\s", " ".join(words)) 
    words = list(filter(None, words))

    return words


# Glossary building
def build_glossary(data):
    glossary = set()

    # Variables for progress display
    current = 0
    total = len(data)

    # Comment loop
    for comment in data:
        # Progress display
        current += 1
        print("\r> Building glossary : " + str(current) + "/" + str(total), end="", flush=True)

        comment_text = str(comment.find("commentaire").text)
        words = normalize(comment_text)
        glossary.update(words)
    
    glossary = list(glossary)
    glossary.sort()

    # Writing the glossary
    with open("glossary.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(glossary))
    
    return glossary


# SVM file generation
def generate_svm(data, glossary):

    # Glossary and note map
    glossary_index = {word: str(index + 1) for index, word in enumerate(glossary)}
    note_map = {
        "5,0": "0",
        "4,5": "1",
        "4,0": "2",
        "3,5": "3",
        "3,0": "4",
        "2,5": "5",
        "2,0": "6",
        "1,5": "7",
        "1,0": "8",
        "0,5": "9"
    }

    # Variables for progress display
    current = 0
    total = len(data)

    results = []

    for comment in data:
        # Progress display
        current += 1
        print("\r> Building SVM : " + str(current) + "/" + str(total) + "          ", end="", flush=True)

        line_result = ""
        comment_text = str(comment.find("commentaire").text)
        note = comment.find("note")
        comment_note = "5,0" if note is None else str(comment.find("note").text)

        # Note class
        line_result += note_map[comment_note]

        words = normalize(comment_text)
        words = set(words)
        words = sorted(words)

        for word in words:
            if word in glossary_index:
                line_result += " " + str(glossary_index[word]) + ":" + str(comment_text.count(word))
        
        results.append(line_result)
        
    with open(".\output\out.svm", "w") as f:
        f.write("\n".join(results))
            


# Main function
if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        tree = ET.parse(sys.argv[1])
        root = tree.getroot()
        data = root.findall(".//comment")
        
        # Getting the glossary
        glossary = []
        if (len(sys.argv) > 2 and (sys.argv[2] == "-b" or sys.argv[2] == "--build")):
            dev_data = ET.parse("input\\dev.xml").getroot().findall(".//comment")
            train_data = ET.parse("input\\train.xml").getroot().findall(".//comment")
            test_data = ET.parse("input\\test.xml").getroot().findall(".//comment")
            g_data = [*dev_data, *train_data, *test_data]
            glossary = build_glossary(g_data)
        else:
            with open("glossary.txt", mode="r", encoding="utf-8") as g_file:
                for row in g_file:
                    glossary.append(row.rstrip("\n"))
        
        # Generating the svm file
        generate_svm(data, glossary)
          
    else:
        print("Veuillez spécifier un fichier de données.")