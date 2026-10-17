// ============================================
// PetConecta - JavaScript
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    // 1. Confirmação antes de marcar como adotado
    const formsAdotar = document.querySelectorAll('form[action*="adotar"]');
    formsAdotar.forEach(form => {
        form.addEventListener('submit', (e) => {
            if (!confirm('Confirmar que este animal foi adotado?')) {
                e.preventDefault();
            }
        });
    });

    // 2. Preview da foto ao cadastrar
    const inputFoto = document.querySelector('input[name="foto"]');
    if (inputFoto) {
        inputFoto.addEventListener('change', (e) => {
            const arquivo = e.target.files[0];
            if (arquivo) {
                const leitor = new FileReader();
                leitor.onload = (ev) => {
                    let preview = document.getElementById('preview-foto');
                    if (!preview) {
                        preview = document.createElement('img');
                        preview.id = 'preview-foto';
                        preview.style.maxWidth = '200px';
                        preview.style.marginTop = '10px';
                        preview.style.borderRadius = '8px';
                        inputFoto.parentElement.appendChild(preview);
                    }
                    preview.src = ev.target.result;
                };
                leitor.readAsDataURL(arquivo);
            }
        });
    }

    // 3. Validação simples de e-mail
    const formCadastro = document.querySelector('form[action*="cadastro"]');
    if (formCadastro) {
        formCadastro.addEventListener('submit', (e) => {
            const email = formCadastro.querySelector('input[name="email"]').value;
            if (!email.includes('@') || !email.includes('.')) {
                e.preventDefault();
                alert('Por favor, informe um e-mail válido.');
            }
        });
    }
});