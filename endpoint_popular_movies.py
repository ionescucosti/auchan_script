import http.client
import json
from pprint import pprint

conn = http.client.HTTPSConnection("imdb188.p.rapidapi.com")

payload = "{\"country\":{\"anyPrimaryCountries\":[\"IN\"]},\"limit\":200,\"releaseDate\":{\"releaseDateRange\":{\"end\":\"2029-12-31\",\"start\":\"2020-01-01\"}},\"userRatings\":{\"aggregateRatingRange\":{\"max\":10,\"min\":6},\"ratingsCountRange\":{\"min\":1000}},\"genre\":{\"allGenreIds\":[\"Action\"]},\"runtime\":{\"runtimeRangeMinutes\":{\"max\":120,\"min\":0}}}"

headers = {
    'x-rapidapi-key': "381b33ca41msh776e7ecbee33c7ap1b18f3jsna7f51d69063e",
    'x-rapidapi-host': "imdb188.p.rapidapi.com",
    'Content-Type': "application/json"
}

conn.request("POST", "/api/v1/getPopularMovies", payload, headers)

response = conn.getresponse()
json.loads(response.read().decode("utf-8"))