#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_epithet
----------------------------------

Tests for `epithet` module.
"""


import sys
import unittest
from contextlib import contextmanager
from click.testing import CliRunner

from epithet import epithet


class TestEpithet(unittest.TestCase):

    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(epithet.cli)
        assert result.exit_code == 0
        assert 'Usage: cli' in result.output
        help_result = runner.invoke(epithet.cli, ['--help'])
        assert help_result.exit_code == 0
        assert 'Show this message and exit.' in help_result.output
