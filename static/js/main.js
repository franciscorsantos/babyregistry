/**
 * Bebê Registry - Lógica JavaScript Vanilla
 */

// Estado global do checkout
let currentItemId = null;
let currentItemValor = 0;
let currentItemValorRestante = 0;
let currentPresenteId = null;
let currentValorContribuicao = 0;

// --- FUNÇÕES DO MODAL DE CHECKOUT ---

function abrirModalCheckout(itemId, nome, valorTotal, valorRestante, imagemUrl) {
    currentItemId = itemId;
    currentItemValor = parseFloat(valorTotal);
    currentItemValorRestante = parseFloat(valorRestante || valorTotal);
    currentPresenteId = null;
    currentValorContribuicao = currentItemValorRestante;

    // Atualizar dados na interface do modal
    const modalItemNome = document.getElementById('modal-item-nome');
    const modalItemValor = document.getElementById('modal-item-valor');
    const modalItemRestante = document.getElementById('modal-item-restante');
    const modalItemImg = document.getElementById('modal-item-img');

    if (modalItemNome) modalItemNome.textContent = nome;
    if (modalItemImg) modalItemImg.src = imagemUrl;
    
    const valorTotalFmt = currentItemValor.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    const valorRestanteFmt = currentItemValorRestante.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    
    if (modalItemValor) modalItemValor.textContent = `Meta: R$ ${valorTotalFmt}`;
    if (modalItemRestante) modalItemRestante.textContent = `Falta R$ ${valorRestanteFmt}`;

    // Configurar campo de valor da contribuição
    const inputValorContrib = document.getElementById('input-valor-contribuicao');
    if (inputValorContrib) {
        inputValorContrib.value = currentItemValorRestante.toFixed(2);
        inputValorContrib.max = currentItemValorRestante.toFixed(2);
    }

    // Atualizar botões de cotas pré-definidas
    atualizarBotoesCotas(currentItemValorRestante);
    atualizarTextoBotaoPix(currentValorContribuicao);

    // Resetar campos e erros
    const inputNome = document.getElementById('input-nome-convidado');
    const inputMsg = document.getElementById('input-mensagem');
    const errorDiv = document.getElementById('checkout-error');

    if (inputNome) inputNome.value = '';
    if (inputMsg) inputMsg.value = '';
    if (errorDiv) {
        errorDiv.textContent = '';
        errorDiv.classList.add('hidden');
    }

    // Alternar para o Passo 1 (Formulário)
    document.getElementById('step-form').classList.remove('hidden');
    document.getElementById('step-pix').classList.add('hidden');

    // Exibir o Modal
    const modal = document.getElementById('checkout-modal');
    if (modal) {
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden'; // Evita scroll do fundo
    }
}

function fecharModalCheckout() {
    const modal = document.getElementById('checkout-modal');
    if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
    }
}

function atualizarBotoesCotas(restante) {
    const container = document.getElementById('container-cotas-rapidas');
    if (!container) return;

    // Opções de cotas adequadas para o valor restante
    const opcoesCotas = [50, 100, 200, 500].filter(val => val < restante);
    
    let html = `<button type="button" onclick="selecionarCota(${restante})" class="cota-btn px-3 py-1.5 rounded-lg border text-xs font-semibold font-sans transition-all bg-[#475949] text-white border-[#475949]">
        Restante Total (R$ ${restante.toLocaleString('pt-BR', {minimumFractionDigits: 2})})
    </button>`;

    opcoesCotas.forEach(val => {
        html += `<button type="button" onclick="selecionarCota(${val})" class="cota-btn px-3 py-1.5 rounded-lg border text-xs font-semibold font-sans transition-all bg-white text-stone-700 border-stone-300 hover:border-[#475949]">
            R$ ${val.toLocaleString('pt-BR', {minimumFractionDigits: 2})}
        </button>`;
    });

    container.innerHTML = html;
}

