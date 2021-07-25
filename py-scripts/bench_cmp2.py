import os
import re
import subprocess
import sys

import time


RUN = "iccma19"
# RUN = "gen"

RESULTS = f"results_{RUN}"

TIMEDOUT = "TIMEDOUT"

def bench_one(cmd, out, timeout, overwrite=False):
    if not overwrite and os.path.isfile(out):
        print(f"file {out} already exists and cannot be overwritten")
        return
    with open(out, "w+") as f:
        try:
            start = time.time_ns()
            subprocess.run(cmd, stdout=f, timeout=timeout)
            end = time.time_ns()
        except subprocess.TimeoutExpired as t:
            f.write('\n')
            f.write(TIMEDOUT)
        else:
            f.write('\n')
            f.write(str(end - start))
        f.write('\n')


def bench_aaf_cadical(path_to_aaf_cadical, filename, stub, timeout, overwrite):
    bench_one(cmd=(os.path.join(path_to_aaf_cadical, "bin", f"aaf-cmp2.exe"), filename),
              out=os.path.join(path_to_aaf_cadical, RESULTS, f"{stub}.cmp2"),
              timeout=timeout,
              overwrite=overwrite)


def main():

    overwrite = (len(sys.argv) == 2 and sys.argv[1] == "-o")

    path_to_aaf_cadical = r"C:\Users\asib1\Documents\Asib\uni\ba_baumann\benching\aaf-cadical"

    path_to_generated = r"C:\Users\asib1\Documents\Asib\uni\ba_baumann\benching\aafs"

    path_to_iccma19 = r"C:\Users\asib1\Documents\Asib\uni\ba_baumann\iccma19\instances"

    timeout = 120

    if RUN == "gen":
        p = path_to_generated
    elif RUN == "iccma19":
        p = path_to_iccma19
    
    bench(overwrite, path_to_aaf_cadical, p, timeout)


def bench(overwrite, path_to_aaf_cadical, path_to_aafs, timeout):
    for file in os.listdir(os.fsencode(path_to_aafs)):
        filename = os.fsdecode(file)
        filepath = os.path.join(path_to_aafs, filename)
        match = re.search(r"(.+)\.apx", filename)
        if match and filepath.endswith(".apx"):
            stub = match[1]
            bench_aaf_cadical(path_to_aaf_cadical, filepath, stub, timeout, overwrite)


if __name__ == '__main__':
    main()
