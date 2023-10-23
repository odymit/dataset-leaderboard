import csv
import json
from operator import itemgetter
from pathlib import Path


def load_data(data_src_dir):
    failed_list = {}
    finished_list = {}
    sample_filter_list = {}
    for item in data_src_dir.iterdir():
        if "finished" in item.as_posix():
            for file in item.iterdir():
                filename = file.name.strip(file.suffix)
                
                if "activation" in file.as_posix():
                    continue
                if "rap" in file.as_posix():
                    continue
                if ".log" not in file.as_posix():
                    if "strip" in file.as_posix():
                        with open(file, "r") as f:
                            data = json.load(f)
                            sample_filter_list[filename] = data
                        continue
                    data = {}
                    with open(file, "r") as f:
                        data = json.load(f)
                    results = {}
                    print(len(data))
                    print(file)
                    if len(data) < 3:
                        results["c-acc"] = "-"
                    else:
                        results["c-acc"] = data[-1][f"test_clean_acc"]
                    results["b-acc"] = data[0][f"test_clean_acc/dataloader_idx_0"]
                    results["asr"] = data[1][f"test_asr/dataloader_idx_1"]
                    results["ra"] = data[1][f"test_ra/dataloader_idx_1"]

                    finished_list[filename] = results
        elif "failed" in item.as_posix():
            for file in item.iterdir():
                filename = file.name
                failed_list[filename] = "failed"
        else:
            pass
    return failed_list, finished_list, sample_filter_list
def get_sf_data(sample_filter_list):
    data = []
    for filename in sample_filter_list.keys():
        try:
            data_type, attack, dataset, model, _, pratio = filename.split("-")
            defense = "-"
        except:
            data_type, attack, dataset, model, _, pratio, defense = filename.split("-")

        tp, tn, fp, fn, acc, err, sen, pre, recall, f1 = itemgetter("tp", "tn", "fp", "fn", "acc", "err", "sen", "pre", "recall", "f1")(
            sample_filter_list[filename]
        )
        keys = [
            "data_type",
            "attack",
            "defense",
            "dataset",
            "model",
            "pratio",
            "tp", "tn", "fp", "fn", "acc", "err", "sen", "pre", "recall", "f1",
        ]
        values = [
            data_type,
            attack,
            defense,
            dataset,
            model,
            pratio,
        tp, tn, fp, fn, acc, err, sen, pre, recall, f1,
        ]
        cur_data = {}
        for k, v in zip(keys, values):
            cur_data[k] = v
        data.append(cur_data)
    return data


def get_format_data(finished_list):
    data = []
    for filename in finished_list.keys():
        try:
            data_type, attack, dataset, model, _, pratio = filename.split("-")
            defense = "-"
        except:
            data_type, attack, dataset, model, _, pratio, defense = filename.split("-")

        c_acc, b_acc, asr, ra = itemgetter("c-acc", "b-acc", "asr", "ra")(
            finished_list[filename]
        )
        keys = [
            "data_type",
            "attack",
            "defense",
            "dataset",
            "model",
            "pratio",
            "c-acc",
            "b-acc",
            "asr",
            "ra",
        ]
        values = [
            data_type,
            attack,
            defense,
            dataset,
            model,
            pratio,
            c_acc,
            b_acc,
            asr,
            ra,
        ]
        cur_data = {}
        for k, v in zip(keys, values):
            cur_data[k] = v
        data.append(cur_data)
    return data


def write2csv(data, filename):
    with open(filename, "w", encoding="utf8", newline="") as output_file:
        fc = csv.DictWriter(
            output_file,
            fieldnames=data[0].keys(),
        )
        fc.writeheader()
        fc.writerows(data)


if __name__ == "__main__":
    data_src_dir = Path(__file__).parent.parent / "logs/collections"
    failed_list, finished_list, sample_filter_list = load_data(data_src_dir)
    data = get_format_data(finished_list)
    sf_data = get_sf_data(sample_filter_list)
    # with open("data.json", "w", encoding="utf-8") as f:
        # json.dump(data, f)
    write2csv(data, "atk_data.csv")
    write2csv(sf_data, "strip_data.csv")
    print("data saved in: ./data.csv")
