import re
from pathlib import Path

import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
import torch
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import MaxNLocator
from scipy.stats import gaussian_kde

# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------

SAVE_PLOTS = True
SHOW_PLOTS = False
SAVE_PDF = True
SAVE_PNG = True

DATA_DIR = Path("data")
BO_DIR = DATA_DIR / "bo_results"
DA_DIR = DATA_DIR / "data_augmentation_results"

BO_CSV = BO_DIR / "bo_cuboid.csv"
BO_DA_CSV = DA_DIR / "bo_prestretches_3764.csv"

DA_FILES = {
    "100 samples": DA_DIR / "uniform_prestretches_100.csv",
    "500 samples": DA_DIR / "uniform_prestretches_500.csv",
    "Full dataset": DA_DIR / "uniform_prestretches_3764.csv",
}

OUT_DIR = Path(__file__).resolve().parent / "paper_figures"
OUT_DIR.mkdir(exist_ok=True)

# -----------------------------------------------------------------------------
# Layout
# -----------------------------------------------------------------------------

FIG_W = 7.10
FIG_H = 3.25

SUBPLOT_LEFT = 0.085
SUBPLOT_RIGHT = 0.985
SUBPLOT_TOP = 0.855
SUBPLOT_BOTTOM = 0.305
WSPACE_3_PANEL = 0.16

LEGEND_Y = 0.082
LEGEND_HANDLE_LENGTH = 1.65
LEGEND_COL_SPACING = 1.05
LEGEND_HANDLE_TEXT_PAD = 0.45

PANEL_LABEL_X = -0.105
PANEL_LABEL_Y = 1.095
SAVE_PAD_INCHES = 0.02

# -----------------------------------------------------------------------------
# Colors and visual grammar
# -----------------------------------------------------------------------------

# BO / GP
COL_GP = "#3F7F93"
COL_GP_BAND = "#E8F1F4"
GP_BAND_ALPHA = 0.85
GP_LW = 1.5

COL_BO = "black"
COL_BEST = "#2B2B2B"
COL_NEXT = "#D55E00"
COL_MEDIAN_LEGEND = "black"

BO_MARKER = "+"
BO_OBS_SIZE = 40
BO_OBS_LW = 0.9
BO_OBS_ALPHA = 1
BO_HALO = False
BO_OBS_HALO_SIZE = BO_OBS_SIZE + 10
BO_OBS_HALO_LW = BO_OBS_LW + 0.3

BEST_LINESTYLE = (0, (1.2, 1.8))
NEXT_LINESTYLE = (0, (1.2, 1.8))
BEST_LINE_LW = 1.3
NEXT_LINE_LW = 1.05

# DA
DA_COLORS = {
    "100 samples": "#C76E5A",  # terracotta
    "500 samples": "#7A6F9B",  # muted violet
    "Full dataset": "#1F77B4",  # blue
}
COL_DA = DA_COLORS["Full dataset"]

DA_BACKGROUND_COLOR = "#6E6E6E"
DA_BACKGROUND_SIZE = 2.0
DA_BACKGROUND_ALPHA = 0.2
DA_BACKGROUND_RASTERIZED = True
DA_BACKGROUND_ALPHA_RIDGE = 0.2

# KDE density glyphs
KDE_BW_1D = 0.22
KDE_GRID_1D = 512
KDE_MIN_N_1D = 3
KDE_DISPLAY_EPS = 0.004
DENSITY_WIDTH_FRACTION = 1
COMBINED_DENSITY_WIDTH_FRACTION = 1
KDE_GLYPH_LW = 1.0
KDE_GLYPH_ALPHA = 0.95
KDE_GLYPH_FILL_ALPHA = 0.18
KDE_GLYPH_MEDIAN_LW = 0.85
KDE_GLYPH_MEDIAN_LS = (0, (2.2, 1.6))

# Matching / clustering
BO_PRESTRETCH_CLUSTER_TOL = 1.0  # N; only for display selection in Fig. 5
GROUP_MATCH_TOL = 1e-7  # exact grouping of true DA prestretches
BEST_PRESTRETCH_MATCH_TOL = 1e-1  # only for matching BO best to rounded DA file values

