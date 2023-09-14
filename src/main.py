import logging
from parcer.parcer import Parcer
from parcer.services import init_db_connection, init_logger

def main():
    init_logger()
    logging.info('Запуск системы..')
    collection = init_db_connection()
    parcer = Parcer()
    parcer.run(collection)
    # source = dict(zip(titles, source_urls))
    # collect_pic(source)

if __name__ == "__main__":
    main()