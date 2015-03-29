"""Tests for Coverage's api."""

import fnmatch, os, re, sys, textwrap

import coverage
from coverage.backward import StringIO

from tests.coveragetest import CoverageTest


class SingletonApiTest(CoverageTest):
    """Tests of the old-fashioned singleton API."""

    def setUp(self):
        super(SingletonApiTest, self).setUp()
        # These tests use the singleton module interface.  Prevent it from
        # writing .coverage files at exit.
        coverage.use_cache(0)

    def do_report_work(self, modname):
        """Create a module named `modname`, then measure it."""
        coverage.erase()

        self.make_file(modname+".py", """\
            a = 1
            b = 2
            if b == 3:
                c = 4
                d = 5
                e = 6
            f = 7
            """)

        # Import the python file, executing it.
        self.start_import_stop(coverage, modname)

    def test_simple(self):
        coverage.erase()

        self.make_file("mycode.py", """\
            a = 1
            b = 2
            if b == 3:
                c = 4
            d = 5
            """)

        # Import the python file, executing it.
        self.start_import_stop(coverage, "mycode")

        _, statements, missing, missingtext = coverage.analysis("mycode.py")
        self.assertEqual(statements, [1,2,3,4,5])
        self.assertEqual(missing, [4])
        self.assertEqual(missingtext, "4")

    def test_report(self):
        self.do_report_work("mycode2")
        coverage.report(["mycode2.py"])
        self.assertEqual(self.stdout(), textwrap.dedent("""\
            Name      Stmts   Miss  Cover   Missing
            ---------------------------------------
            mycode2       7      3    57%   4-6
            """))

    def test_report_file(self):
        # The file= argument of coverage.report makes the report go there.
        self.do_report_work("mycode3")
        fout = StringIO()
        coverage.report(["mycode3.py"], file=fout)
        self.assertEqual(self.stdout(), "")
        self.assertEqual(fout.getvalue(), textwrap.dedent("""\
            Name      Stmts   Miss  Cover   Missing
            ---------------------------------------
            mycode3       7      3    57%   4-6
            """))

    def test_report_default(self):
        # Calling report() with no morfs will report on whatever was executed.
        self.do_report_work("mycode4")
        coverage.report()
        rpt = re.sub(r"\s+", " ", self.stdout())
        self.assertIn("mycode4 7 3 57% 4-6", rpt)


