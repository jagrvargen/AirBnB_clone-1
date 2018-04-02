#!/usr/bin/env bash
# Create necessary directories.
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Add index.html file and add simple content for testing purposes.
touch /data/web_static/releases/test/index.html
echo -e "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>\n" > /data/web_static/releases/test/index.html

# Create symbolic link between /data/web_static/current and
# /data/web_static/releases/test/.
ln -sf /data/web_static/current /data/web_static/releases/test/

# Grant ownership of /data/ recursively to both user and group.
chown -R ubuntu:ubuntu /data/

# Configure Nginx to serve content of /data/web_static/current/ to hbnb_static.
sed -i "39i     location /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}" /etc/nginx/sites-enabled/default

# Restart
service nginx restart
