import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";

function Login() {
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");
  // guarda se a senha está visível
  const [verSenha, setVerSenha] = useState(false);

  // o navigate troca de pagina pelo codigo
  const navigate = useNavigate();

  // async: a funcao vai esperar (await) a resposta da API
  async function handleSubmit(e) {
    e.preventDefault();
    if (!email || !senha) {
      setErro("Preencha todos os campos.");
      return;
    }
    try {
      // o pedido: POST /login com o e-mail e a senha em JSON
      const resposta = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, senha }),
      });
      // o corpo da resposta, de JSON para objeto
      const dados = await resposta.json();
      if (resposta.ok) {
        // 200: a API conferiu e deixou entrar
        setErro("");
        localStorage.setItem("logado", "true");
        navigate("/home");
      } else if (resposta.status === 401) {
        // 401: a mensagem de erro vem da API
        setErro(dados.detail);
      } else {
        setErro("Algo deu errado. Tente de novo.");
      }
    } catch {
      // a API esta desligada ou o CORS bloqueou
      setErro("Não foi possível falar com o servidor.");
    }
  }

  return (
    <div className="container">
      <form onSubmit={handleSubmit}>
        <h2>Ponto Eletrônico</h2>

        <input
          type="email"
          placeholder="E-mail"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <div className="campo-senha">
          {/* o tipo troca conforme o verSenha: text mostra, password esconde */}
          <input
            type={verSenha ? "text" : "password"}
            placeholder="Senha"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
          />
          {/* type="button" para nao enviar o formulario ao clicar */}
          <button
            type="button"
            className="ver-senha"
            onClick={() => setVerSenha(!verSenha)}
          >
            {verSenha ? "ocultar" : "mostrar"}
          </button>
        </div>

        {/* so aparece quando tem alguma mensagem de erro */}
        {erro && <p className="erro">{erro}</p>}

        <button type="submit">Entrar</button>
      </form>
    </div>
  );
}

export default Login;
