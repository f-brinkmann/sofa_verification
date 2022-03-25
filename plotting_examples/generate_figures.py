# tested with pyfar 0.4.0
import pyfar as pf
import matplotlib as mpl
import matplotlib.pyplot as plt

# use the pyfar plot style
pf.plot.use()

# Requires the SOFA file from dx.doi.org/10.14279/depositonce-5718.5
hrirs, sources, _ = pf.io.read_sofa('FABIAN_HRIR_measured_HATO_0.sofa')

# find source at 90 degrees azimuth and 0 degree elevation
index, *_ = sources.find_nearest_k(
    90, 0, 1.5, k=1, domain='sph', convention='top_elev', unit='deg')

# find and plot sources on the horizontal plane
_, mask = sources.find_slice('elevation', unit='deg', value=0, show=True)
plt.tight_layout()

# time and frequency plot of single HRTF
plt.figure(figsize=(5, 4))
ax = pf.plot.time_freq(hrirs[index, 0], c='k', label="left ear")
pf.plot.time_freq(hrirs[index, 1], c=[.5, .5, .5], label="right ear")

ax[1].set_xlim(200, 20e3)
ax[1].set_ylim(-25, 25)
ax[1].legend()

# plot horizontal plane HRTFs
plt.subplots(2, 1, figsize=(5, 5), sharex=True)
angles = sources.get_sph('top_elev', 'deg')[mask, 0]

ax, qm, cb = pf.plot.time_freq_2d(hrirs[mask, 0], indices=angles,
                                  cmap=mpl.cm.get_cmap(name='gist_gray'))

ax[0].set_xlabel("")
ax[0].set_ylim(0, 3)
qm[0].set_clim(-1.5, 1.5)
ax[1].set_xlabel(
    "Azimuth angle in degrees")
ax[1].set_ylim(200, 20e3)
qm[1].set_clim(-25, 25)
plt.tight_layout
