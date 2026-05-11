"""
Template based file parser

data can be passed in as Pydantic model and stored in file.
later re-loaded and converted into a pydantic model
"""

from io import StringIO
from os.path import exists, isfile
from queue import PriorityQueue, SimpleQueue, Queue
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from pydantic import BaseModel

from core.exceptions import InvalidActionException, TemplateFileError


class Parser:
    def __init__(
        self,
        /,
        queue_class: PriorityQueue | SimpleQueue | Queue = PriorityQueue,
        queue_size: int = 0,
        threadpool: ThreadPoolExecutor = None,
        template_file: str | Path | StringIO = None,
        model: BaseModel = None,
    ):
        """
        parser class to parse multiple files as batches asynchronously

        params
        :queue_class:
        the queue class

        :queue_size:
        max size of the queue

        :
        """
        self._queue_size = queue_size
        self._threadpool = threadpool
        self._queue = queue_class
        self._active_count = 0
        self._template_file = template_file
        self.model = model

    def __new__(
        cls,
        /,
        queue_class: PriorityQueue | SimpleQueue | Queue = PriorityQueue,
        threadpool: ThreadPoolExecutor = None,
        queue_size: int = 0,
        template_file: str | Path = None,
        template: StringIO = None,
        model: BaseModel = None,
    ):
        if not isinstance(queue_class, (PriorityQueue, SimpleQueue, Queue, None)):
            raise TypeError("Incompatible type for queue")

        elif queue_class is None:
            raise TypeError("No Queue constructor provided")

        # verify queue size stays within limit
        if queue_size <= 10 or queue_size > 500:
            raise ResourceWarning(
                "size should be between 10 and 500, for optimal performance"
            )

        if not isinstance(template_file, (str, Path)):
            if not exists(template_file):
                raise TemplateFileError("Template file not found")

            if not isfile(template_file):
                raise TemplateFileError("template file type: not a file")

    # handle queue size
    @property
    def queue_size(self):
        return self._queue_size

    @queue_size.getter
    def queue_size(self):
        return self._queue_size

    @queue_size.setter
    def queue_size(self, value):
        return self._queue_size

    # handle threadpool
    @property
    def threadpool(self):
        return self._threadpool

    @threadpool.setter
    def threadpool(self, value):
        raise InvalidActionException("cannot change threadpool")

    @threadpool.getter
    def threadpool(self):
        return self._threadpool

    @threadpool.deleter
    def threadpool(self):
        raise InvalidActionException("Cannot delete threadpool")

    # handle queue
    @property
    def q(self):
        """the queue property"""
        return self._queue

    @q.setter
    def q(self, value):
        raise InvalidActionException("Cannot assign queue")

    @q.deleter
    def q(self):
        raise InvalidActionException("Cannot delete queue")

    @q.getter
    def q(self):
        return self._queue

    # handle active count
    @property
    def active_count(self):
        return self._active_count
