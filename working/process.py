import numpy as np
import json
import os

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


def compute_points(t, params, df):
    """Compute peak, quasi-steady state, and phase transformation points

    Parameters
    ----------
    t : int
        Current step
    params : dict
        Dictionary with material parameters
    df : array
        Numpy array with stress and strain history

    Returns
    -------
    points : array
        1x8 array with id, initial state parameter, stress, strains
    """

    # Shear rigidity
    Ir = params["Gref"] / params["pref"]

    # Initial values
    p0 = df[0, 0]
    psi0 = df[0, 6]

    # Peak, quasi-steady state, phase transformation points
    p_pc_pk = q_pc_pk = eps_Ir_pk = -1
    p_pc_qss = q_pc_qss = eps_Ir_qss = -1

    # Compute steady state
    q_ss = params["Mtc"] * np.exp(-psi0 / params["lambd"]) * p0

    # Save response type
    #   0 := Softening
    #   1 := Quasi-steady state
    #   2 := Hardening
    id = 2

    monotonic = True
    reversal = False

    # Search stress path
    for n, _ in enumerate(df):
        if n == 0:
            continue

        dq = df[n, 1] - df[n - 1, 1]

        # Sample begins to soften
        if (monotonic) and (dq < 0):

            # Check that peak is more than 1% away from steady state
            q_check = np.abs(df[n, 1] - q_ss) / q_ss
            if q_check > 0.01:
                monotonic = False

                p_pc_pk = df[n, 0] / p0
                q_pc_pk = df[n, 1] / p0
                eps_Ir_pk = df[n, 4] * Ir

                id = 0

        # Sample reverses at QSS
        if (not monotonic) and (not reversal) and (dq > 0):

            # Check that quasi-steady state is more than 1% away from steady
            # state
            q_check = np.abs(df[n, 1] - q_ss) / q_ss
            if q_check > 0.01:
                reversal = True

                p_pc_qss = df[n, 0] / p0
                q_pc_qss = df[n, 1] / p0
                eps_Ir_qss = df[n, 4] * Ir

                id = 1

                break

    # Hardening
    if monotonic:
        # Find index for global minimum of mean effective stress
        i = np.argmin(df[:, 0])

        # Phase transformation point
        p_pc_pk = df[i, 0] / p0
        q_pc_pk = df[i, 1] / p0
        eps_Ir_pk = df[i, 4] * Ir

    # Save very simple figure to check
    _, axs = plt.subplots(nrows=1, ncols=2, figsize=(6.5, 3.0))

    # Plot normalized stress and strain paths
    axs[0].plot(df[:, 0] / p0, df[:, 1] / p0)
    axs[1].plot(df[:, 4] * Ir, df[:, 1] / p0)

    # Plot points of interest
    axs[0].plot(p_pc_pk, q_pc_pk, "r.")
    axs[1].plot(eps_Ir_pk, q_pc_pk, "r.")

    if id == 1:
        axs[0].plot(p_pc_qss, q_pc_qss, "rx")
        axs[1].plot(eps_Ir_qss, q_pc_qss, "rx")

    # Save
    plt.tight_layout()
    plt.savefig(f"figures/{id}/ns-{t:06d}.png", dpi=100)
    plt.close()

    return [
        id, psi0, p_pc_pk, q_pc_pk, eps_Ir_pk, p_pc_qss, q_pc_qss, eps_Ir_qss
    ]


def read_input_output(dir_name):
    """Read saveParams.txt and saveData.txt for given filename

    Parameters
    ----------
    dir_name : str
        Directory name for each simulation

    Returns
    -------
    params : dict
        Dictionary with material parameters
    df : array
        Numpy array with stress and strain history
    """

    # Set current working directory
    current_dir = os.getcwd() + "/simulation/data/"

    # Put input parameters into dict
    fname = current_dir + dir_name + "/saveParams.txt"
    with open(fname, "r") as file:
        params_dict_as_str = file.read()
    params_dict_as_str = params_dict_as_str.replace("'", '"')
    params = json.loads(params_dict_as_str)

    # Put simulation data into array
    fname = current_dir + dir_name + "/saveData.txt"
    df = np.loadtxt(fname, delimiter=" ", skiprows=1)

    return params, df


def write_header(id):
    """Print material params and points of interest header

    Parameters
    ----------
    id : int
        Response type

    Returns
    -------
    hdr : str
        String with header
    """

    hdr = "psi0,nu,N,chitc,href,id,"

    # Softening
    if id == 0:
        hdr += "col0,col1,col2"

    # Quasi-steady state
    elif id == 1:
        hdr += "col0,col1,col2,col3,col4,col5"

    # Hardening
    elif id == 2:
        hdr += "col0,col1,col2"

    # Warn and quit
    else:
        print("Warning [in write_header]: no reponse id found!!")
        quit()

    return hdr


def write_message(params, points):
    """Print material params and points of interest message

    Parameters
    ----------
    params : dict
        Dictionary with material parameters
    points : array
        1x7 array with initial state parameter, stress, strains

    Returns
    -------
    msg : str
        String with message
    """

    msg = ""

    # Print material params
    msg += f"{points[1]:.6f},"
    msg += f"{params['nu']:.4f},"
    msg += f"{params['N']:.4f},"
    msg += f"{params['chitc']:.4f},"
    msg += f"{params['href']:.4f},"
    msg += f"{points[0]:d}"

    # Softening
    if points[0] == 0:
        for i in range(2, 5):
            msg += f",{points[i]:.6e}"

    # Quasi-steady state
    elif points[0] == 1:
        for i in range(2, 8):
            msg += f",{points[i]:.6e}"

    # Hardening
    elif points[0] == 2:
        for i in range(2, 5):
            msg += f",{points[i]:.6e}"

    # Warn and quit
    else:
        print("Warning [in write_message]: no reponse id found!!")
        quit()

    return msg


def main():

    total = 150000

    save_0 = [write_header(0)]
    save_1 = [write_header(1)]
    save_2 = [write_header(2)]

    for t in range(total):

        # Load data
        fname = f"ns-{t:06d}"
        params, df = read_input_output(fname)

        # Compute points of interest
        points = compute_points(t, params, df)

        # Write message
        msg = write_message(params, points)

        # Softening
        if points[0] == 0:
            save_0.append(msg)

        # Quasi-steady state
        elif points[0] == 1:
            save_1.append(msg)

        # Hardening
        elif points[0] == 2:
            save_2.append(msg)

        # Warn and quit
        else:
            print("Warning [in main]: no reponse id found!!")
            quit()

    # Save in .csv
    for i, save in enumerate([save_0, save_1, save_2]):
        with open(f"save_{i}.csv", "w") as file:
            for s in save:
                file.write(f"{s}\n")


if __name__ == "__main__":
    main()
