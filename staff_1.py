import plotly.graph_objs as go
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html

df = pd.read_excel("4.2(ii)- ftc vs oec - all staff - WMG.xlsx",header=[0,1])

###################### changing data that can be read by dash
df = df.rename(columns={"Unnamed: 0_level_0":"WMG",
                        "Unnamed: 1_level_0":"function","Unnamed: 1_level_1":"function2",
                        "Unnamed: 2_level_0":"grade1","Unnamed: 2_level_1":"grade2"})
df = df.replace({"Research Only":"2.Research Only", #give oder for label
                 "Support and Professional Staff":"4.Support and Professional Staff",
                 "Teaching Only":"3.Teaching Only",
                 "Teaching and Research":"1.Teaching and Research"
                    })

df = df.drop(["WMG"],axis=1)
df = df.set_index(["function"])
df = df.stack(0)
df = df.fillna(method="bfill")
df = df.reset_index()
df = df.rename(columns={"level_1":"year",
                        "grade2":"grade"})
df = df[df["year"] != "grade1"]
df = df.query('grade == ["FA 5","FA 6","FA 7","FA 8","FA 9","NON FA GRADE"]')
join_df = df.groupby(["grade","year"],as_index=False)[["Male FTC headcount","Female FTC headcount","Male OEC headcount","Female OEC headcount"]].sum()

#################

t =(join_df["Male FTC headcount"]+join_df["Female FTC headcount"]+
        join_df["Male OEC headcount"]+join_df["Female OEC headcount"])

join_df["Male FTC Proportion"]=(join_df["Male FTC headcount"]/t)
join_df["Female FTC Proportion"]=(join_df["Female FTC headcount"]/t)
join_df["Male OEC Proportion"]=(join_df["Male OEC headcount"]/t)
join_df["Female OEC Proportion"]=(join_df["Female OEC headcount"]/t)
join_df = join_df.round(decimals=2)
join_df = join_df.drop(["Male FTC headcount","Female FTC headcount","Male OEC headcount","Female OEC headcount"],axis=1)

yaxis=["Male FTC Proportion","Female FTC Proportion","Male OEC Proportion","Female OEC Proportion"]

trace = [go.Bar(
         x=[join_df["grade"],join_df["year"]],
         y=join_df[i],
         name=i
         ) for i in yaxis]

layout=go.Layout(title=dict(text="Headcount for FTC and OEC by grade by proportion",
                            y=0.9,
                            x=0.5,
                            xanchor="center",
                            yanchor="top"),
                 barmode="stack",
                 yaxis=dict(tickformat="%"),
                 legend=dict(title=None,
                             y=1.02, yanchor="bottom",
                             x=1, xanchor="right",
                             orientation="h"),
                legend_title_text='Click legend to filter data')

fig = dict(data=trace, layout=layout)
'''
app = dash.Dash()
app.layout= html.Div ([
                    dcc.Graph(id="protion",figure=fig)
                    ])


if __name__ == "__main__":
    app.run_server()
'''
###################################################################################################

#pyo.plot(fig, filename='df2.html')
#print(join_df)
