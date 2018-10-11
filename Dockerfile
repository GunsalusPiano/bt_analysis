# Start from a core stack version
FROM jupyter/scipy-notebook:latest
# Install in the default python3 environment
RUN conda install --quiet --yes \
	'biopython' \
	'tabulate' 
RUN conda install --quiet --yes -c bioconda \
	'blast' \
# the conda build for cd-hit doesn't compile with psi-cdhit so I need to compile it locally
	'cd-hit'
RUN conda install --quiet --yes -c conda-forge \
	'tabulate'

WORKDIR $HOME
