from gantt_chart.lib.gantt_chart_lib import *
import pandas as pd


def run():
    end_t = pd.Timestamp.now()
    start_t = end_t - pd.Timedelta(days=1)
    manager = GanttChartManager(start_t, end_t)
    manager.fetch_gantt_chart()