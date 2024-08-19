#!/bin/bash

env DOMAIN="https://gallery.salanileo.dev" \
FLASK_SERVER_ADDR="gallery.salanileo.dev" \
VALIDATE_URL="/api/auth/authenticate" \
REGISTER_URL="/api/auth/register" \
LOGIN_URL="/api/auth/login" \
GET_POSTS_URL="/api/posts/all" \
GET_LATEST_POST_URL="/api/posts/latest" \
DELETE_POST="/api/posts/delete" \
UPLOAD_POST="/api/posts/upload" \
ORIGIN="['https://127.0.0.1:5173','http://127.0.0.1:5173','https://127.0.0.1', 'http://127.0.0.1']" \
npm run dev --prefix frontend -- --host
