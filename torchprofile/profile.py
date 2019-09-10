import warnings

from .handlers import handlers
from .utils.trace import trace

__all__ = ['profile_macs']


def profile_macs(model, args=(), kwargs=None, reduction=sum):
    graph = trace(model, args, kwargs)

    results = dict()
    for node in graph.nodes:
        for operators, func in handlers:
            if isinstance(operators, str):
                operators = [operators]
            if node.operator in operators:
                results[node] = func(node)
                break
        else:
            warnings.warn('No handlers found: "{}". Skipped.'.format(node.operator))

    if reduction is not None:
        return reduction(results.values())
    else:
        return results