function selecionarCota(valor) {
    const inputValorContrib = document.getElementById('input-valor-contribuicao');
    if (inputValorContrib) {
        inputValorContrib.value = valor.toFixed(2);
    }
    currentValorContribuicao = valor;
    atualizarTextoBotaoPix(valor);

    // Destacar botão selecionado
    document.querySelectorAll('.cota-btn').forEach(btn => {
        if (btn.textContent.includes(valor.toLocaleString('pt-BR', {minimumFractionDigits: 2}))) {
            btn.className = "cota-btn px-3 py-1.5 rounded-lg border text-xs font-semibold font-sans transition-all bg-[#475949] text-white border-[#475949]";
        } else {
            btn.className = "cota-btn px-3 py-1.5 rounded-lg border text-xs font-semibold font-sans transition-all bg-white text-stone-700 border-stone-300 hover:border-[#475949]";
        }
    });
}

function aoAlterarInputValor(input) {
    let val = parseFloat(input.value) || 0;
    if (val > currentItemValorRestante) {
        val = currentItemValorRestante;
        input.value = val.toFixed(2);
    }
    currentValorContribuicao = val;
    atualizarTextoBotaoPix(val);
}

function atualizarTextoBotaoPix(valor) {
    const btnValorTexto = document.getElementById('btn-valor-texto');
    if (btnValorTexto) {
        btnValorTexto.textContent = valor.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    }
}

