# %%
import sofar as sf
import os
import requests
from netCDF4 import Dataset
from datetime import date

# %% File and directory handling

# directory for storing SOFA files under test (relative to this file)
base_dir = "resources"

# file for saving issues with SOFA files (at the location of this file)
report_file = "report"

# create directory for saving test files
if not os.path.isdir(base_dir):
    os.mkdir(base_dir)
    print("Created directory 'resources' for storing SOFA files")

# URL from which the SOFA files are downloaded
base_url = "http://sofacoustics.org/data/"

# %% Data to be downloaded

# From each database mentioned on
# https://www.sofaconventions.org/mediawiki/index.php/Files
# a sample of SOFA files is downloaded. If a database contains files with
# different naming schemes, it is considered that the underlying data and
# script for writing these files might differ. Thus one file of each naming
# scheme is downloaded.
# Excpetion: All files from sofa_api_mo_test were taken

# files that are downloaded
data = {
    # ----- Example files -----
    "examples": [
        "FreeFieldDirectivityTF.sofa",
        "GeneralFIR-E.sofa",
        "GeneralFIR.sofa",
        "GeneralTF.sofa",
        "MultiSpeakerBRIR.sofa",
        "SimpleFreeFieldHRIR.sofa",
        "SimpleHeadphoneIR.sofa"],
    # ----- Test data from SOFA API/MO
    "sofa_api_mo_test": [
        "ARI_NH2_hrtf_M_dtf 256.sofa",
        "ARI_NH4_4_freqs.sofa",
        "ARI_NH4_hrtf_M_dtf 256.sofa",
        "BTdei-hp_H010-subj_S115-Set02-COMPENSATED.sofa",
        "CIPIC_subject_003_hrir_final.sofa",
        "FHK_HRIR_L2354.sofa",
        "LISTEN_1002_IRC_1002_C_HRIR.sofa",
        "MIT_KEMAR_large_pinna.sofa",
        "MIT_KEMAR_normal_pinna.sofa",
        "Oldenburg_OfficeII.sofa",
        "Pulse.sofa",
        "TU-Berlin_QU_KEMAR_anechoic_radius_0.5_1_2_3_m.sofa",
        "TU-Berlin_QU_KEMAR_anechoic_radius_0.5m.sofa",
        "TU-Berlin_QU_KEMAR_anechoic_radius_1m.sofa",
        "TU-Berlin_QU_KEMAR_anechoic_radius_2m.sofa",
        "TU-Berlin_QU_KEMAR_anechoic_radius_3m.sofa",
        "hpir_nh5.sofa"],
    # ----- HTTFs, PRTFs -----
    "database/ari": [
        "dtf_nh2.sofa",
        "dtf b_nh2.sofa",
        "dtf c_nh676.sofa",
        "hrtf_nh2.sofa",
        "hrtf b_nh2.sofa",
        "hrtf c_nh676.sofa"],
    "database/ari (altb)": [
        "dtf_nh4.sofa",
        "dtf b_nh4.sofa",
        "hrtf_nh4.sofa",
        "hrtf b_nh4.sofa"],
    "database/cipic": [
        "subject_003.sofa"],
    "database/riec": [
        "RIEC_hrir_subject_001.sofa"],
    "database/aachen": [
        "MRT01.sofa"],
    "database/aachen (high-resolution)": [
        "HRTF_5DegInterpolation.sofa",
        "HRTF_perFrequencyInterpolation.sofa",
        "HRTF_raw.sofa"],
    "database/hutubs": [
        "pp1_HRIRs_measured.sofa",
        "pp1_HRIRs_simulated.sofa"],
    "database/chedar": [
        "chedar_0001_UV02m.sofa",
        "chedar_0001_UV05m.sofa",
        "chedar_0001_UV1m.sofa",
        "chedar_0001_UV2m.sofa"],
    "database/3d3a": [
        "Subject1_BIRs.sofa",
        "Subject1_HRIRs.sofa",
        "Subject1_HRIRs_dfeq.sofa",
        "Subject1_HRIRs_lfc.sofa"],
    "database/crossmod (dtf)": [
        "IRC_1062_C_44100.sofa"],
    "database/crossmod (hrtf)": [
        "IRC_1062_R_44100.sofa"],
    "database/crossmod (dtf, sos)": [
        "IRC_1062_I_SOS12_48000.sofa"],
    "database/listen (dtf)": [
        "IRC_1002_C_44100.sofa"],
    "database/listen (hrtf)": [
        "IRC_1002_R_44100.sofa"],
    "database/listen (dtf, sos)": [
        "IRC_1002_I_SOS12_48000.sofa"],
    # downloaded manually from
    # https://www.york.ac.uk/sadie-project/database.html
    "sadie_II": [
        "D1_44K_16bit_0.3s_FIR_SOFA.sofa",
        "D1_44K_16bit_256tap_FIR_SOFA.sofa",
        "D1_48K_24bit_0.3s_FIR_SOFA.sofa",
        "D1_48K_24bit_256tap_FIR_SOFA.sofa",
        "D1_96K_24bit_0.3s_FIR_SOFA.sofa",
        "D1_96K_24bit_512tap_FIR_SOFA.sofa"],
    "database/mit": [
        "mit_kemar_large_pinna.sofa",
        "mit_kemar_normal_pinna.sofa"],
    # also contains BRIRs and DRIRs
    "database/thk": [
        "BRIR_CR1_KU_MICS_L.sofa",
        "BRIR_SBS_KU_MICS_PAC.sofa",
        "DRIR_CR1_VSA_50RS_L.sofa",
        "DRIR_SBS_VSA_50RS_PAC.sofa",
        "HMSII.sofa",
        "HRIR_CIRC360.sofa",
        "HRIR_FULL2DEG.sofa",
        "KU100.sofa"],
    "database/scut": [
        "SCUT_KEMAR_radius_0.2.sofa"],
    "database/tu-berlin": [
        "FABIAN_CTF_measured.sofa",
        "FABIAN_HRIR_measured_HATO_0.sofa",
        "FABIAN_HRIR_modeled_HATO_0.sofa",
        "qu_kemar_anechoic_0.5m.sofa"],
    "database/clubfritz": [
        "ClubFritz2.sofa"],
    "database/viking": [
        "subj_A.sofa"],
    "database/pku-ioa": [
        "dist_0.2m.sofa"],
    "database/ari (bte)": [
        "dtf_ci1.sofa",
        "dtf b_ci1.sofa",
        "hrtf_ci1.sofa",
        "hrtf b_ci1.sofa"],
    # ----- Source directivities -----
    "database/tu-berlin (directivity)": [
        "ITA_Dodecahedron.sofa",
        "Trumpet_modern_a4_fortissimo.sofa",
        "Trumpet_modern_et_ff_a4_rawData.sofa",
        "Trumpet_modern_et_ff_all_tensorData.sofa"],
    # ----- Room impulse responses -----
    "database/oldenburg": [
        "Kayser2009_Anechoic.sofa",
        "OfficeII.sofa"],
    "database/tuburo": [
        "BRIR_AddAbsorbers_ArrayCentre_Emitters1to64.sofa",
        "RIR_AddAbsorbers_ArrayCentre_Emitters1to64.sofa"],
    "database/sbsbrir": [
        "SBSBRIR_x-0pt5y-0pt5.sofa"],
    "database/room transition dataset": [
        ("Room Transition RIRs_Meeting Room to Hallway_Source in Hallway_"
         "No Line of Sight.sofa")],
    "database/6dof dataset": [
        "6DoF_SRIRs_eigenmike_SH_0percent_absorbers_enabled.sofa"],
    # ----- Headphone impulse responses -----
    "headphones/ari": [
        "hpir_nh2.sofa"],
    "headphones/btdei/H010": [
        "BTDEI-hp_H010-subj_S115-Set02_BEC-COMPENSATED.sofa",
        "BTDEI-hp_H010-subj_S115-Set02_BEC-RAW.sofa"],
    "headphones/tu-berlin": [
        "AKG K141 MKII.sofa"]
}

