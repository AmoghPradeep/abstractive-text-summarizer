from model1 import model
from flask import Flask, render_template, url_for, redirect
from flask import request as req
import flask
import PyPDF2
import re
from apiclient.discovery import build
from urllib.request import urlopen
from bs4 import BeautifulSoup
app = Flask(__name__)

# app.config['uploads']
def search_url(toSearch):
    api_key = "AIzaSyDzge6TKdWatSdRdnMQ8pJ0WZEuZSiE0sU"
    search_engine_id = "e1489b4c883bf51e6"

    resource = build("customsearch", "v1", developerKey = api_key).cse()
    result = resource.list(q = toSearch, cx = search_engine_id).execute()  #for images give another attribute searchType = "image"

    link = result['items'][0]['link']
    return get_page(link)

def get_page(url):
    # Specify url of the web page
    source = urlopen(url).read()

    # Make a soup
    soup = BeautifulSoup(source,'lxml')

    # Extract the plain text content from paragraphs
    paras = []
    for paragraph in soup.find_all('p'):
        paras.append(str(paragraph.text))

    # print(paras)
    # Extract text from paragraph headers
    heads = []
    for head in soup.find_all('span', attrs={'mw-headline'}):
        heads.append(str(head.text))

    # Interleave paragraphs & headers
    text = [val for pair in zip(paras, heads) for val in pair]
    text = ' '.join(text)

    # Drop footnote superscripts in brackets
    text = re.sub(r"\[.*?\]+", '', text)

    # Replace '\n' (a new line) with '' and end the string at $1000.
    text = text.replace('\n', '')[:-11]
    return text


fileSummary = ""
m = model()
@app.route('/')
def home():
   return render_template('struct.html')

@app.route("/Summarize",methods=["GET","POST"])
def Summarize(text):
   text_list = text.split(" ")
   text_len = len(text.split(" "))
   summary = ""
   curr_len = 0
   block = ""
   for word in text_list:
      block = block + " " + word
      curr_len += 1
      if (curr_len == 1023):
         summary += m.summarize(block)
         curr_len = 0
         block = ""

   summary += m.summarize(block)
   if len(summary.split(" ")) >= 1024:
      Summarize(summary)
   elif len(summary.split(" ")) >= 200:
      while(len(summary.split(" ")) >= 200):
         summary = m.summarize(summary)
      return summary
   else:
      return summary



def summarizeDocument(file):
   print("overhere")
   print(file)
   file.save("test.pdf")
   print("saved ? ")
   pdfFileObj = open(r'test.pdf', 'rb')
   pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
   pageObj = pdfReader.getPage(0)
   text = ""
   for i in range (0, pdfReader.numPages):
      text = text + str(pdfReader.getPage(i).extractText())

   text = re.sub("\s+", " ", text)
   output = Summarize(text)
   pdfFileObj.close()

   return text

def summarizeLink(value):
   raw_text = re.sub("\s+", " ", value)
   links = raw_text.split(" ")
   pages = []
   for link in links:
      pages.append(get_page(link))

   summaries = []
   final_summary = ""
   for page in pages:
      final_summary += Summarize(page) + ".\n\n"

   return final_summary


def summarizeKeyword(keys):
   re.sub("\s+", "\n", keys)
   keywords = keys.split("\n")
   pages = []
   for key in keywords:
      pages.append(search_url(key))
   summaries = []
   final_summary = ""
   for page in pages:
      final_summary += Summarize(page) + ".\n\n"
   return final_summary

def summarizeText(text):
   return Summarize(text)

@app.route("/process/", methods=["GET","POST"])
def process():
   if req.method == "POST":
      value = req.json["data"]
      mode = req.json["mode"]
      if mode == "text":
         return summarizeText(value)
      elif mode == "link":
         return summarizeLink(value)
      elif mode == "key":
         return summarizeKeyword(value)

   else:
      return render_template("struct.html")


@app.route("/upload", methods=["post"])
def upload():
   print(req.files)
   fileSummary = summarizeDocument(req.files["file"]) + "\n"
   return render_template("struct.html", result = fileSummary)
if __name__ == '__main__':
   app.run()