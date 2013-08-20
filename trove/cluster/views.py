#Copyright [2013] Rackspace

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

from trove.common.views import create_links


class ClusterView(object):
    """
    Base view for Cluster
    """
    def __init__(self, cluster, req=None):
        """
        Create a ClusterView

        :param cluster:
        :param req:
        :return:
        """
        self.cluster = cluster
        self.req = req

    def data(self):
        """
        Dictionary representation of clustertype data

        :rtype: dict
        """
        cluster = {
            'id': self.cluster.id,
            'links': self._build_links(),
            'name': self.cluster.name,
            'type': self.cluster.type,
            'instances': self.cluster.instances
        }

        return {'cluster': cluster}

    def _build_links(self):
        return create_links('cluster', self.req, self.cluster.id)


class ClustersView(object):
    """
    Clusters View
    """

    view = ClusterView

    def __init__(self, clusters, req=None):
        """
        Create a ClustersView object

        :param clusters:
        :param req:
        :return:
        """
        self.clusters = clusters
        self.req = req

    def data(self):
        """
        List of Cluster dictionary data

        :return:
        """
        data = [
            self.view(cluster, self.req).data()['cluster'] for
            cluster in self.clusters
        ]
        return {'clusters': data}


class ClusterInstanceView(object):
    """
    ClusterInstances View
    """

    def __init__(self, cluster_instance, req=None):
        """
        Create a ClusterInstanceView object

        :param cluster_instance:
        :param req:
        :return:
        """
        self.cluster_instance = cluster_instance
        self.req = req

    def data(self):
        """
        ClusterInstance data

        :return:
        """
        cluster_instance = {
            "id": self._build_link(self.cluster_instance.instance_id)
        }
        return {'instance': cluster_instance}

    def _build_link(self, uuid):
        return create_links('instance', self.req, uuid)


class ClusterInstancesView(object):
    """
    ClusterInstances View
    """
    view = ClusterInstanceView

    def __init__(self, cluster_instances, req=None):
        """
        Create a ClusterInstancesView object

        :param cluster_instances:
        :param req:
        :return:
        """
        self.cluster_instances = cluster_instances
        self.req = req

    def data(self):
        """
        List of cluster_instance data

        :return:
        """
        data = [
            self.view(cluster_instance, self.req).data()['instance']
            for cluster_instance in self.cluster_instances
        ]
        return {'instances': data}