# %% Generate full URLs for downlading the data, file names for saving and a
#    few helping variables

file_urls = []
file_names = []

for database in data:
    for file in data[database]:
        file_urls.append(
            base_url + requests.utils.quote(database + "/" + file))
        file_names.append(database.replace("/", "-") + "-" + file)

n_files = len(file_names)
n_databases = len(data)

# %% Download files

for n, (file_url, file_name) in enumerate(zip(file_urls, file_names)):

    if os.path.isfile(os.path.join(base_dir, file_name)) \
            or file_name.startswith("sadie_II") \
            or file_name.startswith("headphones/tu-berlin"):
        continue

    print(f"Downloading {n+1}/{n_files}: {file_name}")

    # url = requests.utils.quote(base_url + file_url)
    response = requests.get(file_url)
    with open(os.path.join(base_dir, file_name), "wb") as fid:
        fid.write(response.content)

    del response

del n, file_name, file_url

# %% Read files and report issues

# for reporting issues during verification
report_incorrect = "The following files violate the SOFA standard AES69\n\n"
count_incorrect = 0

# for reporting correct files
report_correct = ("The following file are in accordance with the SOFA standard"
                  "AES69\n\n")
count_correct = 0

# for reporting unknown errors during loading
report_errors = "The following files could not be read as they were\n\n"
count_errors_caught = 0
count_errors_fatal = 0

