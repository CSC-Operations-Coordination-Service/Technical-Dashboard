"""Extract mission planning files"""

from dataclasses import dataclass, field
import fnmatch
import typing

from maas_collector.rawdata.collector.filecollector import FileCollectorConfiguration
from maas_collector.rawdata.collector.httpcollector import (
    HttpCollector,
    HttpCollectorConfiguration,
    HttpConfiguration,
)

from maas_collector.rawdata.collector.httpmixin import HttpMixin

from maas_collector.rawdata.collector.journal import CollectorJournal
from maas_collector.rawdata.collector.mpip.v1_impl import (
    MpipQueryV1Implementation,
)

from maas_collector.rawdata.collector.http.authentication import build_authentication

import maas_collector.rawdata.collector.tools.archivetools as archivetools

import os


@dataclass
class MpipCollectorConfiguration(HttpCollectorConfiguration):
    """Configuration for Mpip Collector Configuration"""

    date_attr: str = "ingestion_date"

    refresh_interval: int = 10

    base_url: str = ""

    file_list_url: str = ""

    probe_url: str = ""

    mpip_start_offset: int = 0

    end_date_time_offset: int = 0

    protocol_version: str = "v1"

    product_per_page: int = 20

    download_file_pattern: str = None

    # Query filters

    filetypes: list = None

    extensions: list = None

    platforms: list = None

    fileclasses: list = None

    filenames: list = None

    session_ids: list = None

    versions: list = None

    actives: list = field(default_factory=lambda: ["true"])

    edrs_creation_date: str = None

    ingestion_date: str = None

    # auth argument

    oauth_basic_credential: str = ""

    client_username: str = ""

    client_password: str = ""

    token_url: str = ""

    client_id: str = ""

    client_secret: str = ""

    scope: str = None

    grant_type: str = "password"

    # sub collector

    download_file_pattern: list = field(default_factory=lambda: [])

    parent_file_pattern: str = None

    no_credential: bool = False

    def get_config_product_url(self):
        """Retrieve the product_url field from the collector configuration

        This function can be overloaded by child class in case their product url
        field is named differently and we do not want to break retrocompatibiliy

        Returns:
            str: product url field
        """
        return self.base_url

    def filename_match(self, name: str) -> bool:
        """Check if a filename matches the configuration

        parent_file_pattern is used to link a sub config to its main
        config without altering the file_pattern attribute.

        It allows to test independant parts of the collect pipeline
        (list files, d/l & untar, extract) without having to replay the whole pipeline

        Args:
            name ([str]): name of a file

        Returns:
            bool: True if the file is ok to be processed by the configuration extractor
        """
        if self.parent_file_pattern:
            return fnmatch.fnmatch(name, self.parent_file_pattern)
        elif self.file_pattern:
            return fnmatch.fnmatch(name, self.file_pattern)
        return False


@dataclass
class MpipConfiguration(HttpConfiguration):
    """Store Mpip configuration vars"""


