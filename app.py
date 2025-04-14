from flask import Flask, render_template, request
from datetime import datetime, timedelta
import calendar

app = Flask(__name__)


def calculate_period(start_date, cycle_length, period_days):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    next_period = start_date + timedelta(days=cycle_length)
    ovulation_day = next_period - timedelta(days=14)
    ovulation_start = ovulation_day - timedelta(days=4)
    ovulation_end = ovulation_day + timedelta(days=1)

    return {
        "next_period": next_period,
        "ovulation_start": ovulation_start,
        "ovulation_end": ovulation_end,
        "period_days": period_days,
    }


def get_calendar_with_highlight(year, month, highlights):
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.itermonthdates(year, month)
    calendar_matrix = []
    week = []

    for day in month_days:
        classes = []
        if day.month != month:
            classes.append("other-month")
        if day in highlights:
            classes.append(highlights[day])
        week.append((day, " ".join(classes)))
        if len(week) == 7:
            calendar_matrix.append(week)
            week = []

    return calendar_matrix


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    current_month = datetime.today().month
    current_year = datetime.today().year
    calendar1 = calendar2 = []

    if request.method == "POST":
        start_date = request.form["start_date"]
        cycle_length = int(request.form["cycle_length"])
        period_days = int(request.form["period_days"])

        result = calculate_period(start_date, cycle_length, period_days)

        highlights = {}

        current = result["ovulation_start"]
        while current <= result["ovulation_end"]:
            highlights[current.date()] = "ovulation"
            current += timedelta(days=1)

        for i in range(result["period_days"]):
            period_date = result["next_period"] + timedelta(days=i)
            highlights[period_date.date()] = "period"

        calendar1 = get_calendar_with_highlight(
            result["ovulation_start"].year, result["ovulation_start"].month, highlights
        )

        calendar2 = get_calendar_with_highlight(
            result["next_period"].year, result["next_period"].month, highlights
        )

    return render_template(
        "index.html", result=result, calendar1=calendar1, calendar2=calendar2
    )


if __name__ == "__main__":
    app.run(debug=True)
