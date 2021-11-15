import logging
import requests
import azure.functions as func
from flatten_json import flatten
import pandas as pd
import json


#in the main function we need to include all the names that we specified in the function.json (in this case: req and outputblob)
def main(req: func.HttpRequest, outputblob: func.Out[str]):

    #logs the following message (while debugging):
    logging.info('Python HTTP trigger function processed a request.')

    #retrieves data from the server and writes it as a text file
    api = requests.get('https://api.spotify.com/v1/me/player/recently-played?limit=10&before=1635721200000&access_token=BQB7x-hZfOOXZzVRRqxLxIPgrJ_fso73JJMRzAc8PaYvXnpLTjKuH7vzYCJMJjG8zu46inv0-tw6wP4_8FuJNBwbZVqkKW1XFm_cMBcZ83-et-ZllJzEFoNLHQR8avQGnXVo5IL9VfdvM5tk')   
    data=api.json ()

    song_names=[] 
    artist_name=[] 
    played_at_list=[] 
  
    for song in data["items"]: 
        song_names.append(song["track"]["name"]) 
        artist_name.append(song["track"]["album"]["artists"][0]["name"]) 
        played_at_list.append(song["played_at"]) 
     
    song_dict = { 
        "song_name" : song_names, 
        "artist_name": artist_name, 
        "played_at" : played_at_list
    } 

    song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at"]) 
    result = song_df.to_json(orient="records")
    parsed = json.loads(result)
    new=json.dumps(parsed, indent=4) 

    print(parsed) 
    return outputblob.set(new)
