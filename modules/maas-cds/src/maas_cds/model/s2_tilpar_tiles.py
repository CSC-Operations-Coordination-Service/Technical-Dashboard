"""Custom CDS model definition for s2 tiles"""

import logging, copy, opensearchpy
from itertools import groupby
from maas_cds.model.generated import CdsS2Tilpar

LOGGER = logging.getLogger("S2Tiles")


class S2Tiles(CdsS2Tilpar):
    """
    Sentinel-2 TILPAR Tiles mapping
    """

    DLON_THRESHOLD: float = 180.0

    @staticmethod
    def intersection(footprint: dict) -> list[str]:
        """
        Get the list of tiles intersected by the given geojson footprint.
        """
        assert footprint
        result = []

        # if the footprint cross antemeridian try correction and intersection
        if S2Tiles.is_crossing_antemeridian(footprint):
            corrected_geojson = S2Tiles.correct_polygon(footprint)
            corrected_geojson_without_duplicate = S2Tiles.remove_duplicate_points(
                corrected_geojson
            )
            try:
                tiles_search = (
                    S2Tiles.search()
                    .filter(
                        "geo_shape",
                        geometry={
                            "relation": "intersects",
                            "shape": corrected_geojson_without_duplicate,
                        },
                    )
                    .scan()
                )
                result = [tile.name for tile in tiles_search]
            except opensearchpy.exceptions.RequestError as ex:
                # in case of intersection request error we return the full S2Tile list
                LOGGER.error(
                    "Error requesting intercection between ST2Tiles and corrected polygon! Requesting with original polygon."
                )
                # the global search is done here because the number of occurrences of the error is very low.
                tiles_search = (
                    S2Tiles.search()
                    .filter(
                        "geo_shape",
                        geometry={
                            "relation": "intersects",
                            "shape": S2Tiles.remove_duplicate_points(footprint),
                        },
                    )
                    .scan()
                )
                result = [tile.name for tile in tiles_search]
        else:
            tiles_search = (
                S2Tiles.search()
                .filter(
                    "geo_shape",
                    geometry={
                        "relation": "intersects",
                        "shape": S2Tiles.remove_duplicate_points(footprint),
                    },
                )
                .scan()
            )
            result = [tile.name for tile in tiles_search]
        return result

    @staticmethod
    def remove_duplicate_points(footprint: dict) -> dict:
        """
        Remove duplicated points from geojson geometry.
        """
        footprint["coordinates"] = [[p[0] for p in groupby(*footprint["coordinates"])]]

        return footprint

    @staticmethod
    def is_crossing_antemeridian(geojson_footprint: dict):
        """
        Check if geojson polygon cross antemeridian
        """
        for coordinates in geojson_footprint["coordinates"]:
            nbredges = len(coordinates)
            for edge_nbr in range(0, nbredges):
                if edge_nbr < nbredges - 1:
                    lon1 = float(coordinates[edge_nbr][0])
                    lon2 = float(coordinates[edge_nbr + 1][0])
                    if abs(lon2 - lon1) > S2Tiles.DLON_THRESHOLD:
                        LOGGER.info(
                            "Segment is crossing antemeridian [%s,%s], distance %s  > %s !!",
                            str(lon1),
                            str(lon2),
                            str(abs(lon2 - lon1)),
                            S2Tiles.DLON_THRESHOLD,
                        )
                        return True
        return False

    @staticmethod
    def correct_polygon(geojson_footprint: dict):
        """
        correct longitudes for antemeridian geometries
        """

        corrected_coordinate = []

        for coordinates in geojson_footprint["coordinates"]:
            for coordinate in coordinates:
                corrected_lon = float(coordinate[0])
                if 179.99 <= abs(corrected_lon) <= 180:
                    # This point are too much dangerous don't keep it
                    continue
                if corrected_lon < 0:
                    corrected_lon = corrected_lon + 360
                corrected_coordinate.append([corrected_lon, coordinate[1]])

        corrected_geojson_footprint = copy.deepcopy(geojson_footprint)

        corrected_geojson_footprint["coordinates"] = [corrected_coordinate]

        return corrected_geojson_footprint
