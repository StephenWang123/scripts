#!/bin/env python

import sys
import os
import fcntl


def lockfile_ext():
    return '.lock'


def generate_filename():
    import tempfile
    from datetime import datetime
    # Date Format: Year, Month, Day, Hour, Minute, Second, Microsecond
    filename = 'lockfile_%s' % datetime.now().strftime('%Y%m%d%H%M%S%f')
    filepath = os.path.join(tempfile.mkdtemp(), filename)
    return filename


class LockFile(object):
    """
    A basic lockfile implementation.

    When provided a file or folder path, this class will create a filesystem-
    level semaphore with the same name, suffixed with a '.lock' extension. If
    an exception is thrown at any point while the lockfile exists on the local
    filesystem, the lockfile will still be deleted.


    :note: Forced termination of the Python interpreter will override the
    default behavior of this class (such as when using 'kill -9 python') and
    the lockfile will remain on the filesystem.
    """
    def __init__(self, filepath=None):
        """
        Initialize a LockFile object.

        :param filepath:
        The absolute path to a file/folder which will be associated with a
        lockfile of the same name, in the same parent directory, upon calling
        'instance.lock_file()'.
        """
        self._filepath = filepath
        self._handle = None

    #----------------------------------
    def __enter__(self):
        """
        Lock a file using Python's built-in context-management. This ensures
        that a lockfile will be deleted when it's opened through a 'with'
        statement.

        This method should not be called manually.
        """
        self.lock_file(self._filepath)
        return self

    #----------------------------------
    def __exit__(self, exception_type, exception_value, traceback):
        """
        Unlock a file using Python's built-in context-management. This ensures
        that a lockfile will be deleted when it's opened through a 'with'
        statement.

        This method should not be called manually.
        """
        self.release_file()
        return False

    #----------------------------------
    def __del__(self):
        """
        The destructor merely provides a false sense of security. This method
        attempts to release a lockfile when context-management is not used and
        is not guaranteed to run when an exception is thrown.

        This method should not be called manually.
        """
        self.release_file()

    #----------------------------------
    def is_locked(self):
        """
        Determine if a LockFile instance is currently referencing a file on the
        local filesystem.

        :return:
        TRUE if a file is currently being locked, FALSE if not.
        """
        # Must use the '...is not...' keys so the file handle isn't unsafely
        # returned.
        return self._handle is not None

    #----------------------------------
    @property
    def filepath(self):
        """
        Retrieve the name of the current lockfile's path.

        :return:
        A string containing the absolute path to a lockfile on the filesystem
        or 'None' if a file is not currently being locked.
        """
        if self._filepath:
            return '%s%s' % (self._filepath, lockfile_ext())
        else:
            return None

    #----------------------------------
    def _sanitize_user_path(self, filepath):
        """
        Helper function to get the absolute path to a file provided from user
        input.

        :return:
        A string containing the absolute path to a '.lock' file. If the user
        path is an absolute path, the path of a '.lock' file in the same
        directory will be returned. If a relative path is passed in, an attempt
        is made to convert it into an absolute path, suffixed with the '.lock'
        extension. If you want to be a jerk and pass nothing in, you get a
        generated file name and have to use the 'instance.filepath' property
        to determine where the lockfile was created.
        """
        if not filepath:
            return self._filepath if self._filepath else generate_filename()

        filepath = os.path.abspath(filepath)

        assert os.path.exists(filepath), 'Unable to create a lock for a ' \
            'non-existent file: %r' % filepath

        # no trailing slashes should be allowed
        return filepath.rstrip('/\\')

    #----------------------------------
    def lock_file(self, filepath=None):
        """
        Attempt to create a lock-file without using context-management.

        :param filepath:
        The absolute path to a file/folder which will be associated with a
        lockfile of the same name, in the same parent directory.
        """
        self.release_file()

        filepath = self._sanitize_user_path(filepath)

        # Add a *.lock extension to the file or path that is being locked.
        lockpath = '%s%s' % (filepath, lockfile_ext())

        # Don't allow a file to be locked twice
        assert not os.path.exists(lockpath), 'Unable to ' \
            'create a lockfile at %s. File already exists.' % lockpath

        # UNIX file semaphores only work when a file is opened for writing.
        filehandle = open(lockpath, 'a')

        assert filehandle, 'Unable to open the file %r for locking.' % lockpath

        # Python's version of "touch".
        os.utime(lockpath, None)

        fcntl.flock(filehandle, fcntl.LOCK_EX | fcntl.LOCK_NB)

        # Keep the file path, not the lock path
        self._filepath = filepath
        self._handle = filehandle

    #----------------------------------
    def release_file(self):
        """
        Unlock/delete a lockfile when not using context-management. This will
        release all file-handles, remove any paths that a LockFile instance
        used internally, and delete the lockfile if one existed.
        """
        if not self._handle:
            return

        fcntl.flock(self._handle, fcntl.LOCK_UN)

        # Remove the path with the *.lock extension
        if os.path.exists(self.filepath):
            os.remove(self.filepath)

        self._filepath = None
        self._handle = None

