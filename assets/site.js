// Bouton « Copier » des formules.
document.querySelectorAll(".copier").forEach(function (b) {
  b.addEventListener("click", function () {
    var fini = function (texte) {
      b.textContent = texte;
      b.classList.add("fait");
      setTimeout(function () { b.textContent = "Copier"; b.classList.remove("fait"); }, 1800);
    };
    try {
      navigator.clipboard.writeText(b.dataset.copie).then(function () { fini("Copié"); }, function () { fini("Sélectionnez"); });
    } catch (e) { fini("Sélectionnez"); }
  });
});
