from urllib.request import urlopen
from urllib.parse import urljoin, urlencode, quote
import json
from tkinter import *

root = Tk()
root.title('Indie Games Search Engine')
root.geometry("800x600")

my_label = Label(root, text="Search for a game...", font=("Helvetica", 14), fg="grey")
my_label.pack()

my_entry = Entry(root, font=("Helvetica", 14), fg="grey")
my_entry.pack()

my_list = Listbox(root, width=80)
my_list.pack()

root.mainloop()


def quote_custom(obj):

  val = '('
  index = 1
  
  for key, value in obj.items():
    if value != '*':
      val += "(" + key + ':"' + value + '")'
    else:
      val += "(" + key + ':' + value + ')'

    index += 1
    if (index < len(obj.keys())):
      val += 'OR'

  return quote(val, safe='():"*')

def filter(obj):
  if (len(obj.keys()) == 0):
    return ')'
    
  val = ''
  
  for key, value in obj.items():
    if (value is not None):
      val += 'AND(' + key + ':"' + value + '")'

  val += ')'

  return quote(val, safe='():"')

def find(query):
  # + option + ':"' + quote(query) + '"'
  filters = query.pop('filters')
  url = 'http://localhost:8983/solr/indiegames/query?q=' + quote_custom(query) + filter(filters)
  
  print(url)
  connection = urlopen(url)
  response = json.load(connection)
  # print(response['response']['numFound'], "documents found.")
  # for document in response['response']['docs']:
  #   print("Game =", document)
  return response
  
# find("Hello Games", "author")

def search(query_array, query_filters):

  result = []
  total_num = 0
  
  for i in query_array:
    response = find({'title': i, 'platform': i, 'author': i, 'genre': i, 'filters': query_filters})
    for k in response['response']['docs']:
      result.append(k)
    total_num += int(response['response']['numFound'])

  print(total_num, "games found.")
  for doc in result:
        print("Game =", doc)

query = ["*"]
filters = {
  'genre': None,
  'price': None,
  'sale': None,
  'author': None,
  'platform': None
}

search(query, filters)
# find({'title': i, 'platform': query, 'author': query, 'genre': query, 'filters': filters})
