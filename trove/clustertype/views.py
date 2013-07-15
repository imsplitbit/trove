# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (c) 2013 Rackspace
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from trove.common.views import create_links


class ClusterTypeView(object):
    """
    Base view for ClusterType.
    """
    def __init__(self, clustertype, req=None):
        """
        Create a ClusterTypeView

        :param clustertype:
        :param req:
        :return:
        """
        self.clustertype = clustertype
        self.req = req

    def data(self):
        """
        Dictionary representation of clustertype data
        :rtype: dict
        """
        clustertype = {
            'id': self.clustertype.id,
            'links': self._build_links(),
            'name': self.clustertype.name,
            'type': self.clustertype.type,
            'max_instances': self.clustertype.max_instances,
            'min_instances': self.clustertype.min_instances,
        }

        return {"clustertype": clustertype}

    def _build_links(self):
        return create_links("clustertype", self.req, self.clustertype.id)


class ClusterTypesView(object):
    """
    ClusterTypes View
    """

    view = ClusterTypeView

    def __init__(self, clustertypes, req=None):
        """
        Create a ClusterTypes object

        :param clustertypes:
        :param req:
        :return:
        """
        self.clustertypes = clustertypes
        self.req = req

    def data(self):
        """
        List of ClusterType dictionary data

        :return:
        """
        data = [
            self.view(ctype, self.req).data()['clustertype'] for
            ctype in self.clustertypes
        ]

        return {"clustertypes": data}
