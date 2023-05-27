"""
Tasks for maintaining the project.

Execute 'invoke --list' for guidance on using Invoke
"""
import inspect
import platform
import shutil
import webbrowser
from pathlib import Path

import pytest
from invoke import task, exceptions, Context  # type: ignore

# For python 3.11 support
if not hasattr(inspect, "getargspec"):
    inspect.getargspec = inspect.getfullargspec

ROOT_DIR = Path(__file__).parent
BIN_DIR = ROOT_DIR.joinpath("bin")
SETUP_FILE = ROOT_DIR.joinpath("setup.py")
TEST_DIR = ROOT_DIR.joinpath("tests")
SOURCE_DIR = ROOT_DIR.joinpath("api")
TOX_DIR = ROOT_DIR.joinpath(".tox")
JUNIT_XML_FILE = BIN_DIR.joinpath("report.xml")
COVERAGE_XML_FILE = BIN_DIR.joinpath("coverage.xml")
COVERAGE_HTML_DIR = BIN_DIR.joinpath("coverage_html")
COVERAGE_HTML_FILE = COVERAGE_HTML_DIR.joinpath("index.html")
COVERAGE_FAIL_UNDER = 0
DOCS_DIR = ROOT_DIR.joinpath("docs")
DOCS_SOURCE_DIR = DOCS_DIR.joinpath("source")
DOCS_BUILD_DIR = DOCS_DIR.joinpath("_build")
DOCS_INDEX = DOCS_BUILD_DIR.joinpath("index.html")
PYTHON_DIRS = [str(d) for d in [SOURCE_DIR, TEST_DIR]]
SAFETY_REQUIREMENTS_FILE = BIN_DIR.joinpath("safety_requirements.txt")
PYPI_URL = "https://pypi.org/simple/"
PYTHON_VERSION = 3.9
CI_PROJECT_NAME = "spend-pi"


def _delete_file(file: Path) -> None:
    """
    If the file exists, delete it
    """
    try:
        file.unlink(missing_ok=True)
    except TypeError:
        # missing_ok argument added in 3.8
        try:
            file.unlink()
        except FileNotFoundError:
            pass


def _run(_c: Context, command: str) -> None:
    """
    It runs a command
    """
    return _c.run(command, pty=platform.system() != 'Windows')


@task(help={'check': "Checks if source is formatted without applying changes"})
def format(_c: Context, check: bool = False) -> None:
    """
    It runs the `black` and `isort` tools on the Python code in the `PYTHON_DIRS` directories
    """
    python_dirs_string = " ".join(PYTHON_DIRS)
    # Run black
    black_options = "--check" if check else ""
    _run(_c, f"black {black_options} {python_dirs_string}")
    # Run isort
    isort_options = "--check-only --diff" if check else ""
    _run(_c, f"isort {isort_options} {python_dirs_string}")


@task
def lint_pylint(_c: Context) -> None:
    """
    It runs pylint on all Python files in the project
    """
    _run(_c, "pylint {}".format(" ".join(PYTHON_DIRS)))


@task
def lint_ruff(_c: Context) -> None:
    """
    Lint code with mypy
    """
    _run(_c, f"ruff check {' '.join(PYTHON_DIRS)}")


@task
def lint_mypy(_c: Context) -> None:
    """
    It runs mypy on all Python files in the project
    """
    _run(_c, "mypy {}".format(" ".join(PYTHON_DIRS)))


@task(lint_pylint, lint_ruff, lint_mypy)
def lint(_) -> None:
    """
    It runs all linting tools on all Python files in the project
    """


@task
def security_bandit(_c: Context) -> None:
    """
    It runs bandit security checks on the source directory
    """
    _run(_c, f"bandit -c pyproject.toml -r {SOURCE_DIR}")


@task
def security_safety(_c: Context) -> None:
    """
    It runs security checks on package dependencies
    """
    Path(BIN_DIR).mkdir(parents=True, exist_ok=True)
    _run(_c, f"poetry export --with dev --format=requirements.txt --without-hashes --output={SAFETY_REQUIREMENTS_FILE}")
    _run(_c, f"safety check --file={SAFETY_REQUIREMENTS_FILE} --full-report")


@task(security_bandit, security_safety)
def security(_c: Context) -> None:
    """
    It runs all security checks
    """


