# share-pk-qss
Peak, quasi-steady state, and phase transformation values for a lot of simulations. 


## Model settings

* Critical state line: Roscoe et al. (1958) [linear]
* Operational stress ratio: Extended Dafalias [symmetric]
* Loading: Triaxial compression
* Drainage: Undrained
* Maximum rate of dilatancy:
  * `D^p_min,tc = chi_i * psi_i`
  * `chi_i ~= chi_tc / (1 - lambda * (chi_tc / M_tc))` [Approximation]
* Hardening-softening law:
  * "Bonus" softening term included when `D^p > 0`


## Material parameters

| Parameter | Value  |
|-----------|--------|
| pref [Pa] | 1.0e+5 |
| Mtc       | 1.24   |
| Gamma     | 0.910  |
| lambda    | 0.014  |
| I_r       | 150.0  |
| n_e       | 1.0    |
| n_p       | 0.0    |
| psi_0     | varies |
| nu        | varies |
| N         | varies | 
| chi_tc    | varies |
| h_ref     | varies |

```python
# Variable state parameters
psi0_l = np.random.uniform(-0.2, 0.2, total)

# Variable material parameters
nu_l = np.round(np.random.uniform(0.1, 0.35, total), 4)
N_l = np.round(np.random.uniform(0.1, 0.6, total), 4)
chitc_l = np.round(np.random.uniform(1.0, 6.0, total), 4)
href_l = np.round(np.random.uniform(5, 150, total), 4)
```

> Total test: `total=150000`


## Other notes

### File layout

| Response type       | ID |
|---------------------|----|
| Softening           | 0  |
| Quasi-steady state  | 1  |
| Monotonic hardening | 2  |

`save-0.csv`

| Col 0   | Col 1   | Col 2   |
|---------|---------|---------|
|(p/pc)_pk|(q/pc)_pk|(e*Ir)_pk|

`save-1.csv`

| Col 0   | Col 1   | Col 2   | Col 3    | Col 4    | Col 5    |
|---------|---------|---------|----------|----------|----------|
|(p/pc)_pk|(q/pc)_pk|(e*Ir)_pk|(p/pc)_qss|(q/pc)_qss|(e*Ir)_qss|

`save-2.csv`

| Col 0   | Col 1   | Col 2   |
|---------|---------|---------|
|(p/pc)_pt|(q/pc)_pt|(e*Ir)_pt|


### Definitions
![Representative stress-strain relationships for very loose, loose, medium-dense, and dense sand (undrained shearing).](figures/sand-stress-paths.png)

"Peak" (points B1, B2, or B3)
* `(p/pc)_pk` := normalized mean effective stress @ peak strength
* `(q/pc)_pk` := normalized deviatoric stress @ peak strength
* `(e*Ir)_pk` := normalized axial (or deivatoric) strain @ peak strength

"Quasi-steady state" (point C3)
* `(p/pc)_qss` := normalized mean effective stress @ quasi-steady state
* `(q/pc)_qss` := normalized deviatoric stress @ quasi-steady state
* `(e*Ir)_qss` := normalized axial (or deivatoric) strain @ quasi-steady state

"Phase transformation" (point C4)
* `(p/pc)_pt` := normalized mean effective stress @ phase transformation
* `(q/pc)_pt` := normalized deviatoric stress @ phase transformation
* `(e*Ir)_pt` := normalized axial (or deivatoric) strain @ phase transformation

> Note: Both points C3 and C4 have undergone "phase transformation". However, the subscript `_pt` is specifically used for cases where phase transformation occurs without reaching the quasi-steady state.
