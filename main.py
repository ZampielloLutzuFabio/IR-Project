from urllib.request import urlopen
import json

print("Enter title")
title = input()
connection = urlopen('http://localhost:8983/solr/IndieGames/select?indent=true&q.op=OR&q=' + str(title))
response = json.load(connection)
print(response['response']['numFound'], "documents found.")

# Print the name of each document.

for document in response['response']['docs']:
  print("Game =", document['platform'])