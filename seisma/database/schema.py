# -*- coding: utf-8 -*-

from datetime import date
from datetime import datetime

from sqlalchemy import Index
from sqlalchemy import UniqueConstraint

from .alchemy import alchemy
from .alchemy import ModelMixin
from ..json import ObjectConverter
from .descriptors import MetadataProperty


CASE_BAD_STATUSES = ('failed', 'error')
CASE_SUCCESS_STATUSES = ('passed', 'skipped')
CASE_STATUSES_CHOICE = ('passed', 'skipped', 'failed', 'error')


class Job(alchemy.Model, ModelMixin):

    __tablename__ = 'job'

    id = alchemy.Column(alchemy.Integer, autoincrement=True, primary_key=True)
    created = alchemy.Column(alchemy.Date(), nullable=False, default=date.today)
    name = alchemy.Column(alchemy.String(255), nullable=False, unique=True)
    title = alchemy.Column(alchemy.String(255), nullable=False)
    description = alchemy.Column(alchemy.Text(), nullable=False, default='')
    is_active = alchemy.Column(alchemy.Boolean, nullable=False, default=True)

    to_dict = ObjectConverter(
        ObjectConverter.FromAttribute('name'),
        ObjectConverter.FromAttribute('title'),
        ObjectConverter.FromAttribute('created'),
        ObjectConverter.FromAttribute('description'),
        ObjectConverter.FromAttribute('total_cases', is_optional=True),
        ObjectConverter.FromAttribute('total_builds', is_optional=True),
    )

    @property
    def total_builds(self):
        return Build.query.filter(Build.job_id == self.id).count()

    @property
    def total_cases(self):
        return Case.query.filter(Case.job_id == self.id).count()

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name, is_active=True).first()


class Case(alchemy.Model, ModelMixin):

    __tablename__ = 'case'

    __table_args__ = (
        UniqueConstraint(
            'name',
            'job_id',
            name='case_name',
        ),
    )

    id = alchemy.Column(alchemy.Integer, autoincrement=True, primary_key=True)
    job_id = alchemy.Column(alchemy.Integer, alchemy.ForeignKey('job.id'), nullable=False)
    created = alchemy.Column(alchemy.Date(), nullable=False, default=date.today)
    name = alchemy.Column(alchemy.String(255), nullable=False)
    description = alchemy.Column(alchemy.Text(), nullable=False, default='')

    to_dict = ObjectConverter(
        ObjectConverter.FromAttribute('name'),
        ObjectConverter.FromAttribute('created'),
        ObjectConverter.FromAttribute('description'),
        ObjectConverter.FromAttribute('job', is_optional=True),
    )

    @property
    def job(self):
        return Job.query.filter_by(id=self.job_id).first()


class BuildMetadata(alchemy.Model, ModelMixin):

    __tablename__ = 'build_metadata'

    id = alchemy.Column(alchemy.Integer, autoincrement=True, primary_key=True)
    build_id = alchemy.Column(alchemy.Integer, alchemy.ForeignKey('build.id'), nullable=False)
    key = alchemy.Column(alchemy.String(255), nullable=False)
    value = alchemy.Column(alchemy.Text(), nullable=False)


class Build(alchemy.Model, ModelMixin):

    __tablename__ = 'build'

    __table_args__ = (
        UniqueConstraint(
            'name',
            'job_id',
            name='build_name',
        ),
        Index('by_date_and_running_flag', 'date', 'is_running'),
    )

    id = alchemy.Column(alchemy.Integer, autoincrement=True, primary_key=True)
    job_id = alchemy.Column(alchemy.Integer, alchemy.ForeignKey('job.id'), nullable=False)
    name = alchemy.Column(alchemy.String(255), nullable=False)
    title = alchemy.Column(alchemy.String(255), nullable=False)
    date = alchemy.Column(alchemy.DateTime(), nullable=False, default=datetime.now)
    tests_count = alchemy.Column(alchemy.Integer, nullable=False, default=0)
    success_count = alchemy.Column(alchemy.Integer, nullable=False, default=0)
    fail_count = alchemy.Column(alchemy.Integer, nullable=False, default=0)
    error_count = alchemy.Column(alchemy.Integer, nullable=False, default=0)
    runtime = alchemy.Column(alchemy.Float(), nullable=False)
    was_success = alchemy.Column(alchemy.Boolean(), nullable=False)
    is_running = alchemy.Column(alchemy.Boolean(), nullable=False, default=True)

    md = MetadataProperty(BuildMetadata, fk='build_id')

    to_dict = ObjectConverter(
        ObjectConverter.FromAttribute('name'),
        ObjectConverter.FromAttribute('date'),
        ObjectConverter.FromAttribute('title'),
        ObjectConverter.FromAttribute('runtime'),
        ObjectConverter.FromAttribute('fail_count'),
        ObjectConverter.FromAttribute('is_running'),
        ObjectConverter.FromAttribute('tests_count'),
        ObjectConverter.FromAttribute('error_count'),
        ObjectConverter.FromAttribute('was_success'),
        ObjectConverter.FromAttribute('success_count'),
        ObjectConverter.FromAttribute('job', is_optional=True),
        ObjectConverter.FromAttribute('md', alias='metadata', is_optional=True),
    )

    @property
    def job(self):
        return Job.query.filter_by(id=self.job_id).first()


class CaseResultMetadata(alchemy.Model, ModelMixin):

    __tablename__ = 'case_result_metadata'

    id = alchemy.Column(alchemy.Integer, autoincrement=True, primary_key=True)
    case_result_id = alchemy.Column(alchemy.Integer, alchemy.ForeignKey('case_result.id'), nullable=False)
    key = alchemy.Column(alchemy.String(255), nullable=False)
    value = alchemy.Column(alchemy.Text(), nullable=False)


class CaseResult(alchemy.Model, ModelMixin):

    __tablename__ = 'case_result'

    __table_args__ = (
        Index('by_date_and_status', 'date', 'status'),
    )

    id = alchemy.Column(alchemy.Integer, autoincrement=True, primary_key=True)
    case_id = alchemy.Column(alchemy.Integer, alchemy.ForeignKey('case.id'), nullable=False)
    build_id = alchemy.Column(alchemy.Integer, alchemy.ForeignKey('build.id'), nullable=False)
    date = alchemy.Column(alchemy.DateTime(), nullable=False, default=datetime.now)
    reason = alchemy.Column(alchemy.Text(), nullable=False, default='')
    runtime = alchemy.Column(alchemy.Float(), nullable=False)
    status = alchemy.Column(alchemy.Enum(*CASE_STATUSES_CHOICE), nullable=False)
    dialect = alchemy.Column(alchemy.String(50), nullable=False, default='')

    md = MetadataProperty(CaseResultMetadata, fk='case_result_id')

    to_dict = ObjectConverter(
        ObjectConverter.FromAttribute('id'),
        ObjectConverter.FromAttribute('date'),
        ObjectConverter.FromAttribute('reason'),
        ObjectConverter.FromAttribute('status'),
        ObjectConverter.FromAttribute('runtime'),
        ObjectConverter.FromAttribute('dialect'),
        ObjectConverter.FromAttribute('case', is_optional=True),
        ObjectConverter.FromAttribute('build', is_optional=True),
        ObjectConverter.FromAttribute('md', alias='metadata', is_optional=True),
    )

    @property
    def case(self):
        return Case.query.filter_by(id=self.case_id).first()

    @property
    def build(self):
        return Build.query.filter_by(id=self.build_id).first()
