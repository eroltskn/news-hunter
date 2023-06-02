
### About News Hunter App:
News Hunter is basically created to scan the news from a provided certain resource by using Python and  technologies in its orbit like bs4,feedparser and request.
Here we would like to get to know last updates about specified categories like economy , sport etc. from target resource .    


### Runing Docker-Compose

1. Clone the repo:
    ```bash
    git clone https://github.com/eroltskn/news-hunter.git
    ```

1. Run docker-compose:
    ```bash
    docker-compose up --build
    ```

1. Run testing scripts :
    ```bash
    docker-compose -f docker-compose_test.yml up --build 
    ```