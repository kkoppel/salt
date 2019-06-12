# -*- coding: utf-8 -*-
'''
Integration tests for the beacon states
'''
from __future__ import absolute_import, print_function, unicode_literals

# Import Salt Testing Libs
from tests.support.case import ModuleCase
from tests.support.mixins import SaltReturnAssertsMixin
from tests.support.helpers import flaky
from salt.ext.six.moves import range

import logging
log = logging.getLogger(__name__)


class BeaconStateTestCase(ModuleCase, SaltReturnAssertsMixin):
    '''
    Test beacon states
    '''
    def setUp(self):
        '''
        '''
        self.run_function('beacons.reset', f_timeout=300)

    def tearDown(self):
        self.run_function('beacons.reset', f_timeout=30)

    @flaky
    def test_present_absent(self):
        kwargs = {'/': '38%', 'interval': 5}
        # TODO: Figure out why this will sometimes return 'Beacon "diskusage"
        # is not available.' The loop works around that issue for now
        for _ in range(10):
            ret = self.run_state(
                'beacon.present',
                name='diskusage',
                f_timeout=300,
                **kwargs
            )
            log.error("RET %s", ret)
            if ret['beacon_|-diskusage_|-diskusage_|-present']['result'] is True:
                break
        self.assertSaltTrueReturn(ret)

        ret = self.run_function('beacons.list',
                                return_yaml=False,
                                f_timeout=300)
        self.assertTrue('diskusage' in ret)
        self.assertTrue({'interval': 5} in ret['diskusage'])
        self.assertTrue({'/': '38%'} in ret['diskusage'])

        ret = self.run_state(
            'beacon.absent',
            name='diskusage',
            f_timeout=300
        )
        self.assertSaltTrueReturn(ret)

        ret = self.run_function('beacons.list',
                                return_yaml=False,
                                f_timeout=300)
        self.assertEqual(ret, {'beacons': {}})
