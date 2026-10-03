"""Structured Gaussian log components and job discovery.

Component ``block_pattern`` expressions include their heading and use multiline
matching. Their parsers receive a list of complete matched blocks, except for
``Single`` components. ``large`` controls automatic selection, never explicit
reads. All quantities use the units printed by Gaussian; no conversion is made.
"""

import re
from collections import namedtuple

import numpy as np


NUMBER = r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[DdEe][-+]?\d+)?"
FLOAT = r"[-+]?(?:\d+\.\d*|\.\d+)(?:[DdEe][-+]?\d+)?"
FLAGS = re.MULTILINE
ROUTE = re.compile(r"^[ \t]*-{5,}[ \t]*\n(?P<route>[ \t]*#[^\n]*\n(?:[^\n]*\n)*?)[ \t]*-{5,}[ \t]*$", FLAGS)
HeaderData = namedtuple("HeaderData", ["config", "job"])


def gaussian_float(value):
    return float(value.replace("D", "E").replace("d", "e"))


def gaussian_numbers(text):
    """Read Fortran exponents and adjacent fixed-width signed values."""
    return np.array([gaussian_float(v) for v in re.findall(NUMBER, text)])


def gaussian_route(text):
    # Gaussian wraps at a fixed column, including in the middle of words.
    return "".join(line[1:] if line.startswith(" ") else line
                   for line in text.splitlines()).strip()


def gaussian_route_options(route):
    """Tokenize parentheses as a unit, preserving the historical Header API."""
    route = re.sub(r"\s*=\s*", "=", route).replace("#", " # ")
    tokens, token, depth = [], [], 0
    for char in route:
        if char.isspace() and depth == 0:
            if token:
                tokens.append("".join(token))
                token = []
        else:
            token.append(char)
            depth += (char == "(") - (char == ")")
    if token:
        tokens.append("".join(token))
    options = {}
    for token in tokens:
        if token == "#":
            continue
        depth, assignment = 0, None
        for i, char in enumerate(token):
            if char == "=" and depth == 0:
                assignment = i
                break
            depth += (char == "(") - (char == ")")
        call = re.fullmatch(r"([A-Za-z]+)\((.*)\)", token)
        if assignment is not None:
            name, value = token[:assignment], token[assignment + 1:]
            options[name.lower()] = [v.strip() for v in value.strip("()").split(",")]
        elif call and call[1].lower() in {"freq", "frequency", "opt", "popt", "nmr", "polar", "stable", "td", "cis", "irc", "admp", "bomd"}:
            options[call[1].lower()] = [v.strip() for v in call[2].split(",")]
        else:
            options[token] = []
    return options


def gaussian_header_parser(text):
    if text is None:
        return None
    match = ROUTE.search(text)
    route = gaussian_route(match.group("route")) if match else ""
    config = dict(re.findall(r"^[ \t]*%([^=\s]+)[ \t]*=[ \t]*([^\n]+)", text, FLAGS))
    return HeaderData(config, gaussian_route_options(route))


def gaussian_job_types(route, text=""):
    options = gaussian_route_options(route)
    names = {k.lower() for k in options}
    types = []
    def add(kind, condition):
        if condition and kind not in types:
            types.append(kind)
    add("optimization", bool(names & {"opt", "popt"}) or "Optimization completed." in text)
    add("scan", "scan" in names or bool(re.search(r"\bScan\s+\d+", text))
        or "Summary of the potential surface scan" in text or "Summary of Optimized Potential Surface Scan" in text)
    add("frequency", bool(names & {"freq", "frequency"}) or "Harmonic frequencies (" in text)
    add("anharmonic", any("anharm" in v.lower() for k, vals in options.items()
                         if k.lower() in {"freq", "frequency"} for v in vals)
        or "Anharmonic Infrared Spectroscopy" in text)
    add("excited_state", bool(names & {"td", "tda", "cis", "zindo"}) or "Excited State " in text)
    add("irc", "irc" in names or "Reaction path following" in text)
    add("dynamics", bool(names & {"bomd", "admp"}) or "FrcOut:" in text)
    for name, kind in [("polar", "polarizability"), ("nmr", "nmr"),
                       ("stable", "stability"), ("force", "force")]:
        add(kind, name in names)
    return tuple(types or ["single_point"])


def gaussian_job_metadata(text):
    """Describe each printed route section, including internal Link1 jobs."""
    matches = list(ROUTE.finditer(text))
    starts = [0]
    for previous, current in zip(matches, matches[1:]):
        gap = text[previous.end():current.start()]
        terminations = list(re.finditer(r"^.*(?:Normal termination of Gaussian|Error termination)[^\n]*\n?", gap, FLAGS))
        starts.append(previous.end() + terminations[-1].end() if terminations else current.start())
    jobs = []
    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(text)
        section = text[start:end]
        route = gaussian_route(matches[i].group("route")) if matches else ""
        status = parse_job_status(section)
        jobs.append({"index": i, "route": route, "job_types": gaussian_job_types(route, section),
                     "config": gaussian_header_parser(section).config,
                     "start": start, "end": end, "status": status["status"]})
    return jobs


def parse_job_types(text):
    return tuple(dict.fromkeys(kind for j in gaussian_job_metadata(text) for kind in j["job_types"]))


def parse_job_status(text):
    events = []
    terminal_end = 0
    for match in re.finditer(r"^.*(?:Normal termination of Gaussian|Error termination)[^\n]*", text, FLAGS):
        line = match.group().strip()
        events.append({"status": "normal" if "Normal termination" in line else "error", "message": line})
        terminal_end = match.end()
    warnings = [m.group().strip() for m in re.finditer(r"^.*(?:Warning|WARNING|Error:|ERROR:)[^\n]*", text, FLAGS)]
    status = events[-1]["status"] if events else "incomplete"
    routes = list(ROUTE.finditer(text))
    if routes and routes[-1].start() > terminal_end:
        status = "incomplete"
    return {"status": status, "terminations": events,
            "warnings": list(dict.fromkeys(w for w in warnings if "This program may not be used" not in w)), "optimization_completed": "Optimization completed." in text,
            "optimization_stopped": "Optimization stopped." in text or "Number of steps exceeded" in text}


def parse_run_info(blocks):
    records = []
    for block in blocks:
        version = re.search(r"Gaussian\s+(\d+):\s*([^\n]*)", block)
        if version:
            records.append({"program": "Gaussian " + version[1], "revision": version[2].strip()})
        else:
            records.append({"message": block.strip()})
    return records


