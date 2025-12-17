function openEditModal(id, chinese, pinyin, french, hsk) {
    document.getElementById('edit-id').value = id;
    document.getElementById('edit-chinese').value = chinese;
    document.getElementById('edit-pinyin').value = pinyin;
    document.getElementById('edit-french').value = french;
    document.getElementById('edit-hsk').value = hsk;
    
    document.getElementById('editModal').style.display = 'flex';
}

function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
}

// Fermer la modale si on clique en dehors du formulaire
window.onclick = function(event) {
    let modal = document.getElementById('editModal');
    if (event.target == modal) {
        closeEditModal();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const card = document.getElementById('flashcard');
    const actions = document.getElementById('review-actions');

    if (card) {
        card.addEventListener('click', function() {
            this.classList.toggle('flipped');
            // Affiche les boutons quand la carte est retournée
            if (this.classList.contains('flipped')) {
                actions.style.display = 'block';
            }
        });
    }
});