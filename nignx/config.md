server {
server_name hercules.vitorwdson.dev;

location / {
proxy_pass http://localhost:3333;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header Host $host;
proxy_redirect off;
}

location /static {
alias /home/vitorwdson/hercules/static/;
}

location /secret-files {
internal;
alias /home/vitorwdson/hercules/media/;
}
}
