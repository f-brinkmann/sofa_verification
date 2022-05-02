# %% SOFAsonix 1.07 can not read GeneralTF 2.0 - thus no evaluation was done
from SOFASonix import SOFAFile
import os
from glob import glob

base_dir = r"\sofar_verification_rules\data"

data_dirs = ['deprecations',
             'general_dependencies',
             'restricted_dimensions',
             'restricted_values',
             'specific_dependencies']

for data_dir in data_dirs:
    for file in glob(os.path.join(base_dir, data_dir, "*.sofa")):
        sofa = SOFAFile.load(file)
