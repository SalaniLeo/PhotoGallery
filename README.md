# PhotoGallery

🎑 Self Hostable website to show your best photos!

## Configuration

- Backend urls are customizable inside backend-urls.env
- To connect to postgresql create a database.ini file inside backend/flask/
<details>
<summary>database.ini example</summary>
    
    [postgresql]
    host=postgresql
    database=postgresql
    user=postgresql
    password=postgresql


</details>

## Usage

## With docker (recommanded)

    docker compose up

## Without docker (only for testing)

### Start backend

    bash backend.sh

### Start frontend

    bash frontend.sh
