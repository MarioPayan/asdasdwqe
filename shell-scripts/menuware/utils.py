from importlib import import_module


def get_func(dotted_path):
    module_name = '.'.join(dotted_path.split('.')[:-1])
    function_name = dotted_path.split('.')[-1]
    try:
        _module = import_module(module_name)
    except ImportError:
        return None
    func = getattr(_module, function_name, None)
    return func
