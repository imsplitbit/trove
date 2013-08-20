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
from sqlalchemy import ForeignKey

from sqlalchemy.schema import Column
from sqlalchemy.schema import MetaData

from trove.db.sqlalchemy.migrate_repo.schema import create_tables
from trove.db.sqlalchemy.migrate_repo.schema import DateTime
from trove.db.sqlalchemy.migrate_repo.schema import drop_tables
from trove.db.sqlalchemy.migrate_repo.schema import String
from trove.db.sqlalchemy.migrate_repo.schema import Table
from trove.db.sqlalchemy.migrate_repo.schema import Boolean

meta = MetaData()

clusters = Table(
    'clusters', meta,
    Column('id', String(36), primary_key=True, nullable=False),
    Column('tenant_id', String(36), nullable=False),
    Column('name', String(256), nullable=False),
    Column('type', String(36), nullable=False),
    Column('description', String(256), nullable=False),
    Column('deleted', Boolean(), default=0),
    Column('created', DateTime()),
    Column('updated', DateTime()),
    Column('deleted_at', DateTime()))

cluster_instances = Table(
    'cluster_instances', meta,
    Column('id', String(36), primary_key=True, nullable=False),
    Column(
        'cluster_id', String(36), nullable=False),
    # TODO(imsplitbit): figure out how to make a foreignkey for instances.id
    Column(
        'instance_id', String(36), nullable=False),
    Column('tenant_id', String(36), nullable=False),
    Column('deleted', Boolean(), default=0),
    Column('created', DateTime()),
    Column('updated', DateTime()),
    Column('deleted_at', DateTime())
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    create_tables([clusters, cluster_instances])


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    drop_tables([clusters, cluster_instances])
