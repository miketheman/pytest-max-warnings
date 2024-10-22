# pytest-max-warnings

A Pytest plugin to exit non-zero exit code
when the configured maximum warnings has been exceeded.

## Installation

You can install "pytest-max-warnings" via [pip](https://pypi.org/project/pytest-max-warnings/):

```bash
pip install pytest-max-warnings
```

or any other package manager you prefer.

## Usage

You can set the maximum number of warnings allowed by using the `--max-warnings` option:

```bash
pytest --max-warnings 10
```

If the number of warnings exceeds the maximum, the test run will exit with a non-zero exit code.

## License

Distributed under the terms of the MIT license, "pytest-max-warnings" is free and open source software.
See [LICENSE](./LICENSE) for more details.

## Authors

- [@miketheman](https://github.com/miketheman)
