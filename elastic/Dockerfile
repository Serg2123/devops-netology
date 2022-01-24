FROM centos:7

RUN groupadd -g 1000 elasticsearch && useradd elasticsearch -u 1000 -g 1000
RUN yum -y install wget
RUN wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.16.3-linux-x86_64.tar.gz
RUN tar -xzf elasticsearch-7.16.3-linux-x86_64.tar.gz
RUN mv elasticsearch-7.16.3 elasticsearch 
RUN mkdir /var/lib/elastic
RUN chown -R elasticsearch:elasticsearch "/elasticsearch"
RUN chown -R elasticsearch:elasticsearch "/var/lib/elastic"

WORKDIR /elasticsearch

USER elasticsearch
ENV PATH=$PATH:/elasticsearch/bin

COPY elasticsearch.yml /elasticsearch/config/

CMD ["elasticsearch"]
