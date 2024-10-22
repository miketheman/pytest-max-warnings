def test_help_message(pytester):
    result = pytester.runpytest("--help")

    result.stdout.fnmatch_lines(
        [
            "pytest-max-warnings:",
            "*--max-warnings=MAX_WARNINGS",
            "*Max number of warnings before failing*",
        ]
    )


def test_captures_warning_natively(pytester):
    pytester.makepyfile(
        """
        import warnings

        def test_emit_warnings():
            warnings.warn("Warning")
            warnings.warn("Warning")
        """
    )

    result = pytester.runpytest()
    result.assert_outcomes(passed=1, warnings=2)


def test_does_not_exceed_max_warnings(pytester):
    pytester.makepyfile(
        """
        import warnings

        def test_emit_warnings():
            warnings.warn("Warning")
            warnings.warn("Warning")
        """
    )

    result = pytester.runpytest("--max-warnings=2")
    result.assert_outcomes(passed=1, warnings=2)
    assert result.ret == 0


def test_exceeds_max_warnings(pytester):
    pytester.makepyfile(
        """
        import warnings

        def test_emit_warnings():
            warnings.warn("Warning")
            warnings.warn("Warning")
        """
    )

    result = pytester.runpytest("--max-warnings=1")
    result.assert_outcomes(passed=1, warnings=2)
    assert result.ret == 100
    result.stdout.fnmatch_lines(["*Exceeded the maximum allowed warnings: 2 > 1*"])
