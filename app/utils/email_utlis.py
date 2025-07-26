from langchain_community.document_loaders import WebBaseLoader
import re
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
import os
from langchain_core.exceptions import OutputParserException
import pandas as pd
import chromadb
import uuid

class EmailUtils:
    def __init__(self):
        self.llm = ChatGroq(
        temperature=0, 
        groq_api_key=os.getenv("GROQ_API_KEY"), 
        model_name="llama3-70b-8192"
        )

    def urldata(self, url:str):
        loader = WebBaseLoader(url)
        page_data = loader.load()
        if page_data:
            return page_data[0].page_content
        else:
            return "No content found at the provided URL."
        return page_data
    
    def cleantext(self, text:str):
        # Remove HTML tags, if any
        clean_text = re.sub(r'<.*?>', '', text)
        # Remove URLs
        clean_text = re.sub(r'http[s]?://\S+', '', clean_text)
        # Remove special characters
        clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', clean_text)
        #Remove multiple spaces with single space
        clean_text = re.sub(r'\s+', ' ', clean_text)
        # Remove leading and trailing spaces
        clean_text = clean_text.strip()
        #Remove extra whitespaces
        clean_text = ' '.join(clean_text.split())
        return clean_text
    
    def jobdetails(self,text:str):
        prompt_extract = PromptTemplate.from_template(
                """
                ### SCRAPED TEXT FROM WEBSITE:
                {page_data}
                ### INSTRUCTION:
                The scraped text is from the career's page of a website.
                Your job is to extract the job postings and return them in JSON format containing the 
                following keys: `role`, `experience`, `skills` and `description`.
                Only return the valid JSON.
                ### VALID JSON (NO PREAMBLE):    
                """
        )

        chain_extract = prompt_extract | self.llm 
        res = chain_extract.invoke(input={'page_data':text})
        try:
            json_parser = JsonOutputParser()
            json_res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Failed to parse the output as JSON.")
        return json_res if isinstance(json_res, list) else [json_res]
    

    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Prashanth, a AI Intern at OXZON. OXZON is an AI & Software Consulting company dedicated to facilitating
            the seamless integration of business processes through automated tools. 
            Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
            process optimization, cost reduction, and heightened overall efficiency. 
            Your job is to write a cold email to the client regarding the job mentioned above describing the capability of AtliQ 
            in fulfilling their needs.
            Also add the most relevant ones from the following links to showcase Atliq's portfolio: {link_list}
            Remember you are Prashanth, AI intern at OXZON. 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):

            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res.content
    
class Portfolio:
    def __init__(self, file_path="my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])
                    

