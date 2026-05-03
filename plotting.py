#%%
from utils import *
#%%
def select_bo_stages(checkpoints: dict[int, dict]) -> list[int]:
    available = np.array(sorted(checkpoints))
    preferred = [int(available.min()), (int(available.max())-int(available.min()))//2, int(available.max())]

    selected: list[int] = []
    for target in preferred:
        nearest = int(available[np.argmin(np.abs(available - target))])
        if nearest not in selected:
            selected.append(nearest)

    while len(selected) < 3:
        for candidate in [int(available[0]), int(available[len(available) // 2]), int(available[-1])]:
            if candidate not in selected:
                selected.append(candidate)
            if len(selected) == 3:
                break
    return selected[:3]


def posterior_arrays(chk: dict) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    return clean_xy(tensor_to_numpy(chk["X_plot"]), tensor_to_numpy(chk["mu"]), tensor_to_numpy(chk["sigma"]))


def plot_bo_posterior_stage(
    ax: plt.Axes,
    chk: dict,
    title: str,
    letter: str,
    *,
    is_final: bool,
    global_best: pd.Series,
    show_ylabel: bool = False,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x, mu, sigma = posterior_arrays(chk)

    ax.fill_between(
        x,
        mu - 1.96 * sigma,
        mu + 1.96 * sigma,
        color=COL_GP_BAND,
        alpha=GP_BAND_ALPHA,
        linewidth=0,
        zorder=2,
    )
    ax.plot(x, mu, color=COL_GP, lw=GP_LW, zorder=3)

    train_x = tensor_to_numpy(chk["train_X"]).reshape(-1)
    train_y = tensor_to_numpy(chk["train_Y"]).reshape(-1)

    if BO_HALO:
        ax.scatter(
            train_x,
            train_y,
            marker=BO_MARKER,
            s=BO_OBS_HALO_SIZE,
            color="white",
            linewidth=BO_OBS_HALO_LW,
            alpha=0.95,
            zorder=4.8,
        )

    ax.scatter(
        train_x,
        train_y,
        marker=BO_MARKER,
        s=BO_OBS_SIZE,
        color=COL_BO,
        linewidth=BO_OBS_LW,
        alpha=BO_OBS_ALPHA,
        zorder=5,
    )

    if is_final:
        ax.axvline(
            global_best["prestretch"],
            color=COL_BEST,
            lw=BEST_LINE_LW,
            ls=BEST_LINESTYLE,
            ymax=0.89,
            zorder=4,
        )
    else:
        cand_x = tensor_to_numpy(chk.get("candidate_X"))
        if cand_x is not None:
            ax.axvline(
                float(cand_x.reshape(-1)[0]),
                color=COL_NEXT,
                lw=NEXT_LINE_LW,
                ls=NEXT_LINESTYLE,
                ymax=0.97,
                zorder=4,
            )

    panel_label(ax, letter)
    ax.set_title(title, loc="left", pad=3)
    ax.set_xlabel("Prestretch force (N)")
    if show_ylabel:
        ax.set_ylabel("ROM (cm)")
    ax.grid(axis="y", color="0.88", linewidth=0.45)
    polish_axes(ax)

    return x, mu, sigma


def make_bo_progression_plot() -> None:
    checkpoints = load_bo_checkpoints()
    bo_df = load_bo_csv()
    global_best = bo_df.loc[bo_df["rom"].idxmax()]
    selected = select_bo_stages(checkpoints)

    titles = [
        rf"Initial stage ($i\,=\,{selected[0] + 1}$)",
        rf"Intermediate stage ($i\,=\,{selected[1] + 1}$)",
        rf"Final stage ($i\,=\,{selected[2] + 1}$)",
    ]

    fig, axes = plt.subplots(
        1,
        3,
        figsize=(FIG_W, FIG_H),
        sharey=True,
        constrained_layout=False,
        gridspec_kw={"wspace": WSPACE_3_PANEL},
    )

    all_x: list[float] = []
    all_y: list[float] = []

    for i, (ax, iteration, title, letter) in enumerate(zip(axes, selected, titles, "ABC")):
        x, mu, sigma = plot_bo_posterior_stage(
            ax,
            checkpoints[iteration],
            title,
            letter,
            is_final=(i == 2),
            global_best=global_best,
            show_ylabel=(i == 0),
        )
        all_x.extend(x.tolist())
        all_y.extend((mu - 1.96 * sigma).tolist())
        all_y.extend((mu + 1.96 * sigma).tolist())

    ylo = min(float(np.nanmin(all_y)), float(bo_df["rom"].min()))
    yhi = max(float(np.nanmax(all_y)), float(bo_df["rom"].max()))
    xlo, xhi = float(np.nanmin(all_x)), float(np.nanmax(all_x))
    ypad = 0.1 * max(yhi - ylo, 1.0)

    for ax in axes:
        ax.set_xlim(xlo, xhi)
        ax.set_ylim(np.floor(ylo - ypad), yhi + ypad)
        polish_axes(ax)

    legend_handles = [
        Line2D([0], [0], color=COL_GP, lw=GP_LW, label="GP posterior mean"),
        Patch(facecolor=COL_GP_BAND, alpha=1.0, edgecolor="none", label="95% GP interval"),
        Line2D(
            [0], [0],
            marker=BO_MARKER,
            color=COL_BO,
            lw=0,
            markersize=5.0,
            markeredgewidth=BO_OBS_LW,
            label="BO evaluations",
        ),
        Line2D([0], [0], color=COL_NEXT, lw=NEXT_LINE_LW, ls=NEXT_LINESTYLE, label="next query"),
        Line2D([0], [0], color=COL_BEST, lw=BEST_LINE_LW, ls=BEST_LINESTYLE, label="best prestretch"),
    ]
    add_bottom_legend(fig, legend_handles, ncol=5)
    apply_fixed_layout(fig)
    savefig(fig, "bo_progression")

#%%
make_bo_progression_plot()

#%%
def make_augmentation_density_ridgeline_plot(da: dict[str, pd.DataFrame], show_da_underlay=True) -> None:
    """Compact conditional ROM density ridgelines."""
    frames = list(da.values())
    all_rom = pd.concat([df["rom"] for df in frames]).replace([np.inf, -np.inf], np.nan).dropna()
    rom_min = float(all_rom.min())
    rom_max = float(all_rom.max())
    rom_span = max(rom_max - rom_min, 1.0)
    xlim = (
        rom_min - Y_LIMIT_PAD_FRAC * rom_span,
        rom_max + Y_LIMIT_PAD_FRAC * rom_span,
    )

    x_grid = np.linspace(xlim[0], xlim[1], KDE_GRID_1D)
    density_scale = global_kde_max_for_frames(frames, x_grid)
    display_height = DENSITY_WIDTH_FRACTION  # row spacing is 1

    fig, axes = plt.subplots(
        1,
        3,
        figsize=(FIG_W, FIG_H),
        sharex=True,
        sharey=True,
        constrained_layout=False,
        gridspec_kw={"wspace": WSPACE_3_PANEL},
    )

    for i, (ax, (label, df), letter) in enumerate(zip(axes, da.items(), "ABC")):
        color = DA_COLORS[label]
        prestretches = np.array(sorted(df["prestretch"].dropna().unique()), dtype=float)
        row_pos = np.arange(prestretches.size, dtype=float)

        for y0, p in zip(row_pos, prestretches):
            values = grouped_values_at_x(df, float(p))
            plot_ridgeline_kde(
                ax,
                values,
                float(y0),
                x_grid,
                display_height=display_height,
                density_scale=density_scale,
                color=color,
                zorder=1,
            )

        add_da_underlay_ridgeline(ax, df, alpha=DA_BACKGROUND_ALPHA_RIDGE, zorder=3, show_da_underlay=show_da_underlay)

        panel_label(ax, letter)
        ax.set_title(label, loc="left", pad=5)
        ax.set_xlim(*xlim)
        ax.set_ylim(-0.25, prestretches.size - 1 + display_height + 0.25)
        ax.set_yticks(row_pos)

        if i == 0:
            ax.set_yticklabels([f"{p:.0f}" for p in prestretches])
            ax.set_ylabel("Prestretch force (N)")
        else:
            ax.tick_params(labelleft=False)

        ax.grid(axis="x", color="0.90", linewidth=0.45)
        ax.set_xlabel("")
        ax.tick_params(axis="both", which="major", pad=2.0)
        ax.xaxis.labelpad = 5.0
        ax.yaxis.labelpad = 5.0
        ax.xaxis.set_major_locator(MaxNLocator(nbins=5, prune=None))

    fig.supxlabel("ROM (cm)", y=0.210, fontsize=8.0)
    add_bottom_legend(fig, da_density_legend_handles(show_da_underlay), ncol=5 if show_da_underlay else 4)
    apply_fixed_layout(fig)
    suffix = "_with_underlay" if show_da_underlay else ""
    savefig(fig, f"augmentation_density_ridgeline{suffix}")


def make_augmentation_density_xy_plot(da: dict[str, pd.DataFrame], show_da_underlay:bool=True) -> None:
    """Augmentation densities in data coordinates: x = prestretch force, y = ROM."""
    frames = list(da.values())

    all_prestretches = np.concatenate([df["prestretch"].dropna().unique().astype(float) for df in frames])
    display_width = DENSITY_WIDTH_FRACTION * prestretch_display_spacing(all_prestretches)
    xlim, ylim = finite_xy_limits(frames, x_extra_right=display_width)
    y_grid = np.linspace(ylim[0], ylim[1], KDE_GRID_1D)
    density_scale = global_kde_max_for_frames(frames, y_grid)

    fig, axes = plt.subplots(
        1,
        3,
        figsize=(FIG_W, FIG_H),
        sharex=True,
        sharey=True,
        constrained_layout=False,
        gridspec_kw={"wspace": WSPACE_3_PANEL},
    )

    for i, (ax, (label, df), letter) in enumerate(zip(axes, da.items(), "ABC")):
        color = DA_COLORS[label]
        add_da_underlay_xy(ax, df, alpha=DA_BACKGROUND_ALPHA, zorder=0, show_da_underlay=show_da_underlay)

        for x0 in sorted(df["prestretch"].dropna().unique()):
            values = grouped_values_at_x(df, float(x0))
            plot_conditional_kde_glyph(
                ax,
                values,
                float(x0),
                y_grid,
                display_width=display_width,
                density_scale=density_scale,
                color=color,
                side="right",
                zorder=1,
            )

        panel_label(ax, letter)
        ax.set_title(label, loc="left", pad=5)
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_xlabel("Prestretch force (N)")
        ax.grid(axis="y", color="0.90", linewidth=0.45)
        polish_axes(ax, nbins=4)
        if i == 0:
            ax.set_ylabel("ROM (cm)")
        else:
            ax.tick_params(labelleft=False)

    add_bottom_legend(fig, da_density_legend_handles(show_da_underlay), ncol=5 if show_da_underlay else 4)
    apply_fixed_layout(fig)
    suffix = "_with_underlay" if show_da_underlay else ""
    savefig(fig, f"augmentation_density_xy{suffix}")

#%%
da = load_da()
#xy consistent with other figures
make_augmentation_density_xy_plot(da)
make_augmentation_density_xy_plot(da, False)
#Ridgeline
make_augmentation_density_ridgeline_plot(da)
make_augmentation_density_ridgeline_plot(da, False)

#%%
def cluster_close_prestretches(
    df: pd.DataFrame,
    *,
    tol: float = BO_PRESTRETCH_CLUSTER_TOL,
    max_prestretch: float | None = None,
    best_match_tol: float = BEST_PRESTRETCH_MATCH_TOL,
) -> pd.DataFrame:
    """Select one true DA prestretch per near-duplicate cluster.

    Clustering only avoids overplotting. KDEs are estimated only from the
    selected true prestretch value, not pooled neighboring values.
    """
    unique_p = np.array(sorted(df["prestretch"].dropna().unique()), dtype=float)
    if unique_p.size == 0:
        return pd.DataFrame(columns=[
            "prestretch", "rom", "prestretch_cluster", "selected_prestretch",
            "cluster_id", "cluster_min", "cluster_max", "n_prestretch_values",
        ])

    clusters: list[np.ndarray] = []
    current = [float(unique_p[0])]
    for p in unique_p[1:]:
        p = float(p)
        if p - current[-1] <= tol:
            current.append(p)
        else:
            clusters.append(np.asarray(current, dtype=float))
            current = [p]
    clusters.append(np.asarray(current, dtype=float))

    matched_max_value: float | None = None
    if max_prestretch is not None:
        closest = float(unique_p[np.argmin(np.abs(unique_p - float(max_prestretch)))])
        if abs(closest - float(max_prestretch)) <= best_match_tol:
            matched_max_value = closest
        else:
            raise ValueError(
                "No true DA prestretch value matches the best BO prestretch within "
                f"best_match_tol={best_match_tol}. best BO={max_prestretch:.10g}, nearest DA={closest:.10g}."
            )

    rows = []
    for cluster_id, cluster in enumerate(clusters):
        if matched_max_value is not None and np.any(np.isclose(cluster, matched_max_value, rtol=0.0, atol=GROUP_MATCH_TOL)):
            selected = matched_max_value
        else:
            selected = float(cluster[np.argmin(np.abs(cluster - float(np.median(cluster))))])

        tmp = df.loc[np.isclose(df["prestretch"].to_numpy(dtype=float), selected, rtol=0.0, atol=GROUP_MATCH_TOL), ["prestretch", "rom"]].copy()
        if tmp.empty:
            continue
        tmp["prestretch_cluster"] = selected
        tmp["selected_prestretch"] = selected
        tmp["cluster_id"] = cluster_id
        tmp["cluster_min"] = float(cluster.min())
        tmp["cluster_max"] = float(cluster.max())
        tmp["n_prestretch_values"] = int(cluster.size)
        rows.append(tmp)

    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()


def make_bo_augmentation_overlay_plot(show_da_underlay:bool=True) -> None:
    bo = load_bo_csv()
    bo_da = load_bo_da_predictions()
    best = bo.loc[bo["rom"].idxmax()]
    bo_max = float(best["prestretch"])

    bo_da_selected = cluster_close_prestretches(bo_da, max_prestretch=bo_max)
    cluster_positions = np.array(sorted(bo_da_selected["prestretch_cluster"].unique()), dtype=float)

    display_width = COMBINED_DENSITY_WIDTH_FRACTION * prestretch_display_spacing(cluster_positions)
    xlim, ylim = finite_xy_limits([bo[["prestretch", "rom"]], bo_da[["prestretch", "rom"]]], x_extra_right=display_width)
    y_grid = np.linspace(ylim[0], ylim[1], KDE_GRID_1D)
    density_scale = global_kde_max_for_groups(
        bo_da_selected.rename(columns={"prestretch_cluster": "plot_x"}),
        y_grid,
        x_col="plot_x",
        y_col="rom",
    )

    fig, (ax, ax_leg) = plt.subplots(
        1,
        2,
        figsize=(FIG_W, FIG_H),
        constrained_layout=False,
        gridspec_kw={"width_ratios": [4.8, 1.35], "wspace": 0.18},
    )

    add_da_underlay_xy(ax, bo_da, alpha=DA_BACKGROUND_ALPHA, zorder=0, show_da_underlay=show_da_underlay)

    for x0 in cluster_positions:
        values = grouped_values_at_x(bo_da_selected, float(x0), x_col="prestretch_cluster", y_col="rom")
        plot_conditional_kde_glyph(
            ax,
            values,
            float(x0),
            y_grid,
            display_width=display_width,
            density_scale=density_scale,
            color=COL_DA,
            side="right",
            zorder=1,
        )

    ax.axvline(
        bo_max,
        color=COL_BEST,
        lw=BEST_LINE_LW,
        ls=BEST_LINESTYLE,
        alpha=0.95,
        ymax=0.89,
        zorder=4,
    )

    if BO_HALO:
        ax.scatter(
            bo["prestretch"], bo["rom"],
            marker=BO_MARKER,
            s=BO_OBS_HALO_SIZE,
            color="white",
            linewidth=BO_OBS_HALO_LW,
            alpha=0.95,
            zorder=5,
        )
    ax.scatter(
        bo["prestretch"], bo["rom"],
        marker=BO_MARKER,
        s=BO_OBS_SIZE,
        color=COL_BO,
        linewidth=BO_OBS_LW,
        alpha=BO_OBS_ALPHA,
        zorder=6,
    )

    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xlabel("Prestretch force (N)")
    ax.set_ylabel("ROM (cm)")
    ax.grid(axis="y", color="0.90", linewidth=0.45)
    polish_axes(ax)

    ax_leg.axis("off")
    legend_handles: list = []
    if show_da_underlay:
        legend_handles.append(
            Line2D(
                [0], [0],
                marker="o",
                linestyle="None",
                color=DA_BACKGROUND_COLOR,
                markerfacecolor=DA_BACKGROUND_COLOR,
                markeredgewidth=0,
                alpha=0.8,
                markersize=3.0,
                label="All DA\nsamples",
            )
        )
    legend_handles.extend([
        Patch(
            facecolor=(*mcolors.to_rgb(COL_DA), KDE_GLYPH_FILL_ALPHA),
            edgecolor=(*mcolors.to_rgb(COL_DA), KDE_GLYPH_ALPHA),
            linewidth=0.75,
            label="Selected\nROM density",
        ),
        Line2D([0], [0], color=COL_MEDIAN_LEGEND, lw=KDE_GLYPH_MEDIAN_LW, ls=KDE_GLYPH_MEDIAN_LS, label="DA median"),
        Line2D([0], [0], marker=BO_MARKER, linestyle="None", color=COL_BO, markersize=4.2, markeredgewidth=BO_OBS_LW, label="BO evaluations"),
        Line2D([0], [0], color=COL_BEST, lw=BEST_LINE_LW, ls=BEST_LINESTYLE, label="Best BO\nprestretch"),
    ])
    ax_leg.legend(
        handles=legend_handles,
        loc="center left",
        bbox_to_anchor=(0.0, 0.5),
        frameon=False,
        fontsize=7.0,
        handlelength=1.65,
        handletextpad=0.55,
        labelspacing=1.05,
        borderaxespad=0.0,
    )

    fig.subplots_adjust(left=SUBPLOT_LEFT, right=SUBPLOT_RIGHT, top=SUBPLOT_TOP, bottom=0.185)
    suffix = "_with_underlay" if show_da_underlay else ""
    savefig(fig, f"bo_augmentation_overlay{suffix}")

#%%
make_bo_augmentation_overlay_plot(True)
make_bo_augmentation_overlay_plot(False)