class ApiTest(CoverageTest):
    """Api-oriented tests for Coverage."""

    def clean_files(self, files, pats):
        """Remove names matching `pats` from `files`, a list of filenames."""
        good = []
        for f in files:
            for pat in pats:
                if fnmatch.fnmatch(f, pat):
                    break
            else:
                good.append(f)
        return good

    def assertFiles(self, files):
        """Assert that the files here are `files`, ignoring the usual junk."""
        here = os.listdir(".")
        here = self.clean_files(here, ["*.pyc", "__pycache__"])
        self.assertSameElements(here, files)

    def test_unexecuted_file(self):
        cov = coverage.coverage()

        self.make_file("mycode.py", """\
            a = 1
            b = 2
            if b == 3:
                c = 4
            d = 5
            """)

        self.make_file("not_run.py", """\
            fooey = 17
            """)

        # Import the python file, executing it.
        self.start_import_stop(cov, "mycode")

        _, statements, missing, _ = cov.analysis("not_run.py")
        self.assertEqual(statements, [1])
        self.assertEqual(missing, [1])

    def test_filenames(self):

        self.make_file("mymain.py", """\
            import mymod
            a = 1
            """)

        self.make_file("mymod.py", """\
            fooey = 17
            """)

        # Import the python file, executing it.
        cov = coverage.coverage()
        self.start_import_stop(cov, "mymain")

        filename, _, _, _ = cov.analysis("mymain.py")
        self.assertEqual(os.path.basename(filename), "mymain.py")
        filename, _, _, _ = cov.analysis("mymod.py")
        self.assertEqual(os.path.basename(filename), "mymod.py")

        filename, _, _, _ = cov.analysis(sys.modules["mymain"])
        self.assertEqual(os.path.basename(filename), "mymain.py")
        filename, _, _, _ = cov.analysis(sys.modules["mymod"])
        self.assertEqual(os.path.basename(filename), "mymod.py")

        # Import the python file, executing it again, once it's been compiled
        # already.
        cov = coverage.coverage()
        self.start_import_stop(cov, "mymain")

        filename, _, _, _ = cov.analysis("mymain.py")
        self.assertEqual(os.path.basename(filename), "mymain.py")
        filename, _, _, _ = cov.analysis("mymod.py")
        self.assertEqual(os.path.basename(filename), "mymod.py")

        filename, _, _, _ = cov.analysis(sys.modules["mymain"])
        self.assertEqual(os.path.basename(filename), "mymain.py")
        filename, _, _, _ = cov.analysis(sys.modules["mymod"])
        self.assertEqual(os.path.basename(filename), "mymod.py")

    def test_ignore_stdlib(self):
        self.make_file("mymain.py", """\
            import colorsys
            a = 1
            hls = colorsys.rgb_to_hls(1.0, 0.5, 0.0)
            """)

        # Measure without the stdlib.
        cov1 = coverage.coverage()
        self.assertEqual(cov1.config.cover_pylib, False)
        self.start_import_stop(cov1, "mymain")

        # some statements were marked executed in mymain.py
        _, statements, missing, _ = cov1.analysis("mymain.py")
        self.assertNotEqual(statements, missing)
        # but none were in colorsys.py
        _, statements, missing, _ = cov1.analysis("colorsys.py")
        self.assertEqual(statements, missing)

        # Measure with the stdlib.
        cov2 = coverage.coverage(cover_pylib=True)
        self.start_import_stop(cov2, "mymain")

        # some statements were marked executed in mymain.py
        _, statements, missing, _ = cov2.analysis("mymain.py")
        self.assertNotEqual(statements, missing)
        # and some were marked executed in colorsys.py
        _, statements, missing, _ = cov2.analysis("colorsys.py")
        self.assertNotEqual(statements, missing)

    def test_include_can_measure_stdlib(self):
        self.make_file("mymain.py", """\
            import colorsys, random
            a = 1
            r, g, b = [random.random() for _ in range(3)]
            hls = colorsys.rgb_to_hls(r, g, b)
            """)

        # Measure without the stdlib, but include colorsys.
        cov1 = coverage.coverage(cover_pylib=False, include=["*/colorsys.py"])
        self.start_import_stop(cov1, "mymain")

        # some statements were marked executed in colorsys.py
        _, statements, missing, _ = cov1.analysis("colorsys.py")
        self.assertNotEqual(statements, missing)
        # but none were in random.py
        _, statements, missing, _ = cov1.analysis("random.py")
        self.assertEqual(statements, missing)

    def test_exclude_list(self):
        cov = coverage.coverage()
        cov.clear_exclude()
        self.assertEqual(cov.get_exclude_list(), [])
        cov.exclude("foo")
        self.assertEqual(cov.get_exclude_list(), ["foo"])
        cov.exclude("bar")
        self.assertEqual(cov.get_exclude_list(), ["foo", "bar"])
        self.assertEqual(cov._exclude_regex('exclude'), "(foo)|(bar)")
        cov.clear_exclude()
        self.assertEqual(cov.get_exclude_list(), [])

    def test_exclude_partial_list(self):
        cov = coverage.coverage()
        cov.clear_exclude(which='partial')
        self.assertEqual(cov.get_exclude_list(which='partial'), [])
        cov.exclude("foo", which='partial')
        self.assertEqual(cov.get_exclude_list(which='partial'), ["foo"])
        cov.exclude("bar", which='partial')
        self.assertEqual(cov.get_exclude_list(which='partial'), ["foo", "bar"])
        self.assertEqual(cov._exclude_regex(which='partial'), "(foo)|(bar)")
        cov.clear_exclude(which='partial')
        self.assertEqual(cov.get_exclude_list(which='partial'), [])

    def test_exclude_and_partial_are_separate_lists(self):
        cov = coverage.coverage()
        cov.clear_exclude(which='partial')
        cov.clear_exclude(which='exclude')
        cov.exclude("foo", which='partial')
        self.assertEqual(cov.get_exclude_list(which='partial'), ['foo'])
        self.assertEqual(cov.get_exclude_list(which='exclude'), [])
        cov.exclude("bar", which='exclude')
        self.assertEqual(cov.get_exclude_list(which='partial'), ['foo'])
        self.assertEqual(cov.get_exclude_list(which='exclude'), ['bar'])
        cov.exclude("p2", which='partial')
        cov.exclude("e2", which='exclude')
        self.assertEqual(cov.get_exclude_list(which='partial'), ['foo', 'p2'])
        self.assertEqual(cov.get_exclude_list(which='exclude'), ['bar', 'e2'])
        cov.clear_exclude(which='partial')
        self.assertEqual(cov.get_exclude_list(which='partial'), [])
        self.assertEqual(cov.get_exclude_list(which='exclude'), ['bar', 'e2'])
        cov.clear_exclude(which='exclude')
        self.assertEqual(cov.get_exclude_list(which='partial'), [])
        self.assertEqual(cov.get_exclude_list(which='exclude'), [])

    def test_datafile_default(self):
        # Default data file behavior: it's .coverage
        self.make_file("datatest1.py", """\
            fooey = 17
            """)

        self.assertFiles(["datatest1.py"])
        cov = coverage.coverage()
        self.start_import_stop(cov, "datatest1")
        cov.save()
        self.assertFiles(["datatest1.py", ".coverage"])

    def test_datafile_specified(self):
        # You can specify the data file name.
        self.make_file("datatest2.py", """\
            fooey = 17
            """)

        self.assertFiles(["datatest2.py"])
        cov = coverage.coverage(data_file="cov.data")
        self.start_import_stop(cov, "datatest2")
        cov.save()
        self.assertFiles(["datatest2.py", "cov.data"])

    def test_datafile_and_suffix_specified(self):
        # You can specify the data file name and suffix.
        self.make_file("datatest3.py", """\
            fooey = 17
            """)

        self.assertFiles(["datatest3.py"])
        cov = coverage.coverage(data_file="cov.data", data_suffix="14")
        self.start_import_stop(cov, "datatest3")
        cov.save()
        self.assertFiles(["datatest3.py", "cov.data.14"])

    def test_datafile_from_rcfile(self):
        # You can specify the data file name in the .coveragerc file
        self.make_file("datatest4.py", """\
            fooey = 17
            """)
        self.make_file(".coveragerc", """\
            [run]
            data_file = mydata.dat
            """)

        self.assertFiles(["datatest4.py", ".coveragerc"])
        cov = coverage.coverage()
        self.start_import_stop(cov, "datatest4")
        cov.save()
        self.assertFiles(["datatest4.py", ".coveragerc", "mydata.dat"])

    def test_empty_reporting(self):
        # Used to be you'd get an exception reporting on nothing...
        cov = coverage.coverage()
        cov.erase()
        cov.report()

    def test_start_stop_start_stop(self):
        self.make_file("code1.py", """\
            code1 = 1
            """)
        self.make_file("code2.py", """\
            code2 = 1
            code2 = 2
            """)
        cov = coverage.coverage()
        self.start_import_stop(cov, "code1")
        cov.save()
        self.start_import_stop(cov, "code2")
        _, statements, missing, _ = cov.analysis("code1.py")
        self.assertEqual(statements, [1])
        self.assertEqual(missing, [])
        _, statements, missing, _ = cov.analysis("code2.py")
        self.assertEqual(statements, [1, 2])
        self.assertEqual(missing, [])

    if 0:   # expected failure
        # for https://bitbucket.org/ned/coveragepy/issue/79
        def test_start_save_stop(self):
            self.make_file("code1.py", """\
                code1 = 1
                """)
            self.make_file("code2.py", """\
                code2 = 1
                code2 = 2
                """)
            cov = coverage.coverage()
            cov.start()
            self.import_local_file("code1")
            cov.save()
            self.import_local_file("code2")
            cov.stop()

            _, statements, missing, _ = cov.analysis("code1.py")
            self.assertEqual(statements, [1])
            self.assertEqual(missing, [])
            _, statements, missing, _ = cov.analysis("code2.py")
            self.assertEqual(statements, [1, 2])
            self.assertEqual(missing, [])



