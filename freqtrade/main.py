#!/usr/bin/env python3
"""
Main Freqtrade bot script.
Read the documentation to know what cli arguments you need.
"""

import logging
import sys
from typing import Any


# check min. python version
if sys.version_info < (3, 11):  # pragma: no cover  # noqa: UP036
    sys.exit("Freqtrade requires Python version >= 3.11")

from freqtrade import __version__
from freqtrade.commands import Arguments
from freqtrade.constants import DOCS_LINK
from freqtrade.exceptions import ConfigurationError, FreqtradeException, OperationalException
from freqtrade.loggers import setup_logging_pre
from freqtrade.system import (
    asyncio_setup,
    gc_set_threshold,
    print_version_info,
    set_mp_start_method,
)


logger = logging.getLogger("freqtrade")


def main(sysargv: list[str] | None = None) -> None:
    """
    This function will initiate the bot and start the trading loop.
    :return: None
    """

    return_code: Any = 1
    try:
        setup_logging_pre()
        asyncio_setup()
        arguments = Arguments(sysargv)
        args = arguments.get_parsed_arg()

        # Call subcommand.
        if args.get("version") or args.get("version_main"):
            print_version_info()
            return_code = 0
        elif "func" in args:
            logger.info(f"freqtrade {__version__}")
            gc_set_threshold()
            set_mp_start_method()
            return_code = args["func"](args)
        else:
            # No subcommand was issued.
            raise OperationalException(
                "使用 Freqtrade 需要指定一个子命令。\n"
                "要让机器人在实时/模拟运行模式下执行交易，"
                "根据配置中 `dry_run` 设置的值，运行 Freqtrade "
                "为 `freqtrade trade [选项...]`。\n"
                "要查看所有可用选项，请使用 "
                "`freqtrade --help` 或 `freqtrade <命令> --help`。"
            )

    except SystemExit as e:  # pragma: no cover
        return_code = e
    except KeyboardInterrupt:
        logger.info("收到 SIGINT，正在中止...")
        return_code = 0
    except ConfigurationError as e:
        logger.error(
            f"配置错误：{e}\n"
            f"请确保查看 {DOCS_LINK} 上的文档。"
        )
    except FreqtradeException as e:
        logger.error(str(e))
        return_code = 2
    except Exception:
        logger.exception("致命异常！")
    finally:
        sys.exit(return_code)


if __name__ == "__main__":  # pragma: no cover
    main()
