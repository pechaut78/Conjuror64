from ..Atom import Atom
import csv
import os

class Input(Atom):
    def process(self):
        self.success("Passing input")
        self.output = self.params.get("input")
