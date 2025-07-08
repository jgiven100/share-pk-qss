# 3-Test
Three different `psi_0` for each combination of the material parameters.


## Varying material parameters

```python
total=150000

# Variable state parameters
psi0_l = []
for i in range(3):
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

TODO
