from flask import Flask, render_template, request
from datetime import datetime, timedelta

app = Flask(__name__)


def calculate_period(start_date, cycle_length, period_days):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")

    # 預計下次月經日期
    next_period = start_date + timedelta(days=cycle_length)

    # 排卵日為下次月經日往前推14天
    ovulation_day = next_period - timedelta(days=14)

    # 排卵期為排卵日前4天 ~ 排卵日後1天，總共6天
    ovulation_start = ovulation_day - timedelta(days=4)
    ovulation_end = ovulation_day + timedelta(days=1)

    return {
        "next_period": next_period.strftime("%Y-%m-%d"),
        "ovulation_start": ovulation_start.strftime("%Y-%m-%d"),
        "ovulation_end": ovulation_end.strftime("%Y-%m-%d"),
    }


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        start_date = request.form["start_date"]
        cycle_length = int(request.form["cycle_length"])
        period_days = int(request.form["period_days"])

        result = calculate_period(start_date, cycle_length, period_days)

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
