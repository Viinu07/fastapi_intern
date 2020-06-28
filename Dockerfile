#docker run -d -p 0.0.0.0:27017:27017 -v ~/foo/data/db/:/data/db --name mongodb mongo ##required
FROM python:3.8
#Run this on mac machine 
RUN pip3 install fastapi uvicorn motor aiofiles jinja2
#Run this on windows machine
#RUN pip install fastapi uvicorn motor aiofiles jinja2
EXPOSE 3000

COPY ./app /app

CMD ["python", "app/main.py"]
