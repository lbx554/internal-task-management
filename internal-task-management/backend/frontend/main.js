const apiBase = "http://localhost:8000/api";

// --- USERS ---
const userForm = document.getElementById("userForm");
const usersList = document.getElementById("usersList");

userForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  
  const email = document.getElementById("email").value;
  const role = document.getElementById("role").value;
  const password = document.getElementById("password").value;

  const res = await fetch(`${apiBase}/users/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, role, password })
  });
  const data = await res.json();
  loadUsers();
  userForm.reset();
});

async function loadUsers() {
  const res = await fetch(`${apiBase}/users/`);
  const users = await res.json();
  usersList.innerHTML = users.map(u => `<li>${u.id} - ${u.email} (${u.role})</li>`).join("");
}

loadUsers();

// --- TASKS ---
const taskForm = document.getElementById("taskForm");
const tasksList = document.getElementById("tasksList");

taskForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const title = document.getElementById("title").value;
  const description = document.getElementById("description").value;
  const status = document.getElementById("status").value;
  const assigned_to = document.getElementById("assigned_to").value || null;

  const res = await fetch(`${apiBase}/tasks/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, description, status, assigned_to })
  });
  const data = await res.json();
  loadTasks();
  taskForm.reset();
});

async function loadTasks() {
  const res = await fetch(`${apiBase}/tasks/`);
  const tasks = await res.json();
  tasksList.innerHTML = tasks.map(t => `<li>${t.id} - ${t.title} (${t.status})</li>`).join("");
}

loadTasks();
