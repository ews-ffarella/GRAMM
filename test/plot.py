import logging
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def read(probe_file):

    with probe_file.open("r") as fin:
        header = fin.readline()
        logging.info(header)
        N = int(header.split("=")[1].strip())
        click.echo(f"Reading {N} probes...")

    xyz_df = pd.read_csv(
        probe_file,
        sep=" ",
        decimal=".",
        skiprows=1,
        nrows=N,
        index_col="PROBEI",
        header=0,
    )
    # print(xyz_df)
    data_df = pd.read_csv(
        probe_file,
        sep=" ",
        decimal=".",
        skiprows=3 + N,
        nrows=None,
        header=0,
        index_col=None,
        na_values=["NaN"],
    )   
    data_df = data_df.where(data_df != -99999) 
    data_df['U'] = data_df.U / 1000.0
    data_df['V'] = data_df.V / 1000.0
    data_df['W'] = data_df.W / 10000.0
    data_df['T'] = data_df["T"] / 100.0
    data_df['K'] = data_df.K / 100000.0
    data_df['DP'] = data_df.DP / 1000.0
    data_df['EPSILON'] = data_df.EPSILON / 10000000.0
    data_df['U2D'] = ((data_df.U ** 2.0) + (data_df.V ** 2.0))**0.5
    data_df['INCL'] = np.degrees(np.arctan2(data_df.W, data_df.U2D))
    data_df['DIR'] = np.fmod(270 - np.degrees(np.arctan2(data_df.V, data_df.U)), 360.0)
    data_df['TI'] = 100.0 * ((4.0 * data_df.K / 3.0) ** 0.5) / data_df.U2D
    return xyz_df, data_df


import click


@click.command()
@click.option("--case", "-c", type=int, default=1, show_default=True)
@click.option("--refresh", "-r", type=int, default=2, show_default=True)
def run(case, refresh):
    cwd = Path(".").resolve().absolute()
    ax1 = plt.subplot(321)
    ax2 = plt.subplot(322, sharex=ax1)
    ax3 = plt.subplot(323, sharex=ax1)
    ax4 = plt.subplot(324, sharex=ax1)
    ax5 = plt.subplot(325, sharex=ax1)
    ax6 = plt.subplot(326, sharex=ax1)

    # make these tick labels invisible
    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.setp(ax2.get_xticklabels(), visible=False)
    plt.setp(ax3.get_xticklabels(), visible=False)
    plt.setp(ax4.get_xticklabels(), visible=False)
    plt.setp(ax5.get_xticklabels(), visible=True)
    plt.setp(ax6.get_xticklabels(), visible=True)
    ax2.yaxis.tick_right()
    ax4.yaxis.tick_right()
    ax6.yaxis.tick_right()
    ax2.yaxis.set_label_position("right")
    ax4.yaxis.set_label_position("right")
    ax6.yaxis.set_label_position("right")
    # ax1.legend()

    plt.subplots_adjust(
        left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.1, hspace=0.1
    )
    fig = plt.gcf()
    fig.canvas.set_window_title(f"Test case: {case}")

    ax1.set(
        title="Horizontal wind speed [m/s]",
    )
    ax2.set(title="Wind direction [°]")
    ax3.set(title="Turbulence intensity [%]")
    ax4.set(title="Flow inclination [°]")
    ax5.set(title="Epsilon [°]")
    ax6.set(title="Pressure [Pa]")
    ax1.set_xlim(auto=True)
    ax1.set_ylim(auto=True)
    ax2.set_ylim(auto=True)
    ax3.set_ylim(auto=True)
    ax4.set_ylim(auto=True)
    ax5.set_ylim(auto=True)
    ax6.set_ylim(auto=True)

    probe_file = cwd / f"{case:05d}.probes.dat"

    size_old = None
    while True:
        xyz_df = data_df = None
        if not probe_file.is_file():
            click.echo(f"Waiting for {probe_file.name}")
        else:
            try:
                xyz_df, data_df = read(probe_file)
            except Exception as e:
                click.echo(str(e))
                xyz_df = data_df = None

        do_update = data_df is not None

        t_max = np.nan
        if do_update:
            size_new = data_df.index.size
            data_df = data_df.astype({"Time": "float"})
            t_max = data_df.Time.max()
        else:
            plt.clf()

        if do_update and (size_new != size_old) and not np.isnan(t_max):
            #
            for probei in xyz_df.index:
                pdf = (
                    data_df.query("PROBEI == @probei")
                    .astype("float")
                    .sort_values("Time")
                )
                label = f"{probei}"
                kws = dict(label=label, lw=1)
                ax1.plot(pdf.Time, pdf.U2D, **kws)
                ax2.plot(pdf.Time, pdf.DIR, **kws)
                ax3.plot(pdf.Time, pdf.TI, **kws)
                ax4.plot(pdf.Time, pdf.INCL, **kws)
                ax5.plot(pdf.Time, pdf.EPSILON, **kws)
                ax6.plot(pdf.Time, pdf.DP, **kws)

            size_old = size_new
        else:
            pass
            # plt.clf()

        plt.pause(refresh)

    # plt.show()


if __name__ == "__main__":
    run()
