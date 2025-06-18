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

    total = 150000

    # Variable material parameters
    nu_l = np.round(np.random.uniform(0.1, 0.35, total), 4)
    N_l = np.round(np.random.uniform(0.1, 0.6, total), 4)
    chitc_l = np.round(np.random.uniform(1.0, 6.0, total), 4)
    href_l = np.round(np.random.uniform(5, 150, total), 4)

    # Variable state parameters
    psi0_l = np.random.uniform(-0.2, 0.2, total)

    for t in range(total):
        # Compute current void ratio
        psi0 = psi0_l[t]
        e0 = psi0 + (Gamma - lambd * np.log(p0 / pref))

        # Generate input.json
        data = {
            "params": {
                "pref": pref,
                "Gref": Ir * pref,
                "ne": n_e,
                "nu": nu_l[t],
                "Gamma": Gamma,
                "lambd": lambd,
                "Mtc": Mtc,
                "N": N_l[t],
                "href": href_l[t],
                "np": n_p,
                "nh": n_h,
                "chitc": chitc_l[t],
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
                "name": f"ns-{t:06d}/",
            },
        }

        # Save file
        file_name = f"ns-{t:06d}.json"
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

        # Print status update
        if t % 1000 == 0:
            print(f"COUNT: {t:06d} of {total}")

    print(f"COUNT: {total} of {total}")
    print("DONE!")


def main():

    generate_inputs()


if __name__ == "__main__":
    main()
