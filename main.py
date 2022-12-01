from turtle import heading
from urllib.request import urlopen
from urllib.parse import urljoin, urlencode, quote
import json
from venv import create
import PySimpleGUI as sg
import textwrap



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



# GUI 

def create_table(data_array):

  headings = ['Title', 'Author', 'Genre', 'Platform', 'Price', 'Sale', 'href']

  games_window_layout = [
      [sg.Table(values=data_array, headings=headings, max_col_width=35,
                  auto_size_columns=True,
                  justification='left',
                  num_rows=1000,
                  key='-TABLE-',
                  tooltip='Indie Game Search')]
  ]

  games_window = sg.Window("Games Window", 
  games_window_layout, modal=True)

  while True:
      event, values = games_window.read()
      if event == "Exit" or event == sg.WIN_CLOSED:
          break
      
  games_window.close()

sg.theme('DarkAmber')   # Add a touch of color




# All the stuff inside your window.
layout = [  [sg.Text('Enter the game name'), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Close')]
          ]


# Create the Window
window = sg.Window('Indie Games', 
                    layout,
                    resizable=True,
                    size=(800, 900))
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Close': # if user closes window or clicks cancel
        break
    print('You entered ', values[0])
    search_result = search([values[0]], filters)
    game_information_array = []
    for i in search_result:
      del i['id']
      del i['_version_']
      print(i)
      game_information_array.append([textwrap.fill(''.join(i['title'])), textwrap.fill(''.join(i['author'])), textwrap.fill(','.join(i['genre']), width=45), textwrap.fill(','.join(i['platform'])), i['price'], textwrap.fill(''.join(i['sale'])), textwrap.fill(''.join(i['href']))])
    #TODO : Change the append value with the result of our search with solr, so I suggest a method that creates
    # an array with the results and sends it to create table
    create_table(game_information_array)



window.close()