def parse_archive_summary(blocks):
    """Read archive metadata and named properties without derivative dumps."""
    records = []
    for block in blocks:
        block = re.sub(r"\n[ \t]*", "", block.strip())
        parts = block.split("\\\\")
        header = parts[0].split("\\")[2:]
        if len(header) < 7 or len(parts) < 4:
            raise ValueError("incomplete Gaussian archive header")
        record = dict(zip(("node", "job", "level_of_theory", "basis", "formula", "user", "date"), header))
        record.update(route=parts[1], description=parts[2], molecule=parts[3].split("\\"), properties={})
        for section in parts[4:]:
            for chunk in section.split("\\"):
                if "=" not in chunk:
                    continue
                name, value = chunk.split("=", 1)
                if re.fullmatch(NUMBER, value):
                    value = gaussian_float(value)
                elif re.fullmatch(NUMBER + r"(?:," + NUMBER + r")+", value):
                    value = gaussian_numbers(value)
                record["properties"][name] = value
        records.append(record)
    return records


def parse_timing(blocks):
    records = []
    for block in blocks:
        match = re.search(r"(Job cpu time|Elapsed time):\s*(\d+) days\s*(\d+) hours\s*(\d+) minutes\s*(" + NUMBER + r") seconds", block)
        if match:
            kind, days, hours, minutes, seconds = match.groups()
            records.append({"kind": "cpu" if kind.startswith("Job") else "elapsed",
                            "seconds": int(days) * 86400 + int(hours) * 3600 + int(minutes) * 60 + gaussian_float(seconds)})
    return records


def parse_molecule_info(blocks):
    records = []
    for block in blocks:
        if "Multiplicity" in block:
            charge, multiplicity = re.search(r"Charge\s*=\s*(-?\d+)\s+Multiplicity\s*=\s*(\d+)", block).groups()
            records.append({"charge": int(charge), "multiplicity": int(multiplicity)})
        else:
            records.append({name: int(value) for name, value in re.findall(r"(NAtoms|NActive|NUniq)\s*=\s*(\d+)", block)})
    return records


def parse_basis_info(blocks):
    records = []
    for block in blocks:
        record = {}
        match = re.search(r"Standard basis:\s*(.*)", block)
        if match:
            record["basis"] = match.group(1).strip()
        match = re.search(r"(\d+) basis functions,\s*(\d+) primitive gaussians(?:,\s*(\d+) cartesian basis functions)?", block)
        if match:
            record.update(zip(("basis_functions", "primitive_gaussians", "cartesian_basis_functions"),
                              (int(v) if v else None for v in match.groups())))
        for name, value in re.findall(r"(NBasis|NAE|NBE|NFC|NFV)\s*=\s*(\d+)", block):
            record[name] = int(value)
        match = re.search(r"(\d+) alpha electrons\s+(\d+) beta electrons", block)
        if match:
            record.update(alpha_electrons=int(match[1]), beta_electrons=int(match[2]))
        records.append(record)
    return records


def parse_energy_records(blocks):
    records = []
    for block in blocks:
        match = re.search(r"SCF Done:\s*E\(([^)]+)\)\s*=\s*(" + NUMBER + r")(?:\s+A.U.\s+after\s+(\d+) cycles)?", block)
        if match:
            records.append({"method": match[1], "energy": gaussian_float(match[2]), "units": "hartree",
                            "cycles": int(match[3]) if match[3] else None})
            continue
        for match in re.finditer(r"(E(?:UMP[234](?:\([^)]*\))?|[RU]?MP[234]|\(CORR\)|\(CCSD\)|\(QCISD\)|\(TD-HF/TD-DFT\))|CCSD\(T\)|QCISD\(T\)|ONIOM: extrapolated energy)\s*=\s*(" + NUMBER + ")", block):
            records.append({"method": match[1], "energy": gaussian_float(match[2]), "units": "hartree"})
    return records


def parse_geometry_records(blocks):
    records = []
    for block in blocks:
        rows = re.findall(r"^\s*(\d+)\s+(-?\d+)\s+(-?\d+)\s+(" + NUMBER + r")\s+(" + NUMBER + r")\s+(" + NUMBER + r")\s*$", block, FLAGS)
        if not rows:
            raise ValueError("orientation table contains no coordinates")
        records.append({"orientation": re.search(r"(Standard|Input|Z-Matrix) orientation", block)[1],
                        "centers": np.array([int(r[0]) for r in rows]),
                        "atomic_numbers": np.array([int(r[1]) for r in rows]),
                        "atomic_types": np.array([int(r[2]) for r in rows]),
                        "coordinates": np.array([[gaussian_float(v) for v in r[3:]] for r in rows]), "units": "angstrom"})
    return records


def parse_input_geometry(blocks):
    records = []
    for block in blocks:
        atoms, variables = [], {}
        charge = re.search(r"Charge\s*=\s*(-?\d+)\s+Multiplicity\s*=\s*(\d+)", block)
        in_variables = False
        for line in block.splitlines()[1:]:
            line = line.strip()
            if not line or line.startswith("Charge"):
                continue
            if line in {"Variables:", "Constants:"}:
                in_variables = True
                continue
            if in_variables:
                match = re.match(r"(\w+)\s+(" + NUMBER + r")(.*)", line)
                if match:
                    scan = re.search(r"Scan\s+(\d+)\s+(" + NUMBER + ")", match[3])
                    variables[match[1]] = {"value": gaussian_float(match[2]), "specification": match[3].strip()}
                    if scan:
                        variables[match[1]]["scan"] = {"steps": int(scan[1]), "increment": gaussian_float(scan[2])}
            else:
                parts = line.replace(",", " ").split()
                if parts:
                    atom = {"atom": parts[0], "coordinates": parts[1:]}
                    if len(parts) == 4 and all(re.fullmatch(NUMBER, v) for v in parts[1:]):
                        atom["coordinates"] = gaussian_numbers(" ".join(parts[1:]))
                    else:
                        atom["references"] = []
                        for offset, kind in zip((1, 3, 5), ("distance", "angle", "dihedral")):
                            if len(parts) > offset + 1 and parts[offset].isdigit():
                                value = parts[offset + 1]
                                atom["references"].append({"center": int(parts[offset]), "kind": kind,
                                                           "value": gaussian_float(value) if re.fullmatch(NUMBER, value) else value})
                    atoms.append(atom)
        record = {"atoms": atoms, "variables": variables, "units": {"coordinates": "angstrom", "distance": "angstrom", "angle": "degree", "dihedral": "degree"}}
        if charge:
            record.update(charge=int(charge[1]), multiplicity=int(charge[2]))
        records.append(record)
    return records


