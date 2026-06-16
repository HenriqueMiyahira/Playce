function switchTab(event, tabName) {
    const contents = document.querySelectorAll('.tab-content');
    contents.forEach(content => content.classList.remove('active'));

    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(btn => btn.classList.remove('active'));

    document.getElementById(tabName).classList.add('active');
    event.currentTarget.classList.add('active');
}

// Funções para gerenciar os modais
function abrirModal(modalId) {
    document.getElementById(modalId).classList.add('active');
}

function fecharModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

// Fechar o modal se o usuário clicar fora da caixinha branca
window.onclick = function(event) {
    if (event.target.classList.contains('modal-overlay')) {
        event.target.classList.remove('active');
    }
}