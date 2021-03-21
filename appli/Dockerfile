FROM python:3.9                                       
                                                                 
WORKDIR /app  
                                                  
COPY . .                                                          
                                                                 
RUN ["ls", "-al"]                                                
RUN ["python3", "-m", "pip", "install", "-r", "requirements.txt"]
                                                                 
EXPOSE 5001                                                     
                                                                 
CMD ["python", "api.py"]    