def parse_header_cartesians(block):
    record = parse_input_geometry([block])[0]
    return tuple(a["atom"] for a in record["atoms"]), np.array([a["coordinates"] for a in record["atoms"]])


def parse_scf_geometry_energies(blocks):
    geometries = [parse_geometry_records([b])[0] for b in blocks]
    labels = [np.column_stack((r["centers"], r["atomic_numbers"], r["atomic_types"])) for r in geometries]
    coords = [r["coordinates"] for r in geometries]
    return {"coords": (labels, coords), "energies": np.array([parse_energy_records([b])[0]["energy"] for b in blocks])}


def parse_charges(blocks):
    records = []
    for block in blocks:
        rows = re.findall(r"^\s*(\d+)\s+([A-Za-z]+)\s+(" + NUMBER + r")(?:\s+(" + NUMBER + r"))?\s*$", block, FLAGS)
        if not rows:
            raise ValueError("charge table contains no atoms")
        record = {"centers": np.array([int(r[0]) for r in rows]), "symbols": tuple(r[1] for r in rows),
                  "charges": np.array([gaussian_float(r[2]) for r in rows]), "units": "electron"}
        if all(r[3] for r in rows):
            record["spin_densities"] = np.array([gaussian_float(r[3]) for r in rows])
        total = re.search(r"Sum of .*?charges\s*=\s*(" + NUMBER + ")", block)
        if total:
            record["total"] = gaussian_float(total[1])
        records.append(record)
    return records


def parse_multipoles(blocks):
    records = []
    for block in blocks:
        record = {}
        parts = list(re.finditer(r"^\s*((?:Traceless )?[A-Za-z]+ moment)\s*\(([^\n]*)\):", block, FLAGS))
        for i, match in enumerate(parts):
            end = parts[i + 1].start() if i + 1 < len(parts) else len(block)
            values = {name: gaussian_float(value) for name, value in re.findall(r"\b([XYZ]{1,4}|Tot)\s*=\s*(" + NUMBER + ")", block[match.end():end])}
            record[match[1]] = {"components": values, "units": match[2].rsplit(",", 1)[-1].strip()}
        records.append(record)
    return records


def parse_orbital_energies(blocks):
    records = []
    for block in blocks:
        record = {"units": "hartree"}
        for spin, occupation, values in re.findall(r"(Alpha|Beta)\s+(occ\.|virt\.) eigenvalues\s*--([^\n]*)", block):
            channel = record.setdefault(spin.lower(), {"occupied": [], "virtual": []})
            channel["occupied" if occupation == "occ." else "virtual"].extend(gaussian_numbers(values))
        for spin in ("alpha", "beta"):
            if spin in record:
                record[spin] = {key: np.asarray(values) for key, values in record[spin].items()}
        records.append(record)
    return records


def parse_forces(blocks):
    records = []
    for block in blocks:
        rows = re.findall(r"^\s*(\d+)\s+(\d+)\s+(" + NUMBER + r")\s+(" + NUMBER + r")\s+(" + NUMBER + r")\s*$", block, FLAGS)
        records.append({"centers": np.array([int(r[0]) for r in rows]), "atomic_numbers": np.array([int(r[1]) for r in rows]),
                        "forces": np.array([[gaussian_float(v) for v in r[2:]] for r in rows]), "units": "hartree/bohr"})
    return records


def parse_optimization_convergence(blocks):
    records = []
    for block in blocks:
        rows = re.findall(r"(Maximum Force|RMS\s+Force|Maximum Displacement|RMS\s+Displacement)\s+(" + NUMBER + r")\s+(" + NUMBER + r")\s+(YES|NO)", block)
        records.append({re.sub(r"\s+", " ", name): {"value": gaussian_float(value), "threshold": gaussian_float(threshold),
                                                   "converged": flag == "YES"} for name, value, threshold, flag in rows})
    return records


def parse_optimization_parameters(blocks):
    records = []
    for block in blocks:
        rows = re.findall(r"!\s*(\w+)\s+([RADLXYZ][^\s!]*)\s+(" + NUMBER + r")([^\n!]*)!", block)
        records.append({"kind": "optimized" if "Optimized Parameters" in block else "initial",
                        "parameters": {name: {"definition": definition, "value": gaussian_float(value),
                                               "derivative_info": info.strip()} for name, definition, value, info in rows}})
    return records


def parse_vibrational_modes(blocks):
    """Keep mode order, atom order, and every printed Raman/IR property."""
    records = []
    names = {"Frequencies": "frequencies", "Red. masses": "reduced_masses", "Frc consts": "force_constants",
             "IR Inten": "ir_intensities", "Raman Activ": "raman_activities", "Depolar (P)": "depolarization_p",
             "Depolar (U)": "depolarization_u", "Rot. str.": "rotatory_strengths"}
    for block in blocks:
        record = {key: [] for key in names.values()}
        labels, symmetries, displacements, atomic_numbers = [], [], [], None
        lines = block.splitlines()
        for i, line in enumerate(lines):
            if not re.match(r"\s*Frequencies\s*--", line):
                continue
            values = gaussian_numbers(line.split("--", 1)[1])
            count = len(values)
            if i >= 2 and re.fullmatch(r"\s*(?:\d+\s*)+", lines[i - 2]):
                labels.extend(int(v) for v in lines[i - 2].split())
                symmetries.extend(lines[i - 1].split())
            else:
                labels.extend(range(len(labels) + 1, len(labels) + count + 1))
                symmetries.extend([None] * count)
            record["frequencies"].extend(values)
            j = i + 1
            while j < len(lines) and "Atom" not in lines[j]:
                if "--" in lines[j]:
                    name, vals = lines[j].split("--", 1)
                    key = names.get(name.strip())
                    if key:
                        record[key].extend(gaussian_numbers(vals))
                j += 1
            rows, numbers = [], []
            for line in lines[j + 1:]:
                match = re.match(r"^\s*\d+\s+(\d+)\s+(.+)$", line)
                if not match or not re.search(FLOAT, match[2]):
                    break
                vals = gaussian_numbers(match[2])
                if len(vals) != 3 * count:
                    raise ValueError("normal mode displacement row has incorrect width")
                numbers.append(int(match[1]))
                rows.append(vals.reshape(count, 3))
            if rows:
                if atomic_numbers is not None and not np.array_equal(atomic_numbers, numbers):
                    raise ValueError("normal mode atom order changes within a table")
                atomic_numbers = np.array(numbers)
                displacements.append(np.moveaxis(np.array(rows), 1, 0))
        if not record["frequencies"]:
            raise ValueError("harmonic frequency table contains no modes")
        record = {key: np.array(value) for key, value in record.items() if len(value)}
        record.update(labels=np.array(labels), symmetries=tuple(symmetries), atomic_numbers=atomic_numbers,
                      displacements=np.concatenate(displacements, axis=0) if displacements else None,
                      units={"frequencies": "cm^-1", "reduced_masses": "amu", "force_constants": "mDyne/angstrom",
                             "ir_intensities": "km/mol", "raman_activities": "angstrom^4/amu"})
        records.append(record)
    return records


