import logging
from pathlib import Path

LoggerName = "BioForge"
LogFileName = "BioBorge.log"
LogFormat = "%(asctime)s | %(levelname)-8s | %(message)s"


def setup_logging(out_dir):
    #برای تولید فایل و برگرداندن لاگرمون
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(LoggerName)
    logger.setLevel(logging.INFO)

    #برای اینکه لاگر های تکراری نوشته نشه
    for handler in list(logger.handlers):
        handler.close()
        logger.removeHandler(handler)

    file_handler = logging.FileHandler(
        out_dir / LogFileName, mode="a", encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter(LogFormat, "%Y-%m-%d %H:%M:%S"))   
    logger.addHandler(file_handler)

    return logger


def get_logger():
    #اگر خواستیم لاگر رو از هر جای دیگه برناممون بگیریم کافیه این رو صدا بزنیم
    return logging.getLogger(LoggerName)