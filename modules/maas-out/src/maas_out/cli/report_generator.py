"""CLI to use custom generator"""

import argparse
import json
import logging
import sys

import opensearchpy.connection.connections as db_connections
from maas_engine.cli import args as maas_args
from maas_engine.cli.log import setup_logging
from maas_out.master_of_kpi import demo_extract


def report_generator_main(argv):
    """satruman entry point with args parsing

    Args:
        argv (list): argument provide to run satruman
    """

    # OpenSearch access
    parser = argparse.ArgumentParser(parents=[maas_args.es_parser()])

    # Loglevel
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )

    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )

    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Don't modify database",
        dest="dry_run",
    )

    args = parser.parse_args(argv)

    setup_logging(loglevel=args.loglevel)

    logging.info("Setup connection to Database")
    db_connections.create_connection(
        hosts=[maas_args.get_es_credentials_url(args)],
        retry_on_timeout=True,
        max_retries=args.es_retries,
        verify_certs=not args.es_ignore_certs_verification,
        ssl_show_warn=not args.es_ignore_certs_verification,
    )

    demo_extract()


def run():
    """main entry point"""
    report_generator_main(sys.argv[1:])


if __name__ == "__main__":
    run()