def parse_thermochemistry(blocks):
    records = []
    for block in blocks:
        record = {"corrections": {}, "energies": {}, "contributions": {}, "partition_functions": {}}
        temp = re.search(r"Temperature\s+(" + NUMBER + r") Kelvin\.\s+Pressure\s+(" + NUMBER + r") Atm", block)
        if temp:
            record.update(temperature=gaussian_float(temp[1]), pressure=gaussian_float(temp[2]))
        for label, value in re.findall(r"^\s*(Zero-point correction|Thermal correction to [^=\n]+|Sum of electronic and [^=\n]+)=\s*(" + NUMBER + ")", block, FLAGS):
            target = record["energies"] if label.startswith("Sum") else record["corrections"]
            target[label.strip()] = gaussian_float(value)
        masses = re.findall(r"Atom\s+(\d+) has atomic number\s+(\d+) and mass\s+(" + NUMBER + ")", block)
        record["atomic_masses"] = [{"center": int(i), "atomic_number": int(z), "mass": gaussian_float(m)} for i, z, m in masses]
        for label, key in [("Molecular mass:", "molecular_mass"), ("Rotational symmetry number", "rotational_symmetry_number")]:
            match = re.search(re.escape(label) + r"\s*(" + NUMBER + ")", block)
            if match:
                record[key] = gaussian_float(match[1])
        for name, a, b, c in re.findall(r"^\s*(Total|Electronic|Translational|Rotational|Vibrational)\s+(" + NUMBER + r")\s+(" + NUMBER + r")\s+(" + NUMBER + r")\s*$", block, FLAGS):
            # The second occurrence of Electronic etc. belongs to the Q table.
            target = record["contributions"] if name not in record["contributions"] else record["partition_functions"]
            keys = ("energy", "heat_capacity", "entropy") if target is record["contributions"] else ("Q", "log10_Q", "ln_Q")
            target[name] = dict(zip(keys, map(gaussian_float, (a, b, c))))
        for name, a, b, c in re.findall(r"^\s*(Total Bot|Total V=0|Vib \(Bot\)|Vib \(V=0\))\s+(" + NUMBER + r")\s+(" + NUMBER + r")\s+(" + NUMBER + r")\s*$", block, FLAGS):
            record["partition_functions"][name] = dict(zip(("Q", "log10_Q", "ln_Q"), map(gaussian_float, (a, b, c))))
        record["units"] = {"temperature": "K", "pressure": "atm", "corrections": "hartree", "energies": "hartree",
                           "atomic_masses": "amu", "energy": "kcal/mol", "heat_capacity": "cal/(mol K)", "entropy": "cal/(mol K)"}
        records.append(record)
    return records


def parse_excited_state_records(blocks):
    records = []
    for block in blocks:
        match = re.search(r"Excited State\s+(\d+):\s*(.*?)\s+(" + NUMBER + r") eV\s+(" + NUMBER + r") nm\s+f\s*=\s*(" + NUMBER + ")", block)
        if not match:
            raise ValueError("malformed excited state heading")
        record = {"State": int(match[1]), "Symmetry": match[2], "Energy": gaussian_float(match[3]),
                  "Wavelength": gaussian_float(match[4]), "OscillatorStrength": gaussian_float(match[5]),
                  "Transitions": {}, "transition_records": [], "units": {"Energy": "eV", "Wavelength": "nm"}}
        spin = re.search(r"<S\*\*2>\s*=\s*(" + NUMBER + ")", block)
        if spin:
            record["Overlap"] = record["SpinSquared"] = gaussian_float(spin[1])
        for start, ss, direction, end, es, amplitude in re.findall(r"(\d+)([AB]?)\s*(->|<-)\s*(\d+)([AB]?)\s+(" + NUMBER + ")", block):
            record["Transitions"][(int(start), int(end))] = gaussian_float(amplitude)
            record["transition_records"].append({"from": int(start), "to": int(end), "from_spin": ss or None,
                                                 "to_spin": es or None, "direction": direction, "amplitude": gaussian_float(amplitude)})
        total = re.search(r"Total Energy,.*?=\s*(" + NUMBER + ")", block)
        if total:
            record["TotalEnergy"] = gaussian_float(total[1])
        record["selected"] = "This state for optimization" in block
        records.append(record)
    return records


def parse_transition_tables(blocks):
    records = []
    for block in blocks:
        lines = block.strip().splitlines()
        header = next((line.strip() for line in lines if line.strip().startswith("state")), "")
        labels = re.findall(r"Dip\. S\.|Osc\.\([^)]*\)|Osc\.|R\([^)]*\)|E-M Angle|XX|YY|ZZ|XY|XZ|YZ|X|Y|Z", header)
        rows = []
        for line in lines:
            match = re.match(r"^\s*(\d+)\s+(.+)$", line)
            if match:
                vals = gaussian_numbers(match[2])
                if len(vals) == len(labels):
                    rows.append({"state": int(match[1]), **dict(zip(labels, vals))})
        records.append({"heading": lines[0].strip(), "columns": tuple(labels), "rows": rows})
    return records


def parse_spectroscopy_tables(blocks):
    records = []
    for block in blocks:
        lines = block.strip().splitlines()
        header = next((l.strip() for l in lines if re.search(r"Mode\((?:Quanta|n)\)", l)), "")
        columns = re.sub(r"Mode\((?:Quanta|n)\)|Status", "", header).split()
        rows = []
        for line in lines:
            quanta = re.findall(r"(\d+)\((\d+)\)", line)
            if not quanta:
                continue
            tail = re.sub(r"\d+\(\d+\)", "", line)
            vals = gaussian_numbers(tail)
            if len(vals) != len(columns):
                raise ValueError("spectroscopy table has {} columns but {} values".format(len(columns), len(vals)))
            rows.append({"quanta": tuple((int(m), int(q)) for m, q in quanta), "values": dict(zip(columns, vals)),
                         "annotations": re.sub(NUMBER, "", tail).strip() or None})
        records.append({"heading": lines[0].strip(), "columns": tuple(columns), "rows": rows,
                        "units": {c: "cm^-1" if c.startswith("E(") else "km/mol" if c.startswith("I(") else None for c in columns}})
    return records


