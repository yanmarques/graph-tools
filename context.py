import logger


_logger = logger.get_logger(__name__)


def save_point(old_context, running_context):
    _logger.debug('transaction status: commit')
    new_context = running_context.clone()
    new_context.previous_context = old_context.clone()
    return new_context


def roll_last_context(running_context):
    _logger.debug('transaction status: rolling back')
    old_context = running_context.previous_context.clone()
    return old_context


def run_interactive_context(running_context, predicate, callback,
                 one_transaction=True):
    try:
        while True:
            flash_context = running_context.clone()
            flash_context.previous_context = running_context

            _logger.debug('start-context: %s', flash_context)

            result = predicate(flash_context)
            if result == False:
                break

            running_context = map_and_save(callback, result,
                                           running_context,
                                           flash_context,
                                           one_transaction=one_transaction)
            _logger.debug('context-change: %s', running_context)
    except KeyboardInterrupt:
        print() # jump one line when no logging available
        return roll_last_context(running_context)
    return running_context


def map_and_save(callback, items, global_context, running_context,
                 one_transaction=True):
    def commit(status):
        if status:
            return save_point(global_context, running_context)
        return global_context

    for item in items:
        running_context = callback(running_context, item)
        global_context = commit(not one_transaction)

    return commit(one_transaction)
