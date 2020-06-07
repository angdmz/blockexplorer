# Blockexplorer RESTful API

A simple RESTful API for getting ethereum blockchain data


### Motivations

There are other block explorer dApps around, but are just web apps that shows transactions, balances and other data, if some organization has a big application ecosystem that has to add ethereum blockchain to its business, as Ethereum Protocol just provides fast querying for some information, a stronger option is required for having blockchain information fast. 

### Fundaments

Seems to be natural to have doubts on an abstraction layer in a context of high transparency that blockchain is suppose to give. An API tries to hide implementation representation and have an interface that does not reveal the invariant behind. The idea of this is to have this REST blockexplorer installed in several different ecosystems so the trust on the API relies entirely on those who integrate them

### Internals

This API is built with Python on Django and DRF, using simple features from this frameworks, and exposes documentation on swagger

For retrieving data fast, this API has a Postgres as redundancy for the chain data, which is easy to query, and the API is simply a view for this SQL data

For loading the data, there are several Django Commands for loading full blockchain, a single block, or simply update from the last block in the database

### Plugins

This API uses the following Python plugins, and technologies

| Plugin | Docs |
| ------ | ------ |
| Django | [djangoproject][Pldj] |
| Django Rest Framework | [djangorestframework][Pldrf] |
| Django Ethereum Gateway | [gitlabbfa][Pldeg] |
| Docker | [docker][docker] |


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [Pldj]: <https://docs.djangoproject.com/en/2.2/>
   [Pldrf]: <https://www.django-rest-framework.org/>
   [Pldeg]: <https://gitlab.bfa.ar/public>
   [docker]: <https://www.docker.com/>
