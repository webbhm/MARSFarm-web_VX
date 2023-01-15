# MARSFarm-web_VX
Flask, Blueprint testing of a MARSFarm website
Future version of the MARSFarm server software
This project explores creating a web server using Python, Flask, Blueprints and MongoDB.
Purpose
The goal is to duplicate the current functionality, and add some enhancements (including a new data format).
There are two problems with the current design:
1) It is written in JavaScript (which I don't want to learn)
2) It lacks modularity for incrimental testing and development.  
Large collections of messy code are hard to understand, and what is no understood or trusted doesn't get changed (no improvement).
The Flask app is to become a simple holder of Blueprint includes.
Each Bluepring represents the interfaces to common business processes (data entry, charting).
