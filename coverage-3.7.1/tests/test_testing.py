# -*- coding: utf-8 -*-
"""Tests that our test infrastructure is really working!"""

import os, sys
from coverage.backward import to_bytes, rpartition
from tests.backunittest import TestCase
from tests.coveragetest import CoverageTest

from coverage.backward import set                   # pylint: disable=W0622

class TestingTest(TestCase):
    """Tests of helper methods on `backunittest.TestCase`."""

    run_in_temp_dir = False

    def please_raise(self, exc, msg):
        """Raise an exception for testing assertRaisesRegexp."""
        raise exc(msg)

    def please_succeed(self):
        """A simple successful method for testing assertRaisesRegexp."""
        return "All is well"

    def test_assert_same_elements(self):
        self.assertSameElements(set(), set())
        self.assertSameElements(set([1,2,3]), set([3,1,2]))
        self.assertRaises(AssertionError, self.assertSameElements,
            set([1,2,3]), set()
            )
        self.assertRaises(AssertionError, self.assertSameElements,
            set([1,2,3]), set([4,5,6])
            )

    def test_assert_regexp_matches(self):
        self.assertRegexpMatches("hello", "hel*o")
        self.assertRegexpMatches("Oh, hello there!", "hel*o")
        self.assertRaises(AssertionError, self.assertRegexpMatches,
            "hello there", "^hello$"
            )

    def test_assert_multiline_equal(self):
        self.assertMultiLineEqual("hello", "hello")
        self.assertRaises(AssertionError, self.assertMultiLineEqual,
            "hello there", "Hello there"
            )
        self.assertRaises(AssertionError, self.assertMultiLineEqual,
            "hello\nthere", "hello\nThere"
            )
        # With messages also.
        self.assertMultiLineEqual("hi", "hi", "it's ok")
        self.assertRaisesRegexp(
            AssertionError, "my message",
            self.assertMultiLineEqual, "xyz", "abc", "my message"
        )

    def test_assert_raises_regexp(self):
        # Raising the right error with the right message passes.
        self.assertRaisesRegexp(
            ZeroDivisionError, "Wow! Zero!",
            self.please_raise, ZeroDivisionError, "Wow! Zero!"
            )
        # Raising the right error with a match passes.
        self.assertRaisesRegexp(
            ZeroDivisionError, "Zero",
            self.please_raise, ZeroDivisionError, "Wow! Zero!"
            )
        # Raising the right error with a mismatch fails.
        self.assertRaises(AssertionError,
            self.assertRaisesRegexp, ZeroDivisionError, "XYZ",
            self.please_raise, ZeroDivisionError, "Wow! Zero!"
            )
        # Raising the right error with a mismatch fails.
        self.assertRaises(AssertionError,
            self.assertRaisesRegexp, ZeroDivisionError, "XYZ",
            self.please_raise, ZeroDivisionError, "Wow! Zero!"
            )
        # Raising the wrong error raises the error itself.
        self.assertRaises(ZeroDivisionError,
            self.assertRaisesRegexp, IOError, "Wow! Zero!",
            self.please_raise, ZeroDivisionError, "Wow! Zero!"
            )
        # Raising no error fails.
        self.assertRaises(AssertionError,
            self.assertRaisesRegexp, ZeroDivisionError, "XYZ",
            self.please_succeed
            )

    def test_assert_true(self):
        self.assertTrue(True)
        self.assertRaises(AssertionError, self.assertTrue, False)

    def test_assert_false(self):
        self.assertFalse(False)
        self.assertRaises(AssertionError, self.assertFalse, True)

    def test_assert_in(self):
        self.assertIn("abc", "hello abc")
        self.assertIn("abc", ["xyz", "abc", "foo"])
        self.assertIn("abc", {'abc': 1, 'xyz': 2})
        self.assertRaises(AssertionError, self.assertIn, "abc", "xyz")
        self.assertRaises(AssertionError, self.assertIn, "abc", ["x", "xabc"])
        self.assertRaises(AssertionError, self.assertIn, "abc", {'x':'abc'})

    def test_assert_not_in(self):
        self.assertRaises(AssertionError, self.assertNotIn, "abc", "hello abc")
        self.assertRaises(AssertionError,
            self.assertNotIn, "abc", ["xyz", "abc", "foo"]
            )
        self.assertRaises(AssertionError,
            self.assertNotIn, "abc", {'abc': 1, 'xyz': 2}
            )
        self.assertNotIn("abc", "xyz")
        self.assertNotIn("abc", ["x", "xabc"])
        self.assertNotIn("abc", {'x':'abc'})

    def test_assert_greater(self):
        self.assertGreater(10, 9)
        self.assertGreater("xyz", "abc")
        self.assertRaises(AssertionError, self.assertGreater, 9, 10)
        self.assertRaises(AssertionError, self.assertGreater, 10, 10)
        self.assertRaises(AssertionError, self.assertGreater, "abc", "xyz")
        self.assertRaises(AssertionError, self.assertGreater, "xyz", "xyz")


