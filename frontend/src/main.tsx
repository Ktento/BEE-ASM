import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import { UIProvider } from "@yamada-ui/react";
import { BrowserRouter } from "react-router-dom";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <UIProvider>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </UIProvider>
  </StrictMode>
);
