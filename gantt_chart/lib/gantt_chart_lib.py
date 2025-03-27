import pandas as pd





class GanttChartManager:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time


    def fetch_gantt_chart(self):
        self.get_data()

    def get_data(self):
        self.df_data = pd.read_csv("../data.csv").fillna("")
        # self.df_data['StartTime'] = pd.to_datetime(self.df_data["StartTime"])
        # self.df_data['EndTime'] = pd.to_datetime(self.df_data["EndTime"])
        


    def get_json_of_data(self):
        self.json_data = self.df_data.to_json(orient="records")
        return self.json_data