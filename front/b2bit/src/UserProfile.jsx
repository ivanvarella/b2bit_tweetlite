import { useState, useEffect } from "react";
import axios from "axios";
import PropTypes from "prop-types";

const UserProfile = ({ accessToken }) => {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const userEmail = localStorage.getItem("user_email");
        console.log("Email do usuário:", userEmail); // Verifique o email do usuário

        if (!userEmail) {
          throw new Error("Email do usuário não encontrado.");
        }

        // Substituir o endpoint para usar o email
        const response = await axios.get(
          `http://127.0.0.1:8000/api/v1/users/?eq(email,${userEmail})`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );

        console.log("Dados do usuário:", response.data); // Verifique os dados recebidos
        setUserData(response.data); // Supondo que response.data contenha os dados do usuário
      } catch (err) {
        console.error("Erro ao buscar dados do usuário:", err);
        setError("Erro ao carregar dados do usuário.");
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, [accessToken]);

  if (loading) return <p>Carregando dados do usuário...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <div>
      <h2>Dados do Usuário</h2>
      <pre>{JSON.stringify(userData, null, 2)}</pre>
    </div>
  );
};

UserProfile.propTypes = {
  accessToken: PropTypes.string.isRequired,
};

export default UserProfile;
