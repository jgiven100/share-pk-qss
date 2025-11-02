import numpy as np
import json
import os


def generate_inputs():
    """Generate suite of input files (.json) for NorSand simulations

    Parameters
    ----------
    None

    Returns
    -------
    None
    """

    # Save directory
    output_dir = os.getcwd() + "/json-output"

    # Constant material parameters
    Mtc = 1.24

    Gamma = 0.91
    lambd = 0.014

    Gamma_xi = 0.934
    lambd_xi = 0.019
    xi = 0.7

    pref = 100.0e3

    # Variable parameters
    Ir = [100, 150, 300]
    N_e = [1.0, +0.5, 0.75, 0.5, +0.5, 0.5]
    N_p = [0.0, -0.5, 0.00, 0.0, -0.5, 0.0]
    E0 = np.linspace(1.05, 0.75, 61)
    P0 = np.geomspace(8e3, 1024e3, 59)

    total = 61 * 59 * 3 * 6

    n = 0
    for i, (n_e, n_p) in enumerate(zip(N_e, N_p)):
        for ir in Ir:
            for p0 in P0:
                for e0 in E0:

                    # Initial stress state
                    pi0 = np.ceil(p0 / np.exp(1))

                    if i < 4:
                        # Compute current void ratio
                        # e0 = psi0 + (Gamma - lambd * np.log(p0 / pref))

                        # Generate input.json
                        data = {
                            "params": {
                                "pref": pref,
                                "Gref": ir * pref,
                                "ne": n_e,
                                "nu": 0.15,
                                "Gamma": Gamma,
                                "lambd": lambd,
                                "Mtc": Mtc,
                                "N": 0.35,
                                "href": 50.0,
                                "np": n_p,
                                "nh": 2.0,
                                "chitc": 4.0,
                            },
                            "opts": {
                                "loose": "ED",
                                "csl": "linear",
                                "test": "txc",
                                "dvol": "undrained",
                                "Dmin": "approx2",
                            },
                            "sim": {
                                "p0": p0,
                                "q0": 0,
                                "pi0": pi0,
                                "e0": e0,
                                "epsQ": 0.4,
                                "name": f"n{n:06d}/",
                            },
                        }

                    else:
                        # Compute current void ratio
                        # e0 = psi0 + (Gamma_xi -
                        #              lambd_xi * np.power(p0 / pref, xi))

                        # Generate input.json
                        data = {
                            "params": {
                                "pref": pref,
                                "Gref": ir * pref,
                                "ne": n_e,
                                "nu": 0.15,
                                "Gamma_xi": Gamma_xi,
                                "lambd_xi": lambd_xi,
                                "xi": xi,
                                "Mtc": Mtc,
                                "N": 0.35,
                                "href": 50.0,
                                "np": n_p,
                                "nh": 2.0,
                                "chitc": 4.0,
                            },
                            "opts": {
                                "loose": "ED",
                                "csl": "power",
                                "test": "txc",
                                "dvol": "undrained",
                                "Dmin": "approx2",
                            },
                            "sim": {
                                "p0": p0,
                                "q0": 0,
                                "pi0": pi0,
                                "e0": e0,
                                "epsQ": 0.4,
                                "name": f"n{n:06d}/",
                            },
                        }

                    # Save file
                    file_name = f"ns-{n:05d}.json"
                    file_path = os.path.join(output_dir, file_name)
                    with open(file_path, "w") as f:
                        json.dump(data, f, indent=4)

                    if n % 1000 == 0:
                        print(f"{str(n).zfill(5)} of {total} done")

                    n += 1

    print(f"{n} of {total} done")


def main():

    generate_inputs()


if __name__ == "__main__":
    main()