async function gerarPixCheckout() {
    const inputNome = document.getElementById('input-nome-convidado');
    const inputMsg = document.getElementById('input-mensagem');
    const inputValorContrib = document.getElementById('input-valor-contribuicao');
    const errorDiv = document.getElementById('checkout-error');
    const btnGerar = document.getElementById('btn-gerar-pix');

    const nomeConvidado = inputNome ? inputNome.value.trim() : '';
    const mensagem = inputMsg ? inputMsg.value.trim() : '';
    const valorContrib = inputValorContrib ? parseFloat(inputValorContrib.value) : currentItemValorRestante;

    if (!nomeConvidado) {
        if (errorDiv) {
            errorDiv.textContent = 'Por favor, digite seu nome antes de prosseguir.';
            errorDiv.classList.remove('hidden');
        }
        if (inputNome) inputNome.focus();
        return;
    }

    if (!valorContrib || valorContrib <= 0) {
        if (errorDiv) {
            errorDiv.textContent = 'Informe um valor de contribuição válido maior que R$ 0,00.';
            errorDiv.classList.remove('hidden');
        }
        return;
    }

    if (valorContrib > currentItemValorRestante) {
        if (errorDiv) {
            errorDiv.textContent = `O valor máximo que falta para este presente é R$ ${currentItemValorRestante.toLocaleString('pt-BR', {minimumFractionDigits: 2})}.`;
            errorDiv.classList.remove('hidden');
        }
        return;
    }

    if (errorDiv) errorDiv.classList.add('hidden');

    // Feedback visual de carregamento no botão
    const btnOriginalHTML = btnGerar.innerHTML;
    btnGerar.disabled = true;
    btnGerar.innerHTML = `
        <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        Gerando Pix...
    `;

    try {
        const response = await fetch(`/api/checkout/${currentItemId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nome_convidado: nomeConvidado,
                mensagem: mensagem,
                valor_contribuicao: valorContrib
            })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            currentPresenteId = data.presente_id;

            // Preencher QR Code e Copia e Cola
            const qrImg = document.getElementById('pix-qr-img');
            const copiaColaArea = document.getElementById('pix-copia-cola');

            if (qrImg) qrImg.src = `data:image/png;base64,${data.qr_code_base64}`;
            if (copiaColaArea) copiaColaArea.value = data.qr_code;

            // Trocar para o Passo 2
            document.getElementById('step-form').classList.add('hidden');
            document.getElementById('step-pix').classList.remove('hidden');

            mostrarToast("Pix gerado com sucesso!");
        } else {
            if (errorDiv) {
                errorDiv.textContent = data.message || 'Ocorreu um erro ao gerar o Pix. Tente novamente.';
                errorDiv.classList.remove('hidden');
            }
        }
    } catch (err) {
        console.error('Erro na requisição:', err);
        if (errorDiv) {
            errorDiv.textContent = 'Erro de conexão com o servidor.';
            errorDiv.classList.remove('hidden');
        }
    } finally {
        btnGerar.disabled = false;
        btnGerar.innerHTML = btnOriginalHTML;
    }
}

function copiarPixPayload() {
    const copiaColaArea = document.getElementById('pix-copia-cola');
    if (!copiaColaArea || !copiaColaArea.value) return;

    navigator.clipboard.writeText(copiaColaArea.value).then(() => {
        mostrarToast('Código Pix copiado para a área de transferência! ✨');
    }).catch(err => {
        // Fallback para seleção de texto em navegadores antigos
        copiaColaArea.select();
        document.execCommand('copy');
        mostrarToast('Código Pix copiado!');
    });
}

async function simularPagamentoAprovado() {
    if (!currentPresenteId) return;

    const btnSimular = document.getElementById('btn-simular-pagamento');
    if (btnSimular) {
        btnSimular.disabled = true;
        btnSimular.textContent = 'Confirmando pagamento...';
    }

    try {
        const response = await fetch(`/api/simulate-payment/${currentPresenteId}`, {
            method: 'POST'
        });

        const data = await response.json();
        if (data.success && data.redirect_url) {
            window.location.href = data.redirect_url;
        }
    } catch (err) {
        console.error('Erro ao simular pagamento:', err);
        mostrarToast('Erro ao redirecionar para a confirmação.');
        if (btnSimular) btnSimular.disabled = false;
    }
}

// --- FUNÇÕES DO FAB (MURAL DE RECADOS) ---

function abrirModalFab() {
    const modal = document.getElementById('fab-modal');
    if (modal) {
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }
}

function fecharModalFab() {
    const modal = document.getElementById('fab-modal');
    if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
    }
}

async function enviarRecadoFab() {
    const inputNome = document.getElementById('fab-input-nome');
    const inputMsg = document.getElementById('fab-input-mensagem');
    const errorDiv = document.getElementById('fab-error');

    const nome = inputNome ? inputNome.value.trim() : '';
    const mensagem = inputMsg ? inputMsg.value.trim() : '';

    if (!nome || !mensagem) {
        if (errorDiv) {
            errorDiv.textContent = 'Por favor, preencha seu nome e a mensagem.';
            errorDiv.classList.remove('hidden');
        }
        return;
    }

    try {
        const response = await fetch('/api/mural/mensagem', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome_convidado: nome, mensagem: mensagem })
        });

        const data = await response.json();
        if (data.success) {
            fecharModalFab();
            mostrarToast('Recado enviado com sucesso!');
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            if (errorDiv) {
                errorDiv.textContent = data.message || 'Erro ao publicar recado.';
                errorDiv.classList.remove('hidden');
            }
        }
    } catch (err) {
        console.error(err);
    }
}

// --- UTILITÁRIO DE TOAST NOTIFICATION ---

function mostrarToast(mensagem) {
    const toastContainer = document.getElementById('toast-container');
    const toastText = document.getElementById('toast-text');

    if (toastContainer && toastText) {
        toastText.textContent = mensagem;
        toastContainer.classList.remove('opacity-0', 'translate-y-4');
        toastContainer.classList.add('opacity-100', 'translate-y-0');

        setTimeout(() => {
            toastContainer.classList.remove('opacity-100', 'translate-y-0');
            toastContainer.classList.add('opacity-0', 'translate-y-4');
        }, 3500);
    }
}

// Fechar modais ao clicar no backdrop (fora do contêiner)
window.addEventListener('click', (e) => {
    const checkoutModal = document.getElementById('checkout-modal');
    const fabModal = document.getElementById('fab-modal');

    if (e.target === checkoutModal) fecharModalCheckout();
    if (e.target === fabModal) fecharModalFab();
});