class UsingModulesMixin(object):
    """A mixin for importing modules from test/modules and test/moremodules."""

    run_in_temp_dir = False

    def setUp(self):
        super(UsingModulesMixin, self).setUp()
        # Parent class saves and restores sys.path, we can just modify it.
        self.old_dir = os.getcwd()
        os.chdir(self.nice_file(os.path.dirname(__file__), 'modules'))
        sys.path.append(".")
        sys.path.append("../moremodules")

    def tearDown(self):
        os.chdir(self.old_dir)
        super(UsingModulesMixin, self).tearDown()


class OmitIncludeTestsMixin(UsingModulesMixin):
    """Test methods for coverage methods taking include and omit."""

    def filenames_in(self, summary, filenames):
        """Assert the `filenames` are in the keys of `summary`."""
        for filename in filenames.split():
            self.assertIn(filename, summary)

    def filenames_not_in(self, summary, filenames):
        """Assert the `filenames` are not in the keys of `summary`."""
        for filename in filenames.split():
            self.assertNotIn(filename, summary)

    def test_nothing_specified(self):
        result = self.coverage_usepkgs()
        self.filenames_in(result, "p1a p1b p2a p2b othera otherb osa osb")
        self.filenames_not_in(result, "p1c")
        # Because there was no source= specified, we don't search for
        # unexecuted files.

    def test_include(self):
        result = self.coverage_usepkgs(include=["*/p1a.py"])
        self.filenames_in(result, "p1a")
        self.filenames_not_in(result, "p1b p1c p2a p2b othera otherb osa osb")

    def test_include_2(self):
        result = self.coverage_usepkgs(include=["*a.py"])
        self.filenames_in(result, "p1a p2a othera osa")
        self.filenames_not_in(result, "p1b p1c p2b otherb osb")

    def test_include_as_string(self):
        result = self.coverage_usepkgs(include="*a.py")
        self.filenames_in(result, "p1a p2a othera osa")
        self.filenames_not_in(result, "p1b p1c p2b otherb osb")

    def test_omit(self):
        result = self.coverage_usepkgs(omit=["*/p1a.py"])
        self.filenames_in(result, "p1b p2a p2b")
        self.filenames_not_in(result, "p1a p1c")

    def test_omit_2(self):
        result = self.coverage_usepkgs(omit=["*a.py"])
        self.filenames_in(result, "p1b p2b otherb osb")
        self.filenames_not_in(result, "p1a p1c p2a othera osa")

    def test_omit_as_string(self):
        result = self.coverage_usepkgs(omit="*a.py")
        self.filenames_in(result, "p1b p2b otherb osb")
        self.filenames_not_in(result, "p1a p1c p2a othera osa")

    def test_omit_and_include(self):
        result = self.coverage_usepkgs(include=["*/p1*"], omit=["*/p1a.py"])
        self.filenames_in(result, "p1b")
        self.filenames_not_in(result, "p1a p1c p2a p2b")