# Axis padding
X_LIMIT_PAD_FRAC = 0.06
Y_LIMIT_PAD_FRAC = 0.08

# -----------------------------------------------------------------------------
# Matplotlib style
# -----------------------------------------------------------------------------

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans"],
    "font.size": 8.0,
    "axes.labelsize": 8.0,
    "axes.titlesize": 8.5,
    "axes.titlelocation": "left",
    "legend.fontsize": 7.0,
    "xtick.labelsize": 7.0,
    "ytick.labelsize": 7.0,
    "axes.labelpad": 5.0,
    "axes.titlepad": 3.0,
    "xtick.major.pad": 2.0,
    "ytick.major.pad": 2.0,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.7,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "xtick.major.size": 3.0,
    "ytick.major.size": 3.0,
    "xtick.major.width": 0.7,
    "ytick.major.width": 0.7,
    "lines.linewidth": 1.0,
    "patch.linewidth": 0.7,
    "legend.frameon": False,
    "legend.borderaxespad": 0.0,
    "legend.handlelength": LEGEND_HANDLE_LENGTH,
    "legend.handletextpad": LEGEND_HANDLE_TEXT_PAD,
    "legend.columnspacing": LEGEND_COL_SPACING,
    "figure.figsize": (FIG_W, FIG_H),
    "figure.dpi": 150,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.dpi": 600,
    "savefig.bbox": None,
    "savefig.pad_inches": SAVE_PAD_INCHES,
    "savefig.facecolor": "white",
    "savefig.edgecolor": "none",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})


def savefig(fig: plt.Figure, name: str, size: tuple[float, float] = (FIG_W, FIG_H)) -> None:
    fig.set_size_inches(*size, forward=True)

    if SAVE_PLOTS:
        if SAVE_PDF:
            fig.savefig(OUT_DIR / f"{name}.pdf", bbox_inches=None, pad_inches=SAVE_PAD_INCHES)
        if SAVE_PNG:
            fig.savefig(OUT_DIR / f"{name}.png", bbox_inches=None, pad_inches=SAVE_PAD_INCHES)

    if SHOW_PLOTS:
        plt.show()
    else:
        plt.close(fig)


def apply_fixed_layout(fig: plt.Figure, *, bottom: float = SUBPLOT_BOTTOM) -> None:
    fig.set_size_inches(FIG_W, FIG_H, forward=True)
    fig.subplots_adjust(
        left=SUBPLOT_LEFT,
        right=SUBPLOT_RIGHT,
        top=SUBPLOT_TOP,
        bottom=bottom,
    )


def add_bottom_legend(fig: plt.Figure, handles: list, ncol: int, y: float = LEGEND_Y) -> None:
    fig.legend(
        handles=handles,
        loc="lower center",
        bbox_to_anchor=(0.5, y),
        bbox_transform=fig.transFigure,
        ncol=ncol,
        frameon=False,
        handlelength=LEGEND_HANDLE_LENGTH,
        handletextpad=LEGEND_HANDLE_TEXT_PAD,
        columnspacing=LEGEND_COL_SPACING,
        borderaxespad=0.0,
        alignment="center",
    )


def panel_label(ax: plt.Axes, label: str) -> None:
    ax.text(
        PANEL_LABEL_X,
        PANEL_LABEL_Y,
        label,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=9.0,
        fontweight="bold",
        clip_on=False,
    )


def polish_axes(ax: plt.Axes, nbins: int = 5) -> None:
    ax.tick_params(axis="both", which="major", pad=2.0)
    ax.xaxis.labelpad = 5.0
    ax.yaxis.labelpad = 5.0
    ax.xaxis.set_major_locator(MaxNLocator(nbins=nbins, prune=None))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=nbins, prune=None))


def strip_unnamed_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[:, ~df.columns.str.match(r"^Unnamed")]


def rename_result_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns={"prestretch_force": "prestretch", "range_of_motion": "rom"})


