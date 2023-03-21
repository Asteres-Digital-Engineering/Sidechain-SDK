# Sidechain-SDK
A software development kit used to build optimistic rollups and sidechains for blockchains.

## Purpose
The XRP Ledger (XRPL) provides a narrow range of smart contract functionality primarily focused on financial operations. While this feature is valuable for financial transactions, it constrains the platform's ability to execute arbitrary code. Additionally, within the wider smart contract ecosystem, the transaction fees based on compute cycles restrict the user's capacity to develop complex smart contracts, making even a simple game of chess expensive. Overall, the XRPL's limited smart contract capabilities, and indeed the ineffeciency of the wider smart contract ecosystem, constrain developer creativity.

As the number of transactions and users on blockchains grow, the associated costs and inefficiencies of computation tend to make smart contract blockchains less practical and more expensive. This trend is unacceptable if blockchains are to be adopted at a large scale. To address this issue, this SDK aims to provide a solution to the smart contract problem and support the XRP ecosystem by offering a set of tools for designing efficient systems that can handle arbitrary code execution within the XRP ecosystem. The SDK leverages verified data from the XRPL to enable developers to create smart contracts that are efficient, practical, and scalable, even as the number of users on the network increases. Ultimately, this will support the adoption of blockchain technology and make it a more viable option for large-scale applications.

To address the issue of slow computation and high costs associated with blockchain transactions, we can move the computation off-chain while keeping the user transactions on-chain. This approach is similar to optimistic rollups or sidechains, where a different network or set of validators is responsible for computing the state of the smart contract. This approach retains the key concepts of smart contracts, such as user-specified contract functions or actions, and the inputs required for those functions. However, on the network, only the commands and inputs provided by the user are validated and commited to the XRPL. This method allows for more efficient and cost-effective computation while retaining the security and trustlessness of the blockchain.

One way to achieve this is by utilizing an existing feature in the XRPL transaction data. In a traditional smart contract, user transactions are bundled with an Application Binary Interface (ABI) and the corresponding values. In our proposed approach, similar data is stored in the "MemoData" field of the XRPL transactions. This data is extracted from the network and converted into a format that arbitrary programs can interpret and execute. By doing so, the smart contract can be executed off-chain while retaining the essential security features of the blockchain. This approach offers a more efficient and cost-effective way to execute smart contracts while enabling developers to create complex and sophisticated applications that can run on the XRPL.

While this method offers a more efficient and cost-effective way to execute smart contracts, it can be challenging for many users to implement it themselves due to the complexity of the components involved. The process of developing libraries or tools to successfully implement a sidechain or optimistic rollup can be time-consuming and require specialized knowledge. To address this issue, the SDK aims to provide all the necessary components in an easy-to-use manner. By doing so, developers can focus on creating their own applications rather than worrying about building blockchain infrastructure from scratch. Our goal is to simplify the development process and make it accessible to a broader audience, enabling more users to take advantage of the benefits of blockchain technology.

## Requirements
This project is currently being developed under Python 3.10.6 but will be upgraded to the latest version 3.11.x at our earliest convenience. It also relies on Docker version >= 20.10.21 to stand up the redis server. There are python package requirements in requirements.txt. You can install them with `pip install -r requirements.txt`.

## Steps to Run
In a new command prompt/terminal:
- Get the latest redis container image from bitnami by typing: `docker pull bitnami/redis`
- After it is completely downloaded, change directory to this project: `cd /location/of/this/Sidechain-SDK`
- Create a folder called **redis_data** in the **Sidechain-SDK** project root: `mkdir redis_data`
    - The reason this is needed because I have it ignored in the git ignore file so the project doesn't keep anyone's junk. 
    - The docker-compose.yml file specifically refrences **./redis_data** on line **13**. So if you want to name it something else, you can, but make sure you change the first part of that line as well like this: 
        - `- './custom_name_here:/bitnami/redis/data'`
- Launch the redis server: `docker compose up -d`
- It should boot pretty quickly, then all you need to do is launch the test script: `python test.py`
    - If you have not specifically changed your system variables for python, you may need to type `python3 test.py`.
- You should see **Opened Connection** and then a bunch of transaction data being scrapped from the XRP network. Only successful transactions with '**engine_result_code: 0**' and more than zero **Memos** are scrapped.
- If you want to scrape from other XRP networks, you can change the url in **test.py**.

## Roadmap
At present, the only functional part is a **MemoData** scrapper which listens to the network and stores **MemoData** in a Redis database. This is just one component of the system, and there are several other components that need to be developed to create a fully functional system for arbitrary code execution on the XRPL. Our team is actively working on developing these components to create a comprehensive and user-friendly solution that will enable developers to build complex applications on the XRPL. Here are some of the main components that will be required:

- Conformity Checker
    -  A module that ensures **MemoData**, **MemoType**, and **MemoFormat** adhere and conform to an open specification. There are more checks we would like to add based on **TransactionType** but these are the most important to develop out first. 
-  Sidechain Memo Storage
    -  To store and order transactions on a blockchain, we need to label them by sidechain, blockchain, blocktime, transaction index, and memo index. Although the blockchain verifies and orders transactions, we still need to store them. This module is designed to take in conformed data and label it accordingly. While partially built out, this module currently cannot combine commands from different blockchains to get an ordered set of all transactions for a specific sidechain. The ultimate goal is for sidechains to be cross-chain compatible out of the box.
-  Memo Transmit
    - Separating data storage from computing is a widely used pattern in cloud computing and has been successfully employed by blockchains like Flow. This architecture is both cleaner and more scalable. The proposed module aims to create broadcast points for compute nodes. They will listen for and ingest **MemoData** from the network using a pubsub or RPC connection. While this capability is not yet available in the SDK, it will enable compute nodes to listen to relevant streams of data for their own purposes.
- Compute Ingester
    - The proposed module is designed to listen to data streams coming from memo transmissions. While the coding work required for this module will mostly deal with clients and RPC commands, some networking and containerization efforts will also be required. This will be the first module that needs to communicate with other containers or dedicated servers, as before this module, there will likely only be one container running.
- State Processor Libraries
    - The development of custom logic for the state processor is the responsibility of the user, but libraries will be necessary to tap into the feed and store the computed state. This is a complex process that involves reorgs, block ordering, cross chain support, and integration of transaction type logic such as trade offers and payments.
- State Database
    - This development involves creating a state storage module that tracks the history of state changes. Unlike the Sidechain Memo Storage, this module will not only store the current state but also maintain a record of all changes made to it over time. This is important because in case of a reorg, the state changes need to be undone and redone with new changes. 
- State Access
    - This module will provide endpoints for users to access relevant application data after the state is calculated. It will comprise of components to easily stand up REST, websocket, and RPC routes for arbitrary user interfaces and applications.
