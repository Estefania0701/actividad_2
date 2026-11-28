import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import numpy as np

from matplotlib.lines import Line2D
from matplotlib.patches import Circle
from matplotlib.transforms import Bbox
from pathlib import Path


# ============================================================
# 1. SYSTEM CONFIGURATION
# ============================================================

COLORS = {
    "central": "#E53935",
    "coastal": "#1976D2",
    "university": "#269B50",
    "background": "#FAFBFD",
    "text": "#263238",
    "transfer": "#172F4F",
    "secondary": "#64748B"
}

LINES = {
    "Línea Central": {
        "color": COLORS["central"],
        "stations": [
            "Aurora",
            "Central Park",
            "Distrito Financiero",
            "Plaza Mayor",
            "Universidad",
            "Puerto Norte"
        ]
    },
    "Línea Costera": {
        "color": COLORS["coastal"],
        "stations": [
            "Bahía Sur",
            "Jardines",
            "Plaza Mayor",
            "Museo",
            "Estadio",
            "Puerto Norte"
        ]
    },
    "Línea Universitaria": {
        "color": COLORS["university"],
        "stations": [
            "Bosque Este",
            "Universidad",
            "Mercado Central",
            "Museo",
            "Aeropuerto",
            "Colinas"
        ]
    }
}

TRAVEL_TIMES = {
    "Línea Central": [4, 5, 4, 3, 5],
    "Línea Costera": [5, 4, 6, 5, 4],
    "Línea Universitaria": [6, 5, 4, 6, 5]
}

TRANSFER_TIME = 4  # minutos


# ============================================================
# 2. UNIQUE STATION COORDINATES
# ============================================================

STATIONS = {
    "Aurora": (0, 5),
    "Central Park": (0, 4),
    "Distrito Financiero": (0, 3),
    "Plaza Mayor": (0, 2),
    "Universidad": (0, 0),
    "Puerto Norte": (0, -2),

    "Bahía Sur": (-5, 2.6),
    "Jardines": (-3, 2.6),
    "Museo": (3, 0),
    "Estadio": (4.7, -0.8),

    "Bosque Este": (-2.5, -1),
    "Mercado Central": (1.2, 2.7),
    "Aeropuerto": (4.4, 2),
    "Colinas": (5.8, 3.4)
}


# ============================================================
# 3. TRANSFER STATIONS
# ============================================================

TRANSFER_STATIONS = {
    "Plaza Mayor",
    "Universidad",
    "Museo",
    "Puerto Norte"
}


# ============================================================
# 4. ROUTE GEOMETRY
# ============================================================

ROUTES = {
    "Línea Central": [
        STATIONS["Aurora"],
        STATIONS["Central Park"],
        STATIONS["Distrito Financiero"],
        STATIONS["Plaza Mayor"],
        STATIONS["Universidad"],
        STATIONS["Puerto Norte"]
    ],

    "Línea Costera": [
        STATIONS["Bahía Sur"],
        STATIONS["Jardines"],
        STATIONS["Plaza Mayor"],
        (1.2, 1.2),
        (2.2, 0.3),
        STATIONS["Museo"],
        STATIONS["Estadio"],
        STATIONS["Puerto Norte"]
    ],

    "Línea Universitaria": [
        STATIONS["Bosque Este"],
        STATIONS["Universidad"],
        (-0.5, 0.8),
        (-0.5, 2.5),
        STATIONS["Mercado Central"],
        (2.2, 2.7),
        (3.5, 1.5),
        STATIONS["Museo"],
        (3.6, 1.0),
        STATIONS["Aeropuerto"],
        STATIONS["Colinas"]
    ]
}


# ============================================================
# 5. PREFERRED LABEL POSITIONS (starting point only)
# ============================================================

# (dx, dy, ha, va). The algorithm tries these first and moves the label
# to another position only if there is a collision.

PREFERRED_POSITIONS = {
    "Aurora": (14, 0, "left", "center"),
    "Central Park": (14, 0, "left", "center"),
    "Distrito Financiero": (14, 0, "left", "center"),
    "Plaza Mayor": (-14, 0, "right", "center"),
    "Universidad": (-14, 0, "right", "center"),
    "Puerto Norte": (14, 0, "left", "center"),

    "Bahía Sur": (0, -14, "center", "top"),
    "Jardines": (0, -14, "center", "top"),
    "Museo": (14, -8, "left", "top"),
    "Estadio": (14, 0, "left", "center"),

    "Bosque Este": (-14, -8, "right", "top"),
    "Mercado Central": (0, 14, "center", "bottom"),
    "Aeropuerto": (14, 0, "left", "center"),
    "Colinas": (14, 0, "left", "center"),
}


