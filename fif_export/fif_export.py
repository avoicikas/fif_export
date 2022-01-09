"""Main module."""
import mne
import click
import pathlib
from numpy.core.records import fromarrays
from scipy.io import savemat
from typing import Union


def import_eeg(ifile: Union[pathlib.Path, str]):
    data = mne.io.read_raw_fif(ifile, preload=True)
    return data


def write_set(fname: str, raw: mne.io.BaseRaw):
    """Export raw to EEGLAB .set file."""
    data = raw.get_data()  # convert to microvolts
    fs = raw.info["sfreq"]
    times = raw.times
    ch_names = raw.info["ch_names"]
    chanlocs = fromarrays([ch_names], names=["labels"])
    events = fromarrays([raw.annotations.description,
                         raw.annotations.onset * fs + 1,
                         raw.annotations.duration * fs],
                        names=["type", "latency", "duration"])
    savemat(fname + '.set', dict(EEG=dict(data=data,
                                 setname=fname,
                                 nbchan=float(data.shape[0]),
                                 pnts=float(data.shape[1]),
                                 trials=1.,
                                 ref=[],
                                 srate=float(fs),
                                 xmin=float(times[0]),
                                 xmax=float(times[-1]),
                                 chanlocs=chanlocs,
                                 event=events,
                                 icawinv=[],
                                 icasphere=[],
                                 icaweights=[])),
            appendmat=False)


@ click.command()
@ click.option('--file', type=str, help='Name of the file to convert', default=None)
@ click.option('--path', type=str, help='Path of the folder with .fif files', default='./')
@ click.option('--type', type=str, help='Export to type', default='EEGlab')
def main(file: str = None, path: str = './', type: str = 'EEGlab'):
    if file:
        file = pathlib.Path(file)
        raw = import_eeg(file)
        write_set(file.stem, raw)
    else:
        for ifile in pathlib.Path(path).glob(r'*.fif'):
            raw = import_eeg(ifile)
            write_set(ifile.stem, raw)


if __name__ == "__main__":
    main()
