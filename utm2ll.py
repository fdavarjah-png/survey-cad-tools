#!/usr/bin/env python3
"""Convert UTM coordinates to latitude/longitude (WGS84)."""

import argparse
import sys

try:
    from pyproj import Transformer
except ImportError:
    sys.exit("pyproj is not installed. Install it with: pip install pyproj")


def utm_to_latlon(easting, northing, zone, hemisphere):
    hemisphere = hemisphere.upper()
    if hemisphere not in ("N", "S"):
        raise ValueError("hemisphere must be N or S")
    if not 1 <= zone <= 60:
        raise ValueError("zone must be between 1 and 60")

    # WGS84 UTM: EPSG 326xx (north) or 327xx (south)
    epsg = (32600 if hemisphere == "N" else 32700) + zone
    transformer = Transformer.from_crs(f"EPSG:{epsg}", "EPSG:4326", always_xy=True)
    lon, lat = transformer.transform(easting, northing)
    return lat, lon


def main():
    parser = argparse.ArgumentParser(description="Convert UTM (WGS84) to lat/lon.")
    parser.add_argument("easting", type=float, help="Easting in meters")
    parser.add_argument("northing", type=float, help="Northing in meters")
    parser.add_argument("zone", type=int, help="UTM zone (1-60)")
    parser.add_argument("hemisphere", help="N or S")
    args = parser.parse_args()

    try:
        lat, lon = utm_to_latlon(args.easting, args.northing, args.zone, args.hemisphere)
    except ValueError as e:
        parser.error(str(e))

    print(f"lat: {lat:.6f}")
    print(f"lon: {lon:.6f}")


if __name__ == "__main__":
    main()
