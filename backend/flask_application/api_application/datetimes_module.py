from datetime import datetime,timedelta,date


class Time:
    """
    simple class that returns list of the dates from the current day and seven days before

    Methods:
        week_reversed:
            gets no arguments returns the updated week reversed list of dates
    """
    def week_reversed(self) -> list:
        #
        today = str(date.today())
        week_dates_list = []
        format_dates = datetime.strptime(today,"%Y-%m-%d")
        for i in range(1,8):
            week_dates_list.append(str(format_dates+timedelta(days=-i))[:10:])

        return week_dates_list

