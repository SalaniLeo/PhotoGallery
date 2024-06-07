// @ts-nocheck
export async function get_posts() {
    const response = await fetch('http://127.0.0.1:5000/api/get_posts', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.json();
  }

export async function delete_post(title, description, path, time) {
    const response = await fetch('http://127.0.0.1:5000/api/delete_post', {
      method: 'POST',
      body: JSON.stringify({ title, description, path, time }),
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.json();
  }

export async function upload_post(title, description, file) {
  console.log(file.files[0])
    const response = await fetch('http://127.0.0.1:5000/api/upload_post', {
      method: 'POST',
      body: JSON.stringify({ title, description, file }),
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.json();
  }