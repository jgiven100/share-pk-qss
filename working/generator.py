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
    # output_dir = "/mnt/c/Users/jgive/Documents/norsand-inputs/json-output"
    output_dir = os.getcwd() + "/json-output"

    # Initial stress state
    pref = 100.0e3
    p0 = 160.0e3
    pi0 = np.ceil(p0 / np.exp(1))
    q0 = 0

    # Constant material parameters
    Mtc = 1.24
    Gamma = 0.91
    lambd = 0.014
    Ir = 150
    n_e = 1.0
    n_p = 0.0
    n_h = 2.0

    # Variable material parameters
    nu_l = np.linspace(0.1, 0.35, 6)
    N_l = np.linspace(0.1, 0.6, 11)
    chitc_l = np.linspace(1.0, 6.0, 11)
    href_l = np.logspace(np.log10(5), np.log10(150), 15)

    # Variable state parameters
    psi0_l = np.linspace(-0.2, 0.2, 11)

    count = 0
    for psi0 in psi0_l:
        # Compute current void ratio
        e0 = psi0 + (Gamma - lambd * np.log(p0 / pref))

        for nu in nu_l:
            for N in N_l:
                for chitc in chitc_l:
                    for href in href_l:
                        data = {
                            "params": {
                                "pref": pref,
                                "Gref": Ir * pref,
                                "ne": n_e,
                                "nu": nu,
                                "Gamma": Gamma,
                                "lambd": lambd,
                                "Mtc": Mtc,
                                "N": N,
                                "href": href,
                                "np": n_p,
                                "nh": n_h,
                                "chitc": chitc,
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
                                "q0": q0,
                                "pi0": pi0,
                                "e0": e0,
                                "epsQ": 0.4,
                                "name": f"ns-{count:06d}/",
                            },
                        }

                        file_name = f"ns-{count:06d}.json"
                        file_path = os.path.join(output_dir, file_name)

                        with open(file_path, "w") as f:
                            json.dump(data, f, indent=4)

                        if count % 1000 == 0:
                            print(f"COUNT: {count:06d} of {6*(11**3)*15}")

                        count += 1

    print("DONE!")


def main():

    generate_inputs()


if __name__ == "__main__":
    main()