class MpipCollector(HttpCollector, HttpMixin):
    """A Mpip collector that collect from the mpip interface."""

    CONFIG_CLASS = MpipCollectorConfiguration

    IMPL_DIR = {"v1": MpipQueryV1Implementation}

    def ingest_all_interfaces(self):
        """Nominal ingestion from OData: collect all the OData configurations"""
        # iterate over all OData collector configurations
        for config in self.configs:
            if config.no_credential:
                # pseudo configuration for auxiliary ingestion, like downloaded files
                continue

            self.ingest_interface(CollectorJournal(config), config)

            if self.should_stop_loop:
                break

    def post_process_data(self, data, filename, config, http_session):
        if config.download_file_pattern:

            self.logger.debug("file pattern : %s", config.download_file_pattern)

            url_list = []

            if isinstance(config.download_file_pattern, str):
                file_pattern = config.download_file_pattern
                url_list = self.match_file_pattern_with_product_name(
                    data, config, file_pattern
                )
            elif isinstance(config.download_file_pattern, list):
                for file_pattern in config.download_file_pattern:
                    url_list += self.match_file_pattern_with_product_name(
                        data, config, file_pattern
                    )

            if len(url_list) > 0:
                # download file
                result_download_files = self.download_product(
                    config,
                    self.args.working_directory,
                    http_session,
                    url_list,
                )

                self.extract_from_file_download(result_download_files)

    # pylint: disable=R0913
    # Parameters must be mandatory
    def download_product(
        self, config, working_directory, http_session, url_list
    ) -> list:
        """download file from product

        Args:
            logger (Logger): collector logger
            working_directory (str):  working directory path
            config (MpipCollectorConfiguration): config of the collector
            http_session (Session): http session
            headers (_type_): authentication header
            product (dict): product

        Raises:
            ValueError: _description_

        Returns:
            list: path list of file downloaded
        """

        extract_files_and_config = []

        authentication = build_authentication(config.auth_method, config, http_session)

        headers = authentication.get_headers()

        for name, url in url_list:

            self.logger.debug("Download file in odata interface : %s", url)
            self.logger.debug("url_list name %s", name)
            self.logger.debug("url_list url %s", url)

            # Get file product
            response = http_session.get(
                url,
                headers=headers,
                timeout=self.http_config.timeout,
            )

            if not 200 <= response.status_code <= 300:
                # serious problem
                self.logger.error(
                    "Error querying %s %d: %s",
                    url,
                    response.status_code,
                    response.content,
                )
                raise ValueError(f"Error querying {url}")

            # put data in file at working_directory
            filepath = os.path.join(working_directory, name)

            # -- Common behaviour
            config_download_list = self.get_configurations(name)
            self.logger.debug("Filepath :%s", filepath)
            self.logger.debug("config download list :%s", config_download_list)
            for config_download in config_download_list:
                self.logger.debug(
                    "config download file_pattern :%s", config_download.file_pattern
                )

                with open(filepath, "bw") as file_desc:
                    file_desc.write(response.content)

                # if file is a archive : unarchive
                ext = os.path.splitext(filepath)[1].lower()
                if ext == ".tgz":
                    self.logger.debug("Ext == tgz")
                    extract_files = archivetools.extract_files_in_tar(
                        self.logger,
                        filepath,
                        working_directory,
                        config_download.file_pattern,
                    )
                    self.logger.debug("extract_files :%s", extract_files)

                    for path_file in extract_files:
                        extract_files_and_config.append((path_file, config_download))

                    # remove tgz
                    os.remove(filepath)
                elif ext == ".zip":
                    self.logger.debug("Ext == zip")
                    extract_files = archivetools.extract_files_in_zip(
                        self.logger,
                        filepath,
                        working_directory,
                        config_download.file_pattern,
                    )

                    for path_file in extract_files:
                        extract_files_and_config.append((path_file, config_download))
                    # remove zip
                    os.remove(filepath)
                else:
                    self.logger.debug("Ext == %s", ext)

                    extract_files_and_config.append((filepath, config_download))

        return extract_files_and_config

    def get_configurations(
        self, filename: str
    ) -> typing.List[FileCollectorConfiguration]:
        """Get the FileCollectorConfiguration instances that can handle a file

        Args:
            path ([filename]): filename

        Returns:
            [typing.List[FileCollectorConfiguration]]: list of configuration that can extract
        """
        basename = os.path.basename(filename)
        return [config for config in self.configs if config.filename_match(basename)]

    def match_file_pattern_with_product_name(self, data, config, file_pattern) -> list:
        """Match product names in the given data against a file pattern and return a list of matched names and URLs.

        Args:
            data (dict): The data containing product information.
            config (HttpCollectorConfiguration): The configuration for the HTTP collector.
            file_pattern (str): The file pattern to match against product names.

        Returns:
            list: A list of tuples containing matched product names and their corresponding URLs.
        """
        url_list = []
        for product in data:

            # check file pattern is matched
            if fnmatch.fnmatch(product["filename"].lower(), file_pattern.lower()):
                self.logger.debug(
                    "Download File pattern find : %s", product["filename"]
                )

                url_list.append(
                    (
                        product["filename"],
                        self.get_product_url(config.product),
                    )
                )
        return url_list

    @classmethod
    def build_probe_query(cls, config: MpipCollectorConfiguration):
        """Creation of a query which will be sent to the mpip API to check if it is online

        Args:
            config (MpipCollectorConfiguration): Configuration of the collector

        Returns:
            str: query
        """

        return config.probe_url

    @classmethod
    def attributs_url(cls):
        return super().attributs_url() + ["file_list_url"]

    @classmethod
    def document(cls, config: MpipCollectorConfiguration):
        information = super().document(config)

        return information

    def get_product_url(self, config: MpipCollectorConfiguration, product: dict) -> str:
        """_summary_

        Args:
            config (ODataCollectorConfiguration): config of the collector
            product (dict): the product to =be downloaded

        Returns:
            str: the url that allow to dowload the product content
        """

        name = product["filename"]

        url = f"{config.get_config_product_url()}download?filename={name}"

        return url
