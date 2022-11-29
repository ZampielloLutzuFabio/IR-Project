from urllib.request import urlopen
from urllib.parse import urljoin, urlencode, quote
import json
from tkinter import *
from tkinter import ttk


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
        
  return result

query = ["*"]
filters = {
  'genre': None,
  'price': None,
  'sale': None,
  'author': None,
  'platform': None
}

# search(query, filters)


root = Tk()
root.title('Indie Games Search Engine')
root.geometry("800x600")

def update(data):
	# Clear the listbox
  for item in my_list.get_children():
    my_list.delete(item['id'])
	# Add toppings to listbox
  for item in data:
	  my_list.insert(parent='', index='end', iid=item['id'],text="" ,values=(item['title'],item['author'],"item['genre']","item['platform']",item['price'],item['sale']))

def check(e):
  # grab what was typed
  typed = my_entry.get()
	# update our listbox with selected items
  update(search([typed], filters))				


my_label = Label(root, text="Search for a game...", font=("Helvetica", 14), fg="grey")
my_label.pack()

my_entry = Entry(root, font=("Helvetica", 14), fg="grey")
my_entry.pack(pady=20)







my_list = ttk.Treeview(root, height=100)
my_list['columns'] = ('Title', 'Author', 'Genre', "Platform", "Price", "Sale")
my_list.pack(pady=20)

my_list.heading("Title", text="Title")
my_list.heading("Author", text="Author")
my_list.heading("Genre", text="Genre")
my_list.heading("Platform", text="Platform")
my_list.heading("Price", text="Price")
my_list.heading("Sale", text="Sale")

# Create a binding on the entry box
my_entry.bind("<Return>", check)

root.mainloop()