# ============================================================
# 6. VALIDATE NETWORK STRUCTURE
# ============================================================

all_station_occurrences = [
    station
    for line in LINES.values()
    for station in line["stations"]
]

assert len(all_station_occurrences) == 18
assert len(STATIONS) == 14

for line_name, line in LINES.items():
    assert len(line["stations"]) == 6
    assert all(
        station in STATIONS
        for station in line["stations"]
    )

print(f"Total station occurrences: {len(all_station_occurrences)}")
print(f"Unique physical stations: {len(STATIONS)}")
print(f"Transfer stations: {len(TRANSFER_STATIONS)}")


# ============================================================
# 7. CREATE FIGURE
# ============================================================

fig, ax = plt.subplots(figsize=(16, 9))

fig.patch.set_facecolor(COLORS["background"])
ax.set_facecolor(COLORS["background"])

ax.set_xlim(-6, 7)
ax.set_ylim(-3, 6)

ax.set_aspect("equal")
ax.axis("off")


# ============================================================
# 8. DRAW METRO LINES
# ============================================================

for line_name, route in ROUTES.items():

    color = LINES[line_name]["color"]

    x_coordinates = [point[0] for point in route]
    y_coordinates = [point[1] for point in route]

    ax.plot(
        x_coordinates,
        y_coordinates,
        color=color,
        linewidth=5,
        solid_capstyle="round",
        solid_joinstyle="round",
        zorder=1
    )


# ============================================================
# 8.1. DRAW TRAVEL TIME BADGES BETWEEN STATIONS
# ============================================================

def get_path_midpoint(points):
    """Calcula el punto medio geométrico a lo largo de una polilínea."""
    if len(points) == 2:
        return ((points[0][0] + points[1][0]) / 2.0, (points[0][1] + points[1][1]) / 2.0)

    segments = []
    total_dist = 0.0
    for p0, p1 in zip(points[:-1], points[1:]):
        dist = float(np.hypot(p1[0] - p0[0], p1[1] - p0[1]))
        segments.append((p0, p1, dist))
        total_dist += dist

    half_dist = total_dist / 2.0
    accum = 0.0
    for p0, p1, dist in segments:
        if accum + dist >= half_dist:
            ratio = (half_dist - accum) / dist if dist > 0 else 0
            mx = p0[0] + ratio * (p1[0] - p0[0])
            my = p0[1] + ratio * (p1[1] - p0[1])
            return (mx, my)
        accum += dist
    return points[-1]


time_badge_texts = []

for line_name, line_info in LINES.items():
    color = line_info["color"]
    stations = line_info["stations"]
    route = ROUTES[line_name]
    times = TRAVEL_TIMES[line_name]

    for i in range(len(stations) - 1):
        s_from = stations[i]
        s_to = stations[i + 1]
        t = times[i]

        p_from = STATIONS[s_from]
        p_to = STATIONS[s_to]

        idx_from = next(idx for idx, p in enumerate(route) if np.allclose(p, p_from))
        idx_to = next(idx for idx, p in enumerate(route) if np.allclose(p, p_to))

        if idx_from < idx_to:
            subroute = route[idx_from:idx_to + 1]
        else:
            subroute = route[idx_to:idx_from + 1][::-1]

        mid_x, mid_y = get_path_midpoint(subroute)

        badge = ax.text(
            mid_x,
            mid_y,
            f"{t} min",
            fontsize=8,
            fontweight="bold",
            color=color,
            ha="center",
            va="center",
            zorder=6,
            bbox=dict(
                boxstyle="round,pad=0.25,rounding_size=0.4",
                facecolor="white",
                edgecolor=color,
                linewidth=1.2,
                alpha=0.95
            )
        )
        time_badge_texts.append(badge)


# ============================================================
# 9. DRAW STATIONS
# ============================================================

MARKER_RADIUS = {}  # radius in data units, used for collision checks