def tensor_to_numpy(x) -> np.ndarray | None:
    if x is None:
        return None
    if hasattr(x, "detach"):
        return x.detach().cpu().numpy()
    return np.asarray(x)


def clean_xy(x: np.ndarray, *ys: np.ndarray):
    data = {"x": np.asarray(x, dtype=float).reshape(-1)}
    for i, y in enumerate(ys):
        data[f"y{i}"] = np.asarray(y, dtype=float).reshape(-1)

    df = pd.DataFrame(data).replace([np.inf, -np.inf], np.nan).dropna()
    df = df.groupby("x", as_index=False).mean().sort_values("x")

    return [df["x"].to_numpy()] + [df[f"y{i}"].to_numpy() for i in range(len(ys))]


def finite_xy_limits(frames: list[pd.DataFrame], *, x_extra_right: float = 0.0) -> tuple[
    tuple[float, float], tuple[float, float]]:
    all_df = (
        pd.concat(frames, ignore_index=True)
        .replace([np.inf, -np.inf], np.nan)
        .dropna(subset=["prestretch", "rom"])
    )
    if all_df.empty:
        raise ValueError("Cannot compute plot limits from empty data.")

    x_min = float(all_df["prestretch"].min())
    x_max = float(all_df["prestretch"].max())
    y_min = float(all_df["rom"].min())
    y_max = float(all_df["rom"].max())

    x_span = max(x_max - x_min, 1.0)
    y_span = max(y_max - y_min, 1.0)

    return (
        (x_min - X_LIMIT_PAD_FRAC * x_span, x_max + x_extra_right + X_LIMIT_PAD_FRAC * x_span),
        (y_min - Y_LIMIT_PAD_FRAC * y_span, y_max + Y_LIMIT_PAD_FRAC * y_span),
    )


def kde_1d_on_grid(values: np.ndarray, grid: np.ndarray, *, bw_method: str | float = KDE_BW_1D) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]

    if values.size < KDE_MIN_N_1D or np.nanstd(values) <= np.finfo(float).eps:
        return np.zeros_like(grid, dtype=float)

    try:
        density = gaussian_kde(values, bw_method=bw_method)(grid)
    except Exception:
        return np.zeros_like(grid, dtype=float)

    density = np.asarray(density, dtype=float)
    density[~np.isfinite(density)] = 0.0
    density[density < 0] = 0.0
    return density


def prestretch_display_spacing(prestretches: np.ndarray, *, fallback: float = 1.0) -> float:
    prestretches = np.asarray(sorted(np.unique(prestretches)), dtype=float)
    if prestretches.size < 2:
        return fallback

    spacing = np.diff(prestretches)
    spacing = spacing[np.isfinite(spacing) & (spacing > GROUP_MATCH_TOL)]
    return float(np.min(spacing)) if spacing.size else fallback


def grouped_values_at_x(
        df: pd.DataFrame,
        x0: float,
        *,
        x_col: str = "prestretch",
        y_col: str = "rom",
        match_tol: float = GROUP_MATCH_TOL,
) -> np.ndarray:
    mask = np.isclose(df[x_col].to_numpy(dtype=float), x0, rtol=0.0, atol=match_tol)
    return df.loc[mask, y_col].to_numpy(dtype=float)


def global_kde_max_for_groups(
        df: pd.DataFrame,
        y_grid: np.ndarray,
        *,
        x_col: str = "prestretch",
        y_col: str = "rom",
        bw_method: str | float = KDE_BW_1D,
) -> float:
    max_density = 0.0
    for x0 in sorted(df[x_col].dropna().unique()):
        values = grouped_values_at_x(df, float(x0), x_col=x_col, y_col=y_col)
        dens = kde_1d_on_grid(values, y_grid, bw_method=bw_method)
        if dens.size:
            max_density = max(max_density, float(np.nanmax(dens)))
    return max_density


def global_kde_max_for_frames(frames: list[pd.DataFrame], y_grid: np.ndarray) -> float:
    return max(global_kde_max_for_groups(df, y_grid) for df in frames)


