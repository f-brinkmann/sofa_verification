# %%
import sofar as sf
import numpy as np

# list of all version specific conventions
conventions = sf.sofar._get_conventions('name_version')

# find all unite entries and note in which conventions they are contained
entries = {}

# log occurrences of data types
tf = []
fir = []
sos = []

for convention, version in conventions:

    sofa = sf.Sofa(convention, version=version)
    keys = [k for k in sofa.__dict__.keys() if not k.startswith('_')]

    for key in keys:
        if key not in entries:
            entries[key] = {
                "in": [convention + " " + version],
                "out": []}
        else:
            entries[key]["in"].append(convention + " " + version)

    if sofa.GLOBAL_DataType.startswith("TF"):
        tf.append(f"{convention} {version} ({sofa.GLOBAL_DataType})")
    elif sofa.GLOBAL_DataType.startswith("FIR"):
        fir.append(f"{convention} {version} ({sofa.GLOBAL_DataType})")
    elif sofa.GLOBAL_DataType.startswith("SOS"):
        sos.append(f"{convention} {version} ({sofa.GLOBAL_DataType})")
    else:
        ValueError("nope")

# note in which conventions they are not contained
for entry in entries:
    for convention, version in conventions:
        if convention + " " + version not in entries[entry]["in"]:
            entries[entry]["out"].append(convention + " " + version)


# write occurrences to txt file
report = "Occurrences of DataTypes across conventions\n\n"
report += f"Transfer Function ({len(tf)})\n"
report += "\n".join(tf) + "\n\n"
report += f"Impulse Response ({len(fir)})\n"
report += "\n".join(fir) + "\n\n"
report += f"SOS ({len(sos)})\n"
report += "\n".join(sos) + "\n"

with open("report_DataTypes.txt", "w") as fid:
    fid.write(report)

del keys, key, convention, version, entry, tf, fir, sos, fid, report

# %% print entries and the conventions that they are not contained in, starting
#    with the entry that has the least conventions in which it is not contained

# sort
outs = [len(item["out"]) for _, item in entries.items()]
sort_outs = np.argsort(outs)

# write to string
report = "The following data is not contained in the following conventions\n\n"
report_long = report
keys = list(entries)

for nn in sort_outs:
    if outs[nn] == 0:
        continue

    name = f"{keys[nn]}  ({len(entries[keys[nn]]['out'])})\n"
    report += name
    report_long += name
    report_long += \
        "\n".join([f"    {out}" for out in entries[keys[nn]]["out"]])
    report_long += "\n\n"

with open("report_outs.txt", "w") as fid:
    fid.write(report)

with open("report_outs_long.txt", "w") as fid:
    fid.write(report_long)

del outs, sort_outs, keys, nn, name, fid, report, report_long

# %% print entries and the conventions that they are contained in, starting
#    with the entry that has the least conventions in which it is contained

# sort
ins = [len(item["in"]) for _, item in entries.items()]
sort_ins = np.argsort(ins)

# write to string
report = "The following data is contained in the following conventions\n\n"
report_long = report
keys = list(entries)

for nn in sort_ins:
    if ins[nn] == 0:
        continue

    name = f"{keys[nn]}  ({len(entries[keys[nn]]['in'])})\n"
    report += name
    report_long += name
    report_long += \
        "\n".join([f"    {out}" for out in entries[keys[nn]]["in"]])
    report_long += "\n\n"

with open("report_ins.txt", "w") as fid:
    fid.write(report)

with open("report_ins_long.txt", "w") as fid:
    fid.write(report_long)

del ins, sort_ins, keys, nn, name, fid, report, report_long
