# Facebook Connector

- This is a connector that scrapes images, their description and their comments from facebook.com for a given subject.
- It uses selenium to navigate through the pages and extract the web elements.
- This is compatible with only Goggle Chrome.
- You need to download the [chromedriver.exe](https://chromedriver.chromium.org/downloads) for selenium.
- You need to change facebook_credentials.txt with your credentials and the preferred subject.
- The collected data are saved in a local MongoDB database

### Execution
![Imgur](https://i.imgur.com/uPmxhXW.png)
![Imgur](https://i.imgur.com/ZV490No.png)

- I ran the app for the subject "Smart Conseil" and got 6 results.