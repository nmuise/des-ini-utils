#!/usr/bin/env python

import argparse
import os
import json
from pprint import pprint
from future.moves.itertools import zip_longest

const_prefix = "::InstallAPI::SetVirtualText -virtualtext"

class IniCompare(object):
    def __init__(self, filepath1, filepath2, dump_flag=False):
        self.filepath1 = os.path.abspath(filepath1)
        self.filepath2 = os.path.abspath(filepath2)

        filename1 = os.path.basename(self.filepath1)
        filename2 = os.path.basename(self.filepath2)
        if filename1 == filename2:
            self.filename1 = self.filepath1
            self.filename2 = self.filepath2
        else:
            self.filename1 = filename1
            self.filename2 = filename2

        self.dump_flag = dump_flag

        self.file1_parsed = self.load(self.filepath1)
        if not self.dump_flag:
            self.file2_parsed = self.load(self.filepath2)

    def load(self, path):
        """Convert the contents of the supplied INI file to a dictionary with three
        sections: 
            - params, which holds a map with pairs of the format
                <var>: {"-value": <value>, 
                        "prefix": "::InstallAPI::SetVirtualText -virtualtext"}
                , populated by entries in the given INI file of the format
                ::InstallAPI::SetVirtualText -virtualtext {var} -value {value}
            - comments, which holds a list of all the comments of the file
            - other, which holds a list of all non-comment, non-empty lines that 
                don't start with "::InstallAPI::SetVirtualText -virtualtext".
        """

        parsed_file = {}
        params = {}
        comments = []
        other = []

        with open(path) as input_file:
            for line in input_file:
                line = line.strip()
                if line != "":
                    if line[0] == "#":
                        comments.append(line)
                    elif line.startswith(const_prefix):
                        line = line.split()
                        prefix = line[0]
                        var = line[2]
                        value = line[4]
                        params[var] = {"-value":value, "prefix":prefix}
                    else:
                        other.append(line)
        
        parsed_file["params"] = params
        parsed_file["comments"] = comments
        parsed_file["other"] = other
        return parsed_file
        
    def compare(self):
        """Compare the two supplied INI files and return a readable summary of how
        they differ in content (if at all).
        """
        files_identical = True
        file_params_identical = True
        
        # params that only exist in either file
        params_file1_only = {}
        params_file2_only = {}

        # present in both, but with different values
        param_value_differences = {}
        
        # Compare files' raw lines to see if content is identical
        with open(self.filepath1, "r") as file1, open(self.filepath2, "r") as file2:
            for line1, line2 in zip_longest(file1, file2):
                if line1 != line2:
                    files_identical = False
                    break

        # Check if content of dictionaries is the same even if order is not
        file1_params = self.file1_parsed["params"]
        file2_params = self.file2_parsed["params"]
        # Find and record all vars that are in file1_params but not file2_params
        for var, value in file1_params.items():
            if var not in file2_params:
                file_params_identical = False
                params_file1_only[var] = value

        # Find and record all vars that are in file2_params but not file1_params
        for var, value in file2_params.items():
            if var not in file1_params:
                file_params_identical = False
                params_file2_only[var] = value

        # Find and record all vars that are in both, but have different values
        for var, value in file1_params.items():
            if var in file2_params:
                if value != file2_params[var]:
                    file_params_identical = False
                    param_value_differences[var] = {self.filename1: value, self.filename2: file2_params[var]}

        # Find all unique other lines
        file1_other = self.file1_parsed["other"]
        file2_other = self.file2_parsed["other"]
        other_lines_present = len(file1_other) > 0 or len(file2_other) > 0
        
        # "other" lines unique to each file, or in both, respectively
        other_file1_only = []
        other_file2_only = []
        other_both = []
        all_other_lines_found = {self.filename1: other_file1_only,
                            self.filename2: other_file2_only,
                            "both": other_both}
        
        # Map all unique "other" lines to the files they came from
        # Kept here in case we want other lines as a map instead of a list
        for entry in file1_other:
            if entry in file2_other:
                other_both.append(entry)
            else:
                other_file1_only.append(entry)
        for entry in file2_other:
            if entry not in file1_other:
                other_file2_only.append(entry)
        
        # print out all info
        line = "\n******************************************"
        if files_identical:
            print(line)
            print("The provided files are completely identical.")
        elif file_params_identical:
            print(line)
            print("The parameters in the provided files are the same, but not necessarily in the same order.")
        else:
            print(line)
            print("The parameters in the provided files are not the same.")
            if len(param_value_differences) > 0:
                print(line)
                print("The following parameters were found in both files, but differed in value:")
                pprint(param_value_differences, indent=1)
                
            if len(params_file1_only) > 0:
                print(line)
                print("The following parameters were found only in {0}:".format(self.filename1))
                pprint(params_file1_only, indent=1)
                
            if len(params_file2_only) > 0:
                print(line)
                print("The following parameters were found only in {0}:".format(self.filename2))
                pprint(params_file2_only, indent=1)

        if other_lines_present:
            print(line)
            print("The following non-parameter, non-comment lines were found:")
            pprint(all_other_lines_found, indent=1)
        
    def dump(self, output_path=""):
        """Dump the contents of the dictionary as a JSON file.
        """
        if output_path == "":
            output_path = self.filename1
            output_path, _ = os.path.splitext(output_path)
            filename = os.path.basename(output_path) + ".json"
            output_path = os.path.join(os.path.dirname(output_path), filename)
        if not output_path.endswith(".json"):
            output_path = output_path + ".json"

        with open(output_path, "w") as output_file:
            json.dump(self.file1_parsed, output_file, indent=2)
        
        print("Output file created at {0}".format(os.path.abspath(output_path)))

def inicompare():
    parser = argparse.ArgumentParser(description="A tool to compare the contents of producer install.ini files.")
    parser.add_argument("file1", type=str,
                        help="The first INI file to compare.")
    parser.add_argument("file2", type=str,
                        help="The second INI file to compare.")
    args = parser.parse_args()

    if not os.path.exists(args.file1):
        return "ERROR: file '{0}' not found.".format(args.file1)
    if not os.path.exists(args.file2):
        return "ERROR: file '{0}' not found.".format(args.file2)

    comparer = IniCompare(args.file1, args.file2, dump_flag=False)

    comparer.compare()

def inidump():
    parser = argparse.ArgumentParser(description="A tool to dump the contents of producer install.ini files.")
    parser.add_argument("input", type=str,
                        help="The first INI file to compare.")
    parser.add_argument("output", type=str, nargs='?', default="",
                        help="The path at which to write out the parsed-to-JSON contents of file1 to. The .json extension will be added by default if the given name doesn't have it already.")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        return "ERROR: file '{0}' not found.".format(args.input)
    if not os.access(os.path.dirname(os.path.abspath(args.output)), os.W_OK):
        return "ERROR: path '{0}' not writeable. Ensure that the path exists, and that you have write permission.".format(os.path.abspath(os.path.dirname(args.output)))

    comparer = IniCompare(args.input, args.output, dump_flag=True)

    comparer.dump(args.output)
