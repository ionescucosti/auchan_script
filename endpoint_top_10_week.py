import http.client
import json

conn = http.client.HTTPSConnection("imdb188.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "381b33ca41msh776e7ecbee33c7ap1b18f3jsna7f51d69063e",
    'x-rapidapi-host': "imdb188.p.rapidapi.com"
}

conn.request("GET", "/api/v1/getWeekTop10", headers=headers)

response = conn.getresponse()
json.loads(response.read().decode("utf-8"))