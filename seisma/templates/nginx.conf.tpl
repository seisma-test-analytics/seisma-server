server {
    listen {{ port }};
    expires off;
    sendfile off;

    location / {
        root {{ static_path }};
        try_files $uri /index.html;
    }

    location ~* \.(js|css|jpeg|jpg|png|gif)$ {
        root {{ static_path }};
    }

    location /api/ {
        ssi on;

        include uwsgi_params;
        uwsgi_param HTTPS off;

        uwsgi_pass unix:///var/run/seisma.sock;

        uwsgi_buffer_size 64k;
        uwsgi_buffers 32 4k;
        uwsgi_busy_buffers_size 64k;
        uwsgi_intercept_errors on;
        uwsgi_read_timeout 1800;
    }
}

server {
    listen {{ docs_port }};
    expires off;
    sendfile off;

    location / {
        root {{ docs_folder }};
        try_files $uri /index.html;
    }

}
