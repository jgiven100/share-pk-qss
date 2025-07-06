# 2-Test
Two different `psi_0` for each combination of the material parameters.


## Varying material parameters

```python
total=150000

# Variable state parameters
psi0_l = []
for i in range(2):
    psi0_l.append(np.random.uniform(-0.2, 0.2, total))

# Variable material parameters
nu_l = np.round(np.random.uniform(0.1, 0.35, total), 4)
N_l = np.round(np.random.uniform(0.1, 0.6, total), 4)
chitc_l = np.round(np.random.uniform(1.0, 6.0, total), 4)
href_l = np.round(np.random.uniform(5, 150, total), 4)
```


## Other notes

### File layout

> Order matters!

| First response type | Second response type | ID  | Quantity |
|---------------------|----------------------|-----|----------|
| Softening           | Softening            | 0 0 |          |
| Softening           | Quasi-steady state   | 0 1 |          |
| Softening           | Monotonic hardening  | 0 2 |          |
| Quasi-steady state  | Quasi-steady state   | 1 1 |          |
| Quasi-steady state  | Monotonic hardening  | 1 2 |          |
| Monotonic hardening | Monotonic hardening  | 2 2 |          |

`save_0_0.csv`

| Col 0   | Col 1   | Col 2   | Col 3   | Col 4   | Col 5   | Col 6   | Col 7   |
|---------|---------|---------|---------|---------|---------|---------|---------|
| psi_0   |(p/pc)_pk|(q/pc)_pk|(e*Ir)_pk| psi_0   |(p/pc)_pk|(q/pc)_pk|(e*Ir)_pk|

`save_0_1.csv`

| Col 0   | Col 1   | Col 2   | Col 3   | Col 4   | Col 5   | Col 6   | Col 7   | Col 8    | Col 9    | Col 10   |
|---------|---------|---------|---------|---------|---------|---------|---------|----------|----------|----------|
| psi_0   |(p/pc)_pk|(q/pc)_pk|(e*Ir)_pk| psi_0   |(p/pc)_pk|(q/pc)_pk|(e*Ir)_pk|(p/pc)_qss|(q/pc)_qss|(e*Ir)_qss|

`save_0_2.csv`

| Col 0   | Col 1   | Col 2   | Col 3   | Col 4   | Col 5   | Col 6   | Col 7   |
|---------|---------|---------|---------|---------|---------|---------|---------|
| psi_0   |(p/pc)_pk|(q/pc)_pk|(e*Ir)_pk| psi_0   |(p/pc)_pt|(q/pc)_pt|(e*Ir)_pt|

`save_1_1.csv`

| Col 0   | Col 1   | Col 2   | Col 3   | Col 4    | Col 5    | Col 6    | Col 7   | Col 8   | Col 9   | Col 10  | Col 11   | Col 12   | Col 13   |
|---------|---------|---------|---------|----------|----------|----------|---------|---------|---------|---------|----------|----------|----------|
| psi_0   |(p/pc)_pk|(q/pc)_pk|(e*Ir)_pk|(p/pc)_qss|(q/pc)_qss|(e*Ir)_qss| psi_0   |(p/pc)_pk|(q/pc)_pk|(e*Ir)_pk|(p/pc)_qss|(q/pc)_qss|(e*Ir)_qss|

`save_1_2.csv`

| Col 0   | Col 1   | Col 2   | Col 3   | Col 4    | Col 5    | Col 6    | Col 7   | Col 8   | Col 9   | Col 10  |
|---------|---------|---------|---------|----------|----------|----------|---------|---------|---------|---------|
| psi_0   |(p/pc)_pk|(q/pc)_pk|(e*Ir)_pk|(p/pc)_qss|(q/pc)_qss|(e*Ir)_qss| psi_0   |(p/pc)_pt|(q/pc)_pt|(e*Ir)_pt|

`save_2_2.csv`

| Col 0   | Col 1   | Col 2   | Col 3   | Col 4   | Col 5   | Col 6   | Col 7   |
|---------|---------|---------|---------|---------|---------|---------|---------|
| psi_0   |(p/pc)_pt|(q/pc)_pt|(e*Ir)_pt| psi_0   |(p/pc)_pt|(q/pc)_pt|(e*Ir)_pt|

### Processing

Output file saved in 4 column format:

```python
hdr = 'p q epsQ psi'
```
