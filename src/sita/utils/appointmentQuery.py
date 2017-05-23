from datetime import datetime, timedelta
from sita.appointments.models import Appointment
from calendar import monthrange

def construct_query_view_month(month, year):
    calendar = monthrange(year, month)
    first_day_month = datetime(year=year, month=month, day=1)
    last_day_month = datetime(year=year, month=month, day=calendar[1]) + timedelta(hours=23, minutes=59, seconds=59)
    query = Appointment.objects.extra(where=["date_appointment >= '{0}' and date_appointment <= '{1}'".format(first_day_month, last_day_month)]).order_by("date_appointment")
    return query
