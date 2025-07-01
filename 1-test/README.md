# 1-Test
One `psi_0` for each combination of the material parameters.


## Varying material parameters

```python
total=150000

# Variable state parameters
psi0_l = np.random.uniform(-0.2, 0.2, total)

# Variable material parameters
nu_l = np.round(np.random.uniform(0.1, 0.35, total), 4)
N_l = np.round(np.random.uniform(0.1, 0.6, total), 4)
chitc_l = np.round(np.random.uniform(1.0, 6.0, total), 4)
href_l = np.round(np.random.uniform(5, 150, total), 4)
```


## Other notes

### File layout

| Response type       | ID | Quantity |
|---------------------|----|----------|
| Softening           | 0  | 67,644   |
| Quasi-steady state  | 1  | 30,420   |
| Monotonic hardening | 2  | 51,936   |

`save_0.csv`

| Col 0   | Col 1   | Col 2   | Col 3   |
|---------|---------|---------|---------|
| psi_0   |(p/pc)_pk|(q/pc)_pk|(e*Ir)_pk|

`save_1.csv`

| Col 0   | Col 1   | Col 2   | Col 3   | Col 4    | Col 5    | Col 6    |
|---------|---------|---------|---------|----------|----------|----------|
| psi_0   |(p/pc)_pk|(q/pc)_pk|(e*Ir)_pk|(p/pc)_qss|(q/pc)_qss|(e*Ir)_qss|

`save_2.csv`

| Col 0   | Col 1   | Col 2   | Col 3   |
|---------|---------|---------|---------|
| psi_0   |(p/pc)_pt|(q/pc)_pt|(e*Ir)_pt|
