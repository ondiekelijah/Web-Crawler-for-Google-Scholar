# Web-Crawler-for-Google-Scholar
# Description
A web crawler for google scholar authors profiles for authors from Coventry University. Also included is a vertical search engine similar to google scholar however it returns results where at least one author is from Coventry University. It is implemented using Flask and MySQL
[![GitHub stars](https://img.shields.io/github/stars/Dev-Elie/Web-Crawler-for-Google-Scholar)](https://github.com/Dev-Elie/Web-Crawler-for-Google-Scholar/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/Dev-Elie/Search-Weather-Wordnet-Location-Web-App)](https://github.com/Dev-Elie/Search-Weather-Wordnet-Location-Web-App/issues)
[![GitHub forks](https://img.shields.io/github/forks/Dev-Elie/Search-Weather-Wordnet-Location-Web-App)](https://github.com/Dev-Elie/Search-Weather-Wordnet-Location-Web-App/network)
[![Twitter](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Ftwitter.com%2F)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2FDev-Elie%2FSearch-Weather-Wordnet-Location-Web-App)

**NB:** Commands issued are for a linux environment,however no one is limited.

# Installation
1. Create a new folder for the project and navigate into it
```
$ mkdir my_project
$ cd my_project
```
2.Inside the newly created folder create a virtual environment
```
 $ Python3.9 -m venv < env name>
```
3. Create another folder,name it "main",navigate to it and clone to it the applicatons files.
```
mkdir main
cd main
$ git clone https://github.com/Dev-Elie/Search-Weather-Wordnet-Location-Web-App.git
```
# Usage
1. Activate the virtual environment
```
$. venv/bin/activate
OR
$ source venv/bin/activate
``` 
2. Navigate into the "main" folder and install the requirements.
```
$ pip install -r requirements.txt
```
3. Make the run file an executable
```
$ chmod 777 run
```
4. Launch the application
```
$ ./run
```
# Preview
![Home](https://github.com/Dev-Elie/Portfolio/blob/main/images/projects/gs-crawler.png
 "Crawler Page")
# NB 
> Incase you face any issues with refused connections,below is a quick fix;
  * Restart your network on each subsequent crawl
  * Intergrate a proxy service

Liked this project ? 
Feel free to tweet about it [![Twitter](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Ftwitter.com%2F)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2FDev-Elie%2FSearch-Weather-Wordnet-Location-Web-App)
