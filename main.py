import numpy as np

from graph import (
    add_basis_vectors,
    add_origin,
    plot_lattice,
    plot_parent_and_sublattice,
    plot_primal_and_dual,
)
from lattice_math import Lattice


Z2 = Lattice(np.eye(2))

fig = plot_lattice(
    Z2,
    radius=2,
    title="Z^2: lattice",
)

add_origin(fig)
fig.fig.show()

add_basis_vectors(fig, Z2, radius=2)
fig.change_title("Z^2: lattice with basis")
fig.fig.show()


# -------------------------------------------------------------
# Example 2: primitive sublattice Z(1,0)
# -------------------------------------------------------------
A_primitive = np.array([
    [1],
    [0],
])

fig = plot_parent_and_sublattice(
    Z2,
    A_primitive,
    title="L' = Z(1,0) inside Z²",
)
fig.fig.show()


# -------------------------------------------------------------
# Example 3: non-primitive sublattice Z(2,0)
# -------------------------------------------------------------
A_nonprimitive = np.array([
    [2],
    [0],
])

fig = plot_parent_and_sublattice(
    Z2,
    A_nonprimitive,
    title="L' = Z(2,0) inside Z²",
)
fig.fig.show()


# -------------------------------------------------------------
# Example 4: primal vs dual
# -------------------------------------------------------------
L = Lattice(
    np.array([
        [2.0, 0.0],
        [0.0, 1.0],
    ])
)

fig = plot_primal_and_dual(
    L,
    title="L = 2Z × Z and its dual",
)
fig.fig.show()
