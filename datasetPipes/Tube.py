from .Atom import Atom
from .pipes.CSVMerge import CSVMerge
import csv
import json

class Tube:
    def __init__(self):
        self.atoms = []
        self.registry = {}
        self.register("CSVMerge", CSVMerge)

    def register(self, name, cls):
        if not issubclass(cls, Atom):
            raise ValueError(f"Class {cls.__name__} must derive from Atom")
        self.registry[name] = cls
        

    def create_atom(self, name, params):
        if name not in self.registry:
            raise ValueError(f"Class {name} not registered")
        cls = self.registry[name]
        return cls(params)

    def addAtom(self, atom):
        self.atoms.append(atom)

    def run(self):
        last_result = None
        for atom in self.atoms:
            last_result = atom.run()
            if not last_result['ok']:
                break
        return last_result

    def clear(self):
        self.atoms = []

    def from_json(self, json_file):
        self.clear()
        with open(json_file, 'r') as file:
            data = json.load(file)
            for entry in data:
                atom_name = entry['atom']
                params = entry['params']
                try:
                    atom = self.create_atom(atom_name, params)
                except ValueError as e:
                    return {"ok": False, "error": str(e)}
                self.addAtom(atom)
        return {"ok": True, "error": ""}
