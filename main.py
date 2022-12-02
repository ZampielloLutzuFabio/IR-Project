from urllib.request import urlopen
from urllib.parse import quote
import json
import PySimpleGUI as sg
import textwrap
import webbrowser


def quote_custom(obj):

    val = "(("
    firstElement = True

    for key, value in obj.items():
        if value != "*":
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
                val += "OR(" + key + ':' + value + ')'

    return quote(val, safe='():"*')

def filter(obj):
    if len(obj.keys()) == 0:
        return "))"

    val = ")"

    for key, value in obj.items():
        if value is not None:
            if isinstance(value, list):
                for i in value:
                    val += "AND(" + key + ':"' + i + '")'
            else:
                val += "AND(" + key + ':"' + value + '")'

    val += ")"

    return quote(val, safe='():"')


def find(query):
    # + option + ':"' + quote(query) + '"'
    filters = query.pop("filters")
    url = (
        "http://localhost:8983/solr/indiegames/query?rows=1000&q="
        + quote_custom(query)
        + filter(filters)
    )
    connection = urlopen(url)
    response = json.load(connection)
    # print(response['response']['numFound'], "documents found.")
    # for document in response['response']['docs']:
    #   print("Game =", document)
    return response


def search(query_array, query_filters):

    result = []
    total_num = 0

    for i in query_array:
        response = find(
            {
                "title": i,
                "platform": i,
                "author": i,
                "genre": i,
                "filters": query_filters,
            }
        )
        for k in response["response"]["docs"]:
            if k not in result:
                result.append(k)
        total_num += int(response["response"]["numFound"])

    return result


# GUI


sg.theme("DarkBlue")  # Add a touch of color

headings = ["Title", "Author", "Genre", "Platform", "Price {Sale}", "Description"]
font = ("Arial", 16)

game_information_array = []
game_hrefs = []

# All the stuff inside your window.
layout = [
    [
        sg.Text("Enter the game name"),
        sg.InputText(),
        sg.Button("Search", bind_return_key=True),
        sg.Button("Close"),
        # sg.Button("Hide/Show filters", key="HIDE_FILTERS"),
    ],
    [
        sg.Text("Enter genre filter", key="genre_filter_text"),
        sg.InputText(key="genre_filter", tooltip="Genre filter"),
    ],
    [
        sg.Text("Enter price filter", key="price_filter_text"),
        sg.InputText(key="price_filter", tooltip="Price filter"),
    ],
    [
        sg.Text("Enter sale filter", key="sale_filter_text"),
        sg.InputText(key="sale_filter", tooltip="Sale filter"),
    ],
    [
        sg.Text("Enter author filter", key="author_filter_text"),
        sg.InputText(key="author_filter", tooltip="Author filter"),
    ],
    [
        sg.Text("Enter platform filter", key="platform_filter_text"),
        sg.InputText(key="platform_filter", tooltip="Platform filter"),
    ],
    [
        sg.Table(
            values=game_information_array,
            headings=headings,
            # col_widths=[200, 200, 200, 200, 5, 350],
            auto_size_columns=True,
            # max_col_width=100,
            justification="left",
            num_rows=1000,
            key="-TABLE-",
            row_height=90,
            size=(1000, 500),
            font=font,
            enable_events=True,
            row_colors=(),
            expand_x=True
        )
    ],
]

font = ("Arial", 24)
# Create the Window
window = sg.Window(
    "Indie Games",
    layout,
    resizable=True,
    size=(2000, 1000),
    font=font,
    element_justification="c",
    finalize=True
)

window.FindElement('-TABLE-').AlternatingRowColor=[('#223F5D')]
# window.Maximize()
# Event Loop to process "events" and get the "values" of the inputs
col_widths = [300, 300, 300, 250, 150, 530]
table_widget = window['-TABLE-'].widget

for cid, width in zip(headings, col_widths):    # Set width for each column
      table_widget.column(cid, width=width)

table_widget.pack_forget()

table_widget.pack(side='left', fill='both', expand=True)

while True:
    event, values = window.read()
    if event == "-TABLE-":
        webbrowser.open(game_hrefs[values[event][0]][0])
    # elif event == "HIDE_FILTERS":
    #     isHidden = window["genre_filter_text"].visible

    #     window["genre_filter_text"].Update(visible=not isHidden)
    #     window["genre_filter"].Update(visible=not isHidden)

    #     window["price_filter_text"].Update(visible=not isHidden)
    #     window["price_filter"].Update(visible=not isHidden)

    #     window["sale_filter_text"].Update(visible=not isHidden)
    #     window["sale_filter"].Update(visible=not isHidden)

    #     window["author_filter_text"].Update(visible=not isHidden)
    #     window["author_filter"].Update(visible=not isHidden)

    #     window["platform_filter_text"].Update(visible=not isHidden)
    #     window["platform_filter"].Update(visible=not isHidden)

    #     if isHidden:
    #       window.Element("-TABLE-").Update() # TODO check how to resize table after hiding filters
    #     else:
    #       window.Element("-TABLE-").Update()
    elif event == sg.WIN_CLOSED or event == "Close":
        break
    array_val = values[0].split("|")
    filters = {
        "genre": values["genre_filter"].split("|") or None,
        "price": values["price_filter"].split("|") or None,
        "sale": values["sale_filter"].split("|") or None,
        "author": values["author_filter"].split("|") or None,
        "platform": values["platform_filter"].split("|") or None,
    }

    search_result = search(array_val, filters)
    game_information_array = []
    game_hrefs = []

    for i in search_result:
        try:
            i["genre"] = i["genre"][0 : min(5, len(i["genre"]))]
        except:
            i["genre"] = "Generic"
        game_information_array.append(
            [
                textwrap.fill("".join(i["title"]), width=25),
                textwrap.fill("".join(i["author"]), width=30),
                textwrap.fill(",".join(i["genre"]), width=28),
                textwrap.fill(",".join(i["platform"]), width=30),
                "".join(i["price"]) + " {" + "".join(i["sale"]) + "}",
                textwrap.fill(",".join(i["description"]), width=50),
            ]
        )
        # game_information_array.append([i['description'], '', '', '', '', ''])
        game_hrefs.append(i["href"])

    if len(game_information_array) == 0:
      game_information_array.append([textwrap.fill('No Results Were Found', width=30), '', '', '', '', ''])

    window["-TABLE-"].update(game_information_array)


window.close()
