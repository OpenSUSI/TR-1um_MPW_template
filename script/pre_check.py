# Copyright (c) 2025 Leo Moser <leo.moser@pm.me>
# SPDX-License-Identifier: Apache-2.0
# modified by OpenSUSI jun1okamura <jun1okamura@gmail.com>  

import sys
import pya
import click

FRAME_CELL_NAMES = ["OSS_FRAME", "OSS_FRAME_TEG"]
CHIP_SIZE_WIDTH = 2500.00
CHIP_SIZE_HEIGHT = 2500.00
EXPECTED_DBU = 0.001


def fail(message: str) -> None:
    print(message)
    sys.exit(1)


def pass_check(message: str) -> None:
    print(message)
    sys.exit(0)


def expected_chip_box() -> tuple[pya.DPoint, pya.DPoint]:
    return (
        pya.DPoint(-CHIP_SIZE_WIDTH / 2, -CHIP_SIZE_HEIGHT / 2),
        pya.DPoint(CHIP_SIZE_WIDTH / 2, CHIP_SIZE_HEIGHT / 2),
    )

@click.command()
@click.argument(
    "input",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.option("--top", required=True)
def check_top(input: str, top: str):
    ly = pya.Layout()
    ly.read(input)
    top_cell = ly.top_cell()

    # Ensure exactly one top-level cell exists.
    if len(ly.top_cells()) > 1:
        fail(f"[Error] More than one top-level cell in {input}!")

    # Fail if no top-level cell is found.
    if top_cell is None:
        fail(f"[Error] No top-level cell in {input}!")

    # Validate the top cell name matches the expected design name.
    if top_cell.name != top:
        fail(f"[Error] Top-level cell name '{top_cell.name}' does not match expected name '{top}'!")

    # Report name match.
    print(f"Design name '{top}' matches as the top-level cell in '{input}'.")

    # Check database unit (dbu).
    if ly.dbu != EXPECTED_DBU:
        fail("[Error]: Database unit (dbu) is not 0.001um.")

    # Check bounding box matches expected die area.
    expected_p1, expected_p2 = expected_chip_box()
    top_bbox = top_cell.dbbox()
    if top_bbox.p1 != expected_p1 or top_bbox.p2 != expected_p2:
        fail(
            "[Error]: Layout area is not (%.2f,%.2f)(%.2f,%.2f)."
            % (-CHIP_SIZE_WIDTH / 2, -CHIP_SIZE_HEIGHT / 2, CHIP_SIZE_WIDTH / 2, CHIP_SIZE_HEIGHT / 2)
        )

    # Check required frame/TEG cell exists.
    for cl in ly.each_cell():
        if cl.name in FRAME_CELL_NAMES:
            pass_check(
                f"Design name '{input}' fit into OpenSUSI-MPW die area (%.2f,%.2f)(%.2f,%.2f)."
                % (-CHIP_SIZE_WIDTH / 2, -CHIP_SIZE_HEIGHT / 2, CHIP_SIZE_WIDTH / 2, CHIP_SIZE_HEIGHT / 2)
            )

    # No frame found.
    fail(f"[Error]: There is NO OpenSUSI-MPW recommended frame/TEG in {top_cell.name}.")

if __name__ == "__main__":
    check_top()
