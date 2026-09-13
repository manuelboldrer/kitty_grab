from typing import Any, Callable, Iterable, Sequence, Tuple

from kitty.conf.utils import KittensKeyDefinition, parse_kittens_key

FuncArgsType = Tuple[str, Sequence[Any]]

try:
    from kitty.conf.utils import KeyFuncWrapper
    func_with_args = KeyFuncWrapper[FuncArgsType]()
except ImportError:
    from kitty.conf.utils import key_func
    func_with_args, args_funcs = key_func()
    func_with_args.args_funcs = args_funcs



def parse_map(val: str) -> Iterable[KittensKeyDefinition]:
    x = parse_kittens_key(val, func_with_args.args_funcs)
    if x is not None:
        yield x


def parse_region_type(region_type: str) -> str:
    result = region_type.lower()
    assert result in ['stream', 'columnar']
    return result


def parse_direction(direction: str) -> str:
    direction_lc = direction.lower()
    assert direction_lc in ['left', 'right', 'up', 'down',
                            'page up', 'page down',
                            'first', 'first nonwhite',
                            'last nonwhite', 'last',
                            'top', 'bottom',
                            'word left', 'word right', 'word end',
                            'big word left', 'big word right', 'big word end',
                            'screen top', 'screen middle', 'screen bottom',
                            'matching bracket']
    return direction_lc.replace(' ', '_')


def parse_scroll_direction(direction: str) -> str:
    result = direction.lower()
    assert result in ['up', 'down']
    return result


def parse_mode(mode: str) -> str:
    result = mode.lower()
    assert result in ['normal', 'visual', 'block', 'line']
    return result


def parse_find_args(args: str) -> Tuple[str, str]:
    direction, kind = args.lower().split(' ', 1)
    assert direction in ['forward', 'backward']
    assert kind in ['to', 'till']
    return direction, kind


def parse_repeat_direction(direction: str) -> str:
    result = direction.lower()
    assert result in ['same', 'reverse']
    return result


def parse_search_direction(direction: str) -> str:
    result = direction.lower()
    assert result in ['forward', 'backward']
    return result


@func_with_args('move')
def move(func: Callable, direction: str) -> Tuple[Callable, str]:
    return func, parse_direction(direction)


@func_with_args('scroll')
def scroll(func: Callable, direction: str) -> Tuple[Callable, str]:
    return func, parse_scroll_direction(direction)


@func_with_args('select')
def select(func: Callable, args: str) -> Tuple[Callable, Tuple[str, str]]:
    region_type, direction = args.split(' ', 1)
    return func, (parse_region_type(region_type),
                  parse_direction(direction))


@func_with_args("set_mode")
def set_mode(func: Callable, mode: str) -> Tuple[Callable, str]:
    return func, parse_mode(mode)


@func_with_args('find')
def find(func: Callable, args: str) -> Tuple[Callable, Tuple[str, str]]:
    return func, parse_find_args(args)


@func_with_args('repeat_find')
def repeat_find(func: Callable, direction: str) -> Tuple[Callable, str]:
    return func, parse_repeat_direction(direction)


@func_with_args('start_search')
def start_search(func: Callable, direction: str) -> Tuple[Callable, str]:
    return func, parse_search_direction(direction)


@func_with_args('repeat_search')
def repeat_search(func: Callable, direction: str) -> Tuple[Callable, str]:
    return func, parse_repeat_direction(direction)
