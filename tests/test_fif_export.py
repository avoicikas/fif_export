#!/usr/bin/env python

"""Tests for `test` package."""

import pytest
from fif_export.fif_export import import_eeg
from fif_export.fif_export import write_set


def test_import_eeg():
    ifile = './tests/test_data-raw.fif'
    raw = import_eeg(ifile)
    assert raw.get_data().shape == (7, 85752)
