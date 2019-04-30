{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Simple interactive widget demo"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "from ipywidgets import interactive\n",
    "import ipywidgets as widgets\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "from astropy.io import fits\n",
    "from wotan import flatten\n",
    "from transitleastsquares import resample"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Load the data and bin down (too make this demo fast)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Loading TESS data from archive.stsci.edu...\n"
     ]
    }
   ],
   "source": [
    "def load_file(filename):\n",
    "    \"\"\"Loads a TESS *spoc* FITS file and returns TIME, PDCSAP_FLUX\"\"\"\n",
    "    hdu = fits.open(filename)\n",
    "    time = hdu[1].data['TIME']\n",
    "    flux = hdu[1].data['PDCSAP_FLUX']\n",
    "    flux[flux == 0] = np.nan\n",
    "    return time, flux\n",
    "\n",
    "print('Loading TESS data from archive.stsci.edu...')\n",
    "path = 'https://archive.stsci.edu/hlsps/tess-data-alerts/'\n",
    "filename = \"hlsp_tess-data-alerts_tess_phot_00062483237-s01_tess_v1_lc.fits\"\n",
    "path = 'P:/P/Dok/tess_alarm/'\n",
    "#filename = \"hlsp_tess-data-alerts_tess_phot_00062483237-s01_tess_v1_lc.fits\"\n",
    "filename = 'hlsp_tess-data-alerts_tess_phot_00077031414-s02_tess_v1_lc.fits'\n",
    "#filename = 'tess2018206045859-s0001-0000000201248411-111-s_llc.fits'\n",
    "time, flux = load_file(path + filename)\n",
    "time, flux = resample(time, flux, factor=20)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Detrending function"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "def func(method, window_length, break_tolerance, edge_cutoff='0.1', cval=5):\n",
    "    f, ax = plt.subplots(2, sharex=True, figsize=(12, 12))\n",
    "    if method == 'trim_mean' or method == 'winsorize':\n",
    "        cval /= 10  # must be a fraction >0, <0.5\n",
    "        if cval >=0.5:\n",
    "            cval = 0.49\n",
    "    flatten_lc, trend_lc = flatten(\n",
    "        time,\n",
    "        flux,\n",
    "        method=method,\n",
    "        window_length=window_length,\n",
    "        edge_cutoff=edge_cutoff,\n",
    "        break_tolerance=break_tolerance,\n",
    "        return_trend=True,\n",
    "        cval=cval\n",
    "        )\n",
    "    ax[0].plot(time, trend_lc, color='black', linewidth=3)\n",
    "    ax[0].scatter(time, flux, edgecolors='k', c='yellow', s=30)\n",
    "    ax[0].set_xlim(min(time), max(time))\n",
    "    ax[0].set_ylabel('Raw flux')\n",
    "    ax[1].scatter(time, flatten_lc, edgecolors='k', c='black', s=30)\n",
    "    ax[1].set_ylim(0.995, 1.005)\n",
    "    ax[1].set_ylabel('Detrended flux')\n",
    "    plt.xlabel('Time (days)')\n",
    "    f.subplots_adjust(hspace=0)\n",
    "    plt.show();\n",
    "    return time"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Call the 'interactive' widget with the detrending function, which also plots the data real-time\n",
    "Play with the *'method'* and parameters to see how they impact the detrending"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "96621b3b6e714fdabf5b65a7b9b8a5ac",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "VBox(children=(HBox(children=(interactive(children=(Dropdown(description='method', options=('biweight', 'hodge…"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "y1=interactive(\n",
    "    func,\n",
    "    method=[\"biweight\", \"hodges\", \"welsch\", \"median\", \"andrewsinewave\", \"mean\", \"trim_mean\", \"winsorize\"],\n",
    "    window_length=(0.1, 2, 0.1),\n",
    "    break_tolerance=(0, 1, 0.1),\n",
    "    edge_cutoff=(0, 1, 0.1),\n",
    "    cval=(1, 9, 1)\n",
    "    )\n",
    "y2=interactive(\n",
    "    func,\n",
    "    method=[\"hspline\", \"pspline\", \"rspline\"],\n",
    "    window_length=(0.1, 2, 0.1),\n",
    "    break_tolerance=(0, 1, 0.1),\n",
    "    edge_cutoff=(0, 1, 0.1),\n",
    "    cval=(1, 9, 1)\n",
    "    )\n",
    "widgets.VBox([widgets.HBox([y1, y2])])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
