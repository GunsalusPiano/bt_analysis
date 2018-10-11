# Start from a core stack version
FROM jupyter/scipy-notebook:latest
USER root
RUN apt-get update && apt-get -yq dist-upgrade \
&& apt-get install -yq --no-install-recommends \
xvfb
USER $NB_UID
# Install in the default python3 environment
RUN conda install --quiet --yes \
	'biopython' \
	'tabulate' 
RUN conda install --quiet --yes -c bioconda \
	'blast' \
# the conda build for cd-hit doesn't compile with psi-cdhit so I need to compile it locally
	'cd-hit' \
	'clustalo' \
	'phylip'
RUN conda install --quiet --yes -c conda-forge \
	'tabulate'
RUN conda install --quiet --yes -c etetoolkit \
	'ete3'

WORKDIR $HOME
