import pandas as pd
import requests
import pandas as pd
def get_data():
    url = 'https://raw.githubusercontent.com/omeurer/road-accident-paris-data-viz/master/data/full_data.json'


    # Fetch the JSON file from the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the JSON data
        data = response.json()["results"]

        # Convert JSON data to DataFrame
        df = pd.DataFrame(data)
        print("the df is length", len(df))

    else:
        print('Failed to fetch data from GitHub:', response.status_code)
        df = None
    return df

#print(get_data().head())
