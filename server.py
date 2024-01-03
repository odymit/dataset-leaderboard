import csv
import json
import threading
from time import sleep

from pywebio import *
from pywebio.output import *

from process import process
from rsync import rsync_to_local

Terminate_Thread = False


def rsync_timer():
    global Terminate_Thread
    while not Terminate_Thread:
        rsync_to_local()
        sleep(3600)


def leaderboard():
    rsync_to_local()
    process()
    with open("./data.csv", "r") as f:
        data = list(csv.reader(f))
    with open("./failed.json", "r") as f:
        failed_lst = json.load(f)
    failed_lst = [[idx, key] for idx, key in enumerate(failed_lst.keys())]
    put_text("failed list").style("text-align:center;")
    put_datatable(
        failed_lst,
    )
    with use_scope("datatables"):
        put_text("results").style("text-align:center;")
        put_datatable(
            data,
            instance_id="user",
            height="auto",
            grid_args="resizable=true;sizeColumnsToFit=true;",
        )


if __name__ == "__main__":
    rsync = threading.Thread(target=rsync_timer)
    rsync.start()
    start_server(leaderboard, port=40000, debug=True)
    Terminate_Thread = True
