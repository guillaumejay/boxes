# Copyright (C) 2013-2024 Florian Festi
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from boxes import *


class Counters(Boxes):
    """Game counters/tokens for board games"""

    ui_group = "Misc"

    description = """
Game counters are circular disc-shaped tokens that can be used in board games.
This generator creates laser-cut counters with optional center holes for marking or stacking.

You can customize:
- Counter diameter
- Center hole diameter (0 for no hole)
- Number of counters to generate
- Optional engraving marks (crosshairs or circles)
"""

    def __init__(self) -> None:
        Boxes.__init__(self)

        self.argparser.add_argument(
            "--diameter",  action="store", type=float, default=25.0,
            help="diameter of counter in mm")
        self.argparser.add_argument(
            "--hole_diameter",  action="store", type=float, default=0.0,
            help="diameter of center hole in mm (0 for no hole)")
        self.argparser.add_argument(
            "--count",  action="store", type=int, default=10,
            help="number of counters to generate")
        self.argparser.add_argument(
            "--marking",  action="store", type=str, default="none",
            choices=["none", "crosshair", "circle", "dot"],
            help="optional marking style for center")
        self.argparser.add_argument(
            "--marking_size",  action="store", type=float, default=5.0,
            help="size of marking in mm")

    def crosshair_marking(self):
        """Draw a crosshair marking in the center"""
        size = self.marking_size
        with self.saved_context():
            self.set_source_color(Color.ETCHING)
            self.moveTo(-size/2, 0)
            self.edge(size)
            self.moveTo(-size/2, 0)
            self.moveTo(0, -size/2, 90)
            self.edge(size)
            self.ctx.stroke()

    def circle_marking(self):
        """Draw a circle marking in the center"""
        with self.saved_context():
            self.set_source_color(Color.ETCHING)
            self.hole(0, 0, self.marking_size / 2)

    def dot_marking(self):
        """Draw a small dot in the center"""
        with self.saved_context():
            self.set_source_color(Color.ETCHING)
            self.hole(0, 0, self.marking_size / 4)

    def counter_callback(self):
        """Callback function for each counter"""
        # Add center hole if specified
        if self.hole_diameter > 0:
            self.hole(0, 0, self.hole_diameter / 2)

        # Add marking if specified
        if self.marking == "crosshair":
            self.crosshair_marking()
        elif self.marking == "circle":
            self.circle_marking()
        elif self.marking == "dot":
            self.dot_marking()

    def render(self):
        # Calculate how many counters per row for optimal layout
        counters_per_row = math.ceil(math.sqrt(self.count))
        rows = math.ceil(self.count / counters_per_row)

        # Generate counters using partsMatrix for efficient layout
        self.partsMatrix(
            counters_per_row,
            rows,
            "up",
            self.parts.disc,
            self.diameter,
            callback=self.counter_callback
        )
