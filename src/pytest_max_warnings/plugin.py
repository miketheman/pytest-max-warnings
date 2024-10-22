from __future__ import annotations

import pytest


_STASH_KEY = pytest.StashKey["bool"]()


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("pytest-max-warnings")
    group.addoption(
        "--max-warnings",
        action="store",
        type=int,
        default=None,
        help="Max number of warnings before failing",
    )


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    max_warnings = session.config.option.max_warnings
    terminal_reporter = session.config.pluginmanager.get_plugin("terminalreporter")
    assert terminal_reporter is not None

    warnings_summary = terminal_reporter.stats.get("warnings", [])

    if max_warnings is not None and len(warnings_summary) > max_warnings:
        session.exitstatus = 100
        session.config.stash[_STASH_KEY] = True


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    max_warnings = config.option.max_warnings
    warnings_summary = terminalreporter.stats.get("warnings", [])

    exceeded_max_warnings = config.stash.get(_STASH_KEY, False)
    if not exceeded_max_warnings:
        return

    terminalreporter.write_sep("=", "pytest-max-warnings")
    terminalreporter.write_line(
        f"ERROR: Exceeded the maximum allowed warnings: {len(warnings_summary)} > {max_warnings}"
    )