for station_name, (x, y) in STATIONS.items():

    if station_name in TRANSFER_STATIONS:

        MARKER_RADIUS[station_name] = 0.15

        # Outer transfer ring
        ax.add_patch(
            Circle(
                (x, y),
                radius=0.15,
                facecolor="white",
                edgecolor=COLORS["transfer"],
                linewidth=3,
                zorder=5
            )
        )

        # Inner ring
        ax.add_patch(
            Circle(
                (x, y),
                radius=0.075,
                facecolor="white",
                edgecolor=COLORS["transfer"],
                linewidth=2,
                zorder=6
            )
        )

    else:

        MARKER_RADIUS[station_name] = 0.105

        # Regular station
        station_color = next(
            LINES[ln]["color"]
            for ln, line in LINES.items()
            if station_name in line["stations"]
        )

        ax.add_patch(
            Circle(
                (x, y),
                radius=0.105,
                facecolor="white",
                edgecolor=station_color,
                linewidth=3,
                zorder=5
            )
        )


# ============================================================
# 10. TITLE AND SUBTITLE
# ============================================================

ax.text(
    -5.8,
    5.75,
    "NEXUS METRO",
    fontsize=25,
    fontweight="bold",
    color=COLORS["transfer"],
    ha="left"
)

ax.text(
    -5.8,
    5.35,
    "NOVA CITY  |  TRANSPORT NETWORK",
    fontsize=11,
    color=COLORS["secondary"],
    ha="left"
)


# ============================================================
# 11. LEGEND
# ============================================================

legend_elements = []

for line_name, line in LINES.items():

    legend_elements.append(
        Line2D(
            [0],
            [0],
            color=line["color"],
            linewidth=4,
            marker="o",
            markersize=8,
            markerfacecolor="white",
            markeredgewidth=2,
            label=line_name
        )
    )

legend_elements.append(
    Line2D(
        [0],
        [0],
        color="white",
        marker="o",
        markerfacecolor="white",
        markeredgecolor=COLORS["transfer"],
        markeredgewidth=2,
        markersize=10,
        label=f"Estación de transbordo ({TRANSFER_TIME} min)"
    )
)

legend_elements.append(
    Line2D(
        [0],
        [0],
        color="none",
        marker="s",
        markerfacecolor="white",
        markeredgecolor=COLORS["secondary"],
        markeredgewidth=1.2,
        markersize=9,
        label="Tiempo entre estaciones"
    )
)

legend = ax.legend(
    handles=legend_elements,
    loc="lower left",
    bbox_to_anchor=(0.01, 0.01),
    frameon=True,
    facecolor="white",
    edgecolor="#DCE2EA",
    fontsize=10,
    title="LEYENDA",
    title_fontsize=11
)


# ============================================================
# 12. DRAW STATION LABELS (automatic overlap avoidance)
# ============================================================

# Render once so text sizes and transforms are available.
fig.canvas.draw()
renderer = fig.canvas.get_renderer()

PAD = 3  # extra pixels around each label


def candidate_positions():
    """Candidate offsets (in points): near ring first, then farther rings."""
    candidates = []
    for d in (14, 24, 36):
        diag = d * 0.75
        candidates += [
            (d, 0, "left", "center"),
            (-d, 0, "right", "center"),
            (0, d, "center", "bottom"),
            (0, -d, "center", "top"),
            (diag, diag, "left", "bottom"),
            (-diag, diag, "right", "bottom"),
            (diag, -diag, "left", "top"),
            (-diag, -diag, "right", "top"),
        ]
    return candidates


def to_display(point):
    return ax.transData.transform(point)


# --- Obstacles in display (pixel) coordinates ---

# a) Marker bounding boxes
marker_boxes = []
for name, (x, y) in STATIONS.items():
    cx, cy = to_display((x, y))
    rx = abs(to_display((x + MARKER_RADIUS[name], y))[0] - cx) + 4
    marker_boxes.append(Bbox.from_extents(cx - rx, cy - rx, cx + rx, cy + rx))

# b) Points sampled along every route
line_samples = []
for route in ROUTES.values():
    pts = np.array([to_display(p) for p in route])
    for p0, p1 in zip(pts[:-1], pts[1:]):
        n = max(int(np.hypot(*(p1 - p0)) / 4), 2)
        t = np.linspace(0, 1, n)[:, None]
        line_samples.append(p0 + (p1 - p0) * t)
