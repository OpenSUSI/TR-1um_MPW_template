#!/usr/bin/env python3
# ----- ------ ----- ----- ------ ----- ----- ------ -----
# OpenSUSI
# LICENSE: Apache License Version 2.0, January 2004
# http://www.apache.org/licenses/
# Original:
#   Copyright (c) 2025 Leo Moser <leo.moser@pm.me>
# Modified by:
#   OpenSUSI jun1okamura <jun1okamura@gmail.com>
# ----- ------ ----- ----- ------ ----- ----- ------ -----

from __future__ import annotations

import sys
from pathlib import Path

import click
import pya

FRAME_CELL_NAMES = {"OSS_FRAME", "OSS_FRAME_TEG"}

CHIP_SIZE_WIDTH  = 2500.00
CHIP_SIZE_HEIGHT = 2500.00
EXPECTED_DBU     = 0.001
EPS              = 1e-6

def fail(message: str) -> None:
    print(f"ERROR: {message}")
    sys.exit(1)


def ok(message: str) -> None:
    print(f"OK: {message}")
    sys.exit(0)


def expected_chip_box() -> tuple[pya.DPoint, pya.DPoint]:
    return (
        pya.DPoint(-CHIP_SIZE_WIDTH / 2.0, -CHIP_SIZE_HEIGHT / 2.0),
        pya.DPoint(CHIP_SIZE_WIDTH / 2.0, CHIP_SIZE_HEIGHT / 2.0),
    )


def same_float(a: float, b: float, eps: float = EPS) -> bool:
    return abs(a - b) <= eps


def same_point(a: pya.DPoint, b: pya.DPoint, eps: float = EPS) -> bool:
    return same_float(a.x, b.x, eps) and same_float(a.y, b.y, eps)


def same_box(top_bbox: pya.DBox, expected_p1: pya.DPoint, expected_p2: pya.DPoint) -> bool:
    return same_point(top_bbox.p1, expected_p1) and same_point(top_bbox.p2, expected_p2)


def get_single_top_cell(layout: pya.Layout, layout_file: str) -> pya.Cell:
    top_cells = list(layout.top_cells())

    if len(top_cells) == 0:
        fail(f"No top-level cell found in '{layout_file}'.")

    if len(top_cells) > 1:
        names = ", ".join(cell.name for cell in top_cells)
        fail(f"More than one top-level cell found in '{layout_file}': {names}")

    return top_cells[0]


def validate_top_name(top_cell: pya.Cell, expected_top_name: str) -> None:
    if top_cell.name != expected_top_name:
        fail(
            f"Top-level cell name '{top_cell.name}' does not match expected name "
            f"'{expected_top_name}'."
        )


def validate_dbu(layout: pya.Layout) -> None:
    if not same_float(layout.dbu, EXPECTED_DBU):
        fail(
            f"Database unit (dbu) is {layout.dbu:.12g}, "
            f"but expected {EXPECTED_DBU:.12g}."
        )


def validate_bbox(top_cell: pya.Cell) -> None:
    expected_p1, expected_p2 = expected_chip_box()
    top_bbox = top_cell.dbbox()

    if not same_box(top_bbox, expected_p1, expected_p2):
        fail(
            "Layout area does not match expected die area: "
            f"expected ({expected_p1.x:.2f},{expected_p1.y:.2f})"
            f"({expected_p2.x:.2f},{expected_p2.y:.2f}), "
            f"got ({top_bbox.p1.x:.2f},{top_bbox.p1.y:.2f})"
            f"({top_bbox.p2.x:.2f},{top_bbox.p2.y:.2f})."
        )


def has_required_frame_cell(layout: pya.Layout) -> bool:
    for cell in layout.each_cell():
        if cell.name in FRAME_CELL_NAMES:
            return True
    return False


@click.command()
@click.argument(
    "layout_file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
)
@click.option("--top", "expected_top_name", required=True, help="Expected top cell name")
def main(layout_file: Path, expected_top_name: str) -> None:
    layout = pya.Layout()
    layout.read(str(layout_file))

    top_cell = get_single_top_cell(layout, str(layout_file))

    validate_top_name(top_cell, expected_top_name)
    print(f"OK: Top-level cell name '{expected_top_name}' matches.")

    validate_dbu(layout)
    print(f"OK: Database unit (dbu) is {layout.dbu:.3f} um.")

    validate_bbox(top_cell)
    print(
        "OK: Layout area matches expected die area "
        f"({-CHIP_SIZE_WIDTH / 2:.2f},{-CHIP_SIZE_HEIGHT / 2:.2f})"
        f"({CHIP_SIZE_WIDTH / 2:.2f},{CHIP_SIZE_HEIGHT / 2:.2f})."
    )

    if not has_required_frame_cell(layout):
        fail(
            f"No required OpenSUSI frame/TEG cell found under top cell '{top_cell.name}'. "
            f"Expected one of: {', '.join(sorted(FRAME_CELL_NAMES))}"
        )

    ok(
        f"Design '{top_cell.name}' passed pre-check with required OpenSUSI frame/TEG cell."
    )


if __name__ == "__main__":
    main()