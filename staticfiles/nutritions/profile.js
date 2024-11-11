// Load data from localStorage or a server
document.getElementById("weightDisplay").innerText = localStorage.getItem("weight");
document.getElementById("heightDisplay").innerText = localStorage.getItem("height");
document.getElementById("ageDisplay").innerText = localStorage.getItem("age");
document.getElementById("genderDisplay").innerText = localStorage.getItem("gender");

document.getElementById("editData").addEventListener("click", () => {
  window.location.href = "edit.html"; // Redirect to edit page
});

document.getElementById("logout").addEventListener("click", () => {
  localStorage.clear();
  window.location.href = "index.html"; // Redirect to sign-in page
});