def add_da_underlay_xy(ax: plt.Axes, df: pd.DataFrame, *, alpha: float = DA_BACKGROUND_ALPHA, zorder: float = 0,
                       show_da_underlay=True) -> None:
    if not show_da_underlay:
        return
    ax.scatter(
        df["prestretch"],
        df["rom"],
        s=DA_BACKGROUND_SIZE,
        color=DA_BACKGROUND_COLOR,
        alpha=alpha,
        linewidth=0,
        rasterized=DA_BACKGROUND_RASTERIZED,
        zorder=zorder,
    )


def add_da_underlay_ridgeline(ax: plt.Axes, df: pd.DataFrame, *, alpha: float = DA_BACKGROUND_ALPHA_RIDGE,
                              zorder: float = 3, show_da_underlay=True) -> None:
    if not show_da_underlay:
        return

    prestretches = np.array(sorted(df["prestretch"].dropna().unique()), dtype=float)
    if prestretches.size == 0:
        return

    row_index = {p: i for i, p in enumerate(prestretches)}
    y = np.array([row_index[p] for p in df["prestretch"].to_numpy(dtype=float)], dtype=float)

    ax.scatter(
        df["rom"].to_numpy(dtype=float),
        y,
        s=DA_BACKGROUND_SIZE,
        color=DA_BACKGROUND_COLOR,
        alpha=alpha,
        linewidth=0,
        rasterized=DA_BACKGROUND_RASTERIZED,
        zorder=zorder,
    )


def plot_ridgeline_kde(
        ax: plt.Axes,
        values: np.ndarray,
        y0: float,
        x_grid: np.ndarray,
        *,
        display_height: float,
        density_scale: float,
        color: str,
        fill_alpha: float = KDE_GLYPH_FILL_ALPHA,
        zorder: float = 1,
) -> None:
    """Draw one conditional ROM KDE as a ridgeline ridge."""
    if density_scale <= 0 or display_height <= 0:
        return

    dens = kde_1d_on_grid(values, x_grid)
    if dens.max() <= 0:
        return

    displacement = dens / density_scale * display_height
    visible = displacement >= KDE_DISPLAY_EPS * display_height
    if visible.sum() < 3:
        return

    xv = x_grid[visible]
    yv = y0 + displacement[visible]
    face_rgba = (*mcolors.to_rgb(color), fill_alpha)
    edge_rgba = (*mcolors.to_rgb(color), KDE_GLYPH_ALPHA)

    ax.fill_between(xv, y0, yv, color=face_rgba, linewidth=0, zorder=zorder)
    ax.plot(xv, yv, color=edge_rgba, lw=KDE_GLYPH_LW, zorder=zorder + 1)

    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if values.size:
        median = float(np.median(values))
        median_height = float(np.interp(median, x_grid, displacement))
        ax.plot(
            [median, median],
            [y0, y0 + median_height],
            color=color,
            lw=KDE_GLYPH_MEDIAN_LW,
            ls=KDE_GLYPH_MEDIAN_LS,
            solid_capstyle="butt",
            zorder=zorder + 2,
        )


