# Diffusion in a transition layer

This Python program simulates diffusion between two substances across an initial transition layer. It evolves their number concentrations on a one-dimensional grid using planar, cylindrical, or spherical geometry. Diffusion coefficients follow the Arrhenius relation and can be selected by the dominant local substance or averaged by local concentrations.

The supplied configuration models aluminium and copper. Simulation results are written to tab-separated (`.tsv`) files.

## Setup and launch

Use Python 3.10 or newer. Run all commands from the project root directory, which contains `main.py`.

Create and activate a virtual environment, then install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

Create your local configuration by copying the example:

```bash
cp .env.example .env
```

Edit `.env` as needed. It is excluded from Git. The program loads it automatically from the project root; process environment variables override values in this file.

Create the output directory and launch the program:

```bash
mkdir -p results
python3 main.py
```

The example sets `STOP_TIME=1e12` seconds of simulated time, which can require a very long run. For a short trial with the example time step, override it for one invocation:

```bash
STOP_TIME=0.00328 python3 main.py
```

## Command-line parameters

Arguments use the exact `-name=value` syntax, with no spaces around `=`:

```bash
python3 main.py -g=plain -dc=static
python3 main.py -g=cylindrical -dc=weighted_average
python3 main.py -g=spherical -dc=static
```

| Argument | Values | Default | Meaning |
| --- | --- | --- | --- |
| `-g` | `plain`, `cylindrical`, `spherical` | `cylindrical` | Planar, cylindrical, or spherical geometry. |
| `-dc` | `static`, `weighted_average` | `static` | Method for calculating the effective diffusion coefficient. |

`static` uses the coefficient for the locally most abundant host substance. `weighted_average` combines the host-specific coefficients in proportion to local concentrations.

Omitted or unrecognized options fall back to defaults. The script has no `--help` mode. Numeric settings and substance selection are not command-line arguments: configure them as described below.

## Configuration

All lengths use meters, times use seconds, and temperatures use kelvin.

| Setting | Meaning |
| --- | --- |
| `REFERENCE_TEMPERATURE` | Temperature at which the configured material densities are specified. It is the baseline for thermal expansion and initializes diffusion coefficients. |
| `*_DENSITY_AT_REFERENCE_TEMPERATURE` | Material density at the reference temperature, in kg/m³. |
| `*_VOLUMETRIC_THERMAL_EXPANSION` | Volumetric thermal expansion coefficient, in 1/K. |
| `*_FACTOR` | Arrhenius prefactor, in m²/s. |
| `*_ACTIVATION_ENERGY` | Activation energy, in J/mol. |
| `TEMPERATURE` | Simulation temperature, used for concentrations and diffusion coefficients. |
| `BORDER_COORDINATE` | Position of the initial interface between the substances. |
| `INNER_OFFSET`, `OUTER_OFFSET` | Extent of the initial transition layer on each side of the interface. |
| `SIZE_MULTIPLIER` | Domain length divided by `BORDER_COORDINATE`. |
| `DELTA_COORDINATE` | Spatial grid spacing. |
| `DELTA_TIME` | Simulation time step. |
| `STOP_TIME` | End of simulated time. |
| `LOG_PERIOD_STEPS` | Logging interval multiplier: logging period is `LOG_PERIOD_STEPS * DELTA_TIME`. |
| `LOG_POINTS` | Optional number of sampled grid points. Omit or comment out this setting to log every point. |
| `FILE_PREFIX` | Output path prefix, such as `results/state`. Its parent directory must already exist. |

The node count is `floor(SIZE_MULTIPLIER * BORDER_COORDINATE / DELTA_COORDINATE) + 1`. If set, `LOG_POINTS` must be an integer between 1 and this count. To use the default of all points, remove the setting rather than leaving an empty `LOG_POINTS=` value.

Atomic weights are defined directly in `parameters/substances.py` in kg/mol. All environment settings used by the selected configuration are required except `LOG_POINTS`. Choose the spatial and time steps to suit the material coefficients and numerical stability of the simulation.

## Output

Output filenames include the prefix, temperature, interface position, offsets, spatial step (`dr`), time step (`dt`), substance names, geometry, and coefficient method. Each TSV file contains:

1. A configuration header.
2. A header with the sampled spatial coordinates.
3. Rows containing simulation time, substance name, and number concentrations (atoms/m³) at those coordinates.

The initial state is always logged. Later states are logged when elapsed time since the previous record exceeds the configured logging period. Repeating a run with the same filename configuration overwrites the previous file.

## Adding and selecting substances

The current solver evolves two substances at a time. You can add material definitions and select a different pair without changing the solver.

### 1. Register the name

Add an enum member in `constants/substance_names.py`, for example:

```python
NICKEL = 'nickel'
```

### 2. Define the material

In `parameters/substances.py`, define a `Substance` alongside aluminium and copper:

```python
nickel = Substance(
    name=SubstanceName.NICKEL,
    atomic_weight=58.6934e-3,  # kg/mol
    density_at_reference_temperature=setting(
        "NICKEL_DENSITY_AT_REFERENCE_TEMPERATURE", float
    ),
    volumetric_thermal_expansion=setting(
        "NICKEL_VOLUMETRIC_THERMAL_EXPANSION", float
    ),
    reference_temperature=reference_temperature,
)
```

Add the corresponding settings to both `.env` and `.env.example`, using appropriate material data. Density must correspond to `REFERENCE_TEMPERATURE`. Newly added settings become required when their `setting(...)` calls execute during import.

### 3. Define diffusion coefficients for the selected pair

For a nickel–copper simulation, provide all four ordered combinations:

- Nickel in nickel (self-diffusion).
- Copper in copper (self-diffusion).
- Nickel in copper.
- Copper in nickel.

For each new combination, create a `DiffusionCoefficient`. Here `diffusing_substance` is the diffusing substance and `host_substance` is the host:

```python
nickel_in_copper = DiffusionCoefficient(
    diffusing_substance=SubstanceName.NICKEL,
    host_substance=SubstanceName.COPPER,
    factor=setting("NICKEL_IN_COPPER_FACTOR", float),
    activation_energy=setting("NICKEL_IN_COPPER_ACTIVATION_ENERGY", float),
    temperature=reference_temperature,
)
```

Define `nickel_self` and `copper_in_nickel` in the same way. Add their factors and activation energies to `.env` and `.env.example`, then include all coefficients needed for the selected pair in `diffusion_coefficients`:

```python
diffusion_coefficients = [
    nickel_self,
    copper_self,
    nickel_in_copper,
    copper_in_nickel,
]
```

The program recalculates these coefficients at `TEMPERATURE` before running the simulation.

### 4. Select the pair

Update the import and assignments in `parameters/values.py`:

```python
from parameters.substances import nickel, copper

inner_substance = nickel
outer_substance = copper
```

Run `python3 main.py` from the project root as usual. The selected names are included in the output filename. Reversing the inner and outer substances still requires all four coefficients for that pair.