line_samples = np.vstack(line_samples)

# c) Legend box and axes area
legend_box = legend.get_window_extent(renderer).expanded(1.05, 1.15)
axes_box = ax.get_window_extent(renderer)

# d) Travel time badge boxes
badge_boxes = [
    t.get_window_extent(renderer).expanded(1.1, 1.1)
    for t in time_badge_texts
]


def label_cost(bbox, placed_boxes, rank):
    """Lower cost = better position."""
    cost = rank * 0.3  # small preference for earlier candidates

    # Overlap with other labels
    cost += 1000 * sum(bbox.overlaps(other) for other in placed_boxes)

    # Overlap with station markers
    cost += 1000 * sum(bbox.overlaps(m) for m in marker_boxes)

    # Overlap with travel time badges
    cost += 1000 * sum(bbox.overlaps(b) for b in badge_boxes)

    # Overlap with legend
    if bbox.overlaps(legend_box):
        cost += 1000

    # Outside the drawing area
    if (bbox.x0 < axes_box.x0 or bbox.x1 > axes_box.x1
            or bbox.y0 < axes_box.y0 or bbox.y1 > axes_box.y1):
        cost += 1000

    # Overlap with metro lines (less severe)
    inside = (
        (line_samples[:, 0] >= bbox.x0) & (line_samples[:, 0] <= bbox.x1) &
        (line_samples[:, 1] >= bbox.y0) & (line_samples[:, 1] <= bbox.y1)
    )
    cost += 2 * inside.sum()

    return cost


# Transfer stations first (most crowded), then the rest.
ordered_stations = (
    [s for s in STATIONS if s in TRANSFER_STATIONS] +
    [s for s in STATIONS if s not in TRANSFER_STATIONS]
)

placed_boxes = []

for station_name in ordered_stations:

    x, y = STATIONS[station_name]

    if station_name in TRANSFER_STATIONS:
        display_text = f"{station_name}\n(Transbordo: {TRANSFER_TIME} min)"
        font_size = 7
        font_color = COLORS["transfer"]
    else:
        display_text = station_name
        font_size = 8
        font_color = next(
            LINES[ln]["color"]
            for ln, line in LINES.items()
            if station_name in line["stations"]
        )

    text = ax.annotate(
        display_text,
        xy=(x, y),
        xytext=(0, 0),
        textcoords="offset points",
        fontsize=font_size,
        fontweight="semibold",
        color=font_color,
        ha="left",
        va="center",
        zorder=10,
        path_effects=[
            pe.withStroke(linewidth=3, foreground=COLORS["background"])
        ]
    )

    candidates = [PREFERRED_POSITIONS[station_name]] + candidate_positions()

    best = None

    for rank, (dx, dy, ha, va) in enumerate(candidates):

        text.xyann = (dx, dy)
        text.set_ha(ha)
        text.set_va(va)

        bbox = text.get_window_extent(renderer).expanded(
            1.0, 1.0
        )
        bbox = Bbox.from_extents(
            bbox.x0 - PAD, bbox.y0 - PAD,
            bbox.x1 + PAD, bbox.y1 + PAD
        )

        cost = label_cost(bbox, placed_boxes, rank)

        if best is None or cost < best[0]:
            best = (cost, (dx, dy, ha, va), bbox)

        if cost < 1:  # perfect position, stop searching
            break

    cost, (dx, dy, ha, va), bbox = best

    text.xyann = (dx, dy)
    text.set_ha(ha)
    text.set_va(va)

    placed_boxes.append(bbox)

    if cost >= 1000:
        print(f"Aviso: no se encontró posición libre para '{station_name}'")


# ============================================================
# 13. FOOTER
# ============================================================

ax.text(
    6.8,
    -2.8,
    "NEXUS METRO | NOVA CITY",
    fontsize=8,
    color=COLORS["secondary"],
    ha="right"
)


# ============================================================
# 14. EXPORT AND DISPLAY
# ============================================================

assets_dir = Path(__file__).resolve().parent.parent / "assets"
assets_dir.mkdir(parents=True, exist_ok=True)
output_path = assets_dir / "nexus_metro_map.png"

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight",
    facecolor=fig.get_facecolor()
)
print(f"Mapa guardado en: {output_path}")

plt.show()
