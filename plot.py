from collections import OrderedDict
from datetime import datetime
import argparse
import json
from plot_tb import draw_plots


parser = argparse.ArgumentParser()
parser.add_argument("--debug", default="False")
args = parser.parse_args()
debug = False if args.debug == "False" else True

# Plotting parameters
output_folder_prefix = "img/"
output_folder_suffix = ""

# input_json_path = 'lr_file_names.json'
input_json_path = "plot_config.json"

with open(input_json_path, 'r') as in_file:
    input_json = json.load(in_file)


def provide_file_names(task):
    file_names = OrderedDict(input_json["tasks"][task]["file_names"])
    model_order = input_json["tasks"][task]["order"]
    for model_name in model_order:
        file_names.move_to_end(model_name)
    return file_names


def parse_func(file_name):
    """
    NOTE: Change this function to fit the log file format.
    This function must receive file name as argument as return list of x values
    and list of y values.
    """
    with open(file_name, "r") as in_file:
        lines = in_file.readlines()

    x_list = []
    y_list = []

    for line in lines[1:]:
        x, y = line.split()
        x = float(x)
        y = float(y)
        x_list.append(x)
        y_list.append(y)

    return x_list, y_list


if __name__ == "__main__":
    output_folder = output_folder_prefix
    if debug is True:
        output_folder += "dbg"
    else:
        output_folder += datetime.now().strftime("%Y%m%d_%H%M")
        output_folder += output_folder_suffix

    exp_note = input_json["exp_note"]

    for task, config in input_json["tasks"].items():
        print("task: {}".format(task))
        result_png_path = "./{}/{}.png".format(output_folder, task)
        file_names = provide_file_names(task)

        draw_plots(file_names, result_png_path, config, exp_note)

        print("Plot saved to {}".format(result_png_path))
