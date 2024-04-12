import pandas as pd
import plotly.graph_objects as go
import calendar

accidents = pd.read_csv("/Users/oscarmeurer/Downloads/accidentologie0.csv", sep=";")

def plot_seasonality_map(accidents_df):
    """ Function that takes into input the raw accident dataframe
    Returns a figure that can be used in a Streamlit object."""

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

    accidents = create_age_groups(accidents_df)

    accidents['Date'] = pd.to_datetime(accidents['Date'])
    accidents['Month'] = accidents['Date'].dt.month

    traces = []
    for age_group in accidents['Age_Group'].unique():
        data = accidents[accidents['Age_Group'] == age_group] #filtering the right group
        traces.append(go.Densitymapbox(lat=data['Latitude'], lon=data['Longitude'], z=data['Month'], radius=10))

    #print("traces", traces)
    fig = go.Figure(data=traces,
                     layout=go.Layout(mapbox=dict(center=dict(lat=48.8566, lon=2.3522), zoom=10, style="carto-positron")))
    #print("fig", fig)
    # Set first age group to be visible by default
    fig.data[0].visible = True

    # Update layout to include dropdown menu
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="down",
                active=0,
                x=0.1,
                y=0.9,
                pad={"r": 10, "t": 10},
                showactive=True,
                xanchor="left",
                yanchor="top",
                buttons=[
                    dict(
                        label=age_group,
                        method="update",
                        args=[{"visible": [True if age_group == group else False for group in accidents['Age_Group']]}]
                    )
                    for age_group in accidents['Age_Group'].unique()
                ]
            )
        ]
    )

    frames = []
    max_accidents = 0

    for month in range(1, 13):
        data = accidents[accidents['Month'] == month]

        frame_data = []

        for age_group in accidents['Age_Group'].unique():
            sub_data = data[data['Age_Group'] == age_group]
            frame_data.append(go.Densitymapbox(lat=sub_data['Latitude'], lon=sub_data['Longitude'], z=sub_data['Month'], radius=10))

        frame = go.Frame(data=frame_data)
        frames.append(frame)

        # Calculate total number of accidents for this frame
        total_accidents = len(data)
        if total_accidents > max_accidents:
            max_accidents = total_accidents

    print(max_accidents)

    fig.frames = frames

    # Create a list of dictionaries for animation options
    animation_options = [{"frame": {"duration": 300, "redraw": True},
                           "mode": "immediate",
                           "transition": {"duration": 300, "easing": "cubic-in-out"}} for month in range(1, 13)]

    # Create a list of steps using list comprehension
    slider_steps = [dict(args=[],  # Empty args list
                         label=calendar.month_name[month]) for month, _ in enumerate(animation_options, start=1)]

    # Combine animation options with slider steps (adding animation options to args)
    for i, step in enumerate(slider_steps):
        step['args'] = [animation_options[i]]  # Wrap the dictionary in a list

    fig.update_layout(
        updatemenus=[
            dict(
                type="dropdown",
                direction="down",
                buttons=[
                    dict(
                        label="Age Group",
                        method="update",
                        args=[{"visible": [True if age_group == group else False for group in accidents['Age_Group']]}]
                    )
                    for age_group in accidents['Age_Group'].unique()
                ],
                pad={"r": 10, "t": 10},
                x=0.1,
                xanchor="left",
                y=1.1,
                yanchor="top"
            ),
            dict(
                type="buttons",
                direction="right",
                buttons=[
                    dict(
                        args=[None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": True}],
                        label="Play",
                        method="animate"
                    ),
                    dict(
                        args=[[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate", "transition": {"duration": 0}}],
                        label="Pause",
                        method="animate"
                    )
                ],
                pad={"r": 10, "t": 10},
                showactive=False,
                x=0.2,
                xanchor="left",
                y=1.1,
                yanchor="top"
            )
        ],
        sliders=[dict(
            active=0,
            currentvalue={"prefix": "Month: ", "suffix": "", "font": {"size": 20}},
            pad={"b": 10, "t": 50},
            steps=slider_steps,
            ticklen=10,
            tickwidth=2
        )],
        yaxis=dict(range=[0, max_accidents])
    )


    #fig.show()
return fig

figure  = plot_seasonality_map(accidents)
