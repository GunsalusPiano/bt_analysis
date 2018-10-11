# Start from a core stack version
FROM jupyter/scipy-notebook:latest
# Install in the default python3 environment
RUN conda install --quiet --yes \
	'biopython' \
	'tabulate' 
RUN conda install --quiet --yes -c bioconda \
	'blast' \
	'cd-hit'
RUN conda install --quiet --yes -c conda-forge \
	'tabulate'

WORKDIR $HOME
