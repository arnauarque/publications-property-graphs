# Real use cases of property graphs and their exploitation via data analysis

This project involves exploring the practical application of property graphs and graph embeddings in Data Science. We start by theoretically studying graph embeddings. In the practical aspect, a real-world use case is chosen, and a graph embedding strategy is implemented for data analysis.

## Authors and context

This project has been developed by the users [@arnauarque](https://github.com/arnauarque) and [@danielesquina](https://github.com/danielesquina) as part of the [Semantic Data Management](https://www.fib.upc.edu/en/studies/masters/master-data-science/curriculum/syllabus/SDM-MDS) course in the [Master's in Data Science](https://www.fib.upc.edu/en/studies/masters/master-data-science) program at the [Faculty of Informatics of Barcelona](https://www.fib.upc.edu/en) (Universitat Politècnica de Catalunya). In this file, you can find an introduction to the project and its objectives. Additionally, you will find a detailed description of the repository's organization.

## Summary of the requirements

The project has two components: a research aspect and a practical aspect to understand the potential of graphs in real use cases.  We were expected to conduct a search on the topic, summarize what we found, and apply the approach to a real use case (as realistic as possible). More precisely, we were expected to:

1. Learn and understand what graph embeddings are. Graph embeddings provide a vector representation of graphs (node-based or edge-based) that can be later used to perform data analysis on them.
2. Put into practice what you learnt. Given a real graph, briefly describe it to understand its meaning, propose and implement an embedding strategy, and run a chosen machine learning or data mining algorithm with a specific purpose.

## Overall description

This project involves two sections. The first section summarizes research findings on graph embeddings, exploring various graph types and components. It also discusses techniques and applications in literature. The second section applies graph embeddings to a synthetic dataset representing the paper publication domain, using machine learning algorithms for familiarity and future application.

## Repository organization

This repository is organized as follows: 

- The [code](code/) directory contains the [data](./code/data/) used and the code generated in this project. You can see how to run each file in the **Instructions** section below. 
 - The [report.pdf](report.pdf) file contains a brief introduction to the project, as well as its objectives. It also includes the results and conclusions derived from the data analysis process.
 
## Instructions

Follow these instructions in order to run the programs of the `./code/` directory.

1. Generate the data:

```
python3 data_generator.py
```

2. Load the data to Neo4j (choose one option, see **Note** below):

```
python3 data_loader.py load [store] [all]
python3 data_loader.py [load] store [all]
```

3. Generate the embeddings, train the model and make the predictions.

```
python3 embeddings.py
```

> **Note:** Steps (1) and (2) are not needed in order to run the `embeddings.py` program. They can only be run if you have access to our local `Neo4j` database. For more information, contact the project authors.

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository is licensed under the MIT License.



