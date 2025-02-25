# RAG application
![image](https://github.com/user-attachments/assets/6acdef4f-dbb8-4948-a878-ba783e1faf8f)

*RAG application is taking input query from user and then searches the external knowledge base for results which will then be passed into the LLM to process and the LLM will return a response
Differences from traditional LLM based applications, RAG applications use external knowledge base while LLM based applications only use data within LLM

*Example, if I were to ask ChatGPT "what is gareth's salary in ocbc?", it will not know.
However, if it was a RAG application, it can connect to ocbc database as a knowledge base and query from there which will be able to find my staff records 

*The query passed will be embedded using embedding methods(provided by APIs) to search the external knowledge base(vector db) for similarities in vector values, which will then return relevant documents
