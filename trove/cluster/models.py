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

"""Model classes that form the core of clusters functionality."""

from trove.common import exception
from trove.db import models
from trove.openstack.common.gettextutils import _
from trove.openstack.common import log as logging

LOG = logging.getLogger(__name__)


def persisted_models():
    return {'cluster': DBCluster, 'cluster_instance': DBClusterInstance}


class Cluster(object):
    def __init__(self, cluster=None, cluster_id=None, context=None):
        """
        Create a Cluster object

        :param cluster: Preinstantiated cluster object
        :param cluster_id: UUID of a cluster
        :param context:
        :return:
        """
        LOG.debug(_('Beginning Cluster __init__: '
                    '%(cluster)s, %(cluster_id)s, %s(context)s') % locals())
        if cluster and type(cluster) is Cluster:
            LOG.debug(_('Cluster passed into __init__ using that object: '
                        '%(cluster)s') % locals())
            self.cluster = cluster
        elif cluster_id and context:
            LOG.debug(_('Cluster id and context given, searching...'))
            self.cluster = DBClusterInstance.find_by(
                context, cluster_id=cluster_id)
            LOG.debug(_('Done searching...'))
        else:
            raise exception.ClusterModelError()

        LOG.debug(_('Finished __init__ for Cluster'))

    @property
    def id(self):
        return self.cluster.id

    @property
    def name(self):
        return self.cluster.name

    @property
    def type(self):
        return self.cluster.type

    @property
    def description(self):
        return self.cluster.description


class Clusters(object):
    def __init__(self, context):
        """
        Create a Clusters object which should only contain clusters for the
        given tenant context.

        :param context:
        :return:
        """
        LOG.debug(_('Beginning __init__ in Clusters'))
        self.clusters = DBCluster.find_all(
            tenant_id=context.tenant, deleted=False)
        self.clusters = [Cluster(c) for c in self.clusters]
        LOG.debug(_('Clusters contains %s items') % len(self.clusters))
        LOG.debug(_('Finished __init__ in Clusters'))

    def __iter__(self):
        for cluster in self.clusters:
            yield cluster

    def __getitem__(self, key):
        return self.clusters[key]

    def __contains__(self, item):
        return item in self.clusters


class ClusterInstance(object):
    def __init__(self, cluster_instance=None, cluster_instance_id=None,
                 context=None):
        """
        Create a ClusterInstance object

        :param cluster_instance: Preinstantiated ClusterInstance object
        :param cluster_instance_id: UUID
        :param context:
        :return:
        """
        LOG.debug(_('Beginning __init__ for ClusterInstance'))
        if cluster_instance and type(cluster_instance) is ClusterInstance:
            LOG.debug(_(
                'ClusterInstance passed in: %(cluster_instance)s') % locals())
            self.cluster_instance = cluster_instance
        elif cluster_instance_id and context:
            LOG.debug(_('ClusterInstance id passed in '
                        '"%(cluster_instance_id)s", searching...') % locals())
            self.cluster_instance = DBClusterInstance.find_by(
                tenant_id=context.tenant,
                clusterinstance_id=cluster_instance_id)
            LOG.debug(_('Done searching.'))
        else:
            raise exception.ClusterInstanceModelError()
        LOG.debug(_('Finished __init__ for ClusterInstance'))

    @property
    def id(self):
        return self.cluster_instance.id

    @property
    def cluster_id(self):
        return self.cluster_instance.cluster_id

    @property
    def instance_id(self):
        return self.cluster_instance.instance_id


class ClusterInstances(object):
    def __init__(self, context):
        LOG.debug(_('Beginning __init__ for ClusterInstances'))
        self.cluster_instances = DBClusterInstance.find_all(
            tenant_id=context.tenant, deleted=False)
        self.cluster_instances = [
            ClusterInstance(ci) for ci in self.cluster_instances
        ]
        LOG.debug(_('Finished __init__ for ClusterInstances'))

    def __iter__(self):
        for cluster_instance in self.cluster_instances:
            yield cluster_instance

    def __getitem__(self, key):
        return self.cluster_instances[key]

    def __contains__(self, item):
        return item in self.cluster_instances


class DBCluster(models.DatabaseModelBase):
    _data_fields = ['id', 'tenant_id', 'name', 'type', 'description',
                    'deleted', 'created', 'updated', 'deleted_at']
    preserve_on_delete = True
    _table_name = 'clusters'


class DBClusterInstance(models.DatabaseModelBase):
    _data_fields = ['id', 'cluster_id', 'instance_id']
    preserve_on_delete = True
    _table_name = 'cluster_instances'