def parse_anharmonic_thermochemistry(blocks):
    records = []
    for block in blocks:
        match = re.search(r"(?:T\s*=|T\(K\) and P\(atm\):)\s*(" + NUMBER + r")(?:\s*K;\s*P\s*=)?\s+(" + NUMBER + ")", block)
        record = {"properties": {}}
        if match:
            record.update(temperature=gaussian_float(match[1]), pressure=gaussian_float(match[2]))
        for name, harmonic, anharmonic, units in re.findall(r"^\s*(Qvib|QZvib|Energy|Enthalpy|Entropy|Sp\.Heat\([VP]\))\s+(" + NUMBER + r")\s+(" + NUMBER + r")([^\n]*)", block, FLAGS):
            record["properties"][name] = {"harmonic": gaussian_float(harmonic), "anharmonic": gaussian_float(anharmonic), "units": units.strip() or None}
        records.append(record)
    return records


def parse_force_constant_tables(blocks, order):
    records = []
    for block in blocks:
        indices, reduced, mdyn, atomic, annotations = [], [], [], [], []
        for line in block.splitlines():
            parts = line.split(None, order)
            if len(parts) <= order or not all(v.isdigit() for v in parts[:order]):
                continue
            vals = re.match(r"\s*(" + NUMBER + r")\s+(" + NUMBER + r")\s+(" + NUMBER + r")(.*)$", parts[order])
            if vals:
                indices.append([int(v) for v in parts[:order]])
                reduced.append(gaussian_float(vals[1])); mdyn.append(gaussian_float(vals[2])); atomic.append(gaussian_float(vals[3]))
                annotations.append(vals[4].strip())
        records.append({"indices": np.array(indices, dtype=int).reshape(-1, order), "reduced": np.array(reduced),
                        "attojoule": np.array(mdyn), "hartree": np.array(atomic), "annotations": tuple(annotations),
                        "order": order, "index_base": 1})
    return records


def parse_printed_matrix(block, symmetric=True):
    """Parse column panels; unprinted entries are NaN, never invented zeros."""
    columns, entries, row_labels = [], {}, {}
    for line in block.splitlines():
        if re.fullmatch(r"\s*(?:\d+\s*)+", line):
            columns = [int(v) for v in line.split()]
            continue
        match = re.match(r"^\s*(\d+)\s+(.*)$", line)
        if not match or not columns:
            continue
        tail = match[2]
        first = re.search(FLOAT, tail)
        if not first:
            continue
        label = tail[:first.start()].strip()
        values = [gaussian_float(v) for v in re.findall(FLOAT, tail[first.start():])]
        if len(values) > len(columns):
            raise ValueError("matrix row has more entries than its column panel")
        row = int(match[1])
        if label:
            row_labels[row] = label
        for col, value in zip(columns, values):
            entries[row, col] = value
            if symmetric:
                entries[col, row] = value
    if not entries:
        raise ValueError("matrix block contains no numeric rows")
    nrows = max(r for r, c in entries)
    ncols = max(c for r, c in entries)
    result = np.full((nrows, ncols), np.nan)
    for (row, col), value in entries.items():
        result[row - 1, col - 1] = value
    return result, row_labels


def parse_ao_coefficients(blocks):
    records = []
    for block in blocks:
        matrix, labels = parse_printed_matrix(block, symmetric=False)
        columns, eigenvalues, occupations = [], {}, {}
        for line in block.splitlines():
            if re.fullmatch(r"\s*(?:\d+\s*)+", line):
                columns = [int(v) for v in line.split()]
            elif "Eigenvalues --" in line:
                eigenvalues.update(zip(columns, gaussian_numbers(line.split("--", 1)[1])))
            elif columns and re.fullmatch(r"\s*(?:[OV]\s*)+", line):
                occupations.update(zip(columns, line.split()))
            elif columns and re.search(r"--[OV]", line):
                occupations.update(zip(columns, re.findall(r"--([OV])", line)))
        spin = "beta" if block.lstrip().startswith("Beta") else "alpha" if block.lstrip().startswith("Alpha") else "restricted"
        basis_functions, center, symbol = [], None, None
        for index, label in sorted(labels.items()):
            match = re.match(r"(\d+)\s+([A-Za-z]+)\s+(.*)", label)
            if match:
                center, symbol, label = int(match[1]), match[2], match[3]
            basis_functions.append({"index": index, "center": center, "symbol": symbol, "label": label})
        records.append({"spin": spin, "coefficients": matrix, "ao_labels": labels,
                        "basis_functions": basis_functions,
                        "orbital_indices": np.arange(1, matrix.shape[1] + 1),
                        "eigenvalues": np.array([eigenvalues.get(i, np.nan) for i in range(1, matrix.shape[1] + 1)]),
                        "occupations": tuple(occupations.get(i) for i in range(1, matrix.shape[1] + 1))})
    return records


def parse_matrix_records(blocks):
    return [{"heading": b.strip().splitlines()[0], "matrix": parse_printed_matrix(b)[0]} for b in blocks]


def parse_coriolis_couplings(blocks):
    records = []
    for block in blocks:
        matrix = parse_printed_matrix(block, symmetric=False)[0]
        if matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Coriolis matrix is not square")
        i, j = np.tril_indices(matrix.shape[0], -1)
        matrix[j, i] = -matrix[i, j]
        records.append({"axis": re.search(r"along the ([XYZ]) axis", block)[1], "matrix": matrix})
    return records


def parse_coriolis_terms(block):
    rows = re.findall(r"^\s*([xyz])\s+(\d+)\s+(\d+)\s+(" + NUMBER + r")\s*$", block, FLAGS)
    return np.array([["xyz".index(axis), int(i), int(j), gaussian_float(value)]
                     for axis, i, j, value in rows]).reshape(-1, 4)


def parse_numeric_tables(blocks):
    """Named numeric tables with explicit columns and integer mode labels."""
    records = []
    for block in blocks:
        lines = block.strip().splitlines()
        rows = [gaussian_numbers(line) for line in lines if re.match(r"^\s*(?:\d+\s+|(?:TauP|DELTA|delta)\s+)", line)
                and re.search(FLOAT, line)]
        records.append({"heading": lines[0].strip(), "column_header": next((l.strip() for l in lines[1:] if not re.fullmatch(r"\s*-+\s*", l)), ""),
                        "rows": np.array(rows) if rows else np.empty((0, 0))})
    return records


