import numpy as np
import json
import os

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


def compute_points(t, params, dfs):
    """Compute peak, quasi-steady state, and phase transformation points

    Parameters
    ----------
    t : int
        Current step
    params : dict
        Dictionary with material parameters
    dfs : array
        Array of numpy array with stress and strain history

    Returns
    -------
    points : array
        Array of arrays with id, initial state parameter, stress, strains
    """

    # Shear rigidity
    Ir = params["Gref"] / params["pref"]

    # Peak, quasi-steady state, phase transformation points
    p_pc_pk = [-1, -1]
    q_pc_pk = [-1, -1]
    eps_Ir_pk = [-1, -1]
    p_pc_qss = [-1, -1]
    q_pc_qss = [-1, -1]
    eps_Ir_qss = [-1, -1]

    # Save response type
    #   0 := Softening
    #   1 := Quasi-steady state
    #   2 := Hardening
    id = [2, 2]

    # Initial state parameter
    psi0 = [0, 0]

    for i, df in enumerate(dfs):
        # Initial values
        p0 = df[0, 0]
        psi0[i] = df[0, 3]

        # Compute steady state
        q_ss = params["Mtc"] * np.exp(-psi0[i] / params["lambd"]) * p0

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

                    p_pc_pk[i] = df[n, 0] / p0
                    q_pc_pk[i] = df[n, 1] / p0
                    eps_Ir_pk[i] = df[n, 2] * Ir

                    id[i] = 0

            # Sample reverses at QSS
            if (not monotonic) and (not reversal) and (dq > 0):

                # Check that quasi-steady state is more than 1% away from
                # steady state
                q_check = np.abs(df[n, 1] - q_ss) / q_ss
                if q_check > 0.01:
                    reversal = True

                    p_pc_qss[i] = df[n, 0] / p0
                    q_pc_qss[i] = df[n, 1] / p0
                    eps_Ir_qss[i] = df[n, 2] * Ir

                    id[i] = 1

                    break

        # Hardening
        if monotonic:
            # Find index for global minimum of mean effective stress
            index = np.argmin(df[:, 0])

            # Phase transformation point
            p_pc_pk[i] = df[index, 0] / p0
            q_pc_pk[i] = df[index, 1] / p0
            eps_Ir_pk[i] = df[index, 2] * Ir

    # Softening -- softening
    if sorted(id) == [0, 0]:
        id_single = 0

    # Softening -- quasi-steady state
    elif sorted(id) == [0, 1]:
        id_single = 1

    # Softening -- hardening
    elif sorted(id) == [0, 2]:
        id_single = 2

    # Quasi-steady state -- quasi-steady state
    elif sorted(id) == [1, 1]:
        id_single = 3

    # Quasi-steady state -- hardening
    elif sorted(id) == [1, 2]:
        id_single = 4

    # Hardening -- hardening
    elif sorted(id) == [2, 2]:
        id_single = 5

    # Warn and quit
    else:
        print("Warning [in compute_points]: no match for sorted(id) found!!")
        quit()

    # Save very simple figure to check
    _, axs = plt.subplots(nrows=1, ncols=2, figsize=(6.5, 3.0))

    for i, df in enumerate(dfs):

        # Plot normalized stress and strain paths
        axs[0].plot(df[:, 0] / p0, df[:, 1] / p0)
        axs[1].plot(df[:, 2] * Ir, df[:, 1] / p0)

        # Plot points of interest
        axs[0].plot(p_pc_pk[i], q_pc_pk[i], "r.")
        axs[1].plot(eps_Ir_pk[i], q_pc_pk[i], "r.")

        if id[i] == 1:
            axs[0].plot(p_pc_qss[i], q_pc_qss[i], "rx")
            axs[1].plot(eps_Ir_qss[i], q_pc_qss[i], "rx")

    # Save
    plt.tight_layout()
    plt.savefig(f"figures/{id_single}/ns-{t:06d}.png", dpi=100)
    plt.close()

    return [
        id_single, id, psi0, p_pc_pk, q_pc_pk, eps_Ir_pk, p_pc_qss, q_pc_qss,
        eps_Ir_qss
    ]


