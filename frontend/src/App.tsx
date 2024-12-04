import { Route, Routes } from "react-router-dom";
import Index from "./pages/Index";
import Success from "./pages/Success";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Index />} />
      <Route path="success" element={<Success />} />
    </Routes>
  );
}

export default App;
