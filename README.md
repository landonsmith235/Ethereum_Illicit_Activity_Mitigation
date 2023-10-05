![alt text](https://github.com/landonsmith235/Ethereum_Illicit_Activity_Mitigation/blob/054e566b92974583566aadf5144f684066802cce/Images/title_slide.jpg)

## **Overview**
The recent exponential adoption of blockchain networks such as Ethereum has prompted regulators to introduce measures such as KYC and sanctions to help fend off malicious
activity. This research paper builds upon the framework that blockchain networks must have robust systems in place to mitigate illicit activity if they are to be adopted for mainstream use. Our cohort sought to first replicate the highly effective machine learning models utilized by contemporary researchers in the field to differentiate between illicit and legal addresses, but also harness these methodologies into two main additions: real-time mempool transaction monitoring and multi-categorical classification of illicit addresses. While this research paper doesn't provide a viable solution to our ambitious goal of ushering in a transaction safety layer onto the decentralized Ethereum network, our research contradicts and exposes the lack of efficacy of models created using the aforementioned contemporary methodologies for the purpose of illicit activity detection. Our cohort believes that the segments of the Ethereum community seeking to mitigate illicit activity using machine learning models may need to take a step backward and reassess model foundations before additional progress in the field can be made.

## **Technologies Utilized**
Python Libraries
* web3
* psycopg2
* pandas
* joblib
* etherscan-python
* sklearn
* datetime
* selenium
* tensorflow
* keras
  
Ethereum Node Equipped with Geth Execution Client (Hosted on Quicknode)

Google Cloud PostgreSQL Database

Power BI Visualization Software

## **Relevant Repository Contents & Descriptions**

### **Presentation.pdf**
This file is the PDF version of a PowerPoint presentation given to Saint Mary's College of California faculty. This file is meant to be referenced as a general outline of how we came to our conclusions.

### **Research Paper.pdf**
This file is the PDF version of our in-depth research paper on the topic of illicit activity detection on the Ethereum blockchain. This file is meant to deliver a much more granular explanation of our methodologies than the aforementioned Presentation.pdf.

### **Real-Time Mempool Classification Folder**
This folder is further divided into several sub-folders. The folder titles, being Address-Based Models and Transaction-Based Models, provide a user with the ability to explore the methodologies utilized on datasets of different composition. 

#### **Address-Based Models**
This folder contains sub-folders that seperate files by deployment stage. 

##### **Address Acquisition & Feature Engineering**
This folder contains the scripts we utilized to obtain our illiict and legal Ethereum addresses, engineer aggregate features associated with each address, and export our data into the Coinbase and Randomly Sampled datasets.

##### **Ensemble Models Construction**
This folder contains the scripts we utilized to create our address-based ensemble machine learning model, as well as the exported Coinbase and Randomly Sampled models. 

##### **Real-Time Classification**
This folder contains the scripts we utilized to initialize our PostgreSQL database and perform real-time classification of mempool transactions. 

#### **Transaction-Based Models**
This folder contains two scripts that are differentiated by the Ethereum token-standard these aim to address illicit activity on. The first script details our attempts at creating an ML model to detect illicit activity on siple Ether transactions. The second script mirrors these attempts on the ERC-20 token standard. 

### **Multicategorical Classification Files**
This folder contains a single file which details the entirety of our work on the categorization of illicit activity into a variety of different classes. 