def read_input_output(dir_names):
    """Read saveParams.txt and saveData.txt for given filename

    Parameters
    ----------
    dir_names : array
        Array of directory names for each simulation

    Returns
    -------
    params : dict
        Dictionary with material parameters
    dfs : array
        Array of numpy array with stress and strain history
    """

    # Set current working directory
    current_dir = os.getcwd() + "/simulation/data/"

    # Initialize array for saving stress and strain histories
    dfs = []

    for dir_name in dir_names:
        # Put input parameters into dict
        fname = current_dir + dir_name + "/saveParams.txt"
        with open(fname, "r") as file:
            params_dict_as_str = file.read()
        params_dict_as_str = params_dict_as_str.replace("'", '"')

        # Params gets overwritten here... same values anyway
        params = json.loads(params_dict_as_str)

        # Put simulation data into array
        fname = current_dir + dir_name + "/saveData.txt"
        dfs.append(np.loadtxt(fname, delimiter=" ", skiprows=1))

    return params, dfs


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

    hdr = "nu,N,chitc,href,id,"

    # Softening -- softening
    if id == 0:
        hdr += "col0,col1,col2,col3,col4,col5,col6,col7"

    # Softening -- quasi-steady state
    elif id == 1:
        hdr += "col0,col1,col2,col3,col4,col5,col6,col7,col8,col9,col10"

    # Softening -- hardening
    elif id == 2:
        hdr += "col0,col1,col2,col3,col4,col5,col6,col7"

    # Quasi-steady state -- quasi-steady state
    elif id == 3:
        hdr += "col0,col1,col2,col3,col4,col5,col6,col7"
        hdr += ",col8,col9,col10,col11,col12,col13"

    # Quasi-steady state -- hardening
    elif id == 4:
        hdr += "col0,col1,col2,col3,col4,col5,col6,col7,col8,col9,col10"

    # Hardening -- hardening
    elif id == 5:
        hdr += "col0,col1,col2,col3,col4,col5,col6,col7"

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
        Array of arrays with id, initial state parameter, stress, strains

    Returns
    -------
    msg : str
        String with message
    """

    msg = ""

    # Print material params
    msg += f"{params['nu']:.4f},"
    msg += f"{params['N']:.4f},"
    msg += f"{params['chitc']:.4f},"
    msg += f"{params['href']:.4f},"
    msg += f"{points[0]:d}"

    # Get order
    index = sorted(range(len(points[1])), key=lambda i: points[1][i])

    # Softening -- softening
    if points[0] == 0:
        for i in index:
            for j in range(2, 6):
                msg += f",{points[j][i]:.6e}"

    # Softening -- quasi-steady state
    elif points[0] == 1:
        i = index[0]
        for j in range(2, 6):
            msg += f",{points[j][i]:.6e}"
        i = index[1]
        for j in range(2, 9):
            msg += f",{points[j][i]:.6e}"

    # Softening -- hardening
    elif points[0] == 2:
        for i in index:
            for j in range(2, 6):
                msg += f",{points[j][i]:.6e}"

    # Quasi-steady state -- quasi-steady state
    elif points[0] == 3:
        for i in index:
            for j in range(2, 9):
                msg += f",{points[j][i]:.6e}"

    # Quasi-steady state -- hardening
    elif points[0] == 4:
        i = index[0]
        for j in range(2, 9):
            msg += f",{points[j][i]:.6e}"
        i = index[1]
        for j in range(2, 6):
            msg += f",{points[j][i]:.6e}"

    # Hardening -- hardening
    elif points[0] == 5:
        for i in index:
            for j in range(2, 6):
                msg += f",{points[j][i]:.6e}"

    # Warn and quit
    else:
        print("Warning [in write_message]: no reponse id found!!")
        quit()

    return msg


def main():

    total = 100000

    save_0 = [write_header(0)]
    save_1 = [write_header(1)]
    save_2 = [write_header(2)]
    save_3 = [write_header(3)]
    save_4 = [write_header(4)]
    save_5 = [write_header(5)]

    for t in range(total):

        # Load data
        fnames = [f"ns-{t:06d}-0", f"ns-{t:06d}-1"]
        params, dfs = read_input_output(fnames)

        # Compute points of interest
        points = compute_points(t, params, dfs)

        # Write message
        msg = write_message(params, points)

        # Softening -- softening
        if points[0] == 0:
            save_0.append(msg)

        # Softening -- quasi-steady state
        elif points[0] == 1:
            save_1.append(msg)

        # Softening -- hardening
        elif points[0] == 2:
            save_2.append(msg)

        # Quasi-steady state -- quasi-steady state
        elif points[0] == 3:
            save_3.append(msg)

        # Quasi-steady state -- hardening
        elif points[0] == 4:
            save_4.append(msg)

        # Hardening -- hardening
        elif points[0] == 5:
            save_5.append(msg)

        # Warn and quit
        else:
            print("Warning [in main]: no reponse id found!!")
            quit()

        # Print status update
        if t % 1000 == 0:
            print(f"COUNT: {t:06d} of {total}")

    print(f"COUNT: {total} of {total}")
    print("Saving to .csv files...")

    # Save in .csv
    for i, save in enumerate([save_0, save_1, save_2, save_3, save_4, save_5]):
        with open(f"save_{i}.csv", "w") as file:
            for s in save:
                file.write(f"{s}\n")

    print("DONE!")


if __name__ == "__main__":
    main()
