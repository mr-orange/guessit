#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GuessIt - A library for guessing information from filenames
# Copyright (c) 2013 Nicolas Wack <wackou@gmail.com>
#
# GuessIt is free software; you can redistribute it and/or modify it under
# the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# GuessIt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.
#
# You should have received a copy of the Lesser GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import absolute_import, division, print_function, unicode_literals

from guessit.quality import QualitiesContainer, best_quality, best_quality_properties
from guessit.test.guessittest import *


class TestQuality(TestGuessit):
    def test_container(self):
        container = QualitiesContainer()

        container.register_quality('color', 'red', 10)
        container.register_quality('color', 'orange', 20)
        container.register_quality('color', 'green', 30)

        container.register_quality('context', 'sun', 100)
        container.register_quality('context', 'sea', 200)
        container.register_quality('context', 'sex', 300)

        g1 = Guess()
        g1['color'] = 'red'

        g2 = Guess()
        g2['color'] = 'green'

        g3 = Guess()
        g3['color'] = 'orange'

        q3 = container.rate_quality(g3)
        self.assertEqual(q3, 20, "ORANGE should be rated 20. Don't ask why!")

        q1 = container.rate_quality(g1)
        q2 = container.rate_quality(g2)

        self.assertTrue(q2 > q1, "GREEN should be greater than RED. Don't ask why!")

        g1['context'] = 'sex'
        g2['context'] = 'sun'

        q1 = container.rate_quality(g1)
        q2 = container.rate_quality(g2)

        self.assertTrue(q1 > q2, "SEX should be greater than SUN. Don't ask why!")

        self.assertEquals(container.best_quality(g1, g2), g1, "RED&SEX should be better than GREEN&SUN. Don't ask why!")

        self.assertEquals(container.best_quality_properties(['color'], g1, g2), g2, "GREEN should be better than RED. Don't ask why!")

        self.assertEquals(container.best_quality_properties(['context'], g1, g2), g1, "SEX should be better than SUN. Don't ask why!")

        q1 = container.rate_quality(g1, 'color')
        q2 = container.rate_quality(g2, 'color')

        self.assertTrue(q2 > q1, "GREEN should be greater than RED. Don't ask why!")

        container.unregister_quality('context', 'sex')
        container.unregister_quality('context', 'sun')

        q1 = container.rate_quality(g1)
        q2 = container.rate_quality(g2)

        self.assertTrue(q2 > q1, "GREEN&SUN should be greater than RED&SEX. Don't ask why!")

        g3['context'] = 'sea'
        container.unregister_quality('context', 'sea')

        q3 = container.rate_quality(g3, 'context')
        self.assertEquals(q3, 0, "Context should be unregistered.")

        container.unregister_quality('color')
        q3 = container.rate_quality(g3, 'color')

        self.assertEquals(q3, 0, "Color should be unregistered.")

        container.clear_qualities()

        q1 = container.rate_quality(g1)
        q2 = container.rate_quality(g2)

        self.assertTrue(q1 == q2 == 0, "Empty quality container should rate each guess to 0")

    def test_quality_transformers(self):
        guess_720p = guessit.guess_file_info("2012.2009.720p.BluRay.x264.DTS WiKi.mkv", 'autodetect')
        guess_1080p = guessit.guess_file_info("2012.2009.1080p.BluRay.x264.MP3 WiKi.mkv", 'autodetect')

        self.assertTrue('audioCodec' in guess_720p, "audioCodec should be present")
        self.assertTrue('audioCodec' in guess_1080p, "audioCodec should be present")
        self.assertTrue('screenSize' in guess_720p, "screenSize should be present")
        self.assertTrue('screenSize' in guess_1080p, "screenSize should be present")

        best_quality_guess = best_quality(guess_720p, guess_1080p)

        self.assertTrue(guess_1080p == best_quality_guess, "1080p+MP3 is not the best global quality")

        best_quality_guess = best_quality_properties(['screenSize'], guess_720p, guess_1080p)

        self.assertTrue(guess_1080p == best_quality_guess, "1080p is not the best screenSize")

        best_quality_guess = best_quality_properties(['audioCodec'], guess_720p, guess_1080p)

        self.assertTrue(guess_720p == best_quality_guess, "DTS is not the best audioCodec")

suite = allTests(TestQuality)

if __name__ == '__main__':
    TextTestRunner(verbosity=2).run(suite)
