import py
from _pytest import nodes as nodes
from _pytest.compat import TYPE_CHECKING as TYPE_CHECKING
from _pytest.config import Config as Config, ExitCode as ExitCode, UsageError as UsageError, directory_arg as directory_arg, hookimpl as hookimpl
from _pytest.fixtures import FixtureManager as FixtureManager
from _pytest.outcomes import exit as exit
from _pytest.python import Package as Package
from _pytest.reports import CollectReport as CollectReport
from _pytest.runner import SetupState as SetupState, collect_one_node as collect_one_node
from typing import Any, Callable, Optional, Union
from typing_extensions import Literal as Literal

def pytest_addoption(parser: Any) -> None: ...
def wrap_session(config: Config, doit: Callable[[Config, Session], Optional[Union[int, ExitCode]]]) -> Union[int, ExitCode]: ...
def pytest_cmdline_main(config: Any): ...
def pytest_collection(session: Any): ...
def pytest_runtestloop(session: Any): ...
def pytest_ignore_collect(path: py.path.local, config: Config) -> Optional[Literal[True]]: ...
def pytest_collection_modifyitems(items: Any, config: Any) -> None: ...

class NoMatch(Exception): ...

class Interrupted(KeyboardInterrupt):
    __module__: str = ...

class Failed(Exception): ...

class _bestrelpath_cache(dict):
    path: Any = ...
    def __missing__(self, path: py.path.local) -> str: ...
    def __init__(self, path: Any) -> None: ...
    def __ne__(self, other: Any) -> Any: ...
    def __eq__(self, other: Any) -> Any: ...
    def __lt__(self, other: Any) -> Any: ...
    def __le__(self, other: Any) -> Any: ...
    def __gt__(self, other: Any) -> Any: ...
    def __ge__(self, other: Any) -> Any: ...

class Session(nodes.FSCollector):
    Interrupted: Any = ...
    Failed: Any = ...
    exitstatus: Union[int, ExitCode] = ...
    testsfailed: int = ...
    testscollected: int = ...
    shouldstop: bool = ...
    shouldfail: bool = ...
    trace: Any = ...
    startdir: Any = ...
    def __init__(self, config: Config) -> None: ...
    @classmethod
    def from_config(cls, config: Any): ...
    def pytest_collectstart(self) -> None: ...
    def pytest_runtest_logreport(self, report: Any) -> None: ...
    pytest_collectreport: Any = ...
    def isinitpath(self, path: Any): ...
    def gethookproxy(self, fspath: py.path.local) -> Any: ...
    def perform_collect(self, args: Optional[Any] = ..., genitems: bool = ...): ...
    def collect(self) -> None: ...
    def matchnodes(self, matching: Any, names: Any): ...
    def genitems(self, node: Any) -> None: ...
