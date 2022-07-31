import requests
import altair as alt
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
url = 'https://agsi.gie.eu/api'
params = {
    "country": "de",
    "from": "2022-01-02",
    "size": 300
}
head = {
    "x-key": os.environ.get("API_KEY")
}


def create_diagram():
    resp = requests.get(url=url, params=params, headers=head)
    data = resp.json()

    if not data['data']:
        exit("Error reading data from api. Check API key")

    # Create pandas dataframe
    df = pd.json_normalize(data['data'])
    df['full'] = df['full'].astype(float)
    df['injection'] = df['injection'].astype(float)
    df['gasDayStart'] = pd.to_datetime(df['gasDayStart'], errors='coerce')

    # Create altair diagram
    base = alt.Chart(df).mark_line().encode(x=alt.X('gasDayStart', axis=alt.Axis(title="Datum", format="%b %Y"))
                                            )

    line = base.mark_line(color='red').encode(y=alt.Y('full',
                                                      axis=alt.Axis(title="FÃ¼llstand [%]"),
                                                      scale=alt.Scale(padding=0, domain=[0, 100])))

    bar = base.mark_bar(color='green').encode(y=alt.Y('injection',
                                                      axis=alt.Axis(title="Einspeisung [GWh/d]"))
                                              )

    diagram = line + bar

    diagram.properties(height=600, width=1200, title='Gasspeicher in Deutschland').resolve_scale(y='independent').save(
        'data.html')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    create_diagram()
