from datetime import datetime, timedelta

def construct_query_view_month(query, month, year):
    first_day = datetime(year=year, month=month, day=1)
    first_day
