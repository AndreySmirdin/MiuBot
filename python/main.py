import time

from bot import get_updates, process_new_message

if __name__ == '__main__':
    last_update = 0
    while True:
        updates = get_updates(last_update)
        if updates:
            for update in updates:
                last_update = max(last_update, update['update_id'] + 1)
                process_new_message(update)
        time.sleep(0.5)
