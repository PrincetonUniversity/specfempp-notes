
# SPECFEM++ workshop

## Abstract

SPECFEM++ is a suite of computational tools based on the spectral element method, designed for simulating wave propagation through heterogeneous media. This software aims to consolidate the legacy SPECFEM codes—three separate Fortran packages (SPECFEM2D, SPECFEM3D, and SPECFEM3D_globe)—into a single C++ package. The new package seeks to optimize performance across various architectures by utilizing the Kokkos library.

The tutorial is structured as a two-part workshop. In the first part, we will introduce the SPECFEM++ package, highlighting its features and capabilities. Participants will then install the code and run a simple example that demonstrates how to set up a simulation, execute it, and visualize the results.

The second part of the workshop will cater to developers interested in contributing to the codebase. We will review essential development tools such as linters and formatters, guiding participants on how to install them using the package manager `uv`. Additionally, we will cover our development workflow with Git and GitHub, which includes creating a new branch, making changes, and submitting a pull request. Finally, we will take a deep dive into the code architecture, discussing how to navigate the codebase and our design principles. We will also provide a brief introduction to the Kokkos library, which facilitates performance portability across different hardware architectures.

The first part of the workshop is intended for new users, and the second part is aimed towards more experienced SPECFEM developers.
