#Copyright [2013] Rackspace
#All rights reserved

#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""Model classes that form the core of clusters functionality."""

from trove.common import exception
from trove.db import models
from trove.openstack.common.gettextutils import _
from trove.openstack.common import log as logging

LOG = logging.getLogger(__name__)


def persisted_models():
    return {'cluster': DBCluster, 'cluster_instance': DBClusterInstance}


class Cluster(object):
    def __init__(self, cluster=None, instances=None,
                 cluster_id=None, context=None):
        """
        Create a Cluster object

        :param cluster: Preinstantiated cluster object
        :param instances: Preinstantiated cluster_instances object
        :param cluster_id: UUID of a cluster
        :param context:
        :return:
        """
        LOG.debug(_('Beginning Cluster __init__: '
                    '%(cluster)s, %(cluster_id)s, %(context)s') %
                  {'cluster': cluster, 'cluster_id': cluster_id,
                   'context': context})
        if cluster:
            LOG.debug(_('Cluster passed into __init__ using that object: %s')
                      % (cluster,))
            self.cluster = cluster

            if instances:
                LOG.debug(_('ClusterInstances passed into __init__, using '
                            'that object: %s') % (instances,))
            self.instances = instances
        elif cluster_id and context:
            LOG.debug(_('Cluster id and context given, searching...'))
            self.cluster = DBCluster.find_by(context, id=cluster_id)
            self.instances = ClusterInstances(context, cluster_id)
            LOG.debug(_('Done searching...'))
        else:
            raise exception.ClusterModelError()

        LOG.debug(_('Finished __init__ for Cluster'))

    @property
    def id(self):
        return self.cluster.id

    @property
    def tenant_id(self):
        return self.cluster.tenant_id

    @property
    def name(self):
        return self.cluster.name

    @property
    def type(self):
        return self.cluster.type

    @property
    def description(self):
        return self.cluster.description

    def delete(self):
        LOG.info(_('Deleting cluster: %s') % self.id)
        self.cluster.delete()
        LOG.info(_('Deleted cluster: %s') % self.id)

    @classmethod
    def create(cls, **values):
        """
        Factory method for creating cluster instances.

        :param cls:
        :param kwargs:
        :return:
        """
        LOG.info(_('Creating cluster'))
        cluster = DBCluster.create(**values)
        LOG.info(_('Created cluster: %s') % cluster.id)
        return Cluster(cluster=cluster)


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
        self.clusters = [
            Cluster(
                cluster=c, instances=ClusterInstances(
                    context, cluster_id=c.id)) for c in self.clusters
        ]
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
        if cluster_instance:
            LOG.debug(_(
                'ClusterInstance passed in: %(cluster_instance)s') % locals())
            self.cluster_instance = cluster_instance
        elif cluster_instance_id and context:
            LOG.debug(_('ClusterInstance id passed in '
                        '"%(cluster_instance_id)s", searching...') % locals())
            self.cluster_instance = DBClusterInstance.find_by(
                tenant_id=context.tenant,
                id=cluster_instance_id)
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

    @property
    def tenant_id(self):
        return self.cluster_instance.tenant_id

    def delete(self):
        msg_vars = {
            'instance_id': self.instance_id,
            'cluster_id': self.cluster_id
        }
        LOG.info(
            _('Deleting instance %(instance_id)s '
              'from DB for cluster %(cluster_id)s') % msg_vars)
        cluster_instance = DBClusterInstance.find_by(
            cluster_id=self.cluster_id, instance_id=self.instance_id)
        cluster_instance.delete()
        LOG.info(
            _('Deleted instance %(instance_id)s '
              'from DB for cluster %(cluster_id)s') % msg_vars)

    @classmethod
    def create(cls, **values):
        """
        Factory method for creating ClusterInstance objects

        :param cls:
        :param values:
        :return:
        """
        LOG.info(_('Creating ClusterInstance'))
        cluster_instance = DBClusterInstance.create(**values)
        LOG.info(_('Created ClusterInstance: %s') % cluster_instance.id)
        return ClusterInstance(cluster_instance=cluster_instance)


class ClusterInstances(object):
    def __init__(self, context, cluster_id):
        self.context = context
        self.cluster_id = cluster_id
        LOG.debug(_('Beginning __init__ for ClusterInstances'))
        self.cluster_instances = DBClusterInstance.find_all(
            cluster_id=cluster_id, deleted=False)
        self.cluster_instances = [
            ClusterInstance(ci) for ci in self.cluster_instances
        ]
        LOG.info(_('ClusterInstances: %s') % self.cluster_instances)
        LOG.debug(_('Finished __init__ for ClusterInstances'))

    def __iter__(self):
        for cluster_instance in self.cluster_instances:
            yield cluster_instance

    def __getitem__(self, key):
        return self.cluster_instances[key]

    def __contains__(self, item):
        return item in self.cluster_instances

    def delete(self):
        LOG.info(
            _('Deleting cluster instances from DB for cluster: %s') %
            self.cluster_id)

        cluster_instances = DBClusterInstance.find_all(
            deleted=False, tenant_id=self.context.tenant,
            cluster_id=self.cluster_id)
        for cluster_instance in cluster_instances:
            cluster_instance.delete()

        LOG.info(
            _('Deleted cluster instances from DB for cluster: %s') %
            self.cluster_id)


class DBCluster(models.DatabaseModelBase):
    _data_fields = ['id', 'tenant_id', 'name', 'type', 'description',
                    'deleted', 'created', 'updated', 'deleted_at']
    preserve_on_delete = False
    _table_name = 'clusters'


class DBClusterInstance(models.DatabaseModelBase):
    _data_fields = ['id', 'cluster_id', 'instance_id', 'tenant_id', 'deleted',
                    'created', 'updated', 'deleted_at']
    preserve_on_delete = False
    _table_name = 'cluster_instances'