@task(
    optional=["coverage", "args", "key", "fail_under"],
    help={
        "junit": "Output a junit xml report (default: False)",
        "coverage": 'Add coverage, ="html" for html output or ="xml" for xml output',
        "args": "Arguments to pass to pytest",
    },
)
def test(
    _, junit=False, coverage=None, fail_under=COVERAGE_FAIL_UNDER, args=None, key=None
) -> None:
    """
    It runs the tests in the current directory. Test default parameters are in the `pyproject.toml` file.

    Usage examples:
    > invoke test --junit --coverage=html --args="-vv"
    > invoke test --coverage --fail-under=75 --key="not integration"
    """
    pytest_args = ["-n", "auto"]

    if args:
        for arg in args.split():
            pytest_args.append(arg)
    if key:
        pytest_args.append(f"-k={key}")
    if junit:
        pytest_args.append(f"--junitxml={JUNIT_XML_FILE}")
    if coverage is not None:
        pytest_args.append(f"--cov={SOURCE_DIR}")
        pytest_args.append(f"--cov-report=term")
        pytest_args.append(f"--cov-fail-under={fail_under}")
        if coverage == "html":
            pytest_args.append(f"--cov-report=html:{COVERAGE_HTML_DIR}")
        elif coverage == "xml":
            pytest_args.append(f"--cov-report=xml:{COVERAGE_XML_FILE}")

    pytest_args.append(str(TEST_DIR))
    return_code = pytest.main(pytest_args)

    if return_code:
        raise exceptions.Exit("Tests failed", code=return_code)

    if coverage == "html":
        webbrowser.open(COVERAGE_HTML_FILE.as_uri())


@task
def clean_docs(_c: Context) -> None:
    """
    It takes a list of strings and returns a list of strings
    """
    _run(_c, f"rm -fr {DOCS_BUILD_DIR}")
    _run(_c, f"rm -fr {DOCS_SOURCE_DIR}")


@task(pre=[clean_docs], help={"launch": "Launch documentation in the web browser"})
def docs(_c: Context, launch: bool = True) -> None:
    """
    It generates and opens the documentation for the project
    """
    # Generate autodoc stub files
    _run(_c, f"sphinx-apidoc -e -P -o {DOCS_SOURCE_DIR} {SOURCE_DIR}")
    # Generate docs
    _run(_c, f"sphinx-build -b html {DOCS_DIR} {DOCS_BUILD_DIR}")
    if launch:
        webbrowser.open(DOCS_INDEX.as_uri())


@task
def clean_build(_c: Context) -> None:
    """
    It cleans all the Python build and distribution artifacts
    """
    _run(_c, "rm -fr build/")
    _run(_c, "rm -fr dist/")
    _run(_c, "rm -fr .eggs/")
    _run(_c, "find . -name '*.egg-info' -exec rm -fr {} +")
    _run(_c, "find . -name '*.egg' -exec rm -f {} +")


@task
def clean_python(_c: Context) -> None:
    """
    It removes all the Python artifacts
    """
    _run(_c, "find . -name '*.pyc' -exec rm -f {} +")
    _run(_c, "find . -name '*.pyo' -exec rm -f {} +")
    _run(_c, "find . -name '*~' -exec rm -f {} +")
    _run(_c, "find . -name '__pycache__' -exec rm -fr {} +")


@task
def clean_tests(_c: Context) -> None:
    """
    It deletes all the test artifacts
    """
    _delete_file(JUNIT_XML_FILE)
    _delete_file(COVERAGE_XML_FILE)
    shutil.rmtree(COVERAGE_HTML_DIR, ignore_errors=True)
    shutil.rmtree(BIN_DIR, ignore_errors=True)
    shutil.rmtree(TOX_DIR, ignore_errors=True)


@task(pre=[clean_build, clean_python, clean_tests, clean_docs])
def clean(_c: Context) -> None:
    """
    It runs all clean sub-tasks
    """


@task(clean)
def dist(_c: Context) -> None:
    """
    It builds source and wheel packages using Poetry
    """
    _run(_c, "poetry build")


@task(pre=[clean, dist])
def release_poetry(
    _c: Context,
    pypi_user: str,
    pypi_pass: str,
) -> None:
    """
    It makes a release of the Python package and publishes to PyPI using Poetry
    """
    pypi_publish_repository = ""
    _run(_c, f"poetry config repositories.pypi_upload {pypi_publish_repository}")
    _run(_c, f"poetry publish -r pypi_upload -u {pypi_user} -p {pypi_pass}")
