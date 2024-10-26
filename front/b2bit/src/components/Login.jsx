import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate(); // Instância do useNavigate

  const handleLogin = async (e) => {
    e.preventDefault(); // Previne o envio do formulário padrão
    setError("");

    console.log("Tentando fazer login...");

    try {
      const response = await axios.post("http://localhost:8000/api/v1/token/", {
        email,
        password,
      });

      console.log("Login bem-sucedido:", response.data);

      // Armazenar os tokens em localStorage
      localStorage.setItem("access_token", response.data.access);
      localStorage.setItem("refresh_token", response.data.refresh);
      localStorage.setItem("user_email", email); // Armazena o email

      // Redirecionar para a página ApiTest
      navigate("/api-test");
    } catch (err) {
      console.error(
        "Erro ao fazer login:",
        err.response ? err.response.data : err.message
      );
      setError("Erro ao fazer login. Verifique suas credenciais.");
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Login</button>
      </form>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
};

export default Login;