class CoverageTestTest(CoverageTest):
    """Test the methods in `CoverageTest`."""

    def file_text(self, fname):
        """Return the text read from a file."""
        return open(fname, "rb").read().decode('ascii')

    def test_make_file(self):
        # A simple file.
        self.make_file("fooey.boo", "Hello there")
        self.assertEqual(open("fooey.boo").read(), "Hello there")
        # A file in a sub-directory
        self.make_file("sub/another.txt", "Another")
        self.assertEqual(open("sub/another.txt").read(), "Another")
        # A second file in that sub-directory
        self.make_file("sub/second.txt", "Second")
        self.assertEqual(open("sub/second.txt").read(), "Second")
        # A deeper directory
        self.make_file("sub/deeper/evenmore/third.txt")
        self.assertEqual(open("sub/deeper/evenmore/third.txt").read(), "")

    def test_make_file_newline(self):
        self.make_file("unix.txt", "Hello\n")
        self.assertEqual(self.file_text("unix.txt"), "Hello\n")
        self.make_file("dos.txt", "Hello\n", newline="\r\n")
        self.assertEqual(self.file_text("dos.txt"), "Hello\r\n")
        self.make_file("mac.txt", "Hello\n", newline="\r")
        self.assertEqual(self.file_text("mac.txt"), "Hello\r")

    def test_make_file_non_ascii(self):
        self.make_file("unicode.txt", "tabblo: «ταБЬℓσ»")
        self.assertEqual(
            open("unicode.txt", "rb").read(),
            to_bytes("tabblo: «ταБЬℓσ»")
            )

    def test_file_exists(self):
        self.make_file("whoville.txt", "We are here!")
        self.assert_exists("whoville.txt")
        self.assert_doesnt_exist("shadow.txt")
        self.assertRaises(
            AssertionError, self.assert_doesnt_exist, "whoville.txt"
            )
        self.assertRaises(AssertionError, self.assert_exists, "shadow.txt")

    def test_sub_python_is_this_python(self):
        # Try it with a python command.
        os.environ['COV_FOOBAR'] = 'XYZZY'
        self.make_file("showme.py", """\
            import os, sys
            print(sys.executable)
            print(os.__file__)
            print(os.environ['COV_FOOBAR'])
            """)
        out = self.run_command("python showme.py").splitlines()
        self.assertEqual(out[0], sys.executable)
        self.assertEqual(out[1], os.__file__)
        self.assertEqual(out[2], 'XYZZY')

        # Try it with a "coverage debug sys" command.
        out = self.run_command("coverage debug sys").splitlines()
        # "environment: COV_FOOBAR = XYZZY" or "COV_FOOBAR = XYZZY"
        executable = [l for l in out if "executable:" in l][0]
        executable = executable.split(":", 1)[1].strip()
        self.assertTrue(same_python_executable(executable, sys.executable))
        environ = [l for l in out if "COV_FOOBAR" in l][0]
        _, _, environ = rpartition(environ, ":")
        self.assertEqual(environ.strip(), "COV_FOOBAR = XYZZY")


def same_python_executable(e1, e2):
    """Determine if `e1` and `e2` refer to the same Python executable.

    Either path could include symbolic links.  The two paths might not refer
    to the exact same file, but if they are in the same directory and their
    numeric suffixes aren't different, they are the same executable.

    """
    e1 = os.path.abspath(os.path.realpath(e1))
    e2 = os.path.abspath(os.path.realpath(e2))

    if os.path.dirname(e1) != os.path.dirname(e2):
        return False

    e1 = os.path.basename(e1)
    e2 = os.path.basename(e2)

    if e1 == "python" or e2 == "python" or e1 == e2:
        # python and python2.3: ok
        # python2.3 and python: ok
        # python and python: ok
        # python2.3 and python2.3: ok
        return True

    return False
