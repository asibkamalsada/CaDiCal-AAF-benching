import os
import re

TIMEDOUT = "TIMEDOUT"

COMPLETE = "cmp"
PREFERRED = "prf"
STABLE = "stb"

SEMANTICS = (COMPLETE, PREFERRED, STABLE)

MUTOKSIA = "mu-toksia"
AAF_CADICAL = "cadical-aaf"

TIMEOUT = 600

ICCMA19 = "iccma19"
GEN = "gen"

# RUN = ICCMA19
RUN = GEN

RESULTS = f"results_{RUN}"

def main():
    path_to_aaf_cadical = r"C:\Users\asib1\Documents\Asib\uni\ba_baumann\benching\aaf-cadical"
    ca_results = os.path.join(path_to_aaf_cadical, RESULTS)

    path_to_mutoksia = r"C:\Users\asib1\Documents\Asib\uni\ba_baumann\benching\mutoksia"
    m_results = os.path.join(path_to_mutoksia, RESULTS)

    path_to_aafs = r"C:\Users\asib1\Documents\Asib\uni\ba_baumann\benching\aafs"

    for sem in SEMANTICS:
        with open(f"{sem}_{RUN}.csv", "w+") as f:
            f.write("file;argcount;prob;ca_sol_n;ca_time_ns;m_sol_n;m_time_ns\n")

    for file in set(os.listdir(os.fsencode(ca_results))).intersection(os.listdir(os.fsencode(m_results))):
        filename = os.fsdecode(file)
        ca_r = os.path.join(ca_results, filename)
        m_r = os.path.join(m_results, filename)
        if RUN == GEN:
            match = re.search(r"(([0-9]+)_(0\.[0-9]))\.(cmp|prf|stb)", filename)
        elif RUN == ICCMA19:
            match = re.search(r"(.+)\.(cmp|prf|stb)", filename)
        if match:
            if RUN == GEN:
                stub = match[1]
                argcount = match[2]
                prob = match[3]
                sem = match[4]
            elif RUN == ICCMA19:
                stub = match[1]
                argcount = ""
                prob = ""
                sem = match[2]
            
            ca_sol_n, ca_time_ns = parse_sol(ca_r)

            m_sol_n, m_time_ns = parse_sol(m_r)

            with open(f"{sem}_{RUN}.csv", "a") as f:
                f.write(f"{stub};{argcount};{prob};{ca_sol_n};{ca_time_ns};{m_sol_n};{m_time_ns}\n")


def parse_sol(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()
        sols = (1 for line in lines if str(line[0]) == "\t")
        # sols = (line for line in lines if str(line[0]) not in ("[", "]", "T", "\n") and str(line[0]) not in (str(n) for n in range(0, 10)))
        sol_n = sum(sols)
        time_ns = None
        for line in lines:
            m = re.match(rf"{TIMEDOUT}|[0-9]+", line)
            if m:
                if m[0] == TIMEDOUT:
                    time_ns = -TIMEOUT * 10**9
                else:
                    time_ns = int(m[0])
                break
        if not time_ns:
            time_ns = -1
        return sol_n, time_ns


if __name__ == '__main__':
    main()
