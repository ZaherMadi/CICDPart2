#Create MySQL Image for JSP Tutorial Application
FROM mysql:latest
# Set environment variables for MySQL root password and database name
COPY ./sqlfiles/migrate-v001.sql /docker-entrypoint-initdb.d
EXPOSE 3306