conventions = {}

for n, file_name in enumerate(file_names):

    # get Convention before doing anything else
    with Dataset(os.path.join(base_dir, file_name), "r", format="NETCDF4") \
            as file:
        convention = getattr(file, "SOFAConventions")

    # load SOFA file
    current_file = f"{file_name} ({convention})\n"
    print(f"{n+1}/{n_files}: {current_file}")

    # try to read and verify with matching version
    try:
        # seperatley read and verify to separate corresponding issues
        sofa = sf.read_sofa(os.path.join(base_dir, file_name),
                            version="match", verify=False)
        issues = sofa.verify(
            version="match", issue_handling="return", mode="write")
    except ValueError as err:
        issues = err

    # check for errors
    if isinstance(issues, ValueError):
        # update error report
        report_errors += current_file + str(issues) + "\n\n"
        count_errors_caught += 1

        # try to read and verify with updating version to latest
        if "Try to access the data with version='latest'" in str(issues):
            try:
                sofa = sf.read_sofa(os.path.join(base_dir, file_name),
                                    verify=False)
                issues = sofa.verify(
                    version="latest", issue_handling="return", mode="write")
            except ValueError:
                if current_file + str(issues) not in report_errors:
                    report_errors += current_file + str(issues) + "\n\n"
                count_errors_caught -= 1
                count_errors_fatal += 1
        else:
            if current_file + str(issues) not in report_errors:
                report_errors += current_file + str(issues) + "\n\n"
            count_errors_caught -= 1
            count_errors_fatal += 1
            continue

    print("\n")

    # update remaining reports
    if issues is None:
        report_correct += current_file + "\n\n"
        count_correct += 1
    else:
        report_incorrect += current_file + issues[15:] + "\n\n"
        count_incorrect += 1

    # count conventions
    if sofa.GLOBAL_SOFAConventions not in conventions:
        conventions[sofa.GLOBAL_SOFAConventions] = 1
    else:
        conventions[sofa.GLOBAL_SOFAConventions] += 1

# %% summary
summary = (f"Tested {n + 1} files from {len(data)} databases on {date.today().strftime('%B %d, %Y')} "
           f"using sofar version {sf.__version__}\n\n"
           f"Correct files:           {count_correct}\n"
           f"Incorrect files:         {count_incorrect}\n"
           f"Reading errors (caught): {count_errors_caught}\n"
           f"Reading errors (fatal):  {count_errors_fatal}\n\n"
           f"The following {len(conventions)} conventions "
           "were contained in the sample:\n")

summary += "\n".join([f"{k}: {v}" for k, v in conventions.items()])

with open(report_file + "_correct.txt", "w") as fid:
    fid.write(report_correct)

with open(report_file + "_incorrect.txt", "w") as fid:
    fid.write(report_incorrect)

with open(report_file + "_errors.txt", "w") as fid:
    fid.write(report_errors)

with open(report_file + "_summary.txt", "w") as fid:
    fid.write(summary)
