import { Route, Routes } from "react-router-dom";
import Index from "./pages/Index";
import Success from "./pages/Success";
import { DetailHost } from "./pages/DetailHost";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Index />} />
      <Route path="success" element={<Success />} />
      <Route path="/detail" element={<DetailHost />} />
    </Routes>
  );
}

export default App;
