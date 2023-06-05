
var breedsSelect = document.getElementById("breedsSelect");
var addToFavoritesBtn = document.getElementById("addToFavorites");
var url = "http://127.0.0.1:5000/api" 

// Adicionar aos Favoritos
addToFavoritesBtn.addEventListener("click", function() {
  var selectedBreedName = breedsSelect.value;

  // Verifique se uma opção foi selecionada
  if (selectedBreedName) {
    // Faça uma solicitação GET para obter as raças de cachorro
    fetch(url + '/breeds',{
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(response => response.json())
      .then(data => {
        // Encontre a raça correspondente pelo nome
        var selectedBreed = data.find(breed => breed.name === selectedBreedName);

        if (selectedBreed) {
          // Faça uma solicitação POST para adicionar aos favoritos
          var apiUrl = url + '/favorites';
  
          var requestBody = {
            image_id: selectedBreed.reference_image_id
          };

          fetch(apiUrl, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
          })
          .then(response => response.json())
          .then(data => {
            console.log('Adicionado aos favoritos:', data);
            alert('Adicionado aos favoritos!');
            location.reload()
          })
          .catch(error => {
            console.error('Erro:', error);
          });
        } else {
          alert('Raça selecionada não encontrada.');
        }
      })
      .catch(error => {
        console.error('Erro:', error);
      });
  } else {
    alert('Selecione uma raça para adicionar aos favoritos.');
  }
});

// Faça uma solicitação para a API para obter as raças de cachorro e preencher o select
fetch(url + '/breeds', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(data => {
    data.forEach(breed => {
      var option = document.createElement("option");
      option.textContent = breed.name;
      breedsSelect.appendChild(option);
    });
  })
  .catch(error => {
    console.error('Erro:', error);
  });


var favoritesList = document.getElementById("favoritesList");

// Função para excluir um favorito
function deleteFavorite(favoriteId) {
  var apiUrl = url + '/favorites/' + favoriteId;

  fetch(apiUrl, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => {
    if (response.ok) {
      // Remova o favorito da lista na página
      var favoriteItem = document.getElementById("favorite-" + favoriteId);
      if (favoriteItem) {
        favoriteItem.remove();
      }
      console.log('Favorito excluído com sucesso.');
    } else {
      console.error('Erro ao excluir o favorito:', response.status);
    }
  })
  .catch(error => {
    console.error('Erro:', error);
  });
}

// Faça uma solicitação GET para obter a lista de favoritos
fetch(url + '/favorites', {
  headers: {
    'Content-Type': 'application/json'
  }
})
  .then(response => response.json())
  .then(data => {
    // Manipule os dados da resposta e exiba-os na página
    data.forEach(favorite => {
      var listItem = document.createElement("li");
      listItem.setAttribute("id", "favorite-" + favorite.id);

      var image = document.createElement("img");
      image.setAttribute("src", favorite.image.url);
      image.setAttribute("alt", "Favorite Image");
      image.classList.add("favorite-image"); // Adicione a classe CSS "favorite-image"
      listItem.appendChild(image);

      var deleteButton = document.createElement("button");
      deleteButton.textContent = "Excluir";
      deleteButton.addEventListener("click", function() {
        deleteFavorite(favorite.id);
      });
      listItem.appendChild(deleteButton);

      favoritesList.appendChild(listItem);
    });
  })
  .catch(error => {
    console.error('Erro:', error);
  });
