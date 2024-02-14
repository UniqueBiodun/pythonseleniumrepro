FROM mcr.microsoft.com/azure-functions/python:4-python3.10
 
ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true
 
COPY requirements.txt .
 
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN apt-get install -y wget
RUN apt-get install -y unzip
 
# Set up the Chrome PPA
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
 
 
 
# Update the package list and install chrome
RUN apt-get update -y
RUN apt-get install -y google-chrome-stable
 
COPY . /home/site/wwwroot