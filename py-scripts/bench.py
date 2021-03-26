import os
import re
import subprocess
import sys

import time


# RUN = "iccma19"
RUN = "gen"

RESULTS = f"results_{RUN}"

TIMEDOUT = "TIMEDOUT"

COMPLETE = "cmp"
PREFERRED = "prf"
STABLE = "stb"

SEMANTICS = (COMPLETE, PREFERRED, STABLE)

s_to_ac = {
    COMPLETE: "cmp",
    PREFERRED: "prf",
    STABLE: "stb"
}

s_to_m = {
    COMPLETE: "EE-CO",
    PREFERRED: "EE-PR",
    STABLE: "EE-ST"
}


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


def bench_aaf_cadical(path_to_aaf_cadical, filename, stub, semantic, timeout, overwrite, results):
    bench_one(cmd=(os.path.join(path_to_aaf_cadical, "bin", f"aaf-{s_to_ac[semantic]}.exe"), filename),
              out=os.path.join(path_to_aaf_cadical, results, f"{stub}.{semantic}"),
              timeout=timeout,
              overwrite=overwrite)


def bench_mutoksia(path_to_mutoksia, filename, stub, semantic, timeout, overwrite, results):
    bench_one(cmd=(os.path.join(path_to_mutoksia, "bin", "mu-toksia.exe"), "-p", s_to_m[semantic], "-f", filename, "-fo", "apx"),
              out=os.path.join(path_to_mutoksia, results, f"{stub}.{semantic}"),
              timeout=timeout,
              overwrite=overwrite)


def main():

    overwrite = (len(sys.argv) == 2 and sys.argv[1] == "-o")

    # path_to_aaf_cadical = sys.argv[1]
    # path_to_mutoksia = sys.argv[2]
    # path_to_generated = sys.argv[3]
    # timeout = sys.argv[4]

    path_to_aaf_cadical = r"C:\Users\asib1\Documents\Asib\uni\ba_baumann\benching\aaf-cadical"

    path_to_mutoksia = r"C:\Users\asib1\Documents\Asib\uni\ba_baumann\benching\mutoksia"

    path_to_generated = r"C:\Users\asib1\Documents\Asib\uni\ba_baumann\benching\aafs"

    path_to_iccma19 = r"C:\Users\asib1\Documents\Asib\uni\ba_baumann\iccma19\instances"

    timeout = 600

    # bench(overwrite, path_to_aaf_cadical, path_to_generated, path_to_mutoksia, timeout, "results_test")

    if RUN == "gen":
        r = "results_gen"
        p = path_to_generated
    elif RUN == "iccma19":
        r = "results_iccma19"
        p = path_to_iccma19
    
    bench(overwrite, path_to_aaf_cadical, p, path_to_mutoksia, timeout, r)


def bench(overwrite, path_to_aaf_cadical, path_to_aafs, path_to_mutoksia, timeout, results):
    for file in os.listdir(os.fsencode(path_to_aafs)):
        filename = os.fsdecode(file)
        filepath = os.path.join(path_to_aafs, filename)
        match = re.search(r"(.+)\.apx", filename)
        if match and filepath.endswith(".apx"):
            stub = match[1]
            for semantic in SEMANTICS:
                bench_aaf_cadical(path_to_aaf_cadical, filepath, stub, semantic, timeout, overwrite, results)
                bench_mutoksia(path_to_mutoksia, filepath, stub, semantic, timeout, overwrite, results)


if __name__ == '__main__':
    main()
