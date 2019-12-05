var perfis;

function busca() {
    var pesquisa = document.querySelector('input[name="perfis"]:checked').value;
    eel.realizarB(pesquisa)();

}

function enviar() {
    var pesquisa = document.querySelector('input[name="perfis"]:checked').value;
    eel.realizarE(pesquisa)();
}

function buscarEnviar() {
    var pesquisa = document.querySelector('input[name="perfis"]:checked').value;
    eel.realizarBE(pesquisa)();
}

function criarPerfil() {
    var Perfil = document.getElementById("Nperfil").value;
    var nome = document.getElementById("Nome").value;
    var email = document.getElementById("Email").value;
    var celular = document.getElementById("Celular").value;
    var telefone = document.getElementById("Telefone").value;
    var pretencao = parseInt(document.getElementById("Pretencao").value);
    var Curriculo = document.getElementById("Curriculo").value;
    var CurriculoTexto = document.getElementById("CurriculoE").value;
    var Carta = document.getElementById("Carta").value;
    var pesquisa = document.getElementById("Carta").value;
    var saida;
    eel.criarP(Perfil, nome, email, celular, telefone, pretencao, pesquisa, Carta, Curriculo, CurriculoTexto, )(function(ret) {
        saida = ret;
    });
    if (saida == false) {
        Swal.fire({
            icon: 'erro',
            title: 'Perfil não criado preencha todos os capos',
            showConfirmButton: false,
            timer: 1500
        })
    }
}

function listaP() {
    eel.listarP()(function(ret) {
        perfis = ret;
    });
    document.getElementById('RadioPerfil').innerHTML = ""
    for (var i = 0; i < perfis.length; i++) {
        document.getElementById('RadioPerfil').innerHTML = document.getElementById('RadioPerfil').innerHTML +
            '<input type="radio" name="perfis" value="' + perfis[i] + '">' + perfis[i] + '<br>';
        console.log(perfis[i]);
    }
}
window.onload = function() {
    listaP();
};
async function getFolder() {
    var arquivo = await eel.SelecionarCurriculo()();
    if (arquivo) {
        console.log(arquivo);
        document.getElementById("Curriculo").value = arquivo
        document.getElementById("Curriculo").innerText = document.getElementById("Curriculo").value
    }
}