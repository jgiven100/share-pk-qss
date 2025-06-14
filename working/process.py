import numpy as np
import scipy as sp
import json
import os

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


def compute_points(t, params, df):
    """Compute peak and quasi-steady points

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
        1x7 array with initial state parameter, stress, strains
    """

    # Shear rigidity
    Ir = params['Gref'] / params['pref']

    # Initial values
    p0 = df[0, 0]
    psi0 = df[0, 6]

    # Find peak, quasi-steady state
    p_pc_pk = q_pc_pk = eps_Ir_pk = -1
    p_pc_qss = q_pc_qss = eps_Ir_qss = -1

    # Steady state
    q_ss = params['Mtc'] * np.exp(-psi0 / params['lambd']) * p0

    # Save response type
    #   0 := Softening
    #   1 := Quasi-steady state
    #   2 := Hardening
    id = 2

    monotonic = True
    reversal = False
    peak_index = 0

    # Search stress path
    for n, _ in enumerate(df):
        if n == 0: continue

        dq = df[n, 1] - df[n - 1, 1]

        # Sample begins to soften
        if ((monotonic) and (dq < 0)):

            # Check that peak is more than 1% away from steady state
            q_check = np.abs(df[n, 1] - q_ss) / q_ss
            if (q_check > 0.01):
                monotonic = False

                p_pc_pk = df[n, 0] / p0
                q_pc_pk = df[n, 1] / p0
                eps_Ir_pk = df[n, 4] * Ir

                id = 0

                peak_index = n

        # Sample reverses at QSS
        if ((not monotonic) and (not reversal) and (dq > 0)):

            # Check that quasi-steady state is more than 1% away from steady
            # state
            q_check = np.abs(df[n, 1] - q_ss) / q_ss
            if (q_check > 0.01):
                reversal = True

                p_pc_qss = df[n, 0] / p0
                q_pc_qss = df[n, 1] / p0
                eps_Ir_qss = df[n, 4] * Ir

                id = 1

                break

    # Initialize cubic spline var
    cs = 0

    # Softening
    if (not monotonic) and (not reversal):

        # Only search post-peak
        for n, _ in enumerate(df):
            if n < peak_index: continue

            # Check that current state is within 1% of steady state
            q_check = np.abs(df[n, 1] - q_ss) / q_ss
            if (q_check < 0.01):
                p_pc_qss = df[n, 0] / p0
                q_pc_qss = df[n, 1] / p0
                eps_Ir_qss = df[n, 4] * Ir

                break

        # Keep searching, if needed
        if (p_pc_qss == -1):
            # Only search post-peak
            for n, _ in enumerate(df):
                if n < peak_index: continue

                # Check that change in deviatoric stress is zero
                dq = df[n, 1] - df[n - 1, 1]
                if abs(dq) < 1e-12:
                    p_pc_qss = df[n, 0] / p0
                    q_pc_qss = df[n, 1] / p0
                    eps_Ir_qss = df[n, 4] * Ir

                    break

        # Keep searching, if needed
        if (p_pc_qss == -1):
            # Extrapolate critical state
            q_rev = df[peak_index:, 1][::-1]
            eps_rev = df[peak_index:, 4][::-1]

            cs = sp.interpolate.CubicSpline(q_rev, eps_rev)
            eps_extrapolated = cs(q_ss)

            p_pc_qss = q_ss / params['Mtc'] / p0
            q_pc_qss = q_ss / p0
            eps_Ir_qss = eps_extrapolated * Ir

    # Hardening
    if monotonic:
        # Find index for global minimum of mean effective stress
        i = np.argmin(df[:, 0])

        # Phase transformation
        p_pc_pk = df[i, 0] / p0
        q_pc_pk = df[i, 1] / p0
        eps_Ir_pk = df[i, 4] * Ir

        # Critical state
        cs = sp.interpolate.CubicSpline(df[i:, 1], df[i:, 4])
        eps_extrapolated = cs(q_ss)

        p_pc_qss = q_ss / params['Mtc'] / p0
        q_pc_qss = q_ss / p0
        eps_Ir_qss = eps_extrapolated * Ir

    # Save very simple figure to check
    if True:
        _, axs = plt.subplots(nrows=1, ncols=2, figsize=(6.5, 3.0))

        # Plot normalized stress and strain paths
        axs[0].plot(df[:, 0] / p0, df[:, 1] / p0)
        axs[1].plot(df[:, 4] * Ir, df[:, 1] / p0)

        # Plot points of interest
        axs[0].plot(p_pc_pk, q_pc_pk, "r.")
        axs[0].plot(p_pc_qss, q_pc_qss, "rx")

        axs[1].plot(eps_Ir_pk, q_pc_pk, "r.")
        axs[1].plot(eps_Ir_qss, q_pc_qss, "rx")

        # Tidy
        plt.tight_layout()
        plt.savefig(f"figures/ns-{t:06d}.png", dpi=100)
        plt.close()

    return [
        psi0, id, p_pc_pk, q_pc_pk, eps_Ir_pk, p_pc_qss, q_pc_qss, eps_Ir_qss
    ]


def print_points(t, params, points):
    """Print material params and points of interest to command line

    Parameters
    ----------
    t : int
        Current step
    params : dict
        Dictionary with material parameters
    points : array
        1x7 array with initial state parameter, stress, strains

    Returns
    -------
    None
    """

    # Print header on first step
    if t == 0:
        msg = ""
        msg += "psi0,nu,N,chitc,href,id,col0,col1,col2,col3,col4,col5"
        print(msg)

    # Print material params
    msg = ""
    msg += f"{points[0]:.2f},"
    msg += f"{params['nu']:.2f},"
    msg += f"{params['N']:.2f},"
    msg += f"{params['chitc']:.2f},"
    msg += f"{params['href']:.8f},"
    msg += f"{points[1]:d}"
    for i in range(2, 8):
        msg += f",{points[i]:.6e}"
    print(msg)


def read_input_output(dir_name):
    """Read input.json and output.txt for given filename

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
    # Note: run from directly where saved
    current_dir = os.getcwd() + "/simulation/data/"

    # Put input parameters into dict
    fname = current_dir + dir_name + "/saveParams.txt"
    with open(fname, "r") as file:
        params_dict_as_str = file.read()
    params_dict_as_str = params_dict_as_str.replace("'", "\"")
    params = json.loads(params_dict_as_str)

    # Put simulation data into array
    fname = current_dir + dir_name + "/saveData.txt"
    df = np.loadtxt(fname, delimiter=" ", skiprows=1)

    return params, df


def main():

    total = 15 * 11 * 11 * 11 * 6

    for t in range(total):

        # if t < 118790: continue

        # Load data
        fname = f"ns-{t:06d}"
        params, df = read_input_output(fname)

        # Compute points of interest
        points = compute_points(t, params, df)

        # Write to command line
        print_points(t, params, points)


if __name__ == "__main__":
    main()
