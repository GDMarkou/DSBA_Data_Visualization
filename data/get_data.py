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

print(get_data().head())


def create_age_groups(df):
    data = df.copy()

    def create_age_group(age):
        if age <= 18:
            return '0-18'
        elif 19 <= age <= 25:
            return '19-25'
        elif 26 <= age <= 35:
            return '26-35'
        elif 36 <= age <= 45:
            return '36-45'
        elif 46 <= age <= 55:
            return '46-55'
        elif 56 <= age <= 65:
            return '56-65'
        else:
            return '65+'

    data['Age_Group'] = data['Age'].apply(create_age_group)

    return data
