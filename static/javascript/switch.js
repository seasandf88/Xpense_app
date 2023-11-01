const checkbox = document.getElementById("checkbox");

checkbox.addEventListener("change", () => {
  if (document.body.classList.contains("dark")) {
    document.body.classList.remove("dark");
    localStorage.removeItem("selected-theme")
  } else {
    document.body.classList.add("dark");
    localStorage.setItem("selected-theme", "dark")
  }
});