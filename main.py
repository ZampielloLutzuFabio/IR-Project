from turtle import heading
from urllib.request import urlopen
from urllib.parse import urljoin, urlencode, quote
import json
from venv import create
import PySimpleGUI as sg
import textwrap



def quote_custom(obj):

  val = '(('
  firstElement = True
  
  for key, value in obj.items():
    if value != '*':
      if firstElement:
        val += "(" + key + ':"' + value + '")'
        firstElement = False
      else:
        val += "OR(" + key + ':"' + value + '")'
    else:
      if firstElement:
        val += "(" + key + ':"' + value + '")'
        firstElement = False
      else:
        val += "OR(" + key + ':"' + value + '")'

  return quote(val, safe='():"*')


#TODO add extra filtering with more than one filter in the same category
def filter(obj):
  if (len(obj.keys()) == 0):
    return '))'
    
  val = ')'
  
  for key, value in obj.items():
    if (value is not None):
      val += 'AND(' + key + ':"' + value + '")'

  val += ')'

  return quote(val, safe='():"')

def find(query):
  # + option + ':"' + quote(query) + '"'
  filters = query.pop('filters')
  url = 'http://localhost:8983/solr/indiegames/query?rows=1000&q=' + quote_custom(query) + filter(filters)
  
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
      if k not in result:
        result.append(k)
    total_num += int(response['response']['numFound'])

  #print(total_num, "games found.")
  #for doc in result:
        #print("Game =", doc)
        
  return result


# GUI 


sg.theme('DarkAmber')   # Add a touch of color

headings = ['Button', 'Title', 'Author', 'Genre', 'Platform', 'Price', 'Sale']
font = ("Arial", 16)

# All the stuff inside your window.
layout = [  [sg.Text('Enter the game name'), sg.InputText(),  sg.Button('Ok', bind_return_key=True), sg.Button('Close')],
            [sg.Text('Enter genre filter'), sg.InputText()],
            [sg.Text('Enter price filter'), sg.InputText()],
            [sg.Text('Enter sale filter'), sg.InputText()],
            [sg.Text('Enter author filter'), sg.InputText()],
            [sg.Text('Enter platform filter'), sg.InputText()],
            [sg.Table(values=[], headings=headings, max_col_width=100,
                  justification='left',
                  num_rows=1000,
                  key='-TABLE-',
                  row_height=70,
                  size=(1000, 500),
                  font=font,
                  expand_x=True,
                  col_widths=200,
                  enable_events=True
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
    print(event)
    if event == sg.WIN_CLOSED or event == 'Close': # if user closes window or clicks cancel
      break
    if event == '-TABLE-':
      print(values[event])
    print('You entered', values[0])
    array_val = values[0].split('|')
    filters = {
      'genre': values[1] or None,
      'price': values[2] or None,
      'sale': values[3] or None,
      'author': values[4] or None,
      'platform': values[5] or None
    }
    print(filters)
    search_result = search(array_val, filters)
    game_information_array = []
    print(len(search_result))
    for i in search_result:
      del i['id']
      del i['_version_']
      try:
        i['genre'] = i['genre'][0:min(5, len(i['genre']))] 
      except:
        i['genre'] = 'Generic'
      game_information_array.append([sg.Button('Link'), textwrap.fill(''.join(i['title']), width=30), textwrap.fill(''.join(i['author']), width=30), textwrap.fill(','.join(i['genre']), width=30), textwrap.fill(','.join(i['platform']), width=30), ''.join(i['price']), ''.join(i['sale'])])
    #TODO : Change the append value with the result of our search with solr, so I suggest a method that creates
    # an array with the results and sends it to create table

    window['-TABLE-'].update(game_information_array)




window.close()










