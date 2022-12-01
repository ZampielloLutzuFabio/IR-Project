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
  url = 'http://localhost:8983/solr/indiegames/query?rows=1000&q=' + quote_custom(query) + filter(filters)
  
  #print(url)
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

  #print(total_num, "games found.")
  #for doc in result:
        #print("Game =", doc)
        
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


sg.theme('DarkAmber')   # Add a touch of color


search("game", filters)

headings = ['Title', 'Author', 'Genre', 'Platform', 'Price', 'Sale']
font = ("Arial", 16)

# All the stuff inside your window.
layout = [  [sg.Text('Enter the game name'), sg.InputText(),  sg.Button('Ok', bind_return_key=True), sg.Button('Close')],
            [sg.Text('Enter filter'), sg.InputText()],
            [sg.Table(values=[], headings=headings, max_col_width=100,
                  justification='left',
                  num_rows=1000,
                  key='-TABLE-',
                  row_height=70,
                  size=(1000, 500),
                  font=font,
                  expand_x=True,
                  col_widths=200
                  )]
          ]

font = ("Arial", 24)
# Create the Window
window = sg.Window('Indie Games', 
                    layout,
                    resizable=True,
                    size=(2000, 1000),
                    font = font,
                    element_justification='c'
                    )
# Event Loop to process "events" and get the "values" of the inputs

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Close': # if user closes window or clicks cancel
      break
    print('You entered ', values[0])
    print('You filter ', values[1])
    array_val = values[0].split('|')
    search_result = search(array_val, [{values[1]}])
    game_information_array = []
    print(len(search_result))
    for i in search_result:
      del i['id']
      del i['_version_']
      try:
        i['genre'] = i['genre'][0:min(5, len(i['genre']))] 
      except:
        i['genre'] = 'Generic'
      game_information_array.append([textwrap.fill(''.join(i['title']), width=45), textwrap.fill(''.join(i['author']), width=45), textwrap.fill(','.join(i['genre']), width=45), textwrap.fill(','.join(i['platform']), width=45), ''.join(i['price']), ''.join(i['sale'])])
    #TODO : Change the append value with the result of our search with solr, so I suggest a method that creates
    # an array with the results and sends it to create table

    window['-TABLE-'].update(game_information_array)




window.close()










