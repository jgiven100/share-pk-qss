# 2-Test
Two different `psi_0` for each combination of the material parameters.


## Varying material parameters

```python
total = 100000

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
| Softening           | Softening            | 0   | 16,979   |
| Softening           | Quasi-steady state   | 1   | 22,470   |
| Softening           | Monotonic hardening  | 2   | 25,750   |
| Quasi-steady state  | Quasi-steady state   | 3   | 12,436   |
| Quasi-steady state  | Monotonic hardening  | 4   | 10,199   |
| Monotonic hardening | Monotonic hardening  | 5   | 12,166   |


| ID      | 0                  | 1                  | 2                  | 3                  | 4                  | 5                  |
|---------|--------------------|--------------------|--------------------|--------------------|--------------------|--------------------|
| Col 00  | psi_0              | psi_0              | psi_0              | psi_0              | psi_0              | psi_0              |
| Col 01  | (p/pc) @ 0.5eps*   | (p/pc) @ 0.5eps*   | (p/pc) @ 0.5eps*   | (p/pc) @ PK        | (p/pc) @ PK        | (p/pc) @ 0.5eps*   |
| Col 02  | (p/pc) @ 1.0eps*   | (p/pc) @ 1.0eps*   | (p/pc) @ 1.0eps*   | (p/pc) @ 1.0eps*   | (p/pc) @ 1.0eps*   | (p/pc) @ 1.0eps*   |
| Col 03  | (p/pc) @ 2.0eps*   | (p/pc) @ 2.0eps*   | (p/pc) @ 2.0eps*   | (p/pc) @ 2.0eps*   | (p/pc) @ 2.0eps*   | (p/pc) @ 2.0eps*   |
| Col 04  | (p/pc) @ 3.0eps*   | (p/pc) @ 3.0eps*   | (p/pc) @ 3.0eps*   | (p/pc) @ 3.0eps*   | (p/pc) @ 3.0eps*   | (p/pc) @ 3.0eps*   |
| Col 05  | (p/pc) @ 4.0eps*   | (p/pc) @ 4.0eps*   | (p/pc) @ 4.0eps*   | (p/pc) @ 4.0eps*   | (p/pc) @ 4.0eps*   | (p/pc) @ 4.0eps*   |
| Col 06  | (q/pc) @ 0.5eps*   | (q/pc) @ 0.5eps*   | (q/pc) @ 0.5eps*   | (q/pc) @ PK        | (q/pc) @ PK        | (q/pc) @ 0.5eps*   |
| Col 07  | (q/pc) @ 1.0eps*   | (q/pc) @ 1.0eps*   | (q/pc) @ 1.0eps*   | (q/pc) @ 1.0eps*   | (q/pc) @ 1.0eps*   | (q/pc) @ 1.0eps*   |
| Col 08  | (q/pc) @ 2.0eps*   | (q/pc) @ 2.0eps*   | (q/pc) @ 2.0eps*   | (q/pc) @ 2.0eps*   | (q/pc) @ 2.0eps*   | (q/pc) @ 2.0eps*   |
| Col 09  | (q/pc) @ 3.0eps*   | (q/pc) @ 3.0eps*   | (q/pc) @ 3.0eps*   | (q/pc) @ 3.0eps*   | (q/pc) @ 3.0eps*   | (q/pc) @ 3.0eps*   |
| Col 10  | (q/pc) @ 4.0eps*   | (q/pc) @ 4.0eps*   | (q/pc) @ 4.0eps*   | (q/pc) @ 4.0eps*   | (q/pc) @ 4.0eps*   | (q/pc) @ 4.0eps*   |
| Col 11  | 0.5eps*            | 0.5eps*            | 0.5eps*            | eps @ PK           | eps @ PK           | 0.5eps*            |
| Col 12  | 1.0eps* [PK]       | 1.0eps* [PK]       | 1.0eps* [PK]       | 1.0eps* [QSS]      | 1.0eps* [QSS]      | 1.0eps* [PT]       |
| Col 13  | 2.0eps*            | 2.0eps*            | 2.0eps*            | 2.0eps*            | 2.0eps*            | 2.0eps*            |
| Col 14  | 3.0eps*            | 3.0eps*            | 3.0eps*            | 3.0eps*            | 3.0eps*            | 3.0eps*            |
| Col 15  | 4.0eps*            | 4.0eps*            | 4.0eps*            | 4.0eps*            | 4.0eps*            | 4.0eps*            |
| Col 16  | psi_0              | psi_0              | psi_0              | psi_0              | psi_0              | psi_0              |
| Col 17  | (p/pc) @ 0.5eps*   | (p/pc) @ PK        | (p/pc) @ 0.5eps*   | (p/pc) @ PK        | (p/pc) @ 0.5eps*   | (p/pc) @ 0.5eps*   |
| Col 18  | (p/pc) @ 1.0eps*   | (p/pc) @ 1.0eps*   | (p/pc) @ 1.0eps*   | (p/pc) @ 1.0eps*   | (p/pc) @ 1.0eps*   | (p/pc) @ 1.0eps*   |
| Col 19  | (p/pc) @ 2.0eps*   | (p/pc) @ 2.0eps*   | (p/pc) @ 2.0eps*   | (p/pc) @ 2.0eps*   | (p/pc) @ 2.0eps*   | (p/pc) @ 2.0eps*   |
| Col 20  | (p/pc) @ 3.0eps*   | (p/pc) @ 3.0eps*   | (p/pc) @ 3.0eps*   | (p/pc) @ 3.0eps*   | (p/pc) @ 3.0eps*   | (p/pc) @ 3.0eps*   |
| Col 21  | (p/pc) @ 4.0eps*   | (p/pc) @ 4.0eps*   | (p/pc) @ 4.0eps*   | (p/pc) @ 4.0eps*   | (p/pc) @ 4.0eps*   | (p/pc) @ 4.0eps*   |
| Col 22  | (q/pc) @ 0.5eps*   | (q/pc) @ PK        | (q/pc) @ 0.5eps*   | (q/pc) @ PK        | (q/pc) @ 0.5eps*   | (q/pc) @ 0.5eps*   |
| Col 23  | (q/pc) @ 1.0eps*   | (q/pc) @ 1.0eps*   | (q/pc) @ 1.0eps*   | (q/pc) @ 1.0eps*   | (q/pc) @ 1.0eps*   | (q/pc) @ 1.0eps*   |
| Col 24  | (q/pc) @ 2.0eps*   | (q/pc) @ 2.0eps*   | (q/pc) @ 2.0eps*   | (q/pc) @ 2.0eps*   | (q/pc) @ 2.0eps*   | (q/pc) @ 2.0eps*   |
| Col 25  | (q/pc) @ 3.0eps*   | (q/pc) @ 3.0eps*   | (q/pc) @ 3.0eps*   | (q/pc) @ 3.0eps*   | (q/pc) @ 3.0eps*   | (q/pc) @ 3.0eps*   |
| Col 26  | (q/pc) @ 4.0eps*   | (q/pc) @ 4.0eps*   | (q/pc) @ 4.0eps*   | (q/pc) @ 4.0eps*   | (q/pc) @ 4.0eps*   | (q/pc) @ 4.0eps*   |
| Col 27  | 0.5eps*            | eps @ PK           | 0.5eps*            | eps @ PK           | 0.5eps*            | 0.5eps*            |
| Col 28  | 1.0eps* [PK]       | 1.0eps* [QSS]      | 1.0eps* [PT]       | 1.0eps* [QSS]      | 1.0eps* [PT]       | 1.0eps* [PT]       |
| Col 29  | 2.0eps*            | 2.0eps*            | 2.0eps*            | 2.0eps*            | 2.0eps*            | 2.0eps*            |
| Col 30  | 3.0eps*            | 3.0eps*            | 3.0eps*            | 3.0eps*            | 3.0eps*            | 3.0eps*            |
| Col 31  | 4.0eps*            | 4.0eps*            | 4.0eps*            | 4.0eps*            | 4.0eps*            | 4.0eps*            |


### Processing

Output file saved in 4 column format:

```python
hdr = 'p q epsQ psi'
```
