import textract, nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag
from itertools import count

from docx import Document

affidavit = textract.process('Affidavit.docx')
sentencelist= filter(lambda word: word != '', affidavit.split("."))

sentencenumber = [i for i, sentence in enumerate(sentencelist) if ("page" in sentence)]


print sentencenumber

document = Document()


table = document.add_table(rows=1, cols=4)
table.style = "TableGrid"

hdr_cells = table.rows[0].cells
hdr_cells[0].text = 'Number'
hdr_cells[1].text = 'Exhibit'
hdr_cells[2].text = 'Date'
hdr_cells[3].text = 'Page number'

numbering = 0
for number in sentencenumber:
    sentence = sentencelist[number].split(" ")
    tagged_sent = pos_tag(sentencelist[int(number)].split())
    propernouns = [word for word,pos in tagged_sent if ((pos == 'NN' or word == "This") and word != "page" and word != "This" and word != "affidavit" and word != "January" and word != "evidence" and word != "copy")]

    row_cells = table.add_row().cells
    numbering +=1
    row_cells[0].text = str(numbering) +"."

    if propernouns != []:
        #print propernouns
        row_cells[1].text = " ".join(propernouns).title()

    else:
        row_cells[1].text = "REQUIRES ATTENTION! Full sentence is: " + sentencelist[number]

    #print sentence
    dates = [i for i, word in enumerate(sentence) if (("January" in word) or ("February" in word)or ("March" in word) or ("April" in word) or ("May" in word) or ("June" in word) or ("July" in word) or ("August" in word) or ("September" in word) or ("October" in word) or ("November" in word) or ("December" in word))]
    for date in dates:
        row_cells[2].text = sentence[date-1] + " " + sentence[date] + " " + sentence[date+1]





# exhibit_cells = table.row[1].cells

# exhibit_cells[1].text = str("1")

document.save('coversheet.docx')
