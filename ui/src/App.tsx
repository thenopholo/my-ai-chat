import "@crayonai/react-ui/styles/index.css";
import "./index.css";
import { C1Chat, ThemeProvider } from "@thesysai/genui-sdk";
import { themePresets } from "@crayonai/react-ui";

export default function App() {
  return (
    <ThemeProvider
      theme={themePresets.charcoal.theme}
      darkTheme={themePresets.charcoal.darkTheme}
      mode="dark"
    >
      <C1Chat apiUrl="/api/chat" />
    </ThemeProvider>
  );
}
