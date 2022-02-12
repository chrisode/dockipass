import subprocess


def test():
    """
    Run all unittests. Equivalent to:
    `poetry run python3 -u -m unittest discover`
    """
    subprocess.run(
        ["python3", "-u", "-m" "unittest", "discover"]
    )

def test_verbose():
    """
    Run all unittests. Equivalent to:
    `poetry run python -u -m unittest discover -v`
    """
    subprocess.run(
        ["python3", "-u", "-m" "unittest", "discover", "-v"]
    )

def test_features():
    """
    Run all unittests. Equivalent to:
    `poetry run python3 -u -m unittest discover -v`
    """
    subprocess.run(
        ["python3", "-u", "-m" "unittest", "discover", "-s", "tests/features", "-v"]
    )