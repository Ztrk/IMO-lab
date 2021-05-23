import matplotlib.pyplot as plt


def draw_arrow(start_pos, end_pos, ax):
    ax.annotate(
        "",
        xy=start_pos,
        xycoords="data",
        xytext=end_pos,
        textcoords="data",
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3"),
    )


def draw_cycle(start, end, points, ax):
    start_node = start
    for i in range(start + 1, end + 1):
        start_pos = points[start_node]
        next_node = i
        end_pos = points[next_node]
        draw_arrow(start_pos, end_pos, ax)
        start_node = next_node

    start_node = start
    start_pos = points[start_node]
    end_pos = points[end]
    draw_arrow(start_pos, end_pos, ax)


def visualize(cycles, coordinates, lengths, total_length, algorithm, instance):
    _fig, ax = plt.subplots()
    instance = instance.split("/")
    name = algorithm + " " + instance[1]
    # ax.set_title(name)
    points = [coordinates[i] for i in cycles[0]] + [coordinates[i] for i in cycles[1]]
    ax.scatter(
        [points[i][0] for i in range(len(points))],
        [points[i][1] for i in range(len(points))],
    )

    draw_cycle(0, len(cycles[0]) - 1, points, ax)
    draw_cycle(len(cycles[0]), len(cycles[0]) + len(cycles[1]) - 1, points, ax)

    textstr = (
        "Całkowita długość cyklu 1: "
        + str(lengths[0])
        + ", cylku 2: "
        + str(lengths[1])
        + ", obu cylki: "
        + str(total_length)
    )
    props = dict(boxstyle="round", facecolor="wheat", alpha=0.5)
    ax.text(
        0.01,
        0.99,
        textstr,
        transform=ax.transAxes,
        fontsize=8,
        verticalalignment="top",
        bbox=props,
    )

    plt.tight_layout()
    plt.savefig(name + ".png", dpi=300)
    plt.show()
