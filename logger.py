import logging
import sys
import traceback


class DeferredLogger:
    def __init__(self, name):
        self.name = name
        self.instance = None
        self.__mixins__ = dir(logging.Logger)
        self.__passthrough__ = ['__passthrough__', '__mixins__', 'name', 'instance']

    def __getattribute__(self, name):
        if name in super().__getattribute__('__passthrough__'):
            return super().__getattribute__(name)
        
        if name in iter(self.__mixins__):
            if self.instance is None:
                self.instance = logging.getLogger(self.name)  
            method = getattr(self.instance, name)
            assert method is not None, f'Logger mixin not found for [{name}]'
            return method
        raise KeyError(f'Item was not found for [{name}]')


def get_logger(name):
    return DeferredLogger(name)


def on_exception(type, value, tb):
    logger = logging.getLogger('excepthook')
    if logger.getEffectiveLevel() == logging.DEBUG:
        traceback.print_tb(tb)
    if type == KeyboardInterrupt:
        print()
        logger.error('[!] Ctrl+C : interrupt received')
        return
    logger.error(value)


def setup(debug=False):
    level = logging.INFO
    if debug:
        level = logging.DEBUG

    logging.basicConfig(level=level,
                        format='%(asctime)s %(levelname)s - %(message)s')
    sys.excepthook = on_exception