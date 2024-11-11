"use strict";

const modal = document.querySelector(".main_plan_modal");
const overlay = document.querySelector(".overlay");
const btnCloseModel = document.querySelector(".close_modal");
const btnOpenModel = document.querySelectorAll(".main_items_wrapper_btn");
console.log(btnOpenModel);

const openModel = function () {
  modal.classList.remove("hidden");
  overlay.classList.remove("hidden");
};

const closeModal = function () {
  modal.classList.add("hidden");
  overlay.classList.add("hidden");
};

for (let i = 0; i < btnOpenModel.length; i++) {
  btnOpenModel[i].addEventListener("click", openModel); //openModelni qavssiz yozilishini sababi bosilgandan keyin ishla degan ma'noda agar qavs qo'yilsa u srazi functionni chaqririb qo'yadi
}

btnCloseModel.addEventListener("click", closeModal);
overlay.addEventListener("click", closeModal);

document.addEventListener("keydown", function (event) {
  if (event.key === "Escape" && !modal.classList.contains("hidden")) {
    closeModal();
  }
});
