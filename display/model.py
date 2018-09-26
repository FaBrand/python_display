import enum
from display import db
from random import randint
from datetime import datetime, timedelta
import pytz

required_jobs = db.Table('required_jobs',
        db.Column('monitor_id', db.Integer, db.ForeignKey('monitor.id')),
        db.Column('jobs_id', db.Integer, db.ForeignKey('jobs.id'))
)


class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True, nullable=False)
    desciption = db.Column(db.Text, nullable=True)
    pretty_name = db.relationship("PrettyJobs", back_populates="jobs", uselist=False)
    builds = db.relationship("Builds", back_populates="jobs", uselist=False)

    def __repr__(self):
        return '<Jobs {}, {}>'.format(self.name, self.desciption)


class PrettyJobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pretty_name = db.Column(db.String(255), nullable=False)
    jobs = db.relationship("Jobs", back_populates="pretty_name")
    jobs_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), unique=True)

    def __repr__(self):
        return '<PrettyJobs {}>'.format(self.pretty_name)


class Monitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True)
    jobs = db.relationship('Jobs', secondary=required_jobs)


class Builds(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # state = db.Column('state', db.Enum(ResultStateEnum))
    jobs_id = db.Column(db.Integer, db.ForeignKey("jobs.id"))
    jobs = db.relationship("Jobs", back_populates="builds")

    changes_id = db.Column(db.Integer, db.ForeignKey("changes.id"))
    changes = db.relationship("Changes", back_populates="builds")


class Changes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    builds = db.relationship("Builds", back_populates="changes", uselist=False)


























































































class Result(object):
    def __init__(self, result):
        self.__result = result

    def __repr__(self):
        return '<Result : {}>'.format(self.__result)

    @property
    def result(self):
        return self.__result


class Change(object):
    def __init__(self, name, time):
        self.__name = name
        self.__time = time
        self.__results = list()

    def __repr__(self):
        return '<Change success:{} time:{} name:"{}" results:{}>'.format(self.is_success(), self.__time, self.__name, self.__results)

    def add_result(self, res):
        assert isinstance(res, Result)
        self.__results.append(res)

    def is_success(self):
        for r in self.__results:
            if not r.result:
                return False
        return True

    @property
    def name(self):
        return self.__name

    @property
    def time(self):
        return self.__time

    @property
    def results(self):
        return self.__results


class Status(object):
    def __init__(self):
        self.__changes = list()
        self.__successful = None
        self.__setup_changes()

    def __setup_changes(self):
        for _ in range(0,15):
            self.add_change(ChangeFactory.make_change())

    def add_change(self, change):
        self.__changes.append(change)
        self.__update_state()

    def __update_state(self):
        self.__changes.sort(reverse=True, key=lambda x: x.time)
        if self.__changes[0].is_success():
            self.__set_to_successful()
        else:
            self.__set_to_failing()

    def __set_to_failing(self):
        self.__successful = False

    def __set_to_successful(self):
        self.__successful = True

    @property
    def changes(self):
        return self.__changes

    @property
    def is_success(self):
        return self.__successful


class ChangeFactory(object):
    CHANGE_NAME_PREFIX = 'Change_no'
    changes_counter = 0

    @classmethod
    def make_change(cls):
        change = Change(cls.__make_class_name(), datetime.now(pytz.UTC))
        for i in range(1,5):
            change.add_result(cls.__make_results())
        return change

    @classmethod
    def make_success(cls):
        change = Change(cls.__make_class_name(), datetime.now(pytz.UTC))
        for i in range(1,5):
            change.add_result(cls.__make_success_result())
        return change

    @classmethod
    def make_failure(cls):
        change = Change(cls.__make_class_name(), datetime.now(pytz.UTC))
        for i in range(1,5):
            change.add_result(cls.__make_fail_result())
        return change


    @classmethod
    def __make_class_name(cls):
        change_name = '{}_{}'.format(cls.CHANGE_NAME_PREFIX, cls.changes_counter)
        cls.changes_counter += 1
        return change_name

    @classmethod
    def __make_results(cls):
        return Result(randint(0, 3) % 2 == 0)

    @classmethod
    def __make_success_result(cls):
        return Result(True)

    @classmethod
    def __make_fail_result(cls):
        return Result(False)


display = Status()
