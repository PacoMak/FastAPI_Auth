// Login functionality
document.addEventListener("DOMContentLoaded", function () {
  const loginButton = document.getElementById("login");
  const usernameInput = document.getElementById("username");
  const passwordInput = document.getElementById("password");

  loginButton.addEventListener("click", async function (e) {
    e.preventDefault();

    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();

    if (!username || !password) {
      alert("Please enter both username and password");
      return;
    }

    try {
      // Prepare form data for the login request
      const formData = new FormData();
      formData.append("username", username);
      formData.append("password", password);

      const response = await fetch("/login/password", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        window.location.href = "/user/me";
      } else {
        const errorData = await response.json();
        alert("Login failed: " + (errorData.detail || "Invalid credentials"));
      }
    } catch (error) {
      alert("Network error. Please try again.");
    }
  });
});
