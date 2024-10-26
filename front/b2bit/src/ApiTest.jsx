import { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import UserProfile from "./UserProfile"; // Importe o novo componente
import "./ApiTest.css";

function ApiTest() {
  const [apiResponse, setApiResponse] = useState("");
  const [accessToken, setAccessToken] = useState("");
  const [refreshToken, setRefreshToken] = useState("");
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const storedAccessToken = localStorage.getItem("access_token");
    const storedRefreshToken = localStorage.getItem("refresh_token");

    if (!storedAccessToken) {
      navigate("/"); // Redireciona para o login se não houver token
    } else {
      setAccessToken(storedAccessToken);
      setRefreshToken(storedRefreshToken);
    }
    setLoading(false); // Carregamento finalizado
  }, [navigate]);

  useEffect(() => {
    if (!accessToken && !loading) {
      navigate("/"); // Redireciona para o login se o token não for encontrado após carregar
    }
  }, [accessToken, loading, navigate]);

  const logout = async () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user_email"); // Remove o email do localStorage

    try {
      await axios.post("http://127.0.0.1:8000/api/v1/token/blacklist/", {
        refresh: refreshToken,
      });
    } catch (error) {
      console.error("Erro ao invalidar o token:", error);
    }

    setAccessToken("");
    setRefreshToken("");
    navigate("/");
  };

  const makeApiCall = async (endpoint) => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/api/v1/${endpoint}`,
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );
      setApiResponse(JSON.stringify(response.data, null, 2));
    } catch (error) {
      console.error("Erro ao fazer a chamada à API:", error);
      setApiResponse("Erro ao fazer a chamada à API");
      if (error.response && error.response.status === 401) {
        navigate("/"); // Redireciona para a página de login
      }
    }
  };

  if (loading) {
    return <p>Carregando...</p>;
  }

  return (
    <div className="api-test-container">
      <button onClick={logout}>Logout</button>
      <UserProfile accessToken={accessToken} />{" "}
      {/* Renderize o novo componente */}
      <h2>Tokens</h2>
      <div className="token-container">
        <div className="token-box">
          <h4>Access Token</h4>
          <p className="tokens-values">{accessToken}</p>
        </div>
        <div className="token-box">
          <h4>Refresh Token</h4>
          <p className="tokens-values">{refreshToken}</p>
        </div>
      </div>
      <h2>Teste de API</h2>
      <div className="button-container">
        <button onClick={() => makeApiCall("users/")}>Listar Usuários</button>
        <button onClick={() => makeApiCall("tweets/")}>Listar Tweets</button>
        <button onClick={() => makeApiCall("likes/")}>Listar Likes</button>
        <button onClick={() => makeApiCall("follows/")}>Listar Follows</button>
      </div>
      <pre>{apiResponse}</pre>
    </div>
  );
}

export default ApiTest;
