FROM ubuntu:latest
RUN apt update
RUN apt upgrade -y
RUN apt install -y dirmngr gnupg apt-transport-https ca-certificates software-properties-common
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
RUN add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu focal-cran40/'
RUN apt install -y r-base
RUN apt install -y python3 python3-pip
RUN apt install -y wget curl

RUN R -e "install.packages('yaml',dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('desc',dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('optparse',dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN python3 -m pip install pyyaml toml

COPY language_scripts/license_rec.py /usr/bin/get-license
RUN chmod +x /usr/bin/get-license
COPY language_scripts/julia_metadata.py /usr/bin/julia_metadata
RUN chmod +x /usr/bin/julia_metadata
COPY language_scripts/python_metadata.py /usr/bin/python_metadata
RUN chmod +x /usr/bin/python_metadata
COPY language_scripts/R_metadata.R /usr/bin/R_metadata
RUN chmod +x /usr/bin/R_metadata