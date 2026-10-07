import { Routes, Route } from "react-router-dom";
import { Login } from './Login';
import Home from "./Home";
import RotaPrivada from "./RotaPrivada";
import NaoEncontrada from "./NaoEncontrada";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/home" element={
        <RotaPrivada><Home /></RotaPrivada>
      } />
      <Route path="*"
        element={<NaoEncontrada />} />
    </Routes>
  );
}

export default App;
