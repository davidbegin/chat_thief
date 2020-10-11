document.addEventListener("DOMContentLoaded", () => {
 const bsod = document.createElement("div");
 bsod.classList.add("bsod");
 document.body.appendChild(bsod);
 const trigger = document.querySelector("span:nth-of-type(2)");
 trigger.innerText="Super secret Beginbot nudes";
 trigger.addEventListener("click", e=>{
   bsod.classList.add("visible");
setTimeout(()=>{bsod.classList.remove("visible")},2000);
 });
});
