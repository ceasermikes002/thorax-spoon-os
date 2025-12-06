import pathlib
import sys


sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from app.agent.runner import execute  # type: ignore


def test_execute_echo():
    assert execute("ping") == "ping"

