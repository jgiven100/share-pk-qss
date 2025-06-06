# share-pk-qss
Peak and quasi-steady state values for a lot of simulations. 

## Model settings

* Critical state line: Roscoe et al. (1958) [linear]
* Operational stress ratio: Extended Dafalias [symmetric]
* Loading: Triaxial compression
* Drainage: Undrained
* Maximum rate of dilatancy:
  * `D^p_min,tc = chi_i * psi_i`
  * `chi_i ~= chi_tc / (1 - lambda * (chi_tc / M_tc))` [Approximation]

## Material parameters

| Parameter | Value  |
|-----------|--------|
| pref [Pa] | 1.0e+5 |
| Mtc       | 1.24   |
| Gamma     | 0.910  |
| lambda    | 0.014  |
| nu        | 0.15   |
| n_e       | 1.0    |
| n_p       | 0.0    |
| I_r       | varies |
| h_ref     | varies |
| N         | varies | 
| chi_tc    | varies |
| psi_0     | varies |

```python
I_r    = np.linspace( 50,  550, 11)
h_ref  = np.linspace( 10,  50,  9)
N      = np.linspace( 0.1, 0.6, 11)
chi_tc = np.linspace( 1.0, 6.0, 11)
psi_0  = np.linspace(-0.2, 0.2, 11)
```

## Other notes

For monotonic hardening:
* There is no distinct peak or quasi-steady state.
* `-1` is used as a placeholder for both missing peak and quasi‐steady state points.

For material softening:
* There is no quasi-steady state observed.
* `-1` is used as a placeholder for the missing quasi-steady state point.
