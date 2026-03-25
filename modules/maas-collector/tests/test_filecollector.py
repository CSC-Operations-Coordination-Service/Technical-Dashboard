"""some file collector testing"""

import datetime
import os
import logging
import sys

import pytest

from maas_collector.rawdata.collector.filecollector import (
    CollectorArgs,
    FileCollectorConfiguration,
    FileCollector,
)

from conftest import mock_client

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

TEST_CONF = os.path.join(
    os.path.dirname(__file__), "conf", "test-maas-filecollector.json"
)

TEST_CONF_LOG_REGEX = os.path.join(
    os.path.dirname(__file__), "conf", "test-maas-filecollector-log-extractor.json"
)


def test_filecollector_init(monkeypatch):

    args = CollectorArgs(rawdata_config=TEST_CONF)

    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    collector = FileCollector(args)

    # ignore setup
    monkeypatch.setattr(collector, "setup", lambda: True)
    collector.setup()

    # tada try ingest something and have the mock classes AHAH
    collector.ingest(
        os.path.join(
            DATA_DIR,
            "S2A_OPER_PRD_L0__DS_SGS__20200420T205828_S20200322T173347_SIZE.xml",
        )
    )


def test_get_date_dirname():
    d = datetime.datetime(1977, 1, 23)
    assert FileCollector.get_date_dirname(d) == "1977/01/23"


def test_filecollector_with_log_extractor(monkeypatch):

    args = CollectorArgs(rawdata_config=TEST_CONF_LOG_REGEX)

    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    collector = FileCollector(args)

    # ignore setup
    monkeypatch.setattr(collector, "setup", lambda: True)
    collector.load_config()

    configs = collector.get_configurations("syslogSample.txt")

    assert len(configs) == 1
    for config in configs:

        items = list(
            config.extractor.extract(
                os.path.join(
                    DATA_DIR,
                    "syslogSample.txt",
                )
            )
        )

        assert len(items) == 60

        assert config.model.__name__ == "S3PMetrics"

        assert items[0] == {
            "check": "OK",
            "day": "9",
            "env": "N",
            "eventname": "LOPP",
            "eventtime": "2026-02-09T16:54:29",
            "filename": "S3B_TM_0_NAT__G_20200121T021231_20200121T035452_20260209T162303_6141______________SVL_O_NR_OPE.ISIP",
            "generationtime": "2020-01-21T03:54:52.000000",
            "hostname": "s3p-s3b-pf-acq-02",
            "level": "0",
            "message": "",
            "month": "Feb",
            "pid": "180335",
            "pmode": "N",
            "process": "ThinLayer",
            "ptype": "0",
            "reftime": "ground",
            "reportName": "syslogSample.txt",
            "sat": "S3B",
            "time": "16:54:29",
            "timelinessKey": "SVL__DCS_01_S3B_20200928074138009060_dat",
            "validitystart": "2020-01-21T02:12:31.000000",
            "validitystop": "2020-01-21T03:54:52.000000",
        }