class SourceOmitIncludeTest(OmitIncludeTestsMixin, CoverageTest):
    """Test using `source`, `omit` and `include` when measuring code."""

    def coverage_usepkgs(self, **kwargs):
        """Run coverage on usepkgs and return the line summary.

        Arguments are passed to the `coverage.coverage` constructor.

        """
        cov = coverage.coverage(**kwargs)
        cov.start()
        import usepkgs  # pragma: nested   # pylint: disable=F0401,W0612
        cov.stop()      # pragma: nested
        cov._harvest_data() # private! sshhh...
        summary = cov.data.summary()
        for k, v in list(summary.items()):
            assert k.endswith(".py")
            summary[k[:-3]] = v
        return summary

    def test_source_package(self):
        lines = self.coverage_usepkgs(source=["pkg1"])
        self.filenames_in(lines, "p1a p1b")
        self.filenames_not_in(lines, "p2a p2b othera otherb osa osb")
        # Because source= was specified, we do search for unexecuted files.
        self.assertEqual(lines['p1c'], 0)

    def test_source_package_dotted(self):
        lines = self.coverage_usepkgs(source=["pkg1.p1b"])
        self.filenames_in(lines, "p1b")
        self.filenames_not_in(lines, "p1a p1c p2a p2b othera otherb osa osb")

    def test_source_package_part_omitted(self):
        # https://bitbucket.org/ned/coveragepy/issue/218
        # Used to be if you omitted something executed and inside the source,
        # then after it was executed but not recorded, it would be found in
        # the search for unexecuted files, and given a score of 0%.
        lines = self.coverage_usepkgs(source=["pkg1"], omit=["pkg1/p1b.py"])
        self.filenames_in(lines, "p1a")
        self.filenames_not_in(lines, "p1b")
        self.assertEqual(lines['p1c'], 0)


