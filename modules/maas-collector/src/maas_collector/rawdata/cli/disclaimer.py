"""Entry point for SAR-MPC Quality Disclaimer collection"""
import argparse
import sys

import maas_collector.rawdata.cli.lib.log as maas_log
from maas_collector.rawdata.cli.lib.args import (
    common_parser,
    get_collector_args,
    disclaimer_parser,
)
from maas_collector.rawdata.collector.filecollector import CollectorArgs
from maas_collector.rawdata.collector.disclaimercollector import (
    DisclaimerCollector,
    DisclaimerConfiguration,
)


def disclaimer_collector_main(args):
    """entry point"""
    parser = argparse.ArgumentParser(
        parents=[common_parser(), disclaimer_parser()]
    )

    namespace = parser.parse_args(args)

    # setup logging
    maas_log.setup_logging(namespace.loglevel)

    args = get_collector_args(CollectorArgs, namespace)

    disclaimer_config = DisclaimerConfiguration(
        namespace.disclaimer_timeout,
        namespace.disclaimer_keep_files,
    )

    collector = DisclaimerCollector(args, disclaimer_config)

    collector.setup()

    try:
        # no path provided
        collector.run(("Disclaimer",))
    except KeyboardInterrupt:
        print("exited by keyboard interruption")


if __name__ == "__main__":
    disclaimer_collector_main(sys.argv[1:])
