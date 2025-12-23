const BASE_URL = import.meta.env.VITE_API_BASE_URL;

/* ---------------- Token helpers ---------------- */

export function setToken(token) {
  localStorage.setItem("token", token);
}

export function getToken() {
  return localStorage.getItem("token");
}

export function clearToken() {
  localStorage.removeItem("token");
}

export function logout() {
  clearToken();
}

/* ---------------- Auth ---------------- */

export async function login(email, password) {
  const res = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.detail || "Login failed");
  }

  if (data.access_token) {
    setToken(data.access_token);
    if (data.user?.name) {
      localStorage.setItem("user_name", data.user.name);
    }
  }

  return data;
}

export async function signup(name, email, password) {
  const res = await fetch(`${BASE_URL}/auth/signup`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name, email, password }),
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.detail || "Signup failed");
  }

  if (data.access_token) {
    setToken(data.access_token);
    if (data.user?.name) {
      localStorage.setItem("user_name", data.user.name);
    }
  }

  return data;
}

/* ---------------- RAG ---------------- */

/**
 * IMPORTANT:
 * - No JSON body
 * - No Content-Type header
 * - No Authorization header
 * - Query params ONLY
 */
export async function askQuestion(question, top_k = 5) {
  if (!question || question.trim().length < 5) {
    throw new Error("Question too short");
  }

  const url =
    `${BASE_URL}/rag/ask` +
    `?question=${encodeURIComponent(question)}` +
    `&top_k=${top_k}`;

  const res = await fetch(url, {
    method: "POST",
  });

  const data = await res.json();
  console.log("RAG RESPONSE:", data);

  if (!res.ok) {
    throw new Error(data.detail || "Failed to get answer");
  }

  return data;
}