def plot_conditional_kde_glyph(
        ax: plt.Axes,
        values_y: np.ndarray,
        x0: float,
        y_grid: np.ndarray,
        *,
        display_width: float,
        density_scale: float,
        color: str,
        fill_alpha: float = KDE_GLYPH_FILL_ALPHA,
        side: str = "right",
        zorder: float = 1,
        draw_median: bool = True,
) -> None:
    """Draw p(y | x=x0) using one shared figure-level density scale."""
    if side not in {"right", "left", "both"}:
        raise ValueError("side must be 'right', 'left', or 'both'.")
    if density_scale <= 0 or display_width <= 0:
        return

    values_y = np.asarray(values_y, dtype=float)
    values_y = values_y[np.isfinite(values_y)]
    dens = kde_1d_on_grid(values_y, y_grid)
    if dens.max() <= 0:
        return

    displacement = dens / density_scale * display_width
    visible = displacement >= KDE_DISPLAY_EPS * display_width
    if visible.sum() < 3:
        return

    yv = y_grid[visible]
    dv = displacement[visible]

    if side == "right":
        x_left = np.full_like(yv, x0, dtype=float)
        x_right = x0 + dv
        median_start, median_end = 0.0, 1.0
    elif side == "left":
        x_left = x0 - dv
        x_right = np.full_like(yv, x0, dtype=float)
        median_start, median_end = -1.0, 0.0
    else:
        x_left = x0 - dv
        x_right = x0 + dv
        median_start, median_end = -1.0, 1.0

    face_rgba = (*mcolors.to_rgb(color), fill_alpha)
    edge_rgba = (*mcolors.to_rgb(color), KDE_GLYPH_ALPHA)

    ax.fill_betweenx(yv, x_left, x_right, color=face_rgba, linewidth=0, zorder=zorder)
    if side in {"left", "both"}:
        ax.plot(x_left, yv, color=edge_rgba, lw=KDE_GLYPH_LW, zorder=zorder + 1)
    if side in {"right", "both"}:
        ax.plot(x_right, yv, color=edge_rgba, lw=KDE_GLYPH_LW, zorder=zorder + 1)

    if draw_median and values_y.size:
        median = float(np.median(values_y))
        median_width = float(np.interp(median, y_grid, displacement))
        ax.plot(
            [x0 + median_start * median_width, x0 + median_end * median_width],
            [median, median],
            color=color,
            lw=KDE_GLYPH_MEDIAN_LW,
            ls=KDE_GLYPH_MEDIAN_LS,
            solid_capstyle="butt",
            zorder=zorder + 2,
        )


def da_density_legend_handles(show_da_underlay=True) -> list:
    handles: list = []
    if show_da_underlay:
        handles.append(
            Line2D(
                [0], [0],
                marker="o",
                linestyle="None",
                color=DA_BACKGROUND_COLOR,
                markerfacecolor=DA_BACKGROUND_COLOR,
                markeredgewidth=0,
                alpha=0.65,
                markersize=3.0,
                label="DA samples",
            )
        )

    for label, color in DA_COLORS.items():
        handles.append(
            Patch(
                facecolor=(*mcolors.to_rgb(color), KDE_GLYPH_FILL_ALPHA),
                edgecolor=(*mcolors.to_rgb(color), KDE_GLYPH_ALPHA),
                linewidth=0.75,
                label=label,
            )
        )

    handles.append(
        Line2D(
            [0], [0],
            color=COL_MEDIAN_LEGEND,
            lw=KDE_GLYPH_MEDIAN_LW,
            ls=KDE_GLYPH_MEDIAN_LS,
            label="median",
        )
    )
    return handles


def load_bo_csv() -> pd.DataFrame:
    df = rename_result_columns(pd.read_csv(BO_CSV))
    df = df[["prestretch", "rom"]].dropna().copy()
    df["iteration"] = np.arange(1, len(df) + 1)
    df["best_so_far"] = df["rom"].cummax()
    return df[["iteration", "prestretch", "rom", "best_so_far"]]


def load_da() -> dict[str, pd.DataFrame]:
    out: dict[str, pd.DataFrame] = {}
    for label, path in DA_FILES.items():
        df = strip_unnamed_columns(pd.read_csv(path))
        df = rename_result_columns(df)
        out[label] = df[["prestretch", "rom"]].dropna().copy()
    return out


def load_bo_da_predictions() -> pd.DataFrame:
    df = strip_unnamed_columns(pd.read_csv(BO_DA_CSV))
    df = rename_result_columns(df)
    return df[["prestretch", "rom"]].dropna().copy()


def checkpoint_iteration(path: Path) -> int:
    match = re.search(r"iter_(\d+)", path.name)
    if not match:
        raise ValueError(f"Could not parse BO iteration from {path}")
    return int(match.group(1))


def load_bo_checkpoints() -> dict[int, dict]:
    checkpoints: dict[int, dict] = {}
    for path in sorted(BO_DIR.glob("*.pt")):
        if path.name.startswith("._"):
            continue
        chk = torch.load(path, map_location="cpu", weights_only=False)
        iteration = int(chk.get("iter", checkpoint_iteration(path)))
        checkpoints[iteration] = chk
    return checkpoints
