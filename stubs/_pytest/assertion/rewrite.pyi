import ast
import importlib.util
from _pytest._io.saferepr import saferepr as saferepr
from _pytest._version import version as version
from _pytest.assertion import AssertionState as AssertionState, util as util
from _pytest.compat import TYPE_CHECKING as TYPE_CHECKING, fspath as fspath
from _pytest.pathlib import Path as Path, PurePath as PurePath, fnmatch_ex as fnmatch_ex
from _pytest.store import StoreKey as StoreKey
from typing import Any, Optional

assertstate_key: Any
PYTEST_TAG: Any
PYC_EXT: Any
PYC_TAIL: Any

class AssertionRewritingHook(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    config: Any = ...
    fnpats: Any = ...
    session: Any = ...
    def __init__(self, config: Any) -> None: ...
    def set_session(self, session: Any) -> None: ...
    def find_spec(self, name: Any, path: Optional[Any] = ..., target: Optional[Any] = ...): ...
    def create_module(self, spec: Any) -> None: ...
    def exec_module(self, module: Any) -> None: ...
    def mark_rewrite(self, *names: str) -> None: ...
    def get_data(self, pathname: Any): ...

def rewrite_asserts(mod: Any, source: Any, module_path: Optional[Any] = ..., config: Optional[Any] = ...) -> None: ...

UNARY_MAP: Any
BINOP_MAP: Any

def set_location(node: Any, lineno: Any, col_offset: Any): ...

class AssertionRewriter(ast.NodeVisitor):
    module_path: Any = ...
    config: Any = ...
    enable_assertion_pass_hook: Any = ...
    source: Any = ...
    def __init__(self, module_path: Any, config: Any, source: Any) -> None: ...
    def run(self, mod: ast.Module) -> None: ...
    @staticmethod
    def is_rewrite_disabled(docstring: Any): ...
    def variable(self): ...
    def assign(self, expr: Any): ...
    def display(self, expr: Any): ...
    def helper(self, name: Any, *args: Any): ...
    def builtin(self, name: Any): ...
    def explanation_param(self, expr: Any): ...
    explanation_specifiers: Any = ...
    def push_format_context(self) -> None: ...
    def pop_format_context(self, expl_expr: Any): ...
    def generic_visit(self, node: Any): ...
    statements: Any = ...
    variables: Any = ...
    variable_counter: Any = ...
    format_variables: Any = ...
    stack: Any = ...
    expl_stmts: Any = ...
    def visit_Assert(self, assert_: Any): ...
    def visit_Name(self, name: Any): ...
    def visit_BoolOp(self, boolop: Any): ...
    def visit_UnaryOp(self, unary: Any): ...
    def visit_BinOp(self, binop: Any): ...
    def visit_Call(self, call: Any): ...
    def visit_Starred(self, starred: Any): ...
    def visit_Attribute(self, attr: Any): ...
    def visit_Compare(self, comp: ast.Compare) -> Any: ...

def try_makedirs(cache_dir: Any) -> bool: ...
def get_cache_dir(file_path: Path) -> Path: ...
