FROM node:lts-alpine             
                           
WORKDIR /src   

COPY package*.json ./
                                        
RUN ["ls", "-al"]          
RUN ["npm", "install"]     

COPY . .   
                           
EXPOSE 8080                
                           
CMD ["npm", "run", "serve"]