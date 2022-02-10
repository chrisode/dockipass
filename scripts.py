import subprocess


def test(verbose=False):
    """
    Run all unittests. Equivalent to:
    `poetry run python -u -m unittest discover`
    """
    subprocess.run(
        ["python", "-u", "-m", "unittest", "discover"]
    )

def testverbose():
    """
    Run all unittests. Equivalent to:
    `poetry run python -u -m unittest discover -v`
    """
    subprocess.run(
        ["python", "-u", "-m", "unittest", "discover", "-v"]
    )