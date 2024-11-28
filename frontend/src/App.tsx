import { Box, Button, FormControl, Heading, Input } from "@yamada-ui/react";
import { useState } from "react";

function App() {
  const [domain, setDomain] = useState("");
  const handleSubmit = (e: React.ChangeEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log(domain);
  };

  return (
    <Box>
      <Heading>ASM Tool</Heading>
      実行ボタン
      <form onSubmit={handleSubmit}>
        <FormControl label="対象ドメイン">
          <Input
            placeholder="domain"
            value={domain}
            onChange={(e) => setDomain(e.target.value)}
          />
        </FormControl>
        <Button type="submit" colorScheme="purple" variant="outline">
          実行
        </Button>
      </form>
    </Box>
  );
}

export default App;
