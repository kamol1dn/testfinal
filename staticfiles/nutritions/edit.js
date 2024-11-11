document.getElementById("editForm").addEventListener("submit", (e) => {
    e.preventDefault();
    // Save updated data to localStorage
    localStorage.setItem("weight", document.getElementById("weight").value);
    localStorage.setItem("height", document.getElementById("height").value);
    localStorage.setItem("age", document.getElementById("age").value);
    localStorage.setItem("gender", document.querySelector('input[name="gender"]:checked').value);
    window.location.href = "profile.html"; // Redirect back to profile
  });
  