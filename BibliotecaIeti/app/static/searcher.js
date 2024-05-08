function buscarAutocompletado() {
  console.log("hola");
  var inputText = document.getElementById("searcher").value.trim();
  var hasStockCheckbox = document.getElementById("has-stock-checkbox").checked;

  if (inputText.length >= 3) {
    $.ajax({
      url: "/buscar/",
      type: "GET",
      data: {
        query: inputText,
        has_stock: hasStockCheckbox,
      },
      success: function (data) {
        $("#searcher").autocomplete({
          source: data.map(function (result) {
            return result.nombre;
          }),
        });
      },
      error: function (xhr, status, error) {
        console.error(
          "Error al obtener los resultados del autocompletado:",
          error
        );
      },
    });
  } else {
    $("#searcher").autocomplete("destroy");
  }
}

$(document).ready(function() {
  document.addEventListener("keydown", function(event) {
    if (event.shiftKey && event.key === "C") {
      event.preventDefault();
      document.getElementById("searchButton").click();
      console.log("g")
    }
  });
});
