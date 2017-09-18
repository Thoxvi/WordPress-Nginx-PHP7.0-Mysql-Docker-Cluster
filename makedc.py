#!/usr/bin/python3.6
import os
import sys

docker_compose_yml = '''
version : "3.2"
services:
  db:
    image: mysql
    volumes:
      - "./data/db:/var/lib/mysql"
    environment:
      MYSQL_DATABASE: wordpress
      MYSQL_ROOT_PASSWORD: NoFfDYpxvWHeEZYMofrwsMYDAI4mJE6H
    expose:
      - "3306"

  adminer:
    image: adminer
    ports:
      - 8080:8080
    links:
      - db
{blogs}

  proxy:
    image: nginx:latest
    ports:
      - 80:80
    volumes:
      - "./proxy.conf:/etc/nginx/nginx.conf"
    links:
{links}'''

blog = '''
  blog{i}:
    image: thoxvi/php_with_nginx
    volumes:
      - "./data/www:/usr/share/nginx/html"
    expose:
      - "80"
    links:
      - db
'''

proxy_conf0 = '''user  www-data;
worker_processes  8;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;

events {
    worker_connections  1024;
}
http {
    upstream localhost {
'''

proxy_conf1 = '''    }
    server{ 
        listen 80; 
        server_name localhost; 
        location / {
                proxy_pass http://localhost;
        }
    }
}'''
n = 5
path = "/".join(os.path.abspath(sys.argv[0]).split("/")[:-1])

blogs = ""
servers = ""
links = ""
for i in range(n):
    blogs += blog.format(i=i)
    servers += "\tserver blog{i};\n".format(i=i)
    links += "      - blog{i}\n".format(i=i)

docker_compose_yml = docker_compose_yml.format(blogs=blogs, links=links)
proxy_conf = proxy_conf0 + servers + proxy_conf1

print(docker_compose_yml)
print(proxy_conf)

with open(path + "/docker-compose.yml", 'w') as f:
    f.write(docker_compose_yml)

with open(path + "/proxy.conf", 'w') as f:
    f.write(proxy_conf)
