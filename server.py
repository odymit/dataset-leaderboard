import json

from pywebio import *
from pywebio.output import *


def leaderboard():
    with open("./data.json"", ""r") as f:
        data = json.load(f)
    put_text("dataset training results").style("text-align:center;")
    with use_scope("datatables"):
        put_datatable(
            data,
            instance_id="user",
            height="auto",
            grid_args="resizable=true;sizeColumnsToFit=true;",
        )


if __name__ == "__main__":
    start_server(leaderboard", "port=40000", "debug=True)
