"""Base test case class for coverage testing."""

import glob, imp, os, random, shlex, shutil, sys, tempfile, textwrap
import atexit

import coverage
from coverage.backward import sorted, StringIO      # pylint: disable=W0622
from coverage.backward import to_bytes
from coverage.control import _TEST_NAME_FILE
from tests.backtest import run_command
from tests.backunittest import TestCase

class Tee(object):
    """A file-like that writes to all the file-likes it has."""

    def __init__(self, *files):
        """Make a Tee that writes to all the files in `files.`"""
        self._files = files
        if hasattr(files[0], "encoding"):
            self.encoding = files[0].encoding

    def write(self, data):
        """Write `data` to all the files."""
        for f in self._files:
            f.write(data)

    if 0:
        # Use this if you need to use a debugger, though it makes some tests
        # fail, I'm not sure why...
        def __getattr__(self, name):
            return getattr(self._files[0], name)


# Status returns for the command line.
OK, ERR = 0, 1

class CoverageTest(TestCase):
    """A base class for Coverage test cases."""

    # Our own setting: most CoverageTests run in their own temp directory.
    run_in_temp_dir = True

    # Standard unittest setting: show me diffs even if they are very long.
    maxDiff = None

    def setUp(self):
        super(CoverageTest, self).setUp()

        if _TEST_NAME_FILE:
            f = open(_TEST_NAME_FILE, "w")
            f.write("%s_%s" % (self.__class__.__name__, self._testMethodName))
            f.close()

        # Tell newer unittest implementations to print long helpful messages.
        self.longMessage = True

        # tearDown will restore the original sys.path
        self.old_syspath = sys.path[:]

        if self.run_in_temp_dir:
            # Create a temporary directory.
            self.noise = str(random.random())[2:]
            self.temp_root = os.path.join(tempfile.gettempdir(), 'test_cover')
            self.temp_dir = os.path.join(self.temp_root, self.noise)
            os.makedirs(self.temp_dir)
            self.old_dir = os.getcwd()
            os.chdir(self.temp_dir)

            # Modules should be importable from this temp directory.  We don't
            # use '' because we make lots of different temp directories and
            # nose's caching importer can get confused.  The full path prevents
            # problems.
            sys.path.insert(0, os.getcwd())

            # Keep a counter to make every call to check_coverage unique.
            self.n = 0

        # Record environment variables that we changed with set_environ.
        self.environ_undos = {}

        # Capture stdout and stderr so we can examine them in tests.
        # nose keeps stdout from littering the screen, so we can safely Tee it,
        # but it doesn't capture stderr, so we don't want to Tee stderr to the
        # real stderr, since it will interfere with our nice field of dots.
        self.old_stdout = sys.stdout
        self.captured_stdout = StringIO()
        sys.stdout = Tee(sys.stdout, self.captured_stdout)
        self.old_stderr = sys.stderr
        self.captured_stderr = StringIO()
        sys.stderr = self.captured_stderr

        # Record sys.modules here so we can restore it in tearDown.
        self.old_modules = dict(sys.modules)

        class_behavior = self.class_behavior()
        class_behavior.tests += 1
        class_behavior.test_method_made_any_files = False
        class_behavior.temp_dir = self.run_in_temp_dir

    def tearDown(self):
        super(CoverageTest, self).tearDown()

        # Restore the original sys.path.
        sys.path = self.old_syspath

        if self.run_in_temp_dir:
            # Get rid of the temporary directory.
            os.chdir(self.old_dir)
            shutil.rmtree(self.temp_root)

        # Restore the environment.
        self.undo_environ()

        # Restore stdout and stderr
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr

        self.clean_modules()

        class_behavior = self.class_behavior()
        if class_behavior.test_method_made_any_files:
            class_behavior.tests_making_files += 1

    def clean_modules(self):
        """Remove any new modules imported during the test run.

        This lets us import the same source files for more than one test.

        """
        for m in [m for m in sys.modules if m not in self.old_modules]:
            del sys.modules[m]

    def set_environ(self, name, value):
        """Set an environment variable `name` to be `value`.

        The environment variable is set, and record is kept that it was set,
        so that `tearDown` can restore its original value.

        """
        if name not in self.environ_undos:
            self.environ_undos[name] = os.environ.get(name)
        os.environ[name] = value

    def original_environ(self, name, if_missing=None):
        """The environment variable `name` from when the test started."""
        if name in self.environ_undos:
            ret = self.environ_undos[name]
        else:
            ret = os.environ.get(name)
        if ret is None:
            ret = if_missing
        return ret

    def undo_environ(self):
        """Undo all the changes made by `set_environ`."""
        for name, value in self.environ_undos.items():
            if value is None:
                del os.environ[name]
            else:
                os.environ[name] = value

    def stdout(self):
        """Return the data written to stdout during the test."""
        return self.captured_stdout.getvalue()

    def stderr(self):
        """Return the data written to stderr during the test."""
        return self.captured_stderr.getvalue()

    def make_file(self, filename, text="", newline=None):
        """Create a temp file.

        `filename` is the path to the file, including directories if desired,
        and `text` is the content. If `newline` is provided, it is a string
        that will be used as the line endings in the created file.

        Returns the path to the file.

        """
        # Tests that call `make_file` should be run in a temp environment.
        assert self.run_in_temp_dir
        self.class_behavior().test_method_made_any_files = True

        text = textwrap.dedent(text)
        if newline:
            text = text.replace("\n", newline)

        # Make sure the directories are available.
        dirs, _ = os.path.split(filename)
        if dirs and not os.path.exists(dirs):
            os.makedirs(dirs)

        # Create the file.
        f = open(filename, 'wb')
        try:
            f.write(to_bytes(text))
        finally:
            f.close()

        return filename

    def clean_local_file_imports(self):
        """Clean up the results of calls to `import_local_file`.

        Use this if you need to `import_local_file` the same file twice in
        one test.

        """
        # So that we can re-import files, clean them out first.
        self.clean_modules()
        # Also have to clean out the .pyc file, since the timestamp
        # resolution is only one second, a changed file might not be
        # picked up.
        for pyc in glob.glob('*.pyc'):
            os.remove(pyc)
        if os.path.exists("__pycache__"):
            shutil.rmtree("__pycache__")

    def import_local_file(self, modname):
        """Import a local file as a module.

        Opens a file in the current directory named `modname`.py, imports it
        as `modname`, and returns the module object.

        """
        modfile = modname + '.py'
        f = open(modfile, 'r')

        for suff in imp.get_suffixes():
            if suff[0] == '.py':
                break
        try:
            # pylint: disable=W0631
            # (Using possibly undefined loop variable 'suff')
            mod = imp.load_module(modname, f, modfile, suff)
        finally:
            f.close()
        return mod

    def start_import_stop(self, cov, modname):
        """Start coverage, import a file, then stop coverage.

        `cov` is started and stopped, with an `import_local_file` of
        `modname` in the middle.

        The imported module is returned.

        """
        cov.start()
        try:                                    # pragma: nested
            # Import the python file, executing it.
            mod = self.import_local_file(modname)
        finally:                                # pragma: nested
            # Stop Coverage.
            cov.stop()
        return mod

    def get_module_name(self):
        """Return the module name to use for this test run."""
        # We append self.n because otherwise two calls in one test will use the
        # same filename and whether the test works or not depends on the
        # timestamps in the .pyc file, so it becomes random whether the second
        # call will use the compiled version of the first call's code or not!
        modname = 'coverage_test_' + self.noise + str(self.n)
        self.n += 1
        return modname

    # Map chars to numbers for arcz_to_arcs
    _arcz_map = {'.': -1}
    _arcz_map.update(dict([(c, ord(c)-ord('0')) for c in '123456789']))
    _arcz_map.update(dict(
        [(c, 10+ord(c)-ord('A')) for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
        ))

    def arcz_to_arcs(self, arcz):
        """Convert a compact textual representation of arcs to a list of pairs.

        The text has space-separated pairs of letters.  Period is -1, 1-9 are
        1-9, A-Z are 10 through 36.  The resulting list is sorted regardless of
        the order of the input pairs.

        ".1 12 2." --> [(-1,1), (1,2), (2,-1)]

        Minus signs can be included in the pairs:

        "-11, 12, 2-5" --> [(-1,1), (1,2), (2,-5)]

        """
        arcs = []
        for pair in arcz.split():
            asgn = bsgn = 1
            if len(pair) == 2:
                a,b = pair
            else:
                assert len(pair) == 3
                if pair[0] == '-':
                    _,a,b = pair
                    asgn = -1
                else:
                    assert pair[1] == '-'
                    a,_,b = pair
                    bsgn = -1
            arcs.append((asgn*self._arcz_map[a], bsgn*self._arcz_map[b]))
        return sorted(arcs)

    def assertEqualArcs(self, a1, a2, msg=None):
        """Assert that the arc lists `a1` and `a2` are equal."""
        # Make them into multi-line strings so we can see what's going wrong.
        s1 = "\n".join([repr(a) for a in a1]) + "\n"
        s2 = "\n".join([repr(a) for a in a2]) + "\n"
        self.assertMultiLineEqual(s1, s2, msg)

    def check_coverage(self, text, lines=None, missing="", report="",
            excludes=None, partials="",
            arcz=None, arcz_missing="", arcz_unpredicted=""):
        """Check the coverage measurement of `text`.

        The source `text` is run and measured.  `lines` are the line numbers
        that are executable, or a list of possible line numbers, any of which
        could match. `missing` are the lines not executed, `excludes` are
        regexes to match against for excluding lines, and `report` is the text
        of the measurement report.

        For arc measurement, `arcz` is a string that can be decoded into arcs
        in the code (see `arcz_to_arcs` for the encoding scheme),
        `arcz_missing` are the arcs that are not executed, and
        `arcs_unpredicted` are the arcs executed in the code, but not deducible
        from the code.

        """
        # We write the code into a file so that we can import it.
        # Coverage wants to deal with things as modules with file names.
        modname = self.get_module_name()

        self.make_file(modname+".py", text)

        arcs = arcs_missing = arcs_unpredicted = None
        if arcz is not None:
            arcs = self.arcz_to_arcs(arcz)
            arcs_missing = self.arcz_to_arcs(arcz_missing or "")
            arcs_unpredicted = self.arcz_to_arcs(arcz_unpredicted or "")

        # Start up Coverage.
        cov = coverage.coverage(branch=(arcs_missing is not None))
        cov.erase()
        for exc in excludes or []:
            cov.exclude(exc)
        for par in partials or []:
            cov.exclude(par, which='partial')

        mod = self.start_import_stop(cov, modname)

        # Clean up our side effects
        del sys.modules[modname]

        # Get the analysis results, and check that they are right.
        analysis = cov._analyze(mod)
        statements = sorted(analysis.statements)
        if lines is not None:
            if type(lines[0]) == type(1):
                # lines is just a list of numbers, it must match the statements
                # found in the code.
                self.assertEqual(statements, lines)
            else:
                # lines is a list of possible line number lists, one of them
                # must match.
                for line_list in lines:
                    if statements == line_list:
                        break
                else:
                    self.fail("None of the lines choices matched %r" %
                                                                statements
                        )

            if type(missing) == type(""):
                self.assertEqual(analysis.missing_formatted(), missing)
            else:
                for missing_list in missing:
                    if analysis.missing_formatted() == missing_list:
                        break
                else:
                    self.fail("None of the missing choices matched %r" %
                                            analysis.missing_formatted()
                        )

        if arcs is not None:
            self.assertEqualArcs(
                analysis.arc_possibilities(), arcs, "Possible arcs differ"
                )

            if arcs_missing is not None:
                self.assertEqualArcs(
                    analysis.arcs_missing(), arcs_missing,
                    "Missing arcs differ"
                    )

            if arcs_unpredicted is not None:
                self.assertEqualArcs(
                    analysis.arcs_unpredicted(), arcs_unpredicted,
                    "Unpredicted arcs differ"
                    )

        if report:
            frep = StringIO()
            cov.report(mod, file=frep)
            rep = " ".join(frep.getvalue().split("\n")[2].split()[1:])
            self.assertEqual(report, rep)

    def nice_file(self, *fparts):
        """Canonicalize the filename composed of the parts in `fparts`."""
        fname = os.path.join(*fparts)
        return os.path.normcase(os.path.abspath(os.path.realpath(fname)))

    def assert_same_files(self, flist1, flist2):
        """Assert that `flist1` and `flist2` are the same set of file names."""
        flist1_nice = [self.nice_file(f) for f in flist1]
        flist2_nice = [self.nice_file(f) for f in flist2]
        self.assertSameElements(flist1_nice, flist2_nice)

    def assert_exists(self, fname):
        """Assert that `fname` is a file that exists."""
        msg = "File %r should exist" % fname
        self.assert_(os.path.exists(fname), msg)

    def assert_doesnt_exist(self, fname):
        """Assert that `fname` is a file that doesn't exist."""
        msg = "File %r shouldn't exist" % fname
        self.assert_(not os.path.exists(fname), msg)

    def command_line(self, args, ret=OK, _covpkg=None):
        """Run `args` through the command line.

        Use this when you want to run the full coverage machinery, but in the
        current process.  Exceptions may be thrown from deep in the code.
        Asserts that `ret` is returned by `CoverageScript.command_line`.

        Compare with `run_command`.

        Returns None.

        """
        script = coverage.CoverageScript(_covpkg=_covpkg)
        ret_actual = script.command_line(shlex.split(args))
        self.assertEqual(ret_actual, ret)

    def run_command(self, cmd):
        """Run the command-line `cmd` in a subprocess, and print its output.

        Use this when you need to test the process behavior of coverage.

        Compare with `command_line`.

        Returns the process' stdout text.

        """
        # Running Python subprocesses can be tricky.  Use the real name of our
        # own executable.  So "python foo.py" might get executed as
        # "python3.3 foo.py".  This is important because Python 3.x doesn't
        # install as "python", so you might get a Python 2 executable instead
        # if you don't use the executable's basename.
        if cmd.startswith("python "):
            cmd = os.path.basename(sys.executable) + cmd[6:]

        _, output = self.run_command_status(cmd)
        return output

    def run_command_status(self, cmd, status=0):
        """Run the command-line `cmd` in a subprocess, and print its output.

        Use this when you need to test the process behavior of coverage.

        Compare with `command_line`.

        Returns a pair: the process' exit status and stdout text.

        The `status` argument is returned as the status on older Pythons where
        we can't get the actual exit status of the process.

        """
        # Add our test modules directory to PYTHONPATH.  I'm sure there's too
        # much path munging here, but...
        here = os.path.dirname(self.nice_file(coverage.__file__, ".."))
        testmods = self.nice_file(here, 'tests/modules')
        zipfile = self.nice_file(here, 'tests/zipmods.zip')
        pypath = os.getenv('PYTHONPATH', '')
        if pypath:
            pypath += os.pathsep
        pypath += testmods + os.pathsep + zipfile
        self.set_environ('PYTHONPATH', pypath)

        status, output = run_command(cmd, status=status)
        print(output)
        return status, output

    # We run some tests in temporary directories, because they may need to make
    # files for the tests. But this is expensive, so we can change per-class
    # whether a temp dir is used or not.  It's easy to forget to set that
    # option properly, so we track information about what the tests did, and
    # then report at the end of the process on test classes that were set
    # wrong.

    class ClassBehavior(object):
        """A value object to store per-class in CoverageTest."""
        def __init__(self):
            self.tests = 0
            self.temp_dir = True
            self.tests_making_files = 0
            self.test_method_made_any_files = False

    # Map from class to info about how it ran.
    class_behaviors = {}

    def report_on_class_behavior(cls):
        """Called at process exit to report on class behavior."""
        for test_class, behavior in cls.class_behaviors.items():
            if behavior.temp_dir and behavior.tests_making_files == 0:
                bad = "Inefficient"
            elif not behavior.temp_dir and behavior.tests_making_files > 0:
                bad = "Unsafe"
            else:
                bad = ""

            if bad:
                if behavior.temp_dir:
                    where = "in a temp directory"
                else:
                    where = "without a temp directory"
                print(
                    "%s: %s ran %d tests, %d made files %s" % (
                        bad,
                        test_class.__name__,
                        behavior.tests,
                        behavior.tests_making_files,
                        where,
                    )
                )
    report_on_class_behavior = classmethod(report_on_class_behavior)

    def class_behavior(self):
        """Get the ClassBehavior instance for this test."""
        cls = self.__class__
        if cls not in self.class_behaviors:
            self.class_behaviors[cls] = self.ClassBehavior()
        return self.class_behaviors[cls]


# When the process ends, find out about bad classes.
atexit.register(CoverageTest.report_on_class_behavior)
