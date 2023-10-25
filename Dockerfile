# Use an official Python runtime as the base image
FROM python:3.10-slim

# Update and upgrade libraries, and remove apt cache
RUN apt-get clean all && apt-get update && apt-get upgrade -y && apt-get install -y curl sudo make && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc
RUN curl https://packages.microsoft.com/config/debian/11/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 mssql-tools18 && apt-get install -y  unixodbc unixodbc-dev libgssapi-krb5-2

RUN echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc && . ~/.bashrc

# Create a new user and group
RUN groupadd -r caad && useradd -r -g caad caad
RUN echo 'caad ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/caad-nopasswd
WORKDIR /home/caad
# Copy the requirements file to the working directory

COPY . .

#RUN bash install_driver.sh

# Update pip without caching anything
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt 

RUN chown -R caad:caad /home/caad

# Switch to the new user
USER caad

#RUN sudo echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> /home/caad/.bashrc && source /home/caad/.bashrc

# Set environment variables (modify as needed)a

#ENV PYTHONUNBUFFERED=1

# Expose the port on which the Django app will run (modify if needed)
EXPOSE 8000/tcp

# Set the entrypoint to execute "make" with arguments
ENTRYPOINT ["make"]
CMD ["run-gunicorn"]
#CMD bash
