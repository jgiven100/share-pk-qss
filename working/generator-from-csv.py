import numpy as np
import json
import os
import argparse


def generate_inputs(row, n, row_num, test_num):
    """Generate suite of input files (.json) for NorSand simulations

    Parameters
    ----------
    row : array
        Array of true and nn parameters
    n : int
        Number of outputs with the same material parameters
    row_num : int
        Row number (for saving files)
    test_num : int
        Response type (for saving files)


    Returns
    -------
    None
    """

    # Save directory
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

    # Variable state parameters
    psi0_l = np.linspace(-0.2, 0.2, n)

    for t in range(n):
        for i in range(2):
            # Compute current void ratio
            psi0 = psi0_l[t]
            e0 = psi0 + (Gamma - lambd * np.log(p0 / pref))

            # Generate input.json
            data = {
                "params": {
                    "pref": pref,
                    "Gref": Ir * pref,
                    "ne": n_e,
                    "nu": row[1 + i * 4],
                    "Gamma": Gamma,
                    "lambd": lambd,
                    "Mtc": Mtc,
                    "N": row[2 + i * 4],
                    "href": row[4 + i * 4],
                    "np": n_p,
                    "nh": n_h,
                    "chitc": row[3 + i * 4],
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
                    "name": f"ns-TEST{test_num}-ROW{row_num:d}-{t:02d}-{i:d}/",
                },
            }

            # Save file
            file_name = f"ns-TEST{test_num}-ROW{row_num:d}-{t:02d}-{i:d}.json"
            file_path = os.path.join(output_dir, file_name)
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)

    print(f"TEST {test_num} ROW {row_num} DONE!")


def main():

    parser = argparse.ArgumentParser(
        description="Generate number of inputs based on passed integer.",
    )

    parser.add_argument(
        "--npsi0",
        type=int,
        default=21,
        help="Number of psi_0 for each set of materials params",
    )

    parser.add_argument(
        "--nrows",
        type=int,
        default=5,
        help="Number of psi_0 for each set of materials params",
    )

    args = parser.parse_args()
    npsi0 = args.npsi0
    nrows = args.nrows

    # Known column info from .csv files
    cols = [9, 12, 9]
    indices = [
        [1, 2, 3, 4, 5, 10, 11, 12, 13],
        [1, 2, 3, 4, 5, 13, 14, 15, 16],
        [1, 2, 3, 4, 5, 10, 11, 12, 13],
    ]

    # Loop each response type
    for i in range(3):
        # Load entire .csv as string
        predicted = np.loadtxt(
            f"predicted-{i}.csv",
            skiprows=1,
            delimiter=",",
            dtype="str",
        )

        # Masks to only keep "Test" rows and material param colums
        predicted = predicted[predicted[:, cols[i]] == "Test"]
        predicted = predicted[:, indices[i]].astype(float)

        # Sort by initial state parameter
        predicted = predicted[np.argsort(predicted[:, 0])]

        # Pick `nrows` approximately across entire range
        indices_tmp = np.linspace(0, predicted.shape[0] - 1, nrows, dtype=int)
        predicted = predicted[indices_tmp]

        # Loop each set of material params
        for j, row in enumerate(predicted):
            generate_inputs(row, npsi0, j, i)


if __name__ == "__main__":
    main()