class ReportIncludeOmitTest(OmitIncludeTestsMixin, CoverageTest):
    """Tests of the report include/omit functionality."""

    def coverage_usepkgs(self, **kwargs):
        """Try coverage.report()."""
        cov = coverage.coverage()
        cov.start()
        import usepkgs  # pragma: nested   # pylint: disable=F0401,W0612
        cov.stop()      # pragma: nested
        report = StringIO()
        cov.report(file=report, **kwargs)
        return report.getvalue()


class XmlIncludeOmitTest(OmitIncludeTestsMixin, CoverageTest):
    """Tests of the xml include/omit functionality.

    This also takes care of the HTML and annotate include/omit, by virtue
    of the structure of the code.

    """

    def coverage_usepkgs(self, **kwargs):
        """Try coverage.xml_report()."""
        cov = coverage.coverage()
        cov.start()
        import usepkgs  # pragma: nested   # pylint: disable=F0401,W0612
        cov.stop()      # pragma: nested
        cov.xml_report(outfile="-", **kwargs)
        return self.stdout()


class AnalysisTest(CoverageTest):
    """Test the numerical analysis of results."""
    def test_many_missing_branches(self):
        cov = coverage.coverage(branch=True)

        self.make_file("missing.py", """\
            def fun1(x):
                if x == 1:
                    print("one")
                else:
                    print("not one")
                print("done")           # pragma: nocover

            def fun2(x):
                print("x")

            fun2(3)
            """)

        # Import the python file, executing it.
        self.start_import_stop(cov, "missing")

        nums = cov._analyze("missing.py").numbers
        self.assertEqual(nums.n_files, 1)
        self.assertEqual(nums.n_statements, 7)
        self.assertEqual(nums.n_excluded, 1)
        self.assertEqual(nums.n_missing, 3)
        self.assertEqual(nums.n_branches, 2)
        self.assertEqual(nums.n_partial_branches, 0)
        self.assertEqual(nums.n_missing_branches, 2)


class PluginTest(CoverageTest):
    """Test that the API works properly the way the plugins call it.

    We don't actually use the plugins, but these tests call the API the same
    way they do.

    """
    def pretend_to_be_nose_with_cover(self, erase):
        """This is what the nose --with-cover plugin does."""
        cov = coverage.coverage()

        self.make_file("no_biggie.py", """\
            a = 1
            b = 2
            if b == 1:
                c = 4
            """)

        if erase:
            cov.combine()
            cov.erase()
        cov.load()
        self.start_import_stop(cov, "no_biggie")
        cov.combine()
        cov.save()
        cov.report(["no_biggie.py"])
        self.assertEqual(self.stdout(), textwrap.dedent("""\
            Name        Stmts   Miss  Cover   Missing
            -----------------------------------------
            no_biggie       4      1    75%   4
            """))

    def test_nose_plugin(self):
        self.pretend_to_be_nose_with_cover(erase=False)

    def test_nose_plugin_with_erase(self):
        self.pretend_to_be_nose_with_cover(erase=True)
