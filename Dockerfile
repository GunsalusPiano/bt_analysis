# Start from a core stack version
FROM jupyter/scipy-notebook:latest
# Install in the default python3 environment
RUN conda install --quiet --yes biopython
