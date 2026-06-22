// 1. Função de Alternância de Abas (Tabs)
function switchTab(event, tabName) {
    const contents = document.querySelectorAll('.tab-content');
    contents.forEach(content => content.classList.remove('active'));

    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(btn => btn.classList.remove('active'));

    const tab = document.getElementById(tabName);
    if (tab) {
        tab.classList.add('active');
        event.currentTarget.classList.add('active');
    }
}

// 2. Funções Básicas para abrir/fechar Modais comuns
function abrirModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.add('active');
}

function fecharModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.remove('active');
}

// Função para abrir o modal e listar os horários agendados de uma quadra
function abrirModalReservas(modalId, quadraId, quadraNome) {
    const modal = document.getElementById(modalId);
    const titulo = document.getElementById('modal-reservas-titulo');
    const container = document.getElementById('modal-reservas-corpo');

    if (!modal || !container || !titulo) return;

    // Atualiza o título do modal com o nome da quadra clicada
    titulo.innerText = `Agenda: ${quadraNome}`;

    // Busca as reservas mapeadas para o ID dessa quadra
    const reservas = reservasPorQuadra[quadraId] || [];

    if (reservas.length > 0) {
        let htmlLista = `<p style="color: #64748b; font-size: 0.9rem; margin-bottom: 15px;">Abaixo estão os horários reservados para esta quadra:</p>`;
        htmlLista += `<ul style="list-style: none; padding: 0; margin: 0;">`;

        reservas.forEach(reserva => {
            htmlLista += `
                <li style="padding: 12px; background: #f8fafc; margin-bottom: 10px; border-radius: 8px; border: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; flex-direction: column; gap: 4px;">
                        <span style="font-size: 0.85rem; color: #3b82f6; font-weight: 600;">
                            <i class="fa-regular fa-calendar" style="margin-right: 5px;"></i> ${reserva.data}
                        </span>
                        <strong style="color: #1e293b; font-size: 1rem;">
                            <i class="fa-regular fa-clock" style="margin-right: 5px;"></i> ${reserva.horario}
                        </strong>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 0.8rem; color: #64748b; display: block;">Responsável:</span>
                        <strong style="color: #334155; font-size: 0.9rem;">${reserva.cliente}</strong>
                    </div>
                </li>
            `;
        });

        htmlLista += `</ul>`;
        container.innerHTML = htmlLista;
    } else {
        // Se a quadra não tiver nenhuma reserva no banco
        container.innerHTML = `
            <div style="text-align: center; padding: 40px 20px; color: #64748b;">
                <i class="fa-regular fa-calendar-check" style="font-size: 3rem; margin-bottom: 12px; display: block; color: #cbd5e1;"></i>
                <p style="font-weight: 500; margin: 0;">Esta quadra não possui nenhum horário agendado.</p>
                <span style="font-size: 0.85rem; color: #94a3b8;">Ela está 100% livre para novas reservas.</span>
            </div>`;
    }

    // Abre o modal adicionando a classe active
    modal.classList.add('active');
}

function abrirModalItens(modalId, artigoNome) {
    const modal = document.getElementById(modalId);
    const container = document.getElementById('modal-corpo');

    if (!modal || !container) return;

    const itens = listaItensPorArtigo[artigoNome] || [];

    if (itens.length > 0) {
        let htmlLista = `<ul style="list-style: none; padding: 0; margin-top: 15px;">`;

        itens.forEach((item, index) => {
            let badgeBg = '#e2e8f0';
            let badgeColor = '#475569';
            const statusTexto = item.status_display.toLowerCase();

            if (statusTexto.includes('disp') || statusTexto.includes('novo')) {
                badgeBg = '#dcfce7'; badgeColor = '#166534';
            } else if (statusTexto.includes('manut') || statusTexto.includes('ruim')) {
                badgeBg = '#fee2e2'; badgeColor = '#991b1b';
            } else if (statusTexto.includes('alug') || statusTexto.includes('uso')) {
                badgeBg = '#fef3c7'; badgeColor = '#92400e';
            }

            htmlLista += `
                <li id="item-row-${item.id}" style="padding: 12px; background: #f8fafc; margin-bottom: 8px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #e2e8f0;">
                    <div style="display: flex; flex-direction: column; gap: 4px;">
                        <strong style="color: #1e293b; font-size: 0.95rem;"><i class="fa-solid fa-tag" style="color: #3b82f6; margin-right: 6px;"></i>${item.codigo}</strong>
                        <span style="font-size: 0.75rem; padding: 2px 8px; background: ${badgeBg}; color: ${badgeColor}; border-radius: 9999px; width: max-content; font-weight: 600;">
                            ${item.status_display}
                        </span>
                    </div>
                    <button class="btn-action edit" onclick="ativarEdicionInline('${item.id}', '${item.codigo}', '${item.status}', '${artigoNome}')" style="background: #3b82f6; color: white; border-radius: 4px; padding: 6px 10px;" title="Editar Item">
                        <i class="fa-solid fa-pen" style="font-size: 0.85rem;"></i>
                    </button>
                </li>
            `;
        });

        htmlLista += `</ul>`;
        container.innerHTML = htmlLista;
    } else {
        container.innerHTML = `
            <div style="text-align: center; padding: 30px; color: #64748b;">
                <i class="fa-solid fa-box-open" style="font-size: 2.5rem; margin-bottom: 10px; display: block; color: #cbd5e1;"></i>
                <p>Nenhum item unitário cadastrado para este artigo.</p>
            </div>`;
    }

    modal.classList.add('active');
}


function ativarEdicionInline(itemId, codigoAtual, statusAtual, artigoNome) {
    const linha = document.getElementById(`item-row-${itemId}`);
    if (!linha) return;

    // Resgata o HTML do token de segurança injetado na página
    const csrfToken = document.getElementById('csrf-holder').innerHTML;

    // Substitui o conteúdo da linha por um formulário de submissão direta
    linha.innerHTML = `
        <form method="POST" action="" style="display: flex; width: 100%; gap: 8px; align-items: center; margin: 0;">
            ${csrfToken}
            <input type="hidden" name="tipo_form" value="editar_item_unitario">
            <input type="hidden" name="item_id" value="${itemId}">
            
            <input type="text" name="codigo" value="${codigoAtual}" required 
                   style="flex: 2; padding: 6px 8px; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.9rem; font-weight: bold;">
            
            <select name="status" required style="flex: 1.5; padding: 6px 4px; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.85rem;">
                <option value="DISP" ${statusAtual === 'DISP' || statusAtual === 'Disponível' ? 'selected' : ''}>Disponível</option>
                <option value="ALUG" ${statusAtual === 'ALUG' || statusAtual === 'Alugado' ? 'selected' : ''}>Alugado</option>
                <option value="MANU" ${statusAtual === 'MANU' || statusAtual === 'Manutenção' ? 'selected' : ''}>Manutenção</option>
            </select>
            
            <div style="display: flex; gap: 4px;">
                <button type="submit" class="btn-primary" style="padding: 6px 10px; background: #10b981;" title="Salvar Alterações">
                    <i class="fa-solid fa-check"></i>
                </button>
                <button type="button" class="btn-action delete" onclick="abrirModalItens('modal-itens', '${artigoNome}')" style="padding: 6px 10px;" title="Cancelar">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </div>
        </form>
    `;
}

// 5. Fechar o modal caso clique na área escura (Overlay)
window.onclick = function(event) {
    if (event.target.classList.contains('modal-overlay')) {
        event.target.classList.remove('active');
    }
}