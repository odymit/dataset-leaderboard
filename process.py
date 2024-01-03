import csv
import json
import os
from operator import itemgetter
from pathlib import Path


def load_data(data_src_dir):
    failed_list = {}
    finished_list = {}
    for atk_dir in data_src_dir.iterdir():
        results_dir = atk_dir / "results.json"
        if results_dir.exists():
            filename = atk_dir.name.strip(atk_dir.suffix)
            data = {}
            with open(results_dir, "r") as f:
                data = json.load(f)
            results = {}
            if len(data) < 3:
                results["c-acc"] = "-"
            else:
                results["c-acc"] = data[-1][f"test_clean_acc"]
            results["b-acc"] = data[0][f"test_clean_acc/dataloader_idx_0"]
            results["asr"] = data[1][f"test_asr/dataloader_idx_1"]
            results["ra"] = data[1][f"test_ra/dataloader_idx_1"]

            finished_list[filename] = results
        else:
            filename = atk_dir.name
            failed_list[filename] = "failed"
    return failed_list, finished_list


def get_sf_data(sample_filter_list):
    data = []
    for filename in sample_filter_list.keys():
        try:
            data_type, attack, dataset, model, _, pratio = filename.split("-")
            defense = "-"
        except:
            data_type, attack, dataset, model, _, pratio, defense = filename.split("-")

        tp, tn, fp, fn, acc, err, sen, pre, recall, f1 = itemgetter(
            "tp", "tn", "fp", "fn", "acc", "err", "sen", "pre", "recall", "f1"
        )(sample_filter_list[filename])
        keys = [
            "data_type",
            "attack",
            "defense",
            "dataset",
            "model",
            "pratio",
            "tp",
            "tn",
            "fp",
            "fn",
            "acc",
            "err",
            "sen",
            "pre",
            "recall",
            "f1",
        ]
        values = [
            data_type,
            attack,
            defense,
            dataset,
            model,
            pratio,
            tp,
            tn,
            fp,
            fn,
            acc,
            err,
            sen,
            pre,
            recall,
            f1,
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


def process():
    data_src_dir = Path(__file__).parent / "logs"
    failed_list, finished_list = load_data(data_src_dir)
    # print(failed_list, finished_list)
    data = get_format_data(finished_list)
    with open("failed.json", "w", encoding="utf-8") as f:
        json.dump(failed_list, f)
    write2csv(data, "data.csv")
    # write2csv(sf_data, "strip_data.csv")
    print("data saved in: ./data.csv")


if __name__ == "__main__":
    process()
