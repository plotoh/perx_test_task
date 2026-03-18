""""""

import logging
import sys


def setup_logging(debug: bool = False) -> None:
    """натсройка логирования"""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # логирование для фреймворков
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING if not debug else logging.INFO)
    logging.getLogger("uvicorn").setLevel(logging.INFO)
