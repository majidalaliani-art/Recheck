function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const CSRF_TOKEN = getCookie("csrftoken");

export async function ajax_request(url, formData, errorMessage = "Connection error:") {
  if (!CSRF_TOKEN) {
    console.error("CSRF token not found!");
    return null;
  }

  try {
    const response = await fetch(url, {
      method: "POST",
      body: formData,
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": CSRF_TOKEN,
      },
    });

    if (!response.ok) {
      console.error(errorMessage, response.status);
      return null;
    }

    const contentType = response.headers.get("content-type");

    if (contentType && contentType.includes("application/json")) {
      return await response.json();
    }

    return await response.text();
  } catch (err) {
    console.error(errorMessage, err);
    return null;
  }
}

export async function ajax_json(url, data, errorMessage = "Connection error:") {
  if (!CSRF_TOKEN) {
    console.error("CSRF token not found!");
    return null;
  }

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": CSRF_TOKEN,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      console.error(errorMessage, response.status);
      return null;
    }

    const contentType = response.headers.get("content-type");

    if (contentType && contentType.includes("application/json")) {
      return await response.json();
    }

    return await response.text();
  } catch (err) {
    console.error(errorMessage, err);
    return null;
  }
}

export async function ajax_get(url, errorMessage = "Connection error:") {
  try {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    });

    if (!response.ok) {
      console.error(errorMessage, response.status);
      return null;
    }

    return await response.json();
  } catch (err) {
    console.error(errorMessage, err);
    return null;
  }
}