def parse_nmr_shieldings(blocks):
    records = []
    for block in blocks:
        match = re.search(r"(\d+)\s+([A-Za-z]+)\s+Isotropic\s*=\s*(" + NUMBER + r")\s+Anisotropy\s*=\s*(" + NUMBER + ")", block)
        tensor = {label: gaussian_float(value) for label, value in re.findall(r"\b([XYZ]{2})\s*=\s*(" + NUMBER + ")", block)}
        records.append({"center": int(match[1]), "symbol": match[2], "isotropic": gaussian_float(match[3]),
                        "anisotropy": gaussian_float(match[4]), "tensor": tensor, "units": "ppm"})
    return records


def parse_irc_points(blocks):
    records = []
    for block in blocks:
        point = re.search(r"Point Number\s*[:=]?\s*(\d+)\s*(?:in\s+)?Path Number\s*[:=]?\s*(\d+)", block, re.I)
        record = {"point": int(point[1]), "path": int(point[2])}
        for label, value in re.findall(r"(NET REACTION COORDINATE UP TO THIS POINT|Energy)\s*[:=]\s*(" + NUMBER + ")", block, re.I):
            record[label.lower()] = gaussian_float(value)
        records.append(record)
    return records


def parse_vibrational_averages(blocks):
    records = []
    for block in blocks:
        heading = re.search(r"(?:Property at reference geometry|Temperature:)[^\n]*", block)
        units = re.search(r"Unit:\s*([^\n]*)", block)
        temperature = re.search(r"Temperature:\s*(" + NUMBER + r")K", block)
        record = {"heading": heading[0].strip() if heading else "", "units": units[1].strip() if units else None,
                  "components": {k: gaussian_float(v) for k, v in re.findall(r"\b([XYZ]{1,4})\s*=\s*(" + NUMBER + ")", block)}}
        if temperature:
            record["temperature"] = gaussian_float(temperature[1])
        records.append(record)
    return records


def parse_zero_point_energies(blocks):
    records = []
    for block in blocks:
        values = {}
        for kind, value, units in re.findall(r"ZPE\((harm|anh)\)\s*=\s*(" + NUMBER + r")\s+([^\s]+)", block):
            values[kind] = {units: gaussian_float(value)}
        for name, line in re.findall(r"^\s*([^:\n]+):\s*(cm-1[^\n]*)", block, FLAGS):
            values[name.strip()] = {units: gaussian_float(value) for units, value in re.findall(r"(cm-1|Kcal/mol|KJ/mol)\s*=\s*(" + NUMBER + ")", line)}
        records.append({"values": values})
    return records


def parse_basis_expansions(blocks):
    records = []
    for block in blocks:
        center, shells, primitives = None, [], None
        for line in block.splitlines():
            match = re.fullmatch(r"\s*(\d+)\s+0\s*", line)
            if match:
                center = int(match[1])
            match = re.fullmatch(r"\s*([SPDFGHI]+)\s+(\d+)\s+(" + NUMBER + r")(?:\s+" + NUMBER + r")*\s*", line)
            if match:
                primitives = []
                shells.append({"center": center, "shell": match[1], "count": int(match[2]), "scale": gaussian_float(match[3]), "primitives": primitives})
            elif primitives is not None and re.match(r"\s*" + FLOAT, line):
                primitives.append(gaussian_numbers(line))
        for shell in shells:
            shell["primitives"] = np.array(shell["primitives"])
            if len(shell["primitives"]) != shell["count"]:
                raise ValueError("incomplete basis shell")
        records.append({"shells": shells})
    return records


def parse_scalar_rows(blocks):
    records = []
    for block in blocks:
        heading = block.strip().splitlines()[0]
        values = gaussian_numbers(block.split(":", 1)[-1])
        record = {"heading": heading, "values": values}
        if "Rotational constants" in heading:
            record.update(constants=values, units="GHz")
        elif "polarizability:" in heading:
            record.update(components=values, units="atomic_units")
        elif "spatial extent" in heading:
            record.update(mean_square_radius=gaussian_float(block.split("=", 1)[1]), units="bohr^2")
            record["values"] = np.array([record["mean_square_radius"]])
        records.append(record)
    return records


def parse_optimized_scan(block):
    energies, coords, columns = [], {}, []
    shift = re.search(r"\badd\s+(" + NUMBER + ")", block)
    shift = gaussian_float(shift[1]) if shift else 0.0
    for line in block.splitlines():
        if re.fullmatch(r"\s*(?:\d+\s*)+", line):
            columns = [int(v) for v in line.split()]
        elif "Eigenvalues --" in line:
            values = gaussian_numbers(line.split("--", 1)[1])
            if columns and len(values) != len(columns):
                raise ValueError("scan energy panel has an incorrect width")
            energies.extend(values + shift)
        else:
            match = re.match(r"^\s*(\w+)\s+(.+)$", line)
            if match and re.match(FLOAT, match[2]):
                vals = gaussian_numbers(match[2])
                if columns and len(vals) == len(columns):
                    coords.setdefault(match[1], []).extend(vals)
    return namedtuple("OptimizedScanEnergies", ["energies", "coords"])(
        np.array(energies), {key: np.array(values) for key, values in coords.items()})


def parse_scan(block):
    header = re.search(r"^\s*(N|Point|No\.)\s+([^\n]+)", block, FLAGS)
    if header is None:
        raise ValueError("scan summary is missing its column headings")
    labels = (header[1],) + tuple(header[2].split())
    rows = []
    for line in block[header.end():].splitlines():
        if re.match(r"^\s*\d+\s+", line):
            vals = gaussian_numbers(line)
            if len(vals) == len(labels):
                rows.append(vals)
    return namedtuple("ScanEnergies", ["coords", "energies"])(np.array(labels), np.array(rows))


