import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./components/Login";
import ApiTest from "./components/ApiTest";

function App() {
  return (
    <Router>
      <div>
        <h1>B2Bit</h1>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/api-test" element={<ApiTest />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
