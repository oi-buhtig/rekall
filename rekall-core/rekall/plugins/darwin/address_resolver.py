# Rekall Memory Forensics
# Copyright 2014 Google Inc. All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#

"""The module implements an OSX specific address resolution plugin."""

__author__ = "Michael Cohen <scudette@gmail.com>"
import re

from rekall.plugins.common import address_resolver
from rekall.plugins.darwin import common


class KModModule(address_resolver.Module):
    """A darwin kernel module."""

    def __init__(self, kmod, **kwargs):
        self.kmod = kmod
        start = kmod.address.v()
        super(KModModule, self).__init__(
            name=unicode(kmod.name),
            start=start,
            end=start + kmod.size.v(),
            **kwargs)

        # We currently only support the kernel's profile. In future we should
        # write a Mach-O parser to extract symbols from binaries.
        if self.name == "__kernel__":
            self.profile = self.session.profile


class DarwinAddressResolver(address_resolver.AddressResolverMixin,
                            common.DarwinPlugin):
    """A Darwin specific address resolver plugin."""

    def _EnsureInitialized(self):
        if self._initialized:
            return

        # Add kernel modules.
        for kmod in self.session.plugins.lsmod().get_module_list():
            self.AddModule(KModModule(kmod, session=self.session))

        self._initialized = True