def register_gaussian_components(components):
    def register(name, pattern, parser, mode="List", large=False, default=True, **kwargs):
        components[name] = {"block_pattern": re.compile(pattern, FLAGS), "parser": parser, "mode": mode,
                            "large": large, "default": default, **kwargs}

    # The full-text components only compute metadata. Large numeric fields are
    # never converted by discovery, even if their headings are present.
    register("JobTypes", r"\A[\s\S]*\Z", parse_job_types, "Single")
    register("Jobs", r"\A[\s\S]*\Z", gaussian_job_metadata, "Single")
    register("JobStatus", r"\A[\s\S]*\Z", parse_job_status, "Single")
    register("RunInfo", r"^[ \t]*(?:Gaussian\s+\d+:|Initial command:|Entering Gaussian System)[^\n]*", parse_run_info)
    archive = r"^[ \t]*\d+\\\d+\\GINC-[\s\S]*?\\[ \t\n\\]*@"
    register("ArchiveSummary", archive, parse_archive_summary)
    register("Header", r"\A[\s\S]*?(?:^[ \t]*#[^\n]*\n(?:[^\n]*\n)*?^[ \t]*-{5,}[^\n]*$|\Z)", gaussian_header_parser, "Single")
    register("Timing", r"^.*(?:Job cpu time|Elapsed time):[^\n]*", parse_timing)
    register("MoleculeInfo", r"^.*(?:Charge\s*=\s*-?\d+\s+Multiplicity\s*=\s*\d+|NAtoms\s*=)[^\n]*", parse_molecule_info)
    register("BasisInfo", r"^.*(?:Standard basis:|\d+ basis functions,|NBasis\s*=|\d+ alpha electrons)[^\n]*", parse_basis_info)
    register("ElectronicEnergies", r"^.*(?:SCF Done:|EUMP[234]|E\(CORR\)|E\(CCSD\)|E\(QCISD\)|CCSD\(T\)\s*=|QCISD\(T\)\s*=|Total Energy, E\(TD-HF/TD-DFT\)|ONIOM: extrapolated energy)[^\n]*", parse_energy_records)
    register("Geometries", r"^.*(?:Standard|Input|Z-Matrix) orientation:[^\n]*\n[\s\S]*?Coordinates \(Angstroms\)[^\n]*\n[^\n]*\n[^\n]*\n(?:\s*\d+\s+-?\d+\s+-?\d+[^\n]*\n)+", parse_geometry_records)
    register("InputGeometry", r"^[ \t]*Symbolic Z-matrix:[^\n]*\n[\s\S]*?(?=\n[ \t]*\n|\Z)", parse_input_geometry)
    register("HeaderCartesianCoordinates", r"^[ \t]*Symbolic Z-matrix:[^\n]*\n[ \t]*Charge[^\n]*\n(?:[ \t]*[A-Za-z]+\s+" + FLOAT + r"\s+" + FLOAT + r"\s+" + FLOAT + r"[ \t]*\n)+", parse_header_cartesians, "Single", default=False)
    register("SCFCoordinatesEnergies", r"^[ \t]*Standard orientation:[^\n]*\n(?:(?!^[ \t]*Standard orientation:)[\s\S])*?^[ \t]*SCF Done:[^\n]*", parse_scf_geometry_energies, default=False)
    register("OptimizedScanEnergies", r"^[ \t]*Summary of Optimized Potential Surface Scan[^\n]*\n[\s\S]*?(?=^[ \t]*(?:Largest change|Normal termination|GradGrad|\d+\\\d+\\GINC|Job cpu time)|^[ \t]*-{25,}|\Z)", parse_optimized_scan, "Single")
    register("ScanEnergies", r"^[ \t]*Summary of the potential surface scan:[\s\S]*?(?=^[ \t]*(?:Normal termination|Job cpu time|\d+\\\d+\\GINC)|\Z)", parse_scan, "Single")
    for name, heading in [("MullikenCharges", r"Mulliken charges(?: and spin densities)?"), ("APTCharges", "APT charges"), ("NaturalCharges", "Natural charges")]:
        register(name, r"^[ \t]*" + heading + r":[^\n]*\n[\s\S]*?Sum of [^\n]*charges[^\n]*", parse_charges)
    register("MultipoleMoments", r"^[ \t]*Dipole moment \([^\n]*\n(?:[ \t]*(?:[XYZ]|Tot)[^\n]*\n|[^\n]*moment \([^\n]*\n)+", parse_multipoles)
    register("OrbitalEnergies", r"^[ \t]*(?:Alpha|Beta)\s+(?:occ\.|virt\.) eigenvalues[^\n]*(?:\n[ \t]*(?:Alpha|Beta)\s+(?:occ\.|virt\.) eigenvalues[^\n]*)*", parse_orbital_energies)
    register("Forces", r"^[ \t]*Center\s+Atomic\s+Forces[^\n]*\n[^\n]*\n[^\n]*\n(?:[ \t]*\d+\s+\d+[^\n]*\n)+", parse_forces)
    register("OptimizationConvergence", r"^[ \t]*Item\s+Value\s+Threshold\s+Converged\?[^\n]*\n(?:[^\n]*(?:YES|NO)[ \t]*\n)+", parse_optimization_convergence)
    register("OptimizationParameters", r"^[^\n]*!\s*(?:Initial|Optimized) Parameters[^\n]*\n(?:[^\n]*\n)*?^[ \t]*! Name[^\n]*\n[^\n]*\n(?:[ \t]*![^\n]*\n)+", parse_optimization_parameters)
    modes = r"^[ \t]*Harmonic frequencies \(cm\*\*-1\)[\s\S]*?(?=\n[ \t]*\n|\Z)"
    register("VibrationalModes", modes, parse_vibrational_modes)
    # Preserve the tuple API of NormalModes while fixing displacement ordering
    # and accepting Raman rows and Fortran exponent notation.
    def legacy_modes(blocks):
        return [(r["frequencies"], r["reduced_masses"],
                 r["displacements"].reshape(len(r["frequencies"]), -1).T)
                for r in parse_vibrational_modes(blocks)]
    register("NormalModes", modes, legacy_modes, default=False)
    register("Thermochemistry", r"^[ \t]*- Thermochemistry -[^\n]*\n[\s\S]*?(?=^[ \t]*\*{5}|^[ \t]*-{5,}[ \t]*\n[ \t]*Center|\Z)", parse_thermochemistry)
    register("ExcitedStates", r"^[ \t]*Excited State\s+\d+:[^\n]*(?:\n(?![ \t]*(?:Excited State\s+\d+:|SavETr:|\*{5}))[^\n]*)*", parse_excited_state_records)
    register("TransitionMoments", r"^[ \t]*Ground to excited state transition (?:electric dipole|velocity dipole|magnetic dipole|velocity quadrupole) moments[^\n]*\n[^\n]*\n(?:[ \t]*\d+[^\n]*\n)+", parse_transition_tables)
    register("RotatoryStrengths", r"^[ \t]*Rotatory Strengths[^\n]*\n[^\n]*\n(?:[ \t]*\d+[^\n]*\n)+", parse_transition_tables)
    register("AnharmonicSpectra", r"^[ \t]*(?:Electric dipole : )?(?:Fundamental Bands|Overtones|Combination Bands)[^\n]*\n(?:[ \t]*-+[^\n]*\n)?[ \t]*Mode\((?:Quanta|n)\)[^\n]*\n(?:[^\n]*\d+\(\d+\)[^\n]*\n)+", parse_spectroscopy_tables)
    register("AnharmonicThermochemistry", r"^[ \t]*(?:Input values of T\(K\) and P\(atm\):|T\s*=)[^\n]*\n[ \t]*Harmonic value[^\n]*\n(?:[^\n]+\n)+", parse_anharmonic_thermochemistry)
    for name, order in [("QuadraticForceConstants", 2), ("CubicForceConstants", 3), ("QuarticForceConstants", 4)]:
        labels = ",".join("IJKL"[:order])
        register(name, r"^[ \t]*I\s+J[^\n]*K\(" + re.escape(labels) + r"\)[^\n]*\n[\s\S]*?(?=\n[ \t]*\n[^\n]*derivatives|\Z)",
                 lambda blocks, order=order: parse_force_constant_tables(blocks, order), large=order > 2)
    register("CoriolisCouplings", r"^[ \t]*Coriolis Couplings along the [XYZ] axis[^\n]*\n[\s\S]*?(?=\n[ \t]*\n|\Z)", parse_coriolis_couplings)
    register("CoriolisTerms", r"^[ \t]*Ax\s+I\s+J\s+Zeta\(I,J\)[^\n]*\n[\s\S]*?(?=^[^\n]*Coriolis [Cc]ouplings larger|\Z)", parse_coriolis_terms, "Single", default=False)
    for name, order in [("QuadraticTerms", 2), ("CubicTerms", 3), ("QuarticTerms", 4)]:
        source = components[{2: "QuadraticForceConstants", 3: "CubicForceConstants", 4: "QuarticForceConstants"}[order]]
        def legacy_constants(block, order=order):
            record = parse_force_constant_tables([block], order)[0]
            return np.column_stack((record["indices"], record["reduced"]))
        components[name] = dict(source, mode="Single", parser=legacy_constants, default=False)
    register("AnharmonicResonances", r"^[ \t]*(?:Fermi resonances|[12]-[12] Darling-Dennison resonances)[ \t]*\n[ \t]*-+[^\n]*\n[\s\S]*?(?=\n[ \t]*\n|\Z)", parse_numeric_tables)
    register("CentrifugalDistortion", r"^[ \t]*(?:Quartic Centrifugal Distortion Constants Tau Prime|Constants in the Asymmetrically reduced Hamiltonian)[^\n]*\n[\s\S]*?(?=\n[ \t]*\n|\Z)", parse_numeric_tables)
    register("VibrationalAverages", r"^[ \t]*(?:Property at reference geometry, Unit:|Temperature:\s*\d+K, Unit:)[^\n]*\n[ \t]*-+[^\n]*\n(?:[ \t]*[XYZ][^\n]*\n)+", parse_vibrational_averages)
    register("NMRShieldings", r"^[ \t]*\d+\s+[A-Za-z]+\s+Isotropic\s*=[^\n]*\n(?:[ \t]*[XYZ]{2}\s*=[^\n]*\n)+", parse_nmr_shieldings)
    register("SpinSpinCouplings", r"^[ \t]*Total nuclear spin-spin coupling J[^\n]*\n[\s\S]*?(?=\n[ \t]*\n|\Z)", parse_matrix_records)
    register("IRCPoints", r"^[^\n]*Point Number\s*[:=]?\s*\d+\s*(?:in\s+)?Path Number\s*[:=]?\s*\d+[^\n]*\n[\s\S]*?(?=^[^\n]*Point Number|^[^\n]*Normal termination|\Z)", parse_irc_points)
    register("IRCSummary", r"^[ \t]*Summary of reaction path following[^\n]*\n[\s\S]*?(?=\n[ \t]*\n|\Z)", parse_numeric_tables)
    register("AnharmonicZeroPointEnergy", r"^[ \t]*(?:ZPE\(harm\)\s*=|Anharmonic Zero Point Energy)[^\n]*(?:\n(?![ \t]*$)[^\n]*)*", parse_zero_point_energies)
    register("AOCoefficients", r"^[ \t]*(?:(?:Alpha|Beta) )?Molecular Orbital Coefficients[^\n]*\n[\s\S]*?(?=^[ \t]*(?:(?:Alpha|Beta) Molecular Orbital|Density Matrix|(?:Alpha|Beta) Density Matrix|Mulliken|Condensed|Electronic spatial|[A-Za-z]+ population)|\Z)", parse_ao_coefficients, large=True)
    register("DensityMatrices", r"^[ \t]*(?:(?:Alpha|Beta|Total|Spin) )?Density Matrix[^\n]*\n[\s\S]*?(?=^[ \t]*(?:(?:Alpha|Beta|Total|Spin) Density Matrix|Mulliken|Condensed|Electronic spatial|[A-Za-z]+ population)|\Z)", parse_matrix_records, large=True)
    register("OverlapMatrices", r"^[ \t]*\*{3} Overlap \*{3}[^\n]*\n[\s\S]*?(?=^[ \t]*\*{3}|\Z)", parse_matrix_records, large=True)
    register("BasisSet", r"^[ \t]*AO basis set in the form of general basis input[^\n]*\n[\s\S]*?(?=^[ \t]*\d+ basis functions|^[ \t]*There are|\Z)", parse_basis_expansions, large=True)
    for name, heading in [("RotationalConstants", r"Rotational constants \((?:GHZ|GHz)\):"),
                          ("Polarizabilities", r"(?:Exact|Approx) polarizability:"),
                          ("SpatialExtent", r"Electronic spatial extent \(au\):")]:
        register(name, r"^[ \t]*" + heading + r"[^\n]*", parse_scalar_rows)
    # Existing specialized readers remain addressable. These duplicate the new
    # coordinate/force views or contain potentially enormous derivative payloads.
    for name in ("CartesianCoordinates", "ZMatCartesianCoordinates", "StandardCartesianCoordinates", "InputCartesianCoordinates",
                 "HeaderCartesianCoordinates", "Gradients", "SCFCoordinatesEnergies", "ZMatrices", "InputZMatrix", "Footer"):
        components[name]["default"] = False
    for name in ("Reports", "CubicDerivs", "QuarticDerivs"):
        components[name]["large"] = True
    # These legacy tags don't bound modern anharmonic tables; the new force
    # constant components above retain all three unit conventions.
    for name in ("QuadraticTerms", "CubicTerms", "QuarticTerms", "CoriolisTerms"):
        components[name]["default"] = False
