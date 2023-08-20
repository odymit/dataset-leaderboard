import csv
import json
from operator import itemgetter
from pathlib import Path


def load_data(data_src_dir):
    failed_list = {}
    finished_list = {}
    for item in data_src_dir.iterdir():
        if "finished" in item.as_posix():
            for file in item.iterdir():
                if ".log" not in file.as_posix():
                    data = {}
                    with open(file, "r") as f:
                        data = json.load(f)
                    results = {}
                    results["c-acc"] = data[-1][f"test_clean_acc"]
                    results["b-acc"] = data[0][f"test_clean_acc/dataloader_idx_0"]
                    results["asr"] = data[1][f"test_asr/dataloader_idx_1"]
                    results["ra"] = data[1][f"test_ra/dataloader_idx_1"]

                    filename = file.name.strip(file.suffix)
                    finished_list[filename] = results
        elif "failed" in item.as_posix():
            for file in item.iterdir():
                filename = file.name
                failed_list[filename] = "failed"
        else:
            pass
    return failed_list, finished_list


def get_format_data(finished_list):
    data = []
    for filename in finished_list.keys():
        data_type, attack, dataset, model, _, pratio = filename.split("-")
        c_acc, b_acc, asr, ra = itemgetter("c-acc", "b-acc", "asr", "ra")(
            finished_list[filename]
        )
        keys = [
            "data_type",
            "attack",
            "dataset",
            "model",
            "pratio",
            "c-acc",
            "b-acc",
            "asr",
            "ra",
        ]
        values = [data_type, attack, dataset, model, pratio, c_acc, b_acc, asr, ra]
        cur_data = {}
        for k, v in zip(keys, values):
            cur_data[k] = v
        data.append(cur_data)
    return data


def write2csv(data):
    with open("data.csv", "w", encoding="utf8", newline="") as output_file:
        fc = csv.DictWriter(
            output_file,
            fieldnames=data[0].keys(),
        )
        fc.writeheader()
        fc.writerows(data)


if __name__ == "__main__":
    data_src_dir = Path(__file__).parent.parent / "dataset_collections"
    failed_list, finished_list = load_data(data_src_dir)
    data = get_format_data(finished_list)
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f)
    # write2csv(data)
    print("data saved in: ./data.csv")
