const dialog = document.querySelector("dialog");
const openDialog = document.querySelector("#open-dialog");
const cancelDialog = document.querySelector("#cancel");
const confirmDialog = document.querySelector("#confirm-delete");

openDialog.addEventListener("click", (e) => {
  e.preventDefault();
  dialog.showModal();
});
cancelDialog.addEventListener("click", (e) => {
  e.preventDefault();
  dialog.close();
});

confirmDialog.addEventListener("click", () => {
  fetch("/delete_user", {
    method: "POST",
  }).then((res) => {
    window.location.href = res.url
